from django import forms
from website.models import Users

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=40)
    password1 = forms.CharField(max_length=100)
    password2 = forms.CharField(max_length=100)
    email = forms.EmailField()
    p_nome = forms.CharField(max_length=50)
    u_nome = forms.CharField(max_length=50)
    credito = forms.DecimalField(max_digits=6, decimal_places=2)
    telefone = forms.CharField(max_length=14)
    endereco = forms.CharField(max_length=255)
    cidade = forms.CharField(max_length=45)
    cod_postal = forms.CharField(max_length=45)
    pais = forms.CharField(max_length=45)
    data_registo = forms.DateField()

    class Meta:
            model = Users
            fields = '__all__'

class LoginForm(forms.Form):
    username = forms.CharField(max_length=45)
    password = forms.CharField(max_length=45)



