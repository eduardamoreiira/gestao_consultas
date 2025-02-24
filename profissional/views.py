from django.shortcuts import redirect, render
from .models import Profissional
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.db import connection  # Importa a conexão com o banco
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


#função para cadastrar um profissional
def cadastrar_profissional(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        num_identificaco = request.POST.get('num_identificaco')
        sexo = request.POST.get('sexo')
        id_usuario = request.user.id  #pega o ID do usuário logado para saber qual usuário cadastrou o profissional

        try:
            #conectar ao banco e executar o INSERT
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO profissional (nome, email, telefone, num_identificaco, sexo)
                    VALUES (%s, %s, %s, %s, %s)
                """, (nome, email, telefone, num_identificaco, sexo))

            messages.success(request, f"Profissional {nome} foi cadastrado com sucesso!")
            return redirect('profissional:listar_profissional')

        except Exception as e:
            messages.error(request, f"Erro ao cadastrar profissional: {str(e)}")
            return HttpResponse(f"Erro ao cadastrar profissional: {str(e)}", status=500)

    return render(request, 'profissional/cadastrarProfissional.html')

#função que transforma o resultado da query em um dicionário (como se fosse um array associativo)
def dictfetchall(cursor):
    "Retorna todas as linhas como um dicionário"
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

#função para transformar o resultado da query em um dicionário e pegar apenas um resultado do dicionário
def dictfetchone(cursor):
    "Retorna uma única linha como um dicionário"
    columns = [col[0] for col in cursor.description]
    row = cursor.fetchone()
    return dict(zip(columns, row)) if row else None

#função para listar os profissionais cadastrados no sistema
def listar_profissional(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM profissional
                ORDER BY nome ASC 
            """)
            profissionais = dictfetchall(cursor)  #converte os resultados para dicionário (como se fosse um array)

        return render(request, 'profissional/listarProfissional.html', {'profissionais': profissionais})

    except Exception as e:
        messages.error(request, f"Erro ao listar profissionais: {str(e)}")
        return HttpResponse(f"Erro ao listar profissionais: {str(e)}", status=500)


#função para editar um profissional
def editar_profissional(request, id_profissional):
    try:
        with connection.cursor() as cursor:
            #busca o profissional pelo ID
            cursor.execute("""
                SELECT id_profissional, nome, email, telefone, num_identificaco, sexo 
                FROM profissional
                WHERE id_profissional = %s
            """, [id_profissional])
            
            columns = [col[0] for col in cursor.description]  #obtem os nomes das colunas
            profissional = cursor.fetchone()  #pega apenas um resultado

            if not profissional:
                messages.error(request, "Profissional não encontrado.")
                return redirect('profissional:listar_profissional')

            profissional = dict(zip(columns, profissional))  #convertendo para dicionário

        if request.method == 'POST':
            nome = request.POST.get('nome')
            email = request.POST.get('email')
            telefone = request.POST.get('telefone')
            num_identificaco = request.POST.get('num_identificaco')
            sexo = request.POST.get('sexo')

            with connection.cursor() as cursor:
                #atualiza os dados do profissional no bd
                cursor.execute("""
                    UPDATE profissional
                    SET nome = %s, email = %s, telefone = %s, num_identificaco = %s, sexo = %s
                    WHERE id_profissional = %s
                """, [nome, email, telefone, num_identificaco, sexo, id_profissional])

            messages.success(request, f"Profissional {nome} foi editado com sucesso!")
            return redirect('profissional:listar_profissional')

        return render(request, 'profissional/editarProfissional.html', {'profissional': profissional})

    except Exception as e:
        messages.error(request, f"Erro ao editar profissional: {str(e)}")
        return HttpResponse(f"Erro ao editar profissional: {str(e)}", status=500)

      
#função para excluir um profissional
@csrf_exempt
def excluir_profissional(request, id_profissional):
    if request.method == 'POST':  # Alterado para POST
        try:
            with connection.cursor() as cursor:
                # Verifica se o profissional existe no banco de dados antes de excluir
                cursor.execute("""
                    SELECT nome FROM profissional WHERE id_profissional = %s
                """, [id_profissional])
                profissional = cursor.fetchone()

                if not profissional:
                    return JsonResponse({"status": "error", "message": "Profissional não encontrado."}, status=404)

                nome_profissional = profissional[0]  # Obtém o nome do profissional

                # Exclui o profissional
                cursor.execute("""
                    DELETE FROM profissional WHERE id_profissional = %s
                """, [id_profissional])

            return JsonResponse({"status": "success", "message": f"Profissional {nome_profissional} excluído com sucesso!"})

        except Exception as e:
            return JsonResponse({"status": "error", "message": f"Erro ao excluir: {str(e)}"}, status=500)
    else:
        return JsonResponse({"status": "error", "message": "Método não permitido."}, status=405)


#função para visualizar as informações de um profissional
def detalhe_profissional(request, id_profissional):
    try:
        with connection.cursor() as cursor:
            #busca o profissional pelo ID e retorna um dicionário
            cursor.execute("""
                SELECT * FROM profissional
                WHERE id_profissional = %s
            """, [id_profissional])
            profissional = dictfetchone(cursor)  #pega apenas um resultado

        if not profissional:
            messages.error(request, "Profissional não encontrado.")
            return HttpResponse("Profissional não encontrado.", status=404)

        return render(request, 'profissional/detalheProfissional.html', {'profissional': profissional})

    except Exception as e:
        messages.error(request, f"Erro ao visualizar profissional: {str(e)}")
        return HttpResponse(f"Erro ao visualizar profissional: {str(e)}", status=500)



#função para buscar um profissional pelo nome, cpf ou num_identificacao
def buscar_profissional(request):
    try:
        if request.method == 'POST':
            termo = request.POST.get('termo')
            with connection.cursor() as cursor:
                # busca o profissional pelo nome, cpf ou num_identificacao e ordena a lista por ordem alfabética
                cursor.execute("""
                    SELECT * FROM profissional
                    WHERE nome LIKE %s OR num_identificacao LIKE %s OR cpf LIKE %s
                    ORDER BY nome ASC
                """, (f"%{termo}%", f"%{termo}%"))
                profissionais = cursor.fetchall()

            return render(request, 'listar_profissionais.html', {'profissionais': profissionais})

    except Exception as e:
        messages.error(request, f"Erro ao buscar profissional: {str(e)}")
        return HttpResponse(f"Erro ao buscar profissional: {str(e)}", status=500)