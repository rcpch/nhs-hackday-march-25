from django.shortcuts import render
from ..models import Parent

def home(request):
    template = "home.html"
    
    context = {
        "parents": Parent.objects.all()
    }

    return render(request=request, template_name=template, context=context)


def parent(request, pk):
    parent = Parent.objects.get(pk=pk)

    template = "parent.html"
    context = {
        "parent": parent
    }

    return render(request=request, template_name=template, context=context)