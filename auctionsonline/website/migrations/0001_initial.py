# Generated by Django 4.2.4 on 2023-08-12 14:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Leiloes',
            fields=[
                ('leilao_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('numero_de_licitacoes', models.IntegerField()),
                ('preco_base', models.DecimalField(decimal_places=2, max_digits=6)),
                ('dia', models.DateField()),
                ('hora_inicio', models.TimeField()),
                ('hora_fim', models.TimeField()),
                ('incremento_minimo', models.DecimalField(decimal_places=2, default=100.0, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='Lotes',
            fields=[
                ('lote_id', models.IntegerField(primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('lote_nome', models.CharField(max_length=50)),
                ('descriacao', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Negociacoes',
            fields=[
                ('negociacao_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('numero_de_licitacoes', models.IntegerField()),
                ('valor_proposto', models.DecimalField(decimal_places=2, max_digits=6)),
                ('hora_inicio', models.DateTimeField()),
                ('hora_fim', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('user_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('username', models.CharField(max_length=40, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('p_nome', models.CharField(max_length=50)),
                ('u_nome', models.CharField(max_length=50)),
                ('credito', models.DecimalField(decimal_places=2, max_digits=6)),
                ('telefone', models.CharField(max_length=14)),
                ('endereco', models.CharField(max_length=255)),
                ('cidade', models.CharField(max_length=45)),
                ('cod_postal', models.CharField(max_length=45)),
                ('pais', models.CharField(max_length=45)),
                ('data_registo', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Watchlist',
            fields=[
                ('Watchlist_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.users')),
            ],
        ),
        migrations.CreateModel(
            name='Produtos',
            fields=[
                ('prod_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('titulo', models.CharField(max_length=255)),
                ('imagem', models.ImageField(upload_to='../media/images/')),
                ('descricao', models.CharField(max_length=500)),
                ('quantidade', models.IntegerField()),
                ('category', models.CharField(choices=[('LAP', 'Laptop'), ('CON', 'Console'), ('GAD', 'Gadget'), ('GAM', 'Game'), ('TEL', 'TV')], max_length=3)),
                ('data_insercao', models.DateTimeField(auto_now_add=True)),
                ('leilao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.leiloes')),
                ('lote', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.lotes')),
                ('negociacoes', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='website.negociacoes')),
            ],
        ),
        migrations.AddField(
            model_name='negociacoes',
            name='watch_list',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.watchlist'),
        ),
        migrations.CreateModel(
            name='Licitacoes',
            fields=[
                ('licitacao_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('hora_licitacao', models.DateTimeField()),
                ('valor_minimo', models.DecimalField(decimal_places=2, max_digits=6)),
                ('valor_final', models.DecimalField(decimal_places=2, max_digits=6)),
                ('estado', models.BooleanField(default=0)),
                ('leilao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.leiloes')),
                ('negociacoes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.negociacoes')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='leiloes',
            name='watch_list',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.watchlist'),
        ),
        migrations.CreateModel(
            name='Fotos',
            fields=[
                ('foto_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('url', models.ImageField(upload_to='LeilaoBD2/auctionsonline/media/images/')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.produtos')),
            ],
        ),
        migrations.CreateModel(
            name='Faturas',
            fields=[
                ('fatura_id', models.AutoField(primary_key=True, serialize=False, unique=True, verbose_name='Fatura ID')),
                ('data_fatura', models.DateField(verbose_name='Data da fatura')),
                ('licitacao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.licitacoes')),
            ],
        ),
    ]
