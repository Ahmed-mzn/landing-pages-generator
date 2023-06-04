from django.shortcuts import render, redirect
from .models import Domain, Template, App
from django.conf import settings
from django.http import HttpResponse

from django.db.models import Q


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
        elif request.path == '/':
            # if request.path == '':
            # print("----------------------------------------------------------start")
            # print("host : ", request.META['HTTP_HOST'])
            # print("path : ", request.path)
            response = self.get_response(request)
            return response
        else:
            split_path = request.path.split('/')

            if len(split_path) > 3:
                response = self.get_response(request)
                return response
            else:
                current_path = split_path[1]
                templates = domain.templates.all().filter(
                    Q(is_deleted=False, is_child=True, template_redirect_numbers__gt=0, parent__template_name=current_path) |
                    Q(is_deleted=False, is_child=False, template_redirect_numbers__gt=0, template_name=current_path)
                ).order_by("id")
                app = templates.filter(is_child=False).first()
                if app:
                    if app.next_template == 0:
                        app.next_template = templates[0].id
                        app.next_template_redirect_numbers = templates[0].template_redirect_numbers
                        app.next_template_redirect_numbers = app.next_template_redirect_numbers - 1
                        app.save()
                    else:
                        if app.next_template_redirect_numbers <= 0:
                            # print("next temp: ", app.next_template)

                            template_ids = [t.id for t in templates]
                            # print("temp ids: ", template_ids)

                            current_temp_id_index = template_ids.index(app.next_template)
                            # print("current index: ", current_temp_id_index)
                            # print("len ids: ", (len(template_ids) - 1))

                            if current_temp_id_index == (len(template_ids) - 1):
                                app.next_template = template_ids[0]
                                app.next_template_redirect_numbers = Template.objects.get(
                                    pk=template_ids[0]).template_redirect_numbers
                                app.next_template_redirect_numbers = app.next_template_redirect_numbers - 1
                                app.save()
                            else:
                                app.next_template = template_ids[current_temp_id_index + 1]
                                app.next_template_redirect_numbers = Template.objects.get(
                                    pk=template_ids[current_temp_id_index + 1]).template_redirect_numbers
                                app.next_template_redirect_numbers = app.next_template_redirect_numbers - 1
                                app.save()
                        else:
                            app.next_template_redirect_numbers = app.next_template_redirect_numbers - 1
                            app.save()
                    template = Template.objects.get(pk=app.next_template)
                    context = {
                        "template": template
                    }

                    return render(request, 'preview-editor.html', context)
                else:
                    response = self.get_response(request)
                    return response

        # Code to be executed for each request/response after
        # the view is called.
