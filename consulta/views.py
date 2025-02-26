from django.shortcuts import redirect, render
from django.db import connection
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

#função para cadastrar uma consulta
def cadastrar_consulta(request):
    if request.method == 'POST':  
        dt_consulta = request.POST.get('dt_consulta')  
        hr_consulta = request.POST.get('hr_consulta') 
        id_profissional = request.POST.get('id_profissional')  
        id_paciente = request.POST.get('id_paciente')  

        try:
            #eealiza a insert no bd 
            with connection.cursor() as cursor:
                cursor.execute("""
                INSERT INTO consulta (dt_consulta, hr_consulta, id_profissional, id_paciente)
                VALUES (%s, %s, %s, %s)
                """, (dt_consulta, hr_consulta, id_profissional, id_paciente))

            #exibe uma mensagem de sucesso e redireciona para a lista de consultas
            messages.success(request, "Consulta cadastrada com sucesso!")
            return redirect('consulta:listar_consulta')

        except Exception as e:
            #tratamento de erro
            messages.error(request, f"Erro ao cadastrar consulta: {str(e)}")
            return HttpResponse(f"Erro ao cadastrar consulta: {str(e)}", status=500)

    
    try:
        with connection.cursor() as cursor:
            #busca todos os pacientes cadastrados, em ordem alfabética pelo nome
            cursor.execute("SELECT id_paciente, nome FROM paciente ORDER BY nome ASC")
            pacientes = dictfetchall(cursor)

            ##busca todos os pacientes cadastrados, em ordem alfabética pelo nome
            cursor.execute("SELECT id_profissional, nome FROM profissional ORDER BY nome ASC")
            profissionais = dictfetchall(cursor)

    except Exception as e:
        #tratamento de erro
        messages.error(request, f"Erro ao carregar pacientes e profissionais: {str(e)}")
        pacientes = []
        profissionais = []

    #Eenderiza o template com os dados de pacientes e profissionais
    return render(request, 'consulta/cadastrarConsulta.html', {
        'pacientes': pacientes,
        'profissionais': profissionais
    })


#função que transforma as linhas e tabelas do banco em um dicionário
def dictfetchall(cursor):
    "Retorna todas as linhas como um dicionário"
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

#função para listar as consultas na grid
def listar_consulta(request):
    try:
        #realiza um select no banco, chama a função dictfetchall e retorna o resultado no html
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id_consulta, dt_consulta, hr_consulta, id_profissional, id_paciente
                FROM consulta
                ORDER BY dt_consulta DESC
            """)
            consultas = dictfetchall(cursor)

            #realiza um select no banco de paciente e profissional, chama a função dictfetchone e retorna o resultado no html
            for consulta in consultas:
                cursor.execute("SELECT nome FROM profissional WHERE id_profissional = %s", [consulta['id_profissional']])
                profissional = cursor.fetchone()
                consulta['profissional_nome'] = profissional[0] if profissional else None

                cursor.execute("SELECT nome FROM paciente WHERE id_paciente = %s", [consulta['id_paciente']])
                paciente = cursor.fetchone()
                consulta['paciente_nome'] = paciente[0] if paciente else None

        return render(request, 'consulta/listarConsulta.html', {'consultas': consultas})

    except Exception as e:
        messages.error(request, f"Erro ao listar consultas: {str(e)}")
        return HttpResponse(f"Erro ao listar consultas: {str(e)}", status=500)
    
#função para editar uma consulta
def editar_consulta(request, id_consulta):
    try:
        #realiza um select no bd para verificar se o id passado no parâmetro existe
        #caso exista, realiza um update
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id_consulta, dt_consulta, hr_consulta, id_profissional, id_paciente
                FROM consulta WHERE id_consulta = %s
            """, [id_consulta])
            consulta = cursor.fetchone()

            if not consulta:
                messages.error(request, "Consulta não encontrada.")
                return redirect('consulta:listar_consulta')

            consulta = {
                'id_consulta': consulta[0],
                'dt_consulta': consulta[1],
                'hr_consulta': consulta[2],
                'id_profissional': consulta[3],
                'id_paciente': consulta[4]
            }

        if request.method == 'POST':
            dt_consulta = request.POST.get('dt_consulta')
            hr_consulta = request.POST.get('hr_consulta')
            id_profissional = request.POST.get('id_profissional')
            id_paciente = request.POST.get('id_paciente')

            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE consulta
                    SET dt_consulta = %s, hr_consulta = %s, id_profissional = %s, id_paciente = %s
                    WHERE id_consulta = %s
                """, [dt_consulta, hr_consulta, id_profissional, id_paciente, id_consulta])

            messages.success(request, "Consulta editada com sucesso!")
            return redirect('consulta:listar_consulta')

        return render(request, 'consulta/editarConsulta.html', {'consulta': consulta})

    except Exception as e:
        messages.error(request, f"Erro ao editar consulta: {str(e)}")
        return HttpResponse(f"Erro ao editar consulta: {str(e)}", status=500)

#função para excluir uma consulta
@csrf_exempt
def excluir_consulta(request, id_consulta):
    if request.method == 'POST':
        try:
            #realiza um select no bd para verificar se o id passado como parâmetro existe
            #caso exista, realiza o delete
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT id_consulta FROM consulta WHERE id_consulta = %s
                """, [id_consulta])
                consulta = cursor.fetchone()

                if not consulta:
                    return JsonResponse({"status": "error", "message": "Consulta não encontrada."}, status=404)

                cursor.execute("DELETE FROM consulta WHERE id_consulta = %s", [id_consulta])

            return JsonResponse({"status": "success", "message": "Consulta excluída com sucesso!"})

        except Exception as e:
            return JsonResponse({"status": "error", "message": f"Erro ao excluir: {str(e)}"}, status=500)
    else:
        return JsonResponse({"status": "error", "message": "Método não permitido."}, status=405)
    
#função para ver os detalhes da consulta   
def detalhe_consulta(request, id_consulta):
    try:
        #realiza um select no bd buscando apenas o id passado como parametro
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT c.id_consulta, c.dt_consulta, c.hr_consulta, 
                       p.nome AS profissional_nome, pac.nome AS paciente_nome
                FROM consulta c
                LEFT JOIN profissional p ON c.id_profissional = p.id_profissional
                LEFT JOIN paciente pac ON c.id_paciente = pac.id_paciente
                WHERE c.id_consulta = %s
            """, [id_consulta])
            consulta = cursor.fetchone()

        if not consulta:
            messages.error(request, "Consulta não encontrada.")
            return HttpResponse("Consulta não encontrada.", status=404)

        consulta_dict = {
            'id_consulta': consulta[0],
            'dt_consulta': consulta[1],
            'hr_consulta': consulta[2],
            'profissional_nome': consulta[3],
            'paciente_nome': consulta[4]
        }

        return render(request, 'consulta/detalheConsulta.html', {'consulta': consulta_dict})

    except Exception as e:
        messages.error(request, f"Erro ao visualizar consulta: {str(e)}")
        return HttpResponse(f"Erro ao visualizar consulta: {str(e)}", status=500)


