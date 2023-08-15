from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.db import models

# Create your models here.


class Users(models.Model):
	user_id = models.IntegerField(primary_key=True, serialize=True, unique=True)
	username = models.CharField(max_length=40, null=True)
	password = models.CharField(max_length=100)
	email = models.EmailField()
	p_nome = models.CharField(max_length=50)
	u_nome = models.CharField(max_length=50)
	credito = models.DecimalField(max_digits=6, decimal_places=2)
	telefone = models.CharField(max_length=14,)
	endereco = models.CharField(max_length=255)
	cidade = models.CharField(max_length=45)
	cod_postal = models.CharField(max_length=45)
	pais = models.CharField(max_length=45)
	data_registo = models.DateField()

	def __str__(self):
		user = Users.objects.get(id=self.user_id)
		return "id=" + str(self.pk) + " username=" + Users.username + " email=" + Users.email
	

class Leiloes(models.Model):
    leilao_id = models.IntegerField(primary_key= True, unique= True, serialize= True)
    numero_de_licitacoes = models.IntegerField()
    preco_base = models.FloatField()
    data_hora_inicio = models.DateTimeField()
    data_hora_fim = models.DateTimeField()
    incremento_minimo = models.FloatField(default=100.00)

    def __str__(self):
        return "ID:" + str(self.pk) 
    
class Negociacoes(models.Model):
	negociacao_id = models.IntegerField(primary_key=True, serialize=True, unique=True)
	numero_de_licitacoes = models.IntegerField()
	valor_proposto = models.FloatField()
	data_hora_inicio = models.DateTimeField()
	data_hora_fim = models.DateTimeField()

class Watchlist(models.Model):
	watchlist_id = models.IntegerField(primary_key=True, unique=True, serialize=True)
	temp_user_id = models.CharField()
	leiloes = models.ManyToManyField(Leiloes)
	negociacoes = models.ManyToManyField(Negociacoes)


class Lotes(models.Model):
	lote_id = models.IntegerField('ID', primary_key=True, serialize=True, unique=True)
	lote_nome = models.CharField(max_length=50)
	descriacao = models.TextField()
	
	def __str__(self):
		return 'LOTE ID:'+ str(self.pk) 


class Produtos(models.Model):
    CATEGORIA= (
		('LAP', 'Laptop'),
		('CON', 'Console'),
		('GAD', 'Gadget'),
		('GAM', 'Game'),
		('TEL', 'TV')
	)
    prod_id = models.IntegerField(primary_key=True, unique=True, serialize=True)
    titulo = models.CharField(max_length=255)
    lote = models.ForeignKey(Lotes, on_delete=models.PROTECT)
    leilao = models.ForeignKey(Leiloes, on_delete=models.PROTECT, null=True)
    negociacoes = models.ForeignKey(Negociacoes, on_delete=models.PROTECT, null=True)
    descricao = models.CharField(max_length=500)
    quantidade = models.IntegerField()
    category = models.CharField(
		max_length=3,
		choices=CATEGORIA
	)
    data_insercao = models.DateTimeField(auto_now_add=True, blank=True)
    def __str__(self):
        return "ID:" + str(self.pk) + " " + self.titulo

class Fotos(models.Model):
	foto_id = models.IntegerField(primary_key=True, unique=True, serialize=True)
	url= models.ImageField(upload_to=('LeilaoBD2/auctionsonline/media/images/')) 
	produto = models.ForeignKey(Produtos, on_delete=models.PROTECT)
	
	def __str__(self):
		return "USER_ID:" + str(self.user) + " PRODUTO_ID:" + str(self.produto)
	
class Licitacoes(models.Model):
	licitacao_id = models.IntegerField(primary_key=True, serialize=True, unique=True)
	user= models.ForeignKey(User, on_delete=models.CASCADE)
	leilao = models.ForeignKey(Leiloes, on_delete=models.CASCADE, null=True)
	negociacoes = models.ForeignKey(Negociacoes, on_delete=models.CASCADE, null=True)
	data_hora_licitacao = models.DateTimeField()
	valor_minimo = models.FloatField()
	valor_final = models.FloatField()
	estado = models.BooleanField(default=0)
	
	def __str__(self):
		return "USER_ID:" + str(self.user) + " LEILAO_ID:" + \
			str(self.leilao) + " " + str(self.data_hora_licitacao) 


class Faturas(models.Model):
	fatura_id = models.AutoField('Fatura ID', primary_key=True, unique=True, serialize=True)
	data_fatura  = models.DateTimeField("Data da fatura")
	licitacao = models.ForeignKey(Licitacoes, on_delete=models.CASCADE)
 
