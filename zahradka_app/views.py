from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView, PasswordResetDoneView
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render, HttpResponse, resolve_url, redirect
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, DetailView, ListView
from django.views.generic.edit import FormMixin, CreateView

from zahradka_app.forms import GardenForm, ContactForm, SignUpForm
from zahradka_app.models import Plant, Garden, GardenPlant, Event, Membership, UserMembership, Subscription
from datetime import date
from zahradka_app.utils import get_user_membership


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
            return redirect("login")

        login(request, user)
        return redirect("homepage")


class MyChangePasswordView(PasswordChangeView):
    template_name = "accounts/change_password.html"
    success_url = reverse_lazy("homepage")

#
# class MyPasswordResetDoneView(PasswordResetDoneView):
#     template_name = "accounts/password_done.html"


class RegistrationView(FormMixin, TemplateView):
    template_name = "accounts/register.html"
    form_class = SignUpForm

    def post(self, request, *args, **kwargs):
        bounded_form = self.form_class(request.POST)
        if bounded_form.is_valid():
            bounded_form.save()
            return redirect("homepage")
        else:
            return TemplateResponse(request, "accounts/register.html", context={"form": bounded_form})


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
    plants = Plant.objects.filter(gardens__id=garden_id).order_by("name")
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


def subscription_check(user):
    return UserMembership.objects.get(user=user).membership.membership_type == Membership.PLUS


# @user_passes_test(subscription_check, login_url='/membership/')
def create_garden(request):
    form = GardenForm(request.POST or None, request.FILES, user=request.user)
    if form.is_valid():
        form.save(request.user)

        return redirect('/garden/')
    context = {"form": form,
               "has_subscription": subscription_check(request.user)}
    return render(request, "create_garden.html", context)


# @user_passes_test(subscription_check)
def update_garden(request, garden_id):
    garden = Garden.objects.get(id=garden_id)
    if request.method == 'GET':
        form = GardenForm(request.POST or None, instance=garden, user=request.user)
        context = {
            "form": form,
            "garden_id": garden_id
        }
        return render(request, "update_garden.html", context)

    elif request.method == 'POST':
        form = GardenForm(request.POST or None, request.FILES, instance=garden, user=request.user)
        if form.is_valid():
            form.save(request.user)
            return redirect(f'/garden/{garden_id}')
        else:
            context = {
                "form": form,
                "garden_id": garden_id
            }
            return render(request, "update_garden.html", context)


def delete_garden(request, garden_id):
    garden = Garden.objects.get(id=garden_id)
    garden.delete()
    return redirect('/garden/')


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

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        current_membership = get_user_membership(user=self.request.user)
        context['current_membership'] = str(current_membership)
        return context

    def post(self, request):
        # current_membership = get_user_membership(user=self.request.user)
        current_membership = UserMembership.objects.get(user=self.request.user)
        current_membership.membership = Membership.objects.get(membership_type=request.POST.get('membership_type'))
        current_membership.save()
        return redirect('membership')
