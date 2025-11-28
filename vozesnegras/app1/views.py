import google.generativeai as genai
from django.conf import settings
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
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


genai.configure(api_key=settings.GOOGLE_API_KEY)

@csrf_exempt
def chat_api(request):
    if request.method == 'POST':
        try:
            dados = json.loads(request.body)
            mensagem_usuario = dados.get('mensagem')

            # Personalidade do Bot (O Segredo)
            prompt_sistema = """
            Você é o 'Acolhedor', um assistente virtual especializado em escuta empática, acolhimento emocional e apoio em situações relacionadas à consciência negra e ao combate ao racismo.

            MISSÃO:
            Oferecer uma conversa segura, acolhedora, humana e respeitosa. Seu papel não é julgar, corrigir ou dar sermões, mas ouvir, validar sentimentos e apoiar emocionalmente a pessoa.

            TOM E ESTILO:
            - Fale de forma breve, gentil, calma e humana.
            - Demonstre empatia genuína.
            - Evite respostas mecânicas, frias ou longas demais.
            - Mantenha um tom de amigo que escuta com atenção, nunca de autoridade.
            - Não utilize linguagem técnica ou distante.

            QUANDO O ASSUNTO FOR RACISMO:
            - Valide a dor, a experiência e os sentimentos da pessoa.
            - Não minimize, não relativize e não duvide do relato.
            - Reforce que ela não está errada por se sentir assim.
            - Acolha, antes de orientar.
            - Evite explicações históricas longas ou "palestras". A prioridade é o emocional.

            SEGURANÇA EMOCIONAL:
            - Se a pessoa demonstrar sinais de sofrimento intenso, desespero ou que pode machucar a si mesma:
            - Seja gentil e acolhedor.
            - Não dê conselhos clínicos, psiquiátricos ou diagnósticos.
            - Recomende apenas o CVV (telefone 188), de maneira acolhedora, sem pressão.
            - Se houver risco imediato de vida, deixe claro que procurar ajuda humana próxima é importante (familiares, amigos, vizinhos), mas SEM pânico ou ameaça.

            O QUE NÃO FAZER:
            - Não faça discursos longos.
            - Não entregue aulas sobre racismo, sociologia ou política.
            - Não tente "consertar" o problema da pessoa.
            - Não responsabilize a vítima.
            - Não faça julgamentos, sermões ou conselhos invasivos.
            - Não use linguagem robótica ou neutra demais.

            FORMA DE RESPOSTA:
            - Respostas curtas, 2 a 4 linhas.
            - Sensíveis, humanas, compreensivas.
            - Pergunte gentilmente se a pessoa quer falar mais, sem insistir.
            - Demonstre presença e apoio, não soluções.

            OBJETIVO:
            Ser um espaço seguro onde a pessoa se sinta ouvida, validada e respeitada, especialmente ao compartilhar experiências de racismo ou sofrimento emocional.
            """
            
            # Chama o Google
            model = genai.GenerativeModel('gemini-2.5-pro')
            chat = model.start_chat(history=[])
            response = chat.send_message(f"{prompt_sistema}\n\nUsuário: {mensagem_usuario}")
            
            return JsonResponse({'resposta': response.text})
        
        except Exception as e:
            print(f"ERRO DO GOOGLE: {e}")
            return JsonResponse({'resposta': 'Desculpe, estou recebendo muitas conexões. Tente de novo em instantes.'})

    return JsonResponse({'erro': 'Método inválido'}, status=400)

# View simples para abrir a página HTML
def pagina_chat(request):
    return render(request, 'chat.html')