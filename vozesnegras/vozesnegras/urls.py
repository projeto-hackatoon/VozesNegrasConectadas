from django.contrib import admin
from django.urls import path
from app1.views import feed, nova_postagem, explorar, votar, chat_api, pagina_chat
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', feed, name='feed'),
    path('nova/', nova_postagem, name='nova_postagem'),
    path('votar/<int:post_id>/<str:tipo>/', votar, name='votar'),
    path('explorar/', explorar, name='explorar'),
    path('chat/', pagina_chat, name='chat_tela'),  
    path('api/chat/', chat_api, name='chat_api')
]


# Isso permite ver imagens/videos durante o desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)