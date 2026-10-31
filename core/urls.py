from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('explorar/', views.explorar, name='explorar'),
    path('perfil/', views.perfil, name='perfil'),
]