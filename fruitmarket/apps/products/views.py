from django.views import generic
from django.urls import reverse_lazy
from .models import Fruit


class FruitList(generic.ListView):
    model = Fruit


class FruitCreate(generic.CreateView):
    model = Fruit
    fields = '__all__'
    success_url = reverse_lazy('products:fruits:list')


class FruitUpdate(generic.UpdateView):
    model = Fruit
    fields = '__all__'
    success_url = reverse_lazy('products:fruits:list')


class FruitDelete(generic.DeleteView):
    model = Fruit
    success_url = reverse_lazy('products:fruits:list')
