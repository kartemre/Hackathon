from django.contrib import admin
from django.urls import path
from myApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('auth_home/', views.auth_home, name='auth_home'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout, name='logout'),
    path('tesvik/', views.tesvik, name='tesvik'),  # Yeni rota
    path('forget/', views.forget, name='forget'),  # Şifremi unuttum sayfası

]

