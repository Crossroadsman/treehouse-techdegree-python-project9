from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.utils import timezone

from .models import *
from .forms import *


def menu_list(request):
    menus = Menu.objects.filter(
        expiration_date__gte=timezone.now()
    ).prefetch_related('items')
    return render(
        request, 'menu/list_all_current_menus.html', {'menus': menus}
    )


def menu_detail(request, pk):
    menu = Menu.objects.get(pk=pk)
    return render(request, 'menu/menu_detail.html', {'menu': menu})


def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'menu/detail_item.html', {'item': item})


def create_new_menu(request):
    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            menu = form.save()
            return redirect('menu_detail', pk=menu.pk)
    else:
        form = MenuForm()
    return render(request, 'menu/menu_edit.html', {'form': form})


def edit_menu(request, pk):
    try:
        menu = Menu.objects.prefetch_related('items').get(pk=pk)
    except models.Menu.DoesNotExist:
        raise Http404

    if request.method != "POST":
        form = MenuForm(instance=menu)
        return render(request, 'menu/change_menu.html', {
            'form': form,
        })
    
    else:  # POST
        form = MenuForm(request.POST, instance=menu)
        if form.is_valid():
            menu = form.save()
            return redirect('menu_detail', pk=pk)
