from django.shortcuts import render
from django.apps import apps
from ..models import LocalHealthBoard
from ..general_functions import generate_choropleth_map
from ..general_functions import EnumAbstractionLevel

def home(request, pk=None):
    template = "home.html"

    Organisation = apps.get_model('dochub', 'Organisation')
    if pk==None:
        organisation = Organisation.objects.get(ods_code="7A4BV")
    else:
        organisation = Organisation.objects.get(pk=pk)


    organisations = Organisation.objects.all().order_by('name')
    
    lhb_heatmap = generate_choropleth_map(
            properties="ods_code",
            abstraction_level=EnumAbstractionLevel.LOCAL_HEALTH_BOARD,
            organisation=organisation,
        )
    context = {
        "map": lhb_heatmap,
        "organisations": organisations,
        "organisation": organisation
    }

    return render(request=request, template_name=template, context=context)


def organisation(request, pk):
    """
    htmx get request
    """
    Organisation = apps.get_model('dochub', 'Organisation')
    organisation = Organisation.objects.get(pk=pk)

    if organisation.country.name == "England":
        heatmap = generate_choropleth_map(
            properties="ods_code",
            abstraction_level=EnumAbstractionLevel.TRUST,
            organisation=organisation,
        )

    else:
        heatmap = generate_choropleth_map(
            properties="ods_code",
            abstraction_level=EnumAbstractionLevel.LOCAL_HEALTH_BOARD,
            organisation=organisation,
        )

    template = "map.html"
    context = {
        "organisation": organisation,
        "map": heatmap
    }

    return render(request=request, template_name=template, context=context)

def detail(request):

    template="detail.html"
    return render(request=request, template_name=template)
