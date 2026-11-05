from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.landing, name='landing'),
    path('home/', views.home, name='home'),
    path('explorar/', views.explorar, name='explorar'),
    path('perfil/', views.perfil, name='perfil'),
    path('perfil/<int:usuario_id>/', views.perfil_leitor, name='perfil_leitor'),
    path('adicionar-livro/', views.adicionar_livro, name='adicionar_livro'),
    path('livro/<int:livro_id>/', views.detalhe_livro, name='detalhe_livro'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login_usuario, name='login'),
]