# Generated by Django 3.2.9 on 2021-11-20 09:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zahradka_app', '0002_alter_event_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='type',
            new_name='name',
        ),
    ]