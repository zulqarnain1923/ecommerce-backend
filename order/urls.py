from django.urls import path
from order import views

urlpatterns = [
    path('add/',views.order.as_view()),
    path('month/data/',views.monthlydata)
]
