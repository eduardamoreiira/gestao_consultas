from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

app_name = 'consulta'

urlpatterns = [
    path('listar/', views.listar_consulta, name='listar_consulta'),
    path('cadastrar/', views.cadastrar_consulta, name='cadastrar_consulta'),
    path('editar/<int:id_consulta>/', views.editar_consulta, name='editar_consulta'),
    path('excluir/<int:id_consulta>/', views.excluir_consulta, name='excluir_consulta'),    
]