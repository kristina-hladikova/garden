from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
#from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render, HttpResponse, resolve_url, redirect
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import FormMixin, CreateView

from zahradka_app.forms import RegistrationForm, GardenForm, ContactForm
from zahradka_app.models import Plant, Garden, GardenPlant, Event


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


@login_required(login_url='login')
def garden(request):
    gardens = Garden.objects.filter(user=request.user)
    context = {
        'gardens': gardens
    }
    return render(request, 'garden.html', context=context)


@login_required(login_url='login')
def garden_detail(request, garden_name):
    garden_id = Garden.objects.get(name=garden_name).id
    garden = Garden.objects.get(id=garden_id)
    plants = Plant.objects.filter(gardens__name=garden_name)
    events = Event.objects.filter(plant__gardens__id=garden_id)

    context = {
        'name': garden.name,
        'description': garden.description,
        'address': garden.address,
        'plants': plants,
        'events': events,
    }
    return render(request, 'garden_detail.html', context=context)

# @login_required(login_url='login')
# def garden_settings(request, ...):


# class GardenSettingsView(View):
#     template_name = 'garden_settings.html'
#     model = GardenPlant
#
#     def get(self, request, garden_name, *args, **kwargs):
#         garden_id = Garden.objects.get(name=garden_name).id
#         garden = Garden.objects.get(id=garden_id)
#
#         context = {
#             'name': garden.name,
#             'description': garden.description,
#             'address': garden.address,
#             'plants': Plant.objects.all(),
#         }
#
#         return render(request, 'garden_settings.html', context=context)
#
#
#     def post(self, request, plant, *args, **kwargs):
#         gardenplant = self.get_object()
#         gardenplant.add(plant)
#         gardenplant.save()
#         return self.get(request, *args, **kwargs)


# class EditGardenMixin:
#     template_name = 'create_garden.html'
#     form_class = GardenForm
#     model = Garden
#
#     def get_success_url(self):
#         return resolve_url('garden_detail')
#
#
# class CreateGardenView(EditGardenMixin, CreateView):
#     def get_context_data(self, **kwargs):
#         context = super(CreateGardenView, self).get_context_data(**kwargs)
#         context.update({
#             'action_url': resolve_url('create_garden')
#         })
#         return context


def create_garden(request):
    # post_data = dict(request.POST)
    # post_data['user'] = request.user
    form = GardenForm(request.POST or None)
    if form.is_valid():

        form.save(request.user)

        return redirect('/garden')
    context = {"form": form}
    return render(request, "create_garden.html", context)


def update_garden(request, garden_name):
    garden = Garden.objects.get(name=garden_name)
    form = GardenForm(request.POST or None, instance=garden)
    if form.is_valid():
        form.save()
        return redirect('/garden')
    context = {"form": form}
    return render(request, "update_garden.html", context)


def delete_garden(request, garden_name):
    garden = Garden.objects.get(name=garden_name)
    garden.delete()
    return redirect('/')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "Website Inquiry"
            body = {
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'email': form.cleaned_data['email_address'],
                'message': form.cleaned_data['message'],
            }
            message = "\n".join(body.values())

            try:
                send_mail(subject, message, 'kristi.lackova@gmail.com', ['kristi.lackova@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect("homepage")

    form = ContactForm()
    return render(request, "contact.html", {'form': form})

