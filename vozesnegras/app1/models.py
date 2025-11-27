
from django.db import models
from django.contrib.auth.models import User

# Categorias Temáticas (Arte, Música, etc) [cite: 36]
class Categoria(models.Model):
    nome = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nome

# Perfil do Usuário com Níveis e Conquistas [cite: 31]
class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    biografia = models.TextField(blank=True, max_length=500)
    nivel = models.IntegerField(default=1) # Começa no nível 1
    pontos = models.IntegerField(default=0)

    def __str__(self):
        return f"Perfil de {self.user.username}"

# A Postagem com Suporte Multimídia e Curadoria [cite: 31, 37]
class Postagem(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    conteudo = models.TextField(verbose_name="Descrição/Texto")
    # Arquivo para imagem, audio ou video
    midia = models.FileField(upload_to='uploads/', blank=True, null=True, verbose_name="Arquivo Multimídia")
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    aprovado = models.BooleanField(default=False) # Trava da Curadoria

    def total_votos(self):
        up = self.voto_set.filter(tipo='UP').count()
        down = self.voto_set.filter(tipo='DOWN').count()
        return up - down

# Sistema de Votação (Up/Down) [cite: 35]
class Voto(models.Model):
    TIPO = (('UP', 'Apoiar ✊🏿'), ('DOWN', 'Não Apoiar'))
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    postagem = models.ForeignKey(Postagem, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=4, choices=TIPO)

    class Meta:
        unique_together = ('usuario', 'postagem') # Evita voto duplo