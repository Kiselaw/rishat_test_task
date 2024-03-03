from django.urls import path

from .views import CreateOrderView, IndexView, cancel_view, success_view

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('buy/', CreateOrderView.as_view(), name='create_order'),
    path('success/', success_view, name='success'),
    path('cancel/', cancel_view, name='cancel'),
]