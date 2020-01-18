from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.index,name='name'),
    path('home',views.home,name='home'),
    path('dregister.html',views.dregir,name='dregir'),
    path('dregister',views.dregister,name='dregister'),
    path('dlogin',views.dlogin,name='dlogin'),
    path('pregister',views.pregister,name='pregister'),
    path('nregister',views.nregister,name='nregister'),
    path('vregister',views.vregister,name='vregister'),
]