from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path('',views.index,name='index'),
    path('about/',views.about_view,name='about'),
    path('services/',views.services,name='services'),
    path('dash/',views.dash,name='dash'),
    path('model/',views.model,name='model'),
    path('logout/', views.logout_view, name='logout'),
]