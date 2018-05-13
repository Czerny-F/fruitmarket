from django.views import generic
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import Fruit


@method_decorator(login_required, name='dispatch')
class FruitList(generic.ListView):
    model = Fruit


class FruitEditMixin(object):
    model = Fruit
    success_url = reverse_lazy('products:fruits:list')


@method_decorator(login_required, name='dispatch')
class FruitCreate(FruitEditMixin, generic.CreateView):
    fields = '__all__'


@method_decorator(login_required, name='dispatch')
class FruitUpdate(FruitEditMixin, generic.UpdateView):
    fields = '__all__'


@method_decorator(login_required, name='dispatch')
class FruitDelete(FruitEditMixin, generic.DeleteView):
    pass
