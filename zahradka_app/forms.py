from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from zahradka_app.models import Garden, Plant, Membership, UserMembership, Subscription
from zahradka_app.utils import get_user_membership


# class RegistrationForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']


class SignUpForm(UserCreationForm):
    try:
        free_membership = Membership.objects.get(membership_type=Membership.FREE)
    except Membership.DoesNotExist:
        pass

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self):
        user = super().save(commit=False)
        user.save()
        # Creating a new UserMembership
        user_membership = UserMembership.objects.create(user=user, membership=self.free_membership)
        user_membership.save()
        # Creating a new UserSubscription
        user_subscription = Subscription()
        user_subscription.user_membership = user_membership
        user_subscription.save()
        return user


class GardenForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    class Meta:
        model = Garden
        fields = ['name', 'description', 'address', 'garden_image', 'plant']

    plant = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                           queryset=Plant.objects.all().order_by('name'))

    def save(self, user):
        garden = super().save(commit=False)
        garden.user = user
        garden.save()
        garden.plant.set(self.cleaned_data.get('plant'))


    def clean_plant(self):
        membership = get_user_membership(self.user)
        value = self.cleaned_data['plant']
        if membership.membership_type != Membership.PLUS:

            if len(value) > 3:
                raise forms.ValidationError("Pokud nejste naším členem, je možné vybrat max. 3 rostliny. ")
        return value


class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email_address = forms.EmailField(max_length=150)
    message = forms.CharField(widget=forms.Textarea, max_length=2000)
