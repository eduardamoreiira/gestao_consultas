from django.shortcuts import render, redirect, get_object_or_404
from .models import Paciente
from .forms import PacienteForm
from django.utils.timezone import now
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

#função para cadastrar um paciente
def cadastrar_paciente(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        cpf = request.POST.get('cpf')
        dt_nasc = request.POST.get('dt_nasc')
        sexo = request.POST.get('sexo')
        telefone = request.POST.get('telefone')
        email = request.POST.get('email')
        

        Paciente.objects.create(
            id_paciente=None,
            nome=nome,
            cpf=cpf,
            dt_nasc=dt_nasc,
            sexo=sexo,
            telefone=telefone,
            email=email,
            ativo='sim',
            dt_cadastro=now()  # Define a data atual
        )

        # Adiciona uma mensagem com o nome do paciente cadastrado
        messages.success(request, f"Paciente {nome} foi cadastrado com sucesso!")

        return redirect('paciente:listar_paciente')
    return render(request, 'paciente/cadastrarPaciente.html')

#função para listar os pacientes
def listar_paciente(request):
    pacientes = Paciente.objects.all()
    for paciente in pacientes:
        print(f"Paciente: {paciente.nome}, ID: {paciente.id_paciente}")
    return render(request, 'paciente/listarPaciente.html', {'pacientes': pacientes})

#função para editar um paciente
def editar_paciente(request, id_paciente):
    paciente = get_object_or_404(Paciente, id_paciente=id_paciente)    
    form = PacienteForm(request.POST or None, instance=paciente)
    if form.is_valid():
        form.save()
        messages.success(request, f"Paciente {paciente.nome} foi editado com sucesso!")
        return redirect('paciente:listar_paciente')
    return render(request, 'paciente/editarPaciente.html', {'form': form, 'paciente': paciente})


#função para visualizar as informações de um paciente
def detalhe_paciente(request, id_paciente):
    paciente = Paciente.objects.get(id_paciente=id_paciente)
    return render(request, 'paciente/detalhePaciente.html', {'paciente': paciente})


# função para excluir um paciente
@csrf_exempt  # Se não estiver usando CSRF Token no JavaScript, mas não recomendado
def excluir_paciente_ajax(request, id_paciente):
    if request.method == "POST":
        paciente = get_object_or_404(Paciente, id=id_paciente)
        paciente.delete()
        return JsonResponse({"success": True})
    
    return JsonResponse({"success": False, "error": "Método não permitido"}, status=405)



