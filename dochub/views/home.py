from django.shortcuts import render
from ..models import LocalHealthBoard
from ..general_functions import generate_choropleth_map

def home(request):
    template = "home.html"
    
    context = {
        "parents": LocalHealthBoard.objects.all()
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