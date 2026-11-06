from django.contrib import admin
from .models import Livro, Perfil, Resenha

admin.site.register(Livro)
admin.site.register(Resenha)
admin.site.register(Perfil)