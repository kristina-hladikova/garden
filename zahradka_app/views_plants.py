from django.shortcuts import render

from zahradka_app.models import Plant


def vegetable(request):
    plants = Plant.objects.filter(type='VE').order_by('name')
    context = {
        'plants': plants,
    }
    return render(request, 'plants/vegetable.html', context=context)


def fruit(request):
    plants = Plant.objects.filter(type='FR', species='HR' or 'BU').order_by('name')
    context = {
        'plants': plants,
    }
    return render(request, 'plants/fruit.html', context=context)


def herbs(request):
    plants = Plant.objects.filter(other='bylinky').order_by('name')
    context = {
        'plants': plants,
    }
    return render(request, 'plants/plants.html', context=context)


def fruit_tree(request):
    plants = Plant.objects.filter(type='FR', species='TR').order_by('name')
    context = {
        'plants': plants,
    }
    return render(request, 'plants/fruit.html', context=context)
