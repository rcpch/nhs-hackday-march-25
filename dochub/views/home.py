from django.shortcuts import render
from django.apps import apps
from ..models import LocalHealthBoard
from ..general_functions import generate_choropleth_map
from ..general_functions import EnumAbstractionLevel

def home(request):
    template = "home.html"

    Organisation = apps.get_model('dochub', 'Organisation')
    organisation = Organisation.objects.get(ods_code="7A4BV")
    
    lhb_heatmap = generate_choropleth_map(
            properties="ods_code",
            abstraction_level=EnumAbstractionLevel.LOCAL_HEALTH_BOARD,
            organisation=organisation,
        )
    context = {
        "map": lhb_heatmap
    }

    return render(request=request, template_name=template, context=context)


def parent(request, pk):
    parent = LocalHealthBoard.objects.get(pk=pk)

    map = generate_choropleth_map()

    template = "parent.html"
    context = {
        "parent": parent,
        "map": map
    }

    return render(request=request, template_name=template, context=context)

def detail(request):

    template="detail.html"
    return render(request=request, template_name=template)
