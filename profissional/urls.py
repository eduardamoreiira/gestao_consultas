from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

app_name = 'profissional'

urlpatterns = [
    path('listar/', views.listar_profissional, name='listar_profissional'),
    path('cadastrar/', views.cadastrar_profissional, name='cadastrar_profissional'),
    path('detalhe/<int:id_profissional>/', views.detalhe_profissional, name='detalhe_profissional'),
    path('editar/<int:id_profissional>/', views.editar_profissional, name='editar_profissional'),
    path('excluir/<int:id_profissional>/', views.excluir_profissional, name='excluir_profissional'),
    #path('buscar/int:id_profissional>/', views.buscar_profissional, name='buscar_profissional'),
] 
