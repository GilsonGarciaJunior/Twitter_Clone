"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path

from users.views import public_profile
from .views import cadastro_page, feed_page, home, login_page, perfil_page, seguidores_page, seguindo_page, usuários_page


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('posts.urls')),
    path('api/', include('users.urls')),
    path('', home, name='home'),
    path('login/', login_page, name='login'),
    path('feed/', feed_page, name='feed'),
    path('cadastro/', cadastro_page, name='cadastro'),
    path('perfil/', perfil_page, name='perfil'),
    path('usuarios/', usuários_page, name='usuarios'),
    path('usuarios/<int:user_id>/', public_profile, name='perfil-publico'),
    path('seguidores/', seguidores_page, name='seguidores'),
    path('seguindo/', seguindo_page, name='seguindo'),
]
