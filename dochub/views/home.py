from django.shortcuts import render
from ..models import LocalHealthBoard

def home(request):
    template = "home.html"
    
    context = {
        "parents": LocalHealthBoard.objects.all()
    }

    return render(request=request, template_name=template, context=context)


def parent(request, pk):
    parent = LocalHealthBoard.objects.get(pk=pk)

    template = "parent.html"
    context = {
        "parent": parent
    }

    return render(request=request, template_name=template, context=context)

def detail(request):

    template="detail.html"
    return render(request=request, template_name=template)
