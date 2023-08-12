from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Users(models.Model):
	user_id = models.IntegerField(primary_key=True, serialize=True, unique=True)
	username = models.CharField(max_length=40, unique=True)
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
	
class Watchlist(models.Model):
	Watchlist_id = models.IntegerField(primary_key=True, unique=True, serialize=True)
	user = models.ForeignKey(Users, on_delete=models.CASCADE)
	

class Leiloes(models.Model):
    leilao_id = models.IntegerField(primary_key= True, unique= True, serialize= True)
    numero_de_licitacoes = models.IntegerField()
    preco_base = models.DecimalField(max_digits=6, decimal_places=2)
    hora_inicio = models.DateTimeField()
    hora_fim = models.DateTimeField()
    incremento_minimo = models.DecimalField(max_digits=6, decimal_places=2, default=100.00)
    watch_list = models.ForeignKey(Watchlist, on_delete=models.CASCADE )

    def __str__(self):
        return "ID:" + str(self.pk) 
    
class Negociacoes(models.Model):
	negociacao_id = models.IntegerField(primary_key=True, serialize=True, unique=True)
	numero_de_licitacoes = models.IntegerField()
	valor_proposto = models.DecimalField(max_digits=6, decimal_places=2)
	hora_inicio = models.DateTimeField()
	hora_fim = models.DateTimeField()
	watch_list = models.ForeignKey(Watchlist, on_delete=models.CASCADE )



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
    lote = models.ForeignKey(Lotes, on_delete=models.CASCADE)
    leilao = models.ForeignKey(Leiloes, on_delete=models.CASCADE)
    negociacoes = models.ForeignKey(Negociacoes, on_delete=models.CASCADE, null=True)
    imagem = models.ImageField(upload_to='../media/images/')
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
	produto = models.ForeignKey(Produtos, on_delete=models.CASCADE)
	
	def __str__(self):
		return "USER_ID:" + str(self.user) + " LEILAO_ID:" + str(self.leilao)
	
class Licitacoes(models.Model):
	licitacao_id = models.IntegerField(primary_key=True, serialize=True, unique=True)
	user= models.ForeignKey(User, on_delete=models.CASCADE)
	leilao = models.ForeignKey(Leiloes, on_delete=models.CASCADE)
	negociacoes = models.ForeignKey(Negociacoes, on_delete=models.CASCADE)
	hora_licitacao = models.DateTimeField()
	valor_minimo = models.DecimalField(max_digits=6, decimal_places=2)
	valor_final = models.DecimalField(max_digits=6, decimal_places=2)
	estado = models.BooleanField(default=0)
	
	def __str__(self):
		return "USER_ID:" + str(self.user) + " LEILAO_ID:" + \
			str(self.leilao) + " " + str(self.hora_licitacao) 


class Faturas(models.Model):
	fatura_id = models.AutoField('Fatura ID', primary_key=True, unique=True, serialize=True)
	data_fatura  = models.DateField("Data da fatura")
	licitacao = models.ForeignKey(Licitacoes, on_delete=models.CASCADE)
 
