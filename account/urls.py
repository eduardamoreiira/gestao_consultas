from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('', views.signIn, name='login'),
    path('login/', views.signIn, name='login'),
    path('register/', views.register_view, name='register'),
    path('home/', views.home, name='home'),
    path('sair/', views.signOut, name='sair'),
]
