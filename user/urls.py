from django.urls import path 
from user import views

urlpatterns = [
    path('user/', views.checkuser.as_view()),
    path('user/login/',views.userlogin),
    path('user/register/',views.userregister),
    path('user/token/',views.token),
    path('user/addtocart/',views.Cartadded.as_view()),
]
