from django.contrib import admin
from .models import *

#Username : admin
#Password : administrator

# Register your models here.
admin.site.register(Users)
admin.site.register(Produtos)
admin.site.register(Leiloes)
admin.site.register(Negociacoes)
admin.site.register(Watchlist)
admin.site.register(Faturas)
admin.site.register(Lotes)
admin.site.register(Fotos)
