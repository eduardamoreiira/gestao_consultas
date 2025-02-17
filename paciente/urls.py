from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin


app_name = 'paciente'

urlpatterns = [
    path('listar/', views.listar_paciente, name='listar_paciente'),
    path('cadastrar/', views.cadastrar_paciente, name='cadastrar_paciente'),
    path('detalhe/<int:id_paciente>/', views.detalhe_paciente, name='detalhe_paciente'),
    path('editar/<int:id_paciente>/', views.editar_paciente, name='editar_paciente'),
    path('excluir_paciente_ajax/<int:id_paciente>/', views.excluir_paciente_ajax, name='excluir_paciente_ajax'),
]
