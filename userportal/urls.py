from django.urls import path
from .views import *

urlpatterns = [
    path('home', home, name = "home"),
    path('add-item', addItem, name = "add-item"),
    path('cart', cart, name = "cart"),
    path('order', cartOrder),
    path('add', add),
    path('remove', remove)

]
