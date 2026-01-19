from django.http import Http404
from django.shortcuts import redirect, render
from django.contrib import messages

from django.urls import reverse

from django.contrib.auth.decorators import login_required    # é um decorator que coloca na view que quer que seja fechada
from django.contrib.auth import authenticate, login, logout

from .forms import RegisterForm, LoginForm

# Create your views here.

def register_view(request):
    # Recupera os dados da sessão do usuário ou None se não haver nada.
    register_form_data = request.session.get('register_form_data', None)

    # Se houver dados na sessão, ai é feito o 'bound Form'  Passando esses dados p/ o formulário que será criado
                                # Um bound form é um formulário que já está ligado a dados.
    # Cria o form
    form = RegisterForm(register_form_data)

    return render(request, 'authors/pages/register_view.html', {
        'form': form,
        'form_action': reverse('authors:register_create'),
    })

def register_create(request):
    # Cria o form
    if not request.POST:
        raise Http404        

    POST = request.POST
    
    # Joga os dados (o dicionário do POST inteiro) do post na sessão.
    # Salva os dados do form na sessão (do navegador) do usuário
    request.session['register_form_data'] = POST    

    form = RegisterForm(POST)

    if form.is_valid():
        user = form.save(commit = False)   # commit = False não deixa salvar na base de dados ainda. Apenas retorna o form.
        user.set_password(user.password)  # set_password   coloca criptografia no password.
        user.save()

        messages.success(request, 'Your user is created. Please log in.')        

        # deleta a chave 'register_form_data' desse  dicionário 
        del(request.session['register_form_data'])   

        return redirect(reverse('authors:login'))   # Redireciona para a página de login

    # Essa view não vai renderizar nada. Ela apenas vai ler os dados do POST e depois vai redirecionar novamente para
    # chamar o register_create que  renderiza register_view.html
    return redirect('authors:register') 


def login_view(request):
    form = LoginForm()
    return render(request, 'authors/pages/login.html', {
        'form': form,
        'form_action': reverse('authors:login_create')
    })

# Recebe o post de login e redireciona
def login_create(request):
    # Cria o form se passar uma requisição do tipo POST
    if not request.POST:
        raise Http404        

    form = LoginForm(request.POST)
    login_url = reverse('authors:login')

    if form.is_valid():
        # o método authenticate apenas verifica se é possível fazer a autenticação. Ele não faz login.
        authenticated_user = authenticate(
            username = form.cleaned_data.get('username', ''),
            password = form.cleaned_data.get('password', ''),
        )

        if authenticated_user is not None:
            messages.success(request, 'Your are logged in.')
            login(request, authenticated_user)
        else:
            messages.error(request, 'Invalid credentials')                        
    else:
        # se o form não for válido
        messages.error(request, 'Invalid username or password')
    
    return redirect(login_url)


# é um decorator que você coloca na view que você quer que seja fechada
@login_required(login_url = 'authors:login', redirect_field_name = 'next')         
def logout_view(request):
    if not request.POST:
        return redirect(reverse('authors:login'))

    if request.POST.get('username') != request.user.username:
        return redirect(reverse('authors:login'))
    
    
    logout(request)
    return redirect(reverse('authors:login'))