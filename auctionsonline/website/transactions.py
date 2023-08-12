from website.models import Users, Leiloes, Licitacoes
from django.utils import timezone
from datetime import datetime, timedelta

def increase_bid(user, leiloes):
    """
    Removes €1.0 from user.
    Creates a Bid record
    Increases the auction's number of bids

    Parameters
    ----------
    auction : class 'website.models.Auction
    """
    user = Users.objects.filter(user_id= Users.user_id)
    user.saldo = float(user.credito) - 1.0
    user.save()
    bid = Bid()
    bid.user_id = user
    bid.auction_id = auction
    bid.bid_time = timezone.now()
    bid.save()
    auction.number_of_bids += 1
    auction.time_ending = timezone.now() + timedelta(minutes=5)
    auction.save()

def remaining_time(leiloes):
    """
    Calculates the auction's remaining time
    in minutes and seconds and converts them 
    into a string.
    
    Parameters
    ----------
    auction : class 'website.models.Auction
    
    Returns
    -------
    
    time_left : str
        string representation of remaining time in
        minutes and seconds.
    expired : int
        if the value is less than zero then the auction ended.
    
    """
    tempo_em_falta = Leiloes.hora_fim - timezone.now()
    days, seconds = tempo_em_falta.days, tempo_em_falta.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    tempo_em_falta = str(minutes) + "m " + str(seconds) + "s"
    expired = days
    
    return tempo_em_falta, expired