from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginpage, name='login'),
    path('register/',views.student_register,name='register'),
    path('contactus/',views.contact,name='contact'),
]