from django.shortcuts import render, redirect, get_object_or_404
from .models import Postagem, Voto, Categoria
from .forms import PostagemForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count

def feed(request):
    # Feed prioriza posts aprovados pela curadoria [cite: 34]
    posts = Postagem.objects.filter(aprovado=True).order_by('-data_criacao')
    categorias = Categoria.objects.all()
    return render(request, 'feed.html', {'posts': posts, 'categorias': categorias})

@login_required
def nova_postagem(request):
    if request.method == 'POST':
        form = PostagemForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = request.user
            post.save()
            # Redireciona com mensagem (idealmente usaria django messages)
            return redirect('feed')
    else:
        form = PostagemForm()
    return render(request, 'nova_postagem.html', {'form': form})

@login_required
def votar(request, post_id, tipo):
    post = get_object_or_404(Postagem, id=post_id)
    Voto.objects.update_or_create(
        usuario=request.user, 
        postagem=post,
        defaults={'tipo': tipo}
    )
    return redirect('feed')

def explorar(request):
    # Página de categorias e tópicos em alta [cite: 36]
    return render(request, 'feed.html') # Simplificado para usar o mesmo template por enquanto