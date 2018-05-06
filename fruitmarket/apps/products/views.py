from django.views import generic
from django.urls import reverse_lazy
from .models import Fruit


class FruitList(generic.ListView):
    model = Fruit


class FruitEditMixin(object):
    model = Fruit
    success_url = reverse_lazy('products:fruits:list')


class FruitCreate(FruitEditMixin, generic.CreateView):
    fields = '__all__'


class FruitUpdate(FruitEditMixin, generic.UpdateView):
    fields = '__all__'


class FruitDelete(FruitEditMixin, generic.DeleteView):
    pass
