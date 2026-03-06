from django.urls import path
from api1 import views

urlpatterns = [
    path('post/',views.post),
    path('get/',views.getdata),
    path('get/<str:id>',views.getdata),
    path('catagory/', views.catagory),
    path('catagory/<int:id>', views.catagory),
]
