from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from django.db.models import Count, Q #isso aqui é para buscra tudo

import calendar
from django.utils import timezone #pro desafio 
from datetime import timedelta #pro dias consecutivos

from .forms import CadastroForm, LivroForm, ResenhaForm, PAISES
from .models import Livro, Resenha, Perfil, VisualizacaoLivro, Denuncia

from django.views.decorators.http import require_POST # pro negocio de denuncia do admin la 

def cadastro(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)

        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect('core:home')

    else:
        form = CadastroForm()

    return render(
        request,
        'registration/cadastro.html',
        {'form': form}
    )


def termos(request):
    return render(request, 'termos_de_uso.html')


def privacidade(request):
    return render(request, 'politica_privacidade.html')


def landing(request):
    # Informações exibidas na tela inicial
    total_livros = Livro.objects.count()

    total_usuarios = get_user_model().objects.count()

    total_paises = Perfil.objects.exclude(
        pais__isnull=True
    ).exclude(
        pais=''
    ).values('pais').distinct().count()

    return render(request, 'core/landing.html', {
        'total_livros': total_livros,
        'total_usuarios': total_usuarios,
        'total_paises': total_paises,
    })

@login_required
def home(request):
    livros = Livro.objects.order_by('?')[:3]

    livros_populares = Livro.objects.annotate(
        total_favoritos=Count('favoritado_por')
    ).order_by('-total_favoritos')[:5]

    resenhas = Resenha.objects.select_related(
        'usuario', 'livro'
    ).order_by('-data_publicacao')[:5]

    Usuario = get_user_model()
    leitores = Usuario.objects.filter(is_active=True)

    hoje = timezone.localdate()

    
    # SEQUÊNCIA DE VISUALIZAÇÃO DE LIVROS
    datas_visualizacao = set(
        VisualizacaoLivro.objects.filter(
            usuario=request.user
        ).values_list('data_visualizacao', flat=True)
    )

    sequencia = 0

    if datas_visualizacao:
        ultima_data = max(datas_visualizacao)

        if ultima_data >= hoje - timedelta(days=1):
            data_atual = ultima_data

            while data_atual in datas_visualizacao:
                sequencia += 1
                data_atual -= timedelta(days=1)


    desafios = [
        {
            'titulo': 'Crítico literário',
            'descricao': 'Publique 5 resenhas este mês.',
            'meta': 5,
            'tipo': 'resenhas',
        },
        {
            'titulo': 'Leitor dedicado',
            'descricao': 'Publique 8 resenhas este mês.',
            'meta': 8,
            'tipo': 'resenhas',
        },
        {
            'titulo': 'Explorador literário',
            'descricao': 'Avalie livros de 3 autores diferentes.',
            'meta': 3,
            'tipo': 'autores',
        },
        {
            'titulo': 'Voz da comunidade',
            'descricao': 'Publique 10 resenhas este mês.',
            'meta': 10,
            'tipo': 'resenhas',
        },
    ]

    desafio = desafios[(hoje.month - 1) % len(desafios)]

    resenhas_mes = Resenha.objects.filter(
        usuario=request.user,
        data_publicacao__year=hoje.year,
        data_publicacao__month=hoje.month
    )

    if desafio['tipo'] == 'resenhas':
        progresso = resenhas_mes.count()
    else:
        progresso = resenhas_mes.values(
            'livro__autor'
        ).distinct().count()

    porcentagem = min(
        int((progresso / desafio['meta']) * 100),
        100
    )

    ultimo_dia = calendar.monthrange(
        hoje.year, hoje.month
    )[1]

    dias_restantes = ultimo_dia - hoje.day

    return render(request, 'core/home.html', {
        'livros': livros,
        'resenhas': resenhas,
        'leitores': leitores,
        'desafio': desafio,
        'progresso': progresso,
        'porcentagem': porcentagem,
        'dias_restantes': dias_restantes,
        'sequencia': sequencia,
        'livros_populares': livros_populares,
    })

@login_required
def explorar(request):
    livros = Livro.objects.all()

    dificuldade = request.GET.get('dificuldade')

    if dificuldade:
        livros = livros.filter(nivel_dificuldade=dificuldade)

    destaque_semana = Livro.objects.annotate(
        total_favoritos=Count('favoritado_por')
    ).filter(
        total_favoritos__gt=0
    ).order_by('-total_favoritos').first()

    return render(request, 'core/explorar.html', {
        'livros': livros,
        'destaque_semana': destaque_semana,
        'dificuldade_selecionada': dificuldade,
    })

@login_required
def perfil(request):
    leitor = request.user
    perfil = leitor.perfil

    resenhas = Resenha.objects.filter(
        usuario=leitor
    ).select_related('livro').order_by('-data_publicacao')

    return render(request, 'core/perfil.html', {
        'leitor': leitor,
        'perfil': perfil,
        'resenhas': resenhas,
        'total_resenhas': resenhas.count(),
    })


@login_required
def adicionar_livro(request):
    if request.method == "POST":
        form = LivroForm(request.POST)

        if form.is_valid():
            livro = form.save(commit=False)
            livro.criador = request.user
            livro.save()

            messages.success(request, "Livro cadastrado com sucesso!")
            return redirect("core:explorar")
    else:
        form = LivroForm()

    return render(request, "core/livro.html", {
        "form": form,
        "paises": PAISES,
    })

@login_required
def editar_livro(request, livro_id):
    livro = get_object_or_404(Livro, id=livro_id)

    # O criador e o administrador podem editar
    if livro.criador != request.user and not request.user.is_staff:
        messages.error(request, "Você não tem permissão para editar este livro.")
        return redirect('core:detalhe_livro', livro_id=livro.id)

    if request.method == "POST":
        form = LivroForm(request.POST, instance=livro)

        if form.is_valid():
            form.save()
            messages.success(request, "Livro atualizado com sucesso!")
            return redirect('core:detalhe_livro', livro_id=livro.id)

    else:
        form = LivroForm(instance=livro)

    return render(request, "core/livro.html", {
        "form": form,
        "paises": PAISES,
        "livro": livro,
    })

@login_required
def excluir_livro(request, livro_id):
    if not request.user.is_staff:
        messages.error(request, "Você não tem permissão para excluir livros.")
        return redirect('core:explorar')

    livro = get_object_or_404(Livro, id=livro_id)

    if request.method == "POST":
        livro.delete()
        messages.success(request, "Livro excluído com sucesso!")
        return redirect('core:explorar')

    return redirect('core:detalhe_livro', livro_id=livro.id)

# Detalhes do livro e publicação de resenhas
@login_required
def detalhe_livro(request, livro_id):
    livro = get_object_or_404(Livro, id=livro_id)

    VisualizacaoLivro.objects.get_or_create(
        usuario=request.user,
        livro=livro,
        data_visualizacao=timezone.localdate()
    )

    # Verifica se o formulário foi enviado
    if request.method == "POST":
        form = ResenhaForm(request.POST)

        if form.is_valid():
            resenha = form.save(commit=False)
            resenha.usuario = request.user
            resenha.livro = livro
            resenha.save()

            messages.success(request, "Resenha publicada com sucesso!")
            return redirect("core:detalhe_livro", livro_id=livro.id)

        else:
            messages.error(request, "Erro ao publicar resenha. Verifique os dados informados.")

    else:
        form = ResenhaForm()

    # Busca as resenhas relacionadas ao livro
    resenhas = livro.resenhas.select_related(
        "usuario"
    ).order_by("-data_publicacao")

    return render(request, "core/detalhe_livro.html", {
        "livro": livro,
        "resenhas": resenhas,
        "form": form
    })

@login_required
def perfil_leitor(request, usuario_id):
    Usuario = get_user_model()
    leitor = get_object_or_404(Usuario, id=usuario_id)

    perfil, criado = Perfil.objects.get_or_create(
    usuario=leitor,
    defaults={
        'nome_completo': leitor.get_full_name() or leitor.username
    }
)

    resenhas = Resenha.objects.filter(
        usuario=leitor
    ).select_related('livro').order_by('-data_publicacao')

    favoritos = perfil.livros_favoritos.all()

    return render(request, 'core/perfil.html', {
        'leitor': leitor,
        'perfil': perfil,
        'resenhas': resenhas,
        'total_resenhas': resenhas.count(),
        'favoritos': favoritos,
    })

# Excluir resenha
@login_required
def excluir_resenha(request, resenha_id):
    resenha = get_object_or_404(Resenha, id=resenha_id)

    if resenha.usuario != request.user:
        messages.error(request, "Você não pode excluir esta resenha.")
        return redirect("core:detalhe_livro", livro_id=resenha.livro.id)

    if request.method == "POST":
        livro_id = resenha.livro.id
        resenha.delete()

        messages.success(request, "Resenha deletada com sucesso!")
        return redirect("core:detalhe_livro", livro_id=livro_id)

    return render(request, "core/confirmar_exclusao.html", {
        "resenha": resenha,
    })


# Editar resenha
@login_required
def editar_resenha(request, resenha_id):
    resenha = get_object_or_404(Resenha, id=resenha_id)

    if resenha.usuario != request.user:
        messages.error(request, "Você não pode editar esta resenha.")
        return redirect("core:detalhe_livro", livro_id=resenha.livro.id)

    if request.method == "POST":
        form = ResenhaForm(request.POST, instance=resenha)

        if form.is_valid():
            resenha_atualizada = form.save()

            resenha_atualizada.refresh_from_db()

            print("AVALIAÇÃO NO BANCO:", resenha_atualizada.avaliacao)

            messages.success(request, "Resenha atualizada com sucesso!")
            return redirect("core:detalhe_livro", livro_id=resenha.livro.id)

        else:
            print("ERROS DO FORMULÁRIO:", form.errors)
            print("DADOS RECEBIDOS:", request.POST)

    else:
        form = ResenhaForm(instance=resenha)

    return render(request, "core/editar_resenha.html", {
        "form": form,
        "resenha": resenha,
    })

@login_required
def perfil(request):
    leitor = request.user
    perfil = leitor.perfil

    resenhas = Resenha.objects.filter(
        usuario=leitor
    ).select_related('livro').order_by('-data_publicacao')

    favoritos = perfil.livros_favoritos.all()

    return render(request, 'core/perfil.html', {
        'leitor': leitor,
        'perfil': perfil,
        'resenhas': resenhas,
        'total_resenhas': resenhas.count(),
        'favoritos': favoritos,
    })

@login_required
def favoritar_livro(request, livro_id):
    livro = get_object_or_404(Livro, id=livro_id)
    perfil = request.user.perfil

    if livro in perfil.livros_favoritos.all():
        perfil.livros_favoritos.remove(livro)
        messages.success(request, "Livro removido dos favoritos!")
    else:
        perfil.livros_favoritos.add(livro)
        messages.success(request, "Livro adicionado aos favoritos!")

    return redirect('core:detalhe_livro', livro_id=livro.id)

@login_required
def buscar_livros(request):
    pesquisa = request.GET.get('q', '')

    livros = Livro.objects.filter(
        titulo__icontains=pesquisa
    ) | Livro.objects.filter(
        autor__icontains=pesquisa
    ) | Livro.objects.filter(
        pais_origem__icontains=pesquisa
    )

    return render(request, 'core/buscar_livros.html', {
        'livros': livros,
        'pesquisa': pesquisa,
    })

@login_required
def buscar_leitores(request):
    pesquisa = request.GET.get('q', '')

    Usuario = get_user_model()

    leitores = Usuario.objects.filter(
        username__icontains=pesquisa
    ) | Usuario.objects.filter(
        first_name__icontains=pesquisa
    ) | Usuario.objects.filter(
        last_name__icontains=pesquisa
    )

    return render(request, 'core/buscar_leitores.html', {
        'leitores': leitores,
        'pesquisa': pesquisa,
    })

@login_required
def buscar(request):
    pesquisa = request.GET.get('q', '')

    livros = Livro.objects.filter(
        Q(titulo__icontains=pesquisa) |
        Q(autor__icontains=pesquisa) |
        Q(pais_origem__icontains=pesquisa)
    )

    Usuario = get_user_model()

    leitores = Usuario.objects.filter(
        Q(username__icontains=pesquisa) |
        Q(first_name__icontains=pesquisa) |
        Q(last_name__icontains=pesquisa)
    )

    return render(request, 'core/buscar.html', {
        'livros': livros,
        'leitores': leitores,
        'pesquisa': pesquisa,
    })

@login_required
def admin_denuncias(request):
    if not request.user.is_staff:
        return redirect('core:home')

    denuncias = Denuncia.objects.filter(
        status='pendente'
    ).select_related(
        'denunciante',
        'resenha',
        'resenha__usuario',
        'resenha__livro'
    ).order_by('-data_denuncia')

    return render(request, 'core/admin_denuncias.html', {
        'denuncias': denuncias
    })

@login_required
@require_POST
def ignorar_denuncia(request, denuncia_id):
    if not request.user.is_staff:
        return redirect('core:home')

    denuncia = get_object_or_404(Denuncia, id=denuncia_id)

    denuncia.status = 'ignorada'
    denuncia.save()

    return redirect('core:admin_denuncias')

@login_required
@require_POST
def remover_denuncia(request, denuncia_id):
    if not request.user.is_staff:
        return redirect('core:home')

    denuncia = get_object_or_404(Denuncia, id=denuncia_id)

    resenha = denuncia.resenha
    resenha.delete()

    return redirect('core:admin_denuncias')

@login_required
@require_POST
def denunciar_resenha(request, resenha_id):

    resenha = get_object_or_404(Resenha, id=resenha_id)

    if resenha.usuario == request.user:
        return redirect('core:detalhe_livro', livro_id=resenha.livro.id)

    motivo = request.POST.get('motivo')
    descricao = request.POST.get('descricao', '')

    denuncia_existente = Denuncia.objects.filter(
        denunciante=request.user,
        resenha=resenha
    ).exists()

    if denuncia_existente:
        return redirect('core:detalhe_livro', livro_id=resenha.livro.id)

    if motivo not in dict(Denuncia.MOTIVOS):
        return redirect('core:detalhe_livro', livro_id=resenha.livro.id)

    Denuncia.objects.create(
        denunciante=request.user,
        resenha=resenha,
        motivo=motivo,
        descricao=descricao
    )

    return redirect('core:detalhe_livro', livro_id=resenha.livro.id)