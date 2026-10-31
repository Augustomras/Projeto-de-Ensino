from django.shortcuts import render
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