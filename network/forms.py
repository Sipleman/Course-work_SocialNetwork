from django import forms


class LoginForm(forms.Form):
    login_name = forms.CharField(label='Your login', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput())


class RegistrationForm(forms.Form):
    login_name = forms.CharField(label='Your login', max_length=100)
    email = forms.EmailField(label="E-mail address")
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
    name = forms.CharField(label='Your name', max_length=100)
    lastname = forms.CharField(label='Your last name', max_length=100)


