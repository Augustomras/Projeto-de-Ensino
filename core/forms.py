
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Perfil, Livro, Resenha
from django.conf import settings


class CadastroForm(UserCreationForm):

    nome_completo = forms.CharField(
        max_length=150,
        required=True
    )

    email = forms.EmailField(
        required=True
    )

    pais = forms.ChoiceField(
        choices=Perfil.PAISES,
        required=True
    )

    class Meta:
        model = User
        fields = [
            'nome_completo',
            'username',
            'email',
            'pais',
            'password1',
            'password2'
        ]

    def clean_email(self):
        email = self.cleaned_data['email'].strip()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                'Este e-mail já está cadastrado.'
            )

        return email

    def save(self, commit=True):
        usuario = super().save(commit=False)

        usuario.email = self.cleaned_data['email']

        if commit:
            usuario.save()

            Perfil.objects.create(
                usuario=usuario,
                nome_completo=self.cleaned_data['nome_completo'],
                pais=self.cleaned_data['pais']
            )

        return usuario
PAISES = [
    # América
    'Antígua e Barbuda', 'Argentina', 'Bahamas', 'Barbados', 'Belize',
    'Bolívia', 'Brasil', 'Canadá', 'Chile', 'Colômbia', 'Costa Rica',
    'Cuba', 'Dominica', 'El Salvador', 'Equador', 'Estados Unidos',
    'Granada', 'Guatemala', 'Guiana', 'Haiti', 'Honduras', 'Jamaica',
    'México', 'Nicarágua', 'Panamá', 'Paraguai', 'Peru',
    'República Dominicana', 'Santa Lúcia', 'São Cristóvão e Névis',
    'São Vicente e Granadinas', 'Suriname', 'Trinidad e Tobago',
    'Uruguai', 'Venezuela',

    # Europa
    'Alemanha', 'Áustria', 'Bélgica', 'Croácia', 'Dinamarca',
    'Espanha', 'Finlândia', 'França', 'Grécia', 'Holanda',
    'Hungria', 'Irlanda', 'Islândia', 'Itália', 'Noruega',
    'Polônia', 'Portugal', 'Reino Unido', 'República Tcheca',
    'Romênia', 'Rússia', 'Suécia', 'Suíça', 'Ucrânia',

    # Ásia
    'Arábia Saudita', 'China', 'Coreia do Norte', 'Coreia do Sul',
    'Emirados Árabes Unidos', 'Filipinas', 'Índia', 'Indonésia',
    'Irã', 'Iraque', 'Israel', 'Japão', 'Malásia', 'Nepal',
    'Paquistão', 'Singapura', 'Tailândia', 'Taiwan', 'Turquia',
    'Vietnã',

    # África
    'África do Sul', 'Angola', 'Argélia', 'Camarões', 'Egito',
    'Etiópia', 'Gana', 'Marrocos', 'Moçambique', 'Nigéria',
    'Quênia', 'Senegal', 'Tanzânia', 'Tunísia',

    # Oceania
    'Austrália', 'Fiji', 'Nova Zelândia', 'Papua-Nova Guiné'
]

class LivroForm(forms.ModelForm):

    pais_origem = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'list': 'lista-paises',
            'placeholder': 'Digite o nome do país...'
        })
    )

    capa = forms.URLField(
        required=True,
        widget=forms.URLInput(attrs={
            'placeholder': 'Cole o link da capa do livro'
        })
    )

    class Meta:
        model = Livro
        fields = [
            'titulo',
            'autor',
            'pais_origem',
            'descricao',
            'nivel_dificuldade',
            'capa'
        ]

        widgets = {
            'capa': forms.URLInput(attrs={
                'placeholder': 'Cole o link da capa do livro'
            })
        }


class ResenhaForm(forms.ModelForm):

    avaliacao = forms.ChoiceField(
        choices=[
            (1, '1 estrela'),
            (2, '2 estrelas'),
            (3, '3 estrelas'),
            (4, '4 estrelas'),
            (5, '5 estrelas'),
        ],
        required=True
    )

    idioma = forms.ChoiceField(
        choices=settings.LANGUAGES,
        required=True
    )

    class Meta:
        model = Resenha
        fields = [
            'texto',
            'avaliacao',
            'idioma'
        ]

        widgets = {
            'texto': forms.Textarea(attrs={
                'placeholder': 'Escreva uma resenha sobre o livro...',
                'rows': 4
            })
        }