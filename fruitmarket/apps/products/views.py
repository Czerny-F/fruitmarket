from django.views import generic
from .models import Fruit


class FruitList(generic.ListView):
    model = Fruit
