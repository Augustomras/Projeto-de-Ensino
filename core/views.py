from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from .models import Livro, Resenha

def home(request):
    livros = Livro.objects.all()
    resenhas = Resenha.objects.all()

    Usuario = get_user_model()
    leitores = Usuario.objects.filter(is_active=True)

    return render(request, 'core/home.html', {
        'livros': livros,
        'resenhas': resenhas,
        'leitores': leitores
    })

def explorar(request):
    livros = Livro.objects.all()

    return render(request, 'core/explorar.html', {
        'livros': livros
    })

def perfil(request):
    livros = Livro.objects.all()

    return render(request, 'core/perfil.html', {
        'livros': livros
    })

def adicionar_livro(request):
    return render(request, 'core/livro.html')

def detalhe_livro(request, livro_id):
    livro = get_object_or_404(Livro, id=livro_id)

    return render(request, 'core/detalhe_livro.html', {
        'livro': livro
    })

def perfil_leitor(request, usuario_id):
    Usuario = get_user_model()
    leitor = get_object_or_404(Usuario, id=usuario_id)

    return render(request, 'core/perfil.html', {
        'leitor': leitor,
        'livros': Livro.objects.all()
    })

def landing(request):
    return render(request, 'core/landing.html')

def cadastro(request):
    return render(request, 'core/cadastro.html')

def login_usuario(request):
    return render(request, 'core/login.html')