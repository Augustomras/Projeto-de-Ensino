
from django.db import models
from django.conf import settings


class Livro(models.Model):

    NIVEIS = [
        ('iniciante', 'Iniciante'),
        ('intermediario', 'Intermediário'),
        ('avancado', 'Avançado'),
    ]

    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=150)
    pais_origem = models.CharField(max_length=100)
    descricao = models.TextField()

    nivel_dificuldade = models.CharField(
        max_length=20,
        choices=NIVEIS,
        default='intermediario'
    )

    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo



class Resenha(models.Model):
    usuario = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='resenhas',
        verbose_name="Usuário"
    )

    livro = models.ForeignKey(
        'Livro',
        on_delete=models.CASCADE,
        related_name='resenhas',
        verbose_name="Livro"
    )

    texto = models.TextField(verbose_name="Resenha")

    avaliacao = models.PositiveSmallIntegerField(
        verbose_name="Avaliação"
    )

    idioma = models.CharField(
        max_length=2,
        default='pt',
        verbose_name="Idioma"
    )

    data_publicacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Publicação"
    )

    def __str__(self):
        return f"{self.usuario.username} - {self.livro.titulo}"
