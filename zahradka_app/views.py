from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
#from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render, HttpResponse, resolve_url, redirect
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, DetailView, ListView
from django.views.generic.edit import FormMixin, CreateView

from zahradka_app.forms import RegistrationForm, GardenForm, ContactForm
from zahradka_app.models import Plant, Garden, GardenPlant, Event, Membership, UserMembership, Subscription
from datetime import date



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
def garden_detail(request, garden_id):
    garden = Garden.objects.get(id=garden_id)
    plants = Plant.objects.filter(gardens__id=garden_id)
    calendar_str = request.POST.get('calendar')
    if calendar_str:
        my_today = date.fromisoformat(calendar_str)
    else:
        my_today = date.today()
    shifted_today = date(year=1970, month=my_today.month, day=my_today.day)
    events = Event.objects.filter(plant__gardens__id=garden_id)
    events = events.filter(dates__start_date__lte=shifted_today, dates__end_date__gte=shifted_today)

    context = {
        "garden": garden,
        'plants': plants,
        'date': my_today,
        'events': events,
        'calendar': calendar_str,
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

def subscription_check(user):
    return UserMembership.objects.get(user=user).membership.membership_type == Membership.PLUS

#@user_passes_test(subscription_check, login_url='/membership/')
def create_garden(request):
    form = GardenForm(request.POST or None)
    if form.is_valid():
        form.save(request.user)

        return redirect('/garden')
    context = {"form": form,
               "has_subscription": subscription_check(request.user)}
    return render(request, "create_garden.html", context)


@user_passes_test(subscription_check)
def update_garden(request, garden_id):
    garden = Garden.objects.get(id=garden_id)
    form = GardenForm(request.POST or None, instance=garden)
    if form.is_valid():
        form.save(request.user)
        return redirect('/garden')
    context = {"form": form}
    return render(request, "update_garden.html", context)


def delete_garden(request, garden_id):
    garden = Garden.objects.get(id=garden_id)
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


class MembershipView(ListView):
    model = Membership
    template_name = 'membership.html'

    def get_user_membership(self):
        user_membership_qs = UserMembership.objects.filter(user=self.request.user)
        if user_membership_qs.exists():
            return user_membership_qs.first()
        return None

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        current_membership = self.get_user_membership()
        context['current_membership'] = str(current_membership.membership)
        return context

    def post(self, request):
        current_membership = self.get_user_membership()
        current_membership.membership = Membership.objects.get(membership_type=request.POST.get('membership_type'))
        current_membership.save()
        return redirect('membership')
