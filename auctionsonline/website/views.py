from django.contrib.auth.models import User
from django.shortcuts import render

from django.db import connection
from django.db.models import Q
from django.utils import timezone
from datetime import datetime
from itertools import chain

from website.forms import *
from website.models import Licitacoes, Leiloes, Produtos, Users, Leiloes, Lotes, Fotos, Negociacoes, Watchlist

from website.validation import validate_login, validate_registration
from website.transactions import increase_bid, remaining_time

def index(request):
    """
    The main page of the website

    Returns
    -------
    HTTPResponse
        The index page with the current and future Leiloes.
    """
    leilao = Leiloes.objects.filter(hora_fim__gte=datetime.now()).order_by('hora_inicio')

    try:
        if request.session['username']:
            user = Users.objects.get(username=request.session['username'])

            w = Watchlist.objects.filter(user.user_id)
            watchlist = Leiloes.objects.none()
            for item in w:
                l = Leiloes.objects.filter(id=item.Leilao_id)
                watchlist = list(chain(watchlist, l))

            userDetails = Users.objects.get(user.user_id)
            return render(request, 'index.html',
                {'Leiloes': leilao, 'balance': userDetails.credito, 'watchlist': watchlist})
    except KeyError:
        return render(request, 'index.html', {'Leiloes': leilao})

    return render(request, 'index.html', {'Leiloes': leilao})

def bid_page(request, leilao_id):
    """
    Returns the bid page for the
    selected Leiloes.

    Parametes
    ---------
    Leiloe_id : class 'int'

    Returns
    -------
    HTTPResponse
        Return the bidding page for the selected Leiloes.
    Function : index(request)
        If the user is not logged in.
    """
    print(type(leilao_id))
    try:
        # if not logged in return to the index page.
        if request.session['username']:
            # If the Leiloes hasn't started return to the index page.
            leilao = Leiloes.objects.filter(id=leilao_id)
            if leilao[0].hora_inicio > timezone.now():
                return index(request)
            user = User.objects.filter(username=request.session['username'])

            stats = []
            time_left, expired = remaining_time(leilao[0])
            stats.append(time_left) # First element in stats list

            current_cost = 0.20 + (leilao[0].numero_de_licitacoes * 0.20)
            current_cost = "%0.2f" % current_cost
            stats.append(current_cost)

            # Second element in stats list
            if expired < 0: # if Leiloes ended append false.
                stats.append(False)
            else:
                stats.append(True)

            # Third element in stats list
            latest_bid = Licitacoes.objects.all().order_by('-hora_licitacao')
            if latest_bid:
                winner = Users.objects.filter(id=latest_bid[0].user)
                stats.append(winner[0].username)
            else:
                stats.append(None)

            # Fourth element in stats list
            chat = Chat.objects.all().order_by('time_sent')
            stats.append(chat)

            # Getting user's watchlist.
            w = Watchlist.objects.filter(user_id=user[0])
            watchlist = Leiloes.objects.none()
            for item in w:
                l = Leiloes.objects.filter(id=item.Leilao_id)
                watchlist = list(chain(watchlist, l))

            return render(request, 'bid.html',
            {
                'Leiloes': leilao[0],
                'user': user[0],
                'stats': stats,
                'watchlist':watchlist
            })
    except KeyError:
        return index(request)

    return index(request)


def raise_bid(request, leilao_id):
    """
    Ver views
    """
    db_connection = connection
    
    leilao = Leiloes.objects.get(id=Leiloes.leilao_id)
    if leilao.hora_fim < timezone.now():
        return bid_page(request, leilao_id)
    elif leilao.hora_inicio > timezone.now():
        return index(request)

    try:
        if request.session['username']:
            user = Users.objects.get(username=request.session['username'])
            if user.credito > 0.0:
                latest_bid = Licitacoes.objects.filter(Leilao_id=leilao_id).order_by('-hora_licitacao')
                if not latest_bid:
                    increase_bid(user, leilao_id)
                else:
                    current_winner = Users.objects.filter(id=latest_bid[0].user)
                    if current_winner[0].user_id != user:
                        increase_bid(user, leilao_id)

            return bid_page(request, leilao_id)
    except KeyError:
        return index(request)

    return bid_page(request, leilao_id)

def register_page(request):
    """
    Returns the registration page.

    Returns
    -------
    HTTPResponse
        The registration page.
    """
    return render(request, 'register.html')

def watchlist(request, Leiloe_id):
    """
    Adds the Leiloes to the user's watchlist.

    Returns
    -------
    Function : index(request)
    """
    try:
        if request.session['username']:
            user = Users.objects.filter(username=request.session['username'])
            leilao = Leiloes.objects.filter(id=Leiloe_id)

            w = Watchlist.objects.filter(Leiloe_id=Leiloe_id)
            if not w:
                watchlist_item = Watchlist()
                watchlist_item.Leilao_id = leilao[0]
                watchlist_item.user_id = user[0]
                watchlist_item.save()
            else:
                w.delete()

            return index(request)
    except KeyError:
        return index(request)

    return index(request)

def watchlist_page(request):
    """
    Disguises the index page to look
    like a page with the Leiloes the
    user is watching.

    Returns
    -------
    HTTPResponse
        The index page with Leiloes the user is watching.
    Function : index(request)
        If the user is not logged in.
    """
    try:
        if request.session['username']:
            user = Users.objects.filter(username=request.session['username'])
            w = Watchlist.objects.filter(user_id=user[0])

            leilao = Leiloes.objects.none()
            for item in w:
                l = leilao.objects.filter(id=item.Leilao_id, hora_fim__gte=timezone.now())
                leilao = list(chain(Leiloes, l))
            return render(request, 'index.html', {
                'Leiloes': leilao,
                'user': user[0],
                'watchlist': w
            })
    except KeyError:
        return index(request)

def balance(request):
    """
    If the user is logged in returns
    a HTTPResponse with the page that
    allows the user to update his or her balance.

    Returns
    -------
    HTTPResponse
        The page with the user information
        that updates the account's balance.
    Function : index(request)
        If the user is not logged in.
    """
    try:
        if request.session['username']:
            user = User.objects.filter(username=request.session['username'])
            return render(request, 'balance.html', {'user': user[0]})
    except KeyError:
        return index(request)

    return index(request)

def topup(request):
    """
    Adds credit to user's current balance.

    Returns
    -------
    Function : index(request)
        If the user is not logged in.
    """
    if request.method == 'POST':
        form = TopUpForm(request.POST)
        if form.is_valid():
            try:
                if request.session['username']:
                    user = User.objects.get(username=request.session['username'])
                    userDetails = Users.objects.get(user_id=user.id)
                    userDetails.balance += form.cleaned_data['amount']
                    userDetails.save()
            except KeyError:
                return index(request)

    return index(request)

def filter_leilao(request, categoria):
    """
    Searches current and future Leiloes
    that belong in a categoria.

    Parameters
    ----------
    categoria : class 'str'
        The categoria name.

    Returns
    -------
    Function : index(request)
         If the user is not logged in.
    """
    f_leilao = []
    if categoria == "laptops":
        f_leilao = Leiloes.objects.filter(
            hora_fim__gte=datetime.now(), produto_id__categoria="LAP"
            ).order_by('hora_inicio')

    elif categoria == "consoles":
        f_leilao = Leiloes.objects.filter(
            hora_fim__gte=datetime.now(), produto_id__categoria="CON"
            ).order_by('hora_inicio')

    elif categoria == "games":
        f_leilao = Leiloes.objects.filter(
            hora_fim__gte=datetime.now(), produto_id__categoria="GAM"
            ).order_by('hora_inicio')

    elif categoria == "gadgets":
        f_leilao = Leiloes.objects.filter(
            hora_fim__gte=datetime.now(), produto_id__categoria="GAD"
            ).order_by('hora_inicio')

    elif categoria == "tvs":
        f_leilao = Leiloes.objects.filter(
            hora_fim__gte=datetime.now(), produto_id__categoria="TEL"
            ).order_by('hora_inicio')

    try:
        if request.session['username']:
            leilao = Leiloes.objects.filter(hora_fim__gte=datetime.now()).order_by('hora_inicio')
            user = Users.objects.filter(username=request.session['username'])

            w = Watchlist.objects.filter(user_id=user[0])
            watchlist = Leiloes.objects.none()
            for item in w:
                l = Leiloes.objects.filter(id=item.Leilao_id)
                watchlist = list(chain(watchlist, l))
            print(1)
            return render(request, 'index.html', {'Leiloes': f_leilao, 'user': user[0], 'watchlist': watchlist})
    except:
        return render(request, 'index.html', {'Leiloes': f_leilao})

    return index(request)

def register(request):
    """
    Registration POST request.

    Returns
    -------
    Function
        Index page request
    """
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            email = request.POST.get('email')
            p_nome = request.POST.get('p_nome')
            u_nome = request.POST.get('u_nome')
            credito = request.POST.get('credito')
            telefone = request.POST.get('telefone')
            endereco = request.POST.get('endereco')
            cidade = request.POST.get('cidade')
            cod_postal = request.POST.get('cod_postal')
            pais = request.POST.get('pais')
            data_registo = datetime.today         
            is_valid = validate_registration(
                username,
                password1,
                password2,
                email
            )
            if is_valid:
                # Create an User object with the form parameters.
                with connection.cursor() as cursor:
                    cursor.callproc(
                        'inserir_user',
                        [username, password1, email, p_nome, u_nome, 
                        credito, telefone, endereco, cidade, 
                        cod_postal, pais, data_registo]
                    )
    return index(request)

def login_page(request):
    """
    Login POST request.
        
    Returns
    -------
    Function
        Index page request    
    """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            is_valid = validate_login(
                form.cleaned_data['username'], 
                form.cleaned_data['password']
            )
            if is_valid :
                # Creates a session with 'form.username' as key.
                request.session['username'] = form.cleaned_data['username']
    return index(request)

def logout_page(request):
    """
    Deletes the session.
    
    Returns
    -------
    Function
        Index page request
    """
    try:
        del request.session['username']
    except:
        pass # if there is no session pass
    return index(request)

def produto_details(request, produto_id):
    produto = Produtos.objects.get(pk=produto_id)
    return render(request, 'produtos/produto_detail.html', {'produto': produto})

"""def produto_detail(request):
    # Get the database connection using the alias "default"
    db_connection = connection

    # Perform database operations
    with db_connection.cursor() as cursor:
        # Execute a SQL query
        cursor.execute("SELECT * FROM website_produtos")

        rows = cursor.fetchall()

    # Process the data or return a response
    return render(request, 'produtos.html', {'data': rows})"""

def produto_list(request):
    leilao = Leiloes.objects.select_related('produto_id').all()  # Fetch Leiloes with related produto details

    for l in leilao:
        time_remaining = l.hora_fim - timezone.now()
        if l.hora_fim > timezone.now():
            time_remaining
        else:
            time_remaining = None
            
    context = {
        'Leiloes': leilao,
    }

    return render(request, 'products.html', context)

def search_results_page(request):
    produto_ids = request.GET.getlist('produto_ids')
    
    matching_leiloes = Leiloes.objects.filter(produto_id__in=produto_ids)
    
    return render(request, 'search_results.html', {'matching_leiloes': matching_leiloes})

def search_leiloes(request):
    date = request.GET.get('date')
    time = request.GET.get('time')
    datetime_str = f'{date} {time}'
    search_datetime = timezone.make_aware(datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S'))

    matching_leiloes = Leiloes.objects.filter(
        hora_inicio__lte=search_datetime,
        hora_fim__gte=search_datetime
    )
    
    return render(request, 'search_results.html', {'matching_leiloes': matching_leiloes})

"""conexaomongo = pymongo.MongoClient("mongodb+srv://Areias:hu58lz@cluster0.kopdoil.mongodb.net/")["BD2Leilao"]

def session_name():
    bd = conexaomongo
    col2 = bd["session"]
    xx = col2.find({},{'_id': 0})
    for xxx in xx:
        col3 = bd["utilizadores"]
        yy = col3.find({'email': str(xxx["email"])},{'nome':(1), 'apelido':(1), '_id':(0)})
        for yyy in yy:
            nam = yyy["nome"]
            ape = yyy["apelido"]
            nome = nam + " " + ape
            return nome

def session_mail():
    bd = conexaomongo
    col = bd["session"]
    xx = col.find({},{'_id': 0})
    for xxx in xx:
        return str(xxx["email"])

def session():
    bd = conexaomongo
    col = bd["session"]
    x = col.count_documents({})
    return x"""
