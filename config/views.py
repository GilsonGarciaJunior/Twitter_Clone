from django.shortcuts import render


def home(request):
    return render(
        request,
        'home.html'
    )

def login_page(request):
    return render(
        request,
        'login.html'
    )

def feed_page(request):
    return render(
        request,
        'feed.html'
    )

def cadastro_page(request):
    return render(
        request,
        'cadastro.html'
    )

def perfil_page(request):
    return render(
        request,
        'perfil.html'
    )

def usuários_page(request):
    return render(
        request,
        'usuários.html'
    )

def seguidores_page(request):
    return render(
        request,
        'seguidores.html'
    )


def seguindo_page(request):
    return render(
        request,
        'seguindo.html'
    )