from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('account.urls', namespace='account')),
    path('paciente/', include('paciente.urls', namespace='paciente')),
    path('profissional/', include('profissional.urls', namespace='profissional')),
    path('consulta/', include('consulta.urls', namespace='consulta')),
]
