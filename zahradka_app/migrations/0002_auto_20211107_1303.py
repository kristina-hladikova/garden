# Generated by Django 3.2.9 on 2021-11-07 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zahradka_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='event',
            name='type',
            field=models.CharField(choices=[('PL', 'Výsadba'), ('TR', 'Přesazování'), ('VA', 'Očkování'), ('GR', 'Roubování'), ('PC', 'Ochrana proti škůdcům'), ('HA', 'Sklizeň'), ('FE', 'Hnojení'), ('RE', 'Zmlazování'), ('PR', 'Stříhání')], max_length=2),
        ),
        migrations.AlterField(
            model_name='garden',
            name='description',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='plant',
            name='species',
            field=models.CharField(choices=[('TR', 'Strom'), ('BU', 'Keř'), ('HR', 'Bylina')], max_length=2),
        ),
        migrations.AlterField(
            model_name='plant',
            name='type',
            field=models.CharField(choices=[('FR', 'Ovoce'), ('VE', 'Zelenina'), ('DE', 'Okrasné')], max_length=2),
        ),
    ]