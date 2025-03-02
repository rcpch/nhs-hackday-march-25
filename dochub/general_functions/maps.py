# python imports
from datetime import date
import json
import logging
from typing import Literal
from enum import Enum

# django imports
from django.apps import apps
from django.conf import settings
from django.core.serializers import serialize

# third party imports
import pandas as pd
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go


ABSTRACTION_LEVELS = (
    ("organisation", "Organisation"),
    ("trust", "Trust/Local Health Board"),
    ("local_health_board", "Local Health Board"),
    ("icb", "Integrated Care Board"),
    ("open_uk", "OPEN UK network"),
    ("nhs_england_region", "NHS England Region"),
    ("country", "Country"),
    ("national", "National"),
)


class EnumAbstractionLevel(Enum):
    """These are all with respect to Organisation so queries would all require e.g. organisation__ODSCode"""

    ORGANISATION = "ods_code"
    TRUST = "trust__ods_code"
    LOCAL_HEALTH_BOARD = "local_health_board__boundary_identifier"
    ICB = "integrated_care_board__boundary_identifier"
    NHS_ENGLAND_REGION = "nhs_england_region__boundary_identifier"
    OPEN_UK = "openuk_network__boundary_identifier"
    COUNTRY = "country__boundary_identifier"
    NATIONAL = "country__name"


def return_tile_for_region(
    abstraction_level: Literal[
        "icb", "nhs_england_region", "london_borough", "lhb", "country"
    ],
    organisation=None,
):
    """
    Returns geojson data for a given region.
    """
    IntegratedCareBoard = apps.get_model("dochub", "IntegratedCareBoard")
    NHSEnglandRegion = apps.get_model("dochub", "NHSEnglandRegion")
    CountryBoundaries = apps.get_model("dochub", "Country")
    LocalHealthBoard = apps.get_model("dochub", "LocalHealthBoard")

    model = IntegratedCareBoard.objects.all()

    if abstraction_level == "nhs_england_region":
        model = NHSEnglandRegion.objects.all()
    elif abstraction_level == "country":
        model = CountryBoundaries
        if organisation:
            model = CountryBoundaries.objects.filter(
                boundary_identifier=organisation.country.boundary_identifier
            ).all()
        else:
            model = CountryBoundaries.objects.all()
    elif abstraction_level == "lhb":
        model = LocalHealthBoard.objects.all()

    unedited_tile = serialize("geojson", model)

    geojson_dict = json.loads(unedited_tile)
    geojson_dict.pop("crs", None)

    return json.dumps(geojson_dict)


def generate_choropleth_map(
    properties, organisation, abstraction_level
):
    """
    Generates a Plotly Choropleth map from GeoJSON data.
    Accepts the geojson data as a string, the properties key to use as the identifier, and the cohort.
    """
    px.set_mapbox_access_token("pk.eyJ1IjoiZWF0eW91cnBlYXMiLCJhIjoiY2x3ZGxpdGdwMDZjNDJxcWphanVvdmpsMSJ9.TuK1L7iuKayILZMcxAKupw")

    region_tile = region_tile_for_abstraction_level(
        abstraction_level=abstraction_level, organisation=organisation
    )

    geojson_data = json.loads(region_tile)
    features = geojson_data["features"]
    abstraction_level_ids = [feature["properties"][properties] for feature in features]
    abstraction_level_names = [feature["properties"]["name"] for feature in features]

    # Add a layer for the region to highlight
    if abstraction_level == EnumAbstractionLevel.NHS_ENGLAND_REGION:
        identifier = "nhs_england_region"
        custom_zoom = 6
    elif abstraction_level == EnumAbstractionLevel.LOCAL_HEALTH_BOARD:
        identifier = "local_health_board"
        custom_zoom = 7
    elif abstraction_level == EnumAbstractionLevel.ICB:
        identifier = "integrated_care_board"
        custom_zoom = 7
    elif abstraction_level == EnumAbstractionLevel.COUNTRY:
        identifier = "country"
        custom_zoom = 5
    elif abstraction_level == EnumAbstractionLevel.TRUST:
        identifier = "trust"
        custom_zoom = 8
    else:
        identifier = None

    # Highlight the region of the organisation by colouring the region boundary in a pink colour
    organisation_region = getattr(organisation, identifier)
    organisation_region_identifier = getattr(organisation_region, properties)

    df = pd.DataFrame(columns=["identifier", "name", "organisations"])

    level_abstraction_members, identifier = all_level_of_abstraction_members(
        abstraction_level=abstraction_level
    )

    for member in level_abstraction_members:
        
        list_of_organisations_within_member = (
            all_organisations_within_a_level_of_abstraction(
                abstraction_level=abstraction_level, abstraction_level_member=member
            )
        )
        df = pd.concat(
                [
                    df,
                    pd.DataFrame(
                        [
                            {
                                "identifier": getattr(member, identifier),
                                "name": getattr(member, "name"),
                                "organisations": list_of_organisations_within_member,
                            }
                        ]
                    ),
                ],
                ignore_index=True,
            )
        
    highlighted_region = df[
        df["identifier"] == organisation_region_identifier
    ]

    # Create a Plotly map using the GeoJSON data, data, and color data
    fig = go.Figure(
        go.Choroplethmapbox(
            geojson=geojson_data,
            locations=abstraction_level_ids,
            featureidkey=f"properties.{properties}",
            colorscale=[[0, "green"], [1, "lightgreen"]],
            z=[0] * len(abstraction_level_ids),
            marker_line_width=2,  # Set the width of the boundaries
            marker_line_color='red',  # Set the color of the boundaries
            customdata=abstraction_level_names,
            hovertemplate="<b>%{customdata}</b><extra></extra>",  # Custom hovertemplate
        )
    )

    # centre the map on the lead organisation
    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox_center={
            "lat": organisation.latitude,
            "lon": organisation.longitude,
        },
        hoverlabel=dict(
            bgcolor="red",
            font_size=16,
            font_family="Montserrat-Regular",
        ),
        font=dict(family="Montserrat-Regular", size=12, color="black"),
    )

    # Make hover label pink and montserrat
    fig.update_traces(
        hoverlabel=dict(
            bgcolor="#FFFFFF",
            font_size=16,
            font_family="Montserrat-Regular",
        )
    )

    fig.add_trace(
        go.Choroplethmapbox(
            geojson=geojson_data,
            marker_line_color="red",  # Set the outline color
            marker_line_width=3,  # Set the outline width
            locations=highlighted_region["identifier"],
             colorscale=[[0, "lightblue"], [1, "blue"]], 
        )
    )

    # Add a scatterplot point for the organization
    fig.add_trace(
        go.Scattermapbox(
            lat=[organisation.latitude],
            lon=[organisation.longitude],
            mode="markers",
            marker=go.scattermapbox.Marker(
                size=12,
                color="red",  # Set the color of the point
            ),
            text=[organisation.name],  # Set the hover text for the point
            hovertemplate="%{text}<extra></extra>",  # Custom hovertemplate
        )
    )

    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, mapbox_zoom=custom_zoom)

    # Convert the Plotly figure to JSON
    return pio.to_json(fig)


# Helper functions
def all_level_of_abstraction_members(abstraction_level: EnumAbstractionLevel):
    """
    Returns all members of a given level of abstraction and the identifier for the level
    """
    # get lists of all members of each level of abstraction
    Trust = apps.get_model("dochub", "Trust")
    IntegratedCareBoard = apps.get_model("dochub", "IntegratedCareBoard")
    LocalHealthBoard = apps.get_model("dochub", "LocalHealthBoard")
    NHSEnglandRegion = apps.get_model("dochub", "NHSEnglandRegion")
    Country = apps.get_model("dochub", "Country")

    if abstraction_level == EnumAbstractionLevel.TRUST:
        level_abstraction_members = Trust.objects.filter(active=True).order_by("name")
        identifier = "ods_code"
    elif abstraction_level == EnumAbstractionLevel.ICB:
        level_abstraction_members = IntegratedCareBoard.objects.all().order_by("name")
        identifier = "ods_code"
    elif abstraction_level == EnumAbstractionLevel.LOCAL_HEALTH_BOARD:
        level_abstraction_members = LocalHealthBoard.objects.all().order_by("name")
        identifier = "ods_code"
    elif abstraction_level == EnumAbstractionLevel.NHS_ENGLAND_REGION:
        level_abstraction_members = NHSEnglandRegion.objects.all().order_by("name")
        identifier = "region_code"
    elif abstraction_level == EnumAbstractionLevel.COUNTRY:
        level_abstraction_members = Country.objects.all().order_by("name")
        identifier = "boundary_identifier"
    else:  # pragma: no cover
        raise ValueError("Invalid abstraction level")

    return level_abstraction_members, identifier


def all_organisations_within_a_level_of_abstraction(
    abstraction_level: EnumAbstractionLevel,
    abstraction_level_member,
):
    """
    Returns all organisation members of a given level of abstraction, along with the identifier for the level
    """
    Organisation = apps.get_model("dochub", "Organisation")

    level_abstraction_organisations = None
    if abstraction_level == EnumAbstractionLevel.TRUST:
        level_abstraction_organisations = Organisation.objects.filter(
            trust=abstraction_level_member
        )
    elif abstraction_level == EnumAbstractionLevel.ICB:
        level_abstraction_organisations = Organisation.objects.filter(
            integrated_care_board=abstraction_level_member
        )
    elif abstraction_level == EnumAbstractionLevel.LOCAL_HEALTH_BOARD:
        level_abstraction_organisations = Organisation.objects.filter(
            local_health_board=abstraction_level_member
        )
    elif abstraction_level == EnumAbstractionLevel.NHS_ENGLAND_REGION:
        level_abstraction_organisations = Organisation.objects.filter(
            nhs_england_region=abstraction_level_member
        )
    elif abstraction_level == EnumAbstractionLevel.COUNTRY:
        level_abstraction_organisations = Organisation.objects.filter(
            country=abstraction_level_member
        )
    else:  # pragma: no cover
        raise ValueError("Invalid abstraction level")

    return level_abstraction_organisations


def region_tile_for_abstraction_level(
    abstraction_level: EnumAbstractionLevel, organisation
):
    """
    Returns the geojson tile for a given level of abstraction
    """

    if abstraction_level == EnumAbstractionLevel.TRUST:
        region_tile = return_tile_for_region("trust")
    elif abstraction_level == EnumAbstractionLevel.ICB:
        region_tile = return_tile_for_region("icb")
    elif abstraction_level == EnumAbstractionLevel.LOCAL_HEALTH_BOARD:
        region_tile = lhb_tiles = return_tile_for_region("lhb")
    elif abstraction_level == EnumAbstractionLevel.NHS_ENGLAND_REGION:
        region_tile = return_tile_for_region("nhs_england_region")
    elif abstraction_level == EnumAbstractionLevel.COUNTRY:
        region_tile = return_tile_for_region("country", organisation)
    else:  # pragma: no cover
        raise ValueError("Invalid abstraction level")

    return region_tile
