from django.db import models


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
    species = models.CharField(choices=SPECIES_NAME_CHOICES, max_length=2, unique=True)

    FRUIT = 'FR'
    VEGETABLE = 'VE'
    DECORATIVE = 'DE'
    TYPE_NAME_CHOICES = [
        (FRUIT, 'Ovoce'),
        (VEGETABLE, 'Zelenina'),
        (DECORATIVE, 'Okrasné'),
    ]
    type = models.CharField(choices=TYPE_NAME_CHOICES, max_length=2, unique=True)
    event = models.ForeignKey("Event", related_name="plants", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.get_name_display()} : {self.id}'


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
    ]
    type = models.CharField(choices=TYPE_EVENT_CHOICES, max_length=2, unique=True)
    description = models.TextField()
    time = models.ForeignKey("TimeOfEvent", related_name="events", on_delete=models.CASCADE)


class TimeOfEvent(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()


class Garden(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    address = models.CharField(max_length=512)
    plant = models.ForeignKey(Plant, related_name="gardens", on_delete=models.CASCADE)












