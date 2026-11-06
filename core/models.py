
from django.db import models
from django.conf import settings


class Perfil(models.Model):

    PAISES = [
        ('BR', 'Brasil'),
        ('PT', 'Portugal'),
        ('US', 'Estados Unidos'),
        ('JP', 'Japão'),
        ('FR', 'França'),
        ('KR', 'Coreia do Sul'),
        ('ES', 'Espanha'),
        ('IT', 'Itália'),
        ('DE', 'Alemanha'),
        ('UK', 'Reino Unido'),
        ('OUTRO', 'Outro'),
    ]

    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='perfil'
    )

    nome_completo = models.CharField(max_length=150)

    pais = models.CharField(
        max_length=10,
        choices=PAISES,
        default='BR'
    )

    data_criacao = models.DateTimeField(auto_now_add=True)

    livros_favoritos = models.ManyToManyField(
        'Livro',
        blank=True,
        related_name='favoritado_por'
    )

    def __str__(self):
        return self.usuario.username

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

    capa = models.URLField(
        max_length=500,
        blank=True,
        null=True
    )

    nivel_dificuldade = models.CharField(
        max_length=20,
        choices=NIVEIS,
        default='intermediario'

    )

    criador = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='livros_cadastrados'
    )
    
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo



class Resenha(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
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
        max_length=10,
        default='pt',
        verbose_name="Idioma"
    )

    data_publicacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Publicação"
    )

    def __str__(self):
        return f"{self.usuario.username} - {self.livro.titulo}"


class VisualizacaoLivro(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='visualizacoes'
    )

    livro = models.ForeignKey(
        'Livro',
        on_delete=models.CASCADE,
        related_name='visualizacoes'
    )

    data_visualizacao = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.livro.titulo}"

class Denuncia(models.Model):

    MOTIVOS = [
        ('odio', 'Discurso de ódio'),
        ('spam', 'Spam'),
        ('assedio', 'Assédio'),
        ('ofensivo', 'Conteúdo ofensivo'),
        ('outro', 'Outro'),
    ]

    STATUS = [
        ('pendente', 'Pendente'),
        ('ignorada', 'Ignorada'),
        ('resolvida', 'Resolvida'),
    ]

    denunciante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='denuncias_realizadas'
    )

    resenha = models.ForeignKey(
        'Resenha',
        on_delete=models.CASCADE,
        related_name='denuncias'
    )

    motivo = models.CharField(
        max_length=20,
        choices=MOTIVOS
    )

    descricao = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='pendente'
    )

    data_denuncia = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Denúncia de {self.denunciante.username}"