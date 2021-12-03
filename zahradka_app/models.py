import datetime

from django.contrib.auth.models import User
from django.db import models
from django.conf import settings


class Plant(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True, default='')

    TREE = 'TR'
    BUSH = 'BU'
    HERB = 'HR'
    SPECIES_NAME_CHOICES = [
        (TREE, 'Strom'),
        (BUSH, 'Keř'),
        (HERB, 'Bylina'),
    ]
    species = models.CharField(choices=SPECIES_NAME_CHOICES, max_length=2, unique=False)

    FRUIT = 'FR'
    VEGETABLE = 'VE'
    DECORATIVE = 'DE'
    OTHER = 'OT'
    TYPE_NAME_CHOICES = [
        (FRUIT, 'Ovoce'),
        (VEGETABLE, 'Zelenina'),
        (DECORATIVE, 'Okrasné'),
        (OTHER, 'Ostatní'),
    ]
    type = models.CharField(choices=TYPE_NAME_CHOICES, max_length=2, unique=False)
    plant_image = models.ImageField(null=True, upload_to='static/plant_photos/', height_field=None, width_field=None,
                                    max_length=20, blank=True)
    place = models.CharField(max_length=256, default='')
    soil = models.CharField(max_length=256, default='')
    other = models.CharField(max_length=256, default='')

    def __str__(self):
        return f"{self.name}"


class Event(models.Model):
    PLANTING = 'PL'
    TRANSPLANTING = 'TR'
    VACCINATION = 'VA'
    GRAFTING = 'GR'
    PEST_CONTROL = 'PC'
    HARVESTING = 'HA'
    FERTILISATION = 'FE'
    REJUVENATION = 'RE'
    PRUNING = 'PR'
    OTHER = 'OT'
    TYPE_EVENT_CHOICES = [
        (PLANTING, 'Výsadba'),
        (TRANSPLANTING, 'Přesazování'),
        (VACCINATION, 'Očkování'),
        (GRAFTING, 'Roubování'),
        (PEST_CONTROL, 'Ochrana proti škůdcům'),
        (HARVESTING, 'Sklizeň'),
        (FERTILISATION, 'Hnojení'),
        (REJUVENATION, 'Zmlazování'),
        (PRUNING, 'Stříhání'),
        (OTHER, 'Iné'),
    ]
    name = models.CharField(choices=TYPE_EVENT_CHOICES, max_length=20, unique=False)
    description = models.TextField(blank=True, default='')
    plant = models.ForeignKey(Plant, related_name="events", on_delete=models.CASCADE)

    # def is_event_planting(self) -> bool:
    #     return self.name == self.PLANTING

    # def get_name_display(self):
    #     return {self.event.name}
    # def __str__(self):
    #     return f'{self.get_name_display()}'

    def __str__(self):
        return f"{self.plant.name} - {self.get_name_display()}"


class TimeOfEvent(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    event = models.ForeignKey(Event, related_name="dates", on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.start_date = datetime.date(year=1970, month=self.start_date.month, day=self.start_date.day)
        self.end_date = datetime.date(year=1970, month=self.end_date.month, day=self.end_date.day)
        super().save(*args, **kwargs)  # Call the "real" save() method.


def user_directory_path(garden, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(garden.user.id, filename)


class Garden(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True, default='')
    address = models.CharField(max_length=512)
    plant = models.ManyToManyField(Plant, related_name="gardens", through="GardenPlant", blank=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    garden_image = models.ImageField(upload_to=user_directory_path, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"

    def get_url_slug(self):
        return self.get_name_display().lower()


class GardenPlant(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    garden = models.ForeignKey(Garden, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.garden.name} - {self.plant.name}"


class Membership(models.Model):
    PLUS = 'PL'
    FREE = 'FR'
    MEMBERSHIP_CHOICES = (
        (PLUS, 'plus'),
        (FREE, 'základní')
    )
    slug = models.SlugField(null=True, blank=True)
    membership_type = models.CharField(choices=MEMBERSHIP_CHOICES, default=FREE, max_length=30)
    price = models.DecimalField(default=0, max_digits=999, decimal_places=2)

    def __str__(self):
        return f"{self.get_membership_type_display()}"

    def __str__(self):
        return self.membership_type


class UserMembership(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='user_membership', on_delete=models.CASCADE)
    membership = models.ForeignKey(Membership, related_name='user_membership', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username


class Subscription(models.Model):
    user_membership = models.ForeignKey(UserMembership, related_name='subscription', on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.user_membership.user.username
