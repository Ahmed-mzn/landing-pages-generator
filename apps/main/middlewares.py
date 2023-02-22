from django.shortcuts import render, redirect
from .models import Domain, Template, App
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
        elif request.path == '/':
            # if request.path == '':
            # print("----------------------------------------------------------start")
            # print("host : ", request.META['HTTP_HOST'])
            # print("path : ", request.path)

            templates = domain.templates.all().filter(is_deleted=False, template_redirect_numbers__gt=0).order_by("id")

            app = templates.filter(is_child=False).first()

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
                    app.next_template_redirect_numbers = app.next_template_redirect_numbers-1
                    app.save()
            template = Template.objects.get(domain=domain, pk=app.next_template)
            context = {
                "template": template
            }
            if template.template_code == 'template_one':
                return render(request, 'template-one.html', context)
            else:
                return render(request, 'template-two.html', context)
        else:
            split_path = request.path.split('/')
            # print(split_path)
            if len(split_path) > 3:
                response = self.get_response(request)
                return response
            else:
                templates = Template.objects.all().filter(domain=domain).order_by("id")
                templates_names = [t.template_name for t in templates]
                # print(templates_names)
                if split_path[1] in templates_names:
                    template = templates.get(template_name=split_path[1])
                    context = {
                        "template": template
                    }

                    if template.template_code == 'template_one':
                        return render(request, 'template-one.html', context)
                    else:
                        return render(request, 'template-two.html', context)
                else:
                    response = self.get_response(request)
                    return response

        # Code to be executed for each request/response after
        # the view is called.
