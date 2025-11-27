from django.contrib import admin
from .models import Postagem, Categoria, Perfil, Voto

# Isso faz as tabelas aparecerem no painel /admin
admin.site.register(Postagem)
admin.site.register(Categoria)
admin.site.register(Perfil)
admin.site.register(Voto)