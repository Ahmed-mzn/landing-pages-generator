from django.shortcuts import render
from .models import Domain, Template
from django.conf import settings
from django.http import HttpResponse


class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        if request.META['HTTP_HOST'] in settings.ALLOWED_DOMAINS:
            response = self.get_response(request)
            return response

        domain = Domain.objects.all().filter(name=request.META['HTTP_HOST']).first()

        if domain is None:
            return HttpResponse('Unauthorized', status=401)
        else:
            # if request.path == '':
            template = Template.objects.all().filter(app__domain__name=domain.name).first()
            context = {
                "domain": request.META['HTTP_HOST'],
                "uri": request.build_absolute_uri(),
                "path": request.path,
                "template": template
            }
            return render(request, 'test.html', context)

        # Code to be executed for each request/response after
        # the view is called.
