from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.landing, name='landing'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('termos-de-uso/', views.termos, name='termos'),
    path('politica-de-privacidade/', views.privacidade, name='privacidade'),
    path('home/', views.home, name='home'),
    path('explorar/', views.explorar, name='explorar'),
    path('perfil/', views.perfil, name='perfil'),
    path('perfil/<int:usuario_id>/', views.perfil_leitor, name='perfil_leitor'),
    path('adicionar-livro/', views.adicionar_livro, name='adicionar_livro'),
    path('livro/<int:livro_id>/editar/', views.editar_livro, name='editar_livro'),
    path('livro/<int:livro_id>/excluir/', views.excluir_livro, name='excluir_livro'),
    path('livro/<int:livro_id>/', views.detalhe_livro, name='detalhe_livro'),
    path('resenha/<int:resenha_id>/excluir/', views.excluir_resenha, name='excluir_resenha'),
    path('resenha/<int:resenha_id>/editar/', views.editar_resenha, name='editar_resenha'),
    path('livro/<int:livro_id>/favoritar/', views.favoritar_livro, name='favoritar_livro'),
    path('buscar-livros/', views.buscar_livros, name='buscar_livros'),
    path('buscar-leitores/', views.buscar_leitores, name='buscar_leitores'),
    path('buscar/', views.buscar, name='buscar'),
    path('admin-denuncias/', views.admin_denuncias, name='admin_denuncias'),
    path('denuncia/<int:denuncia_id>/ignorar/', views.ignorar_denuncia, name='ignorar_denuncia'),
    path('denuncia/<int:denuncia_id>/remover/', views.remover_denuncia, name='remover_denuncia'),
    path('resenha/<int:resenha_id>/denunciar/', views.denunciar_resenha, name='denunciar_resenha'),
]