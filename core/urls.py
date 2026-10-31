from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('explorar/', views.explorar, name='explorar'),
    path('perfil/', views.perfil, name='perfil'),
    path('adicionar-livro/', views.adicionar_livro, name='adicionar_livro'),
    path('livro/<int:livro_id>/', views.detalhe_livro, name='detalhe_livro'),
]
