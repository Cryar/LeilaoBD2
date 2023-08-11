from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = 'website'

urlpatterns = [
	path('', views.index, name='index'),
	path('login/', views.login_page, name='login_view'),
	path('logout/', views.logout_page, name='logout_view'),
	path('register/', views.register_page, name='register_page'),
	path('register/new_user/', views.register, name='register'),
    path('Leiloes/', views.produto_list, name='Leiloes'),
    path('category/<str:category>/', views.filter_leilao, name='filter_auctions'),
    path('watchlist/<int:auction_id>/', views.watchlist, name='watchlist'),
    path('balance/', views.balance, name='balance'),
    path('balance/topup/', views.topup, name='topup'),
    path('watchlist/', views.watchlist_page, name='watchlist'),
    path('bid/<int:auction_id>/', views.bid_page, name='bid_page'),
    path('bid/<int:auction_id>/raise_bid/', views.raise_bid, name='raise_bid'),
]
