from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render, HttpResponse, resolve_url, redirect
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import FormMixin

from zahradka_app.forms import RegistrationForm
from zahradka_app.models import Plant, Garden, GardenPlant


def homepage(request):
    return render(request, "homepage.html")


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("homepage")


class LoginView(FormMixin, TemplateView):
    template_name = "accounts/login.html"
    form_class = AuthenticationForm

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is None:
            # TODO add messages
            return redirect("login")

        login(request, user)
        return redirect("homepage")


class ChangePasswordView(PasswordChangeView):
    template_name = "accounts/change_password.html"
    success_url = reverse_lazy("homepage")


class RegistrationView(FormMixin, TemplateView):
    template_name = "accounts/register.html"
    form_class = RegistrationForm

    def post(self, request, *args, **kwargs):
        bounded_form = self.form_class(request.POST)
        if bounded_form.is_valid():
            bounded_form.save()
            return redirect("homepage")
        else:
            return TemplateResponse(request, "accounts/register.html", context={"form": bounded_form})


# class GardenView(LoginRequiredMixin, TemplateView):
#     template_name = "garden.html"
#
#     def get(self, request, garden_id, *args, **kwargs):
#         plants_db = Garden.plant.objects.all() #objects.all().filter(name=garden_id)
#         context = {
#             'name': Garden.name,
#             'description': Garden.description,
#             'address': Garden.description,
#             'plant': plants_db,
#         }
#         return TemplateResponse(request, 'garden.html', context=context)

def garden_detail(request, pk):
    garden = Garden.objects.get(id=pk)
    # gardens = Plant.objects.all().get(id=pk)
    context = {
        'name': garden.name,
        'description': garden.description,
        'address': garden.address,
        'gardens': Plant.objects.all(),
    }
    return TemplateResponse(request, 'garden.html', context=context)