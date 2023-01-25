from django.shortcuts import render, get_object_or_404

from .models import Template


def preview(request, pk):
    template = get_object_or_404(Template, pk=pk)
    context = {
        "template": template
    }
    return render(request, 'preview.html', context)
