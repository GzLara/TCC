from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Controlador, Regra, Leitura, Cadastro, Admin, IndexCliente, ControladorAdmin, RegraAdmin, SobreAdmin
from django.views import View
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_date, parse_time
from django.utils.timezone import make_aware
from datetime import datetime
from decimal import Decimal, InvalidOperation
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

API_SECRET_KEY = "Projeto1MC"

@method_decorator(csrf_exempt, name='dispatch')
class LeituraCreateView(View):
    def post(self, request):
        auth_header = request.headers.get("X-API-KEY")
        if auth_header != API_SECRET_KEY:
            return HttpResponseForbidden("Chave de API inválida")

        try:
            data_str = request.POST.get("data")
            time_str = request.POST.get("time")
            sensors_total_str = request.POST.get("sensors_total")

            if not all([data_str, time_str, sensors_total_str]):
                return HttpResponseBadRequest("Campos obrigatórios: data, time, sensors_total")

            data_parsed = parse_date(data_str)
            time_parsed = parse_time(time_str)
            if not data_parsed or not time_parsed:
                return HttpResponseBadRequest("Data ou hora inválida")

            datahora = datetime.combine(data_parsed, time_parsed)
            datahora_aware = make_aware(datahora)

            try:
                sensors_total = int(sensors_total_str)
            except ValueError:
                return HttpResponseBadRequest("sensors_total inválido")

            leituras_criadas = []
            for i in range(1, sensors_total + 1):
                sensor_key = f"sensor_type{i}"
                value_key = f"value{i}"

                sensor = request.POST.get(sensor_key)
                value_str = request.POST.get(value_key)

                if not sensor or not value_str:
                    return HttpResponseBadRequest(f"Faltando dados para sensor {i}")

                try:
                    valor = Decimal(value_str)
                except InvalidOperation:
                    return HttpResponseBadRequest(f"Valor inválido para sensor {i}")

                leitura = Leitura.objects.create(
                    data=datahora_aware,
                    sensor=sensor,
                    valor=valor
                )
                leituras_criadas.append({
                    "sensor": sensor,
                    "valor": str(valor),
                    "id": leitura.id
                })

                return JsonResponse({"status": "sucesso", "leituras": leituras_criadas})
    
        except Exception as e:
            return HttpResponseBadRequest(f"Erro inesperado: {str(e)}")
    

    
def grafico_dados(request):
    #ultimos 20 registros ordenados por data decrescente
    leituras = Leitura.objects.order_by('-data')[:20]

    #agrupa por tipo de sensor (ex: temperatura, umidade etc.)
    dados = {}
    for l in reversed(leituras):  #inverte para mostrar em ordem cronologica
        if l.sensor not in dados:
            dados[l.sensor] = []
        dados[l.sensor].append({
            "data": l.data.strftime("%H:%M:%S"),
            "valor": float(l.valor)
        })

    return JsonResponse(dados)

# Página inicial
class IndexView(TemplateView):
    template_name = 'paginasweb/index.html'

# Página inicial quando o cliente faz login

class IndexClienteView(TemplateView):
    template_name = 'paginasweb/index.html'

# Página "sobre"
class SobreView(TemplateView):
    template_name = 'paginasweb/sobre.html'

# Página "sobre" do admin
class SobreViewAdmin(TemplateView):
    template_name = 'paginasweb/sobreadmin.html'

# Página "Cadastro"
class CadastroView(TemplateView):
     template_name = 'paginasweb/cadastro.html'

#Página "Controlador"
class ControladorView(TemplateView):
     template_name = 'paginasweb/cadastrar/form.html'

#Página "Regra"
class RegraView(TemplateView):
     template_name = 'paginasweb/cadastrar/form.html'

#Página "Controlador" do Admin
class ControladorViewAdmin(TemplateView):
     template_name = 'paginasweb/cadastrar/formadminsenha.html'

#Página "Regra" do Admin
class RegraViewAdmin(TemplateView):
     template_name = 'paginasweb/cadastrar/formadminsenha.html'

#Página "Admin"
class AdminView(TemplateView):
     template_name = 'paginasweb/adminindex.html'

# Views de cadastro (CreateView)

class IndexClienteCreate(LoginRequiredMixin, CreateView):
     model: IndexCliente
     fields = ['descricao']
     template_name = 'paginasweb/index.html'
     success_url = reverse_lazy('index')


class AdminCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Admin
    fields = ['nome']
    template_name = 'paginasweb/adminindex.html'
    success_url = reverse_lazy('adminindex')
    extra_context = {
         'titulo': 'Cadastro de cliente',
         'botao': 'Cadastrar'
     }
    success_message = "Cadastro de administrador feito com sucesso!"

class SobreAdminCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = SobreViewAdmin
    fields = ['titulo', 'conteudo']
    template_name = 'paginasweb/sobreadmin.html'
    success_url = reverse_lazy('sobreadmin')
    extra_context = {
        'titulo': 'Sobre nós',
        'botao': 'Salvar'
    }
    success_message = "Sobre criado com sucesso!"

class CadastroCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
     model = Cadastro
     fields = ['nome']
     template_name = 'paginasweb/cadastro.html'
     success_url = reverse_lazy('index')
     extra_context = {
          'titulo': 'Cadastro de cliente',
          'botao': 'Cadastrar'
     }
     success_message = "Cadastro feito com sucesso!"

class ControladorCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Controlador
    fields = ['nome', 'descricao']
    template_name = 'paginasweb/form.html'
    success_url = reverse_lazy('listar-controlador')
    extra_context = {
        'titulo': 'Cadastro de controlador',
        'botao': 'Cadastrar'
    }
    success_message = "Controlador criado com sucesso!"

class ControladorCreateAdmin(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = ControladorAdmin
    fields = ['nome', 'descricao']
    template_name = 'paginasweb/formadminsenha.html'
    success_url = reverse_lazy('controladores-completo')
    extra_context = {
        'titulo': 'Cadastro de controlador',
        'botao': 'Cadastrar'
    }
    success_message = "Controlador criado com sucesso!"


class RegraCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Regra
    fields = ['descricao', 'horario_inicio', 'horario_fim', 'valor_minimo', 'valor_maximo', 'controlador']
    template_name = 'paginasweb/form.html'
    success_url = reverse_lazy('listar-regra')
    extra_context = {
        'titulo': 'Cadastro regra',
        'botao': 'Cadastrar'
    }
    success_message = "Regra criada com sucesso!"

class RegraCreateAdmin(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = RegraAdmin
    fields = ['descricao', 'horario_inicio', 'horario_fim', 'valor_minimo', 'valor_maximo', 'controlador']
    template_name = 'paginasweb/formadminsenha.html'
    success_url = reverse_lazy('regras-completo')
    extra_context = {
        'titulo': 'Cadastro regra',
        'botao': 'Cadastrar'
    }
    success_message = "Regra criada com sucesso!"

################################################################################

class AdminUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
     model = Admin
     fields = ['nome']
     template_name = 'paginasweb/formlogin.html'
     success_url = reverse_lazy('adminindex')
     extra_context = {
          'titulo': 'Cadastro de cliente',
          'botao': 'Cadastrar'
     }
     success_message = "Administrador atualizado com sucesso!"

class CadastroUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
     model = Cadastro
     fields = ['nome']
     template_name = 'paginasweb/formlogin.html'
     success_url = reverse_lazy('adminindex')
     extra_context = {
          'titulo': 'Cadastro de cliente',
          'botao': 'Cadastrar'
     }
     success_message = "Cadastro atualizado com sucesso!"

class ControladorUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Controlador
    fields = ['nome', 'descricao']
    template_name = 'paginasweb/form.html'
    success_url = reverse_lazy('index')
    extra_context = {
    'titulo': 'Cadastro de controlador',
    'botao': 'Cadastrar'
    }
    success_message = "Controlador atualizado com sucesso!"

class ControladorUpdateAdmin(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = ControladorAdmin
    fields = ['nome', 'descricao']
    template_name = 'paginasweb/formadminsenha.html'
    success_url = reverse_lazy('adminindex')
    extra_context = {
    'titulo': 'Cadastro de controlador',
    'botao': 'Cadastrar'
    }
    success_message = "Controlador atualizado com sucesso!"

class RegraUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Regra
    fields = ['descricao', 'horario_inicio', 'horario_fim', 'valor_minimo', 'valor_maximo', 'controlador']
    template_name = 'paginasweb/form.html'
    success_url = reverse_lazy('index')
    extra_context = {
    'titulo': 'Cadastro regra',
    'botao': 'Cadastrar'
    }
    success_message = "Regra atualizada com sucesso!"

class RegraUpdateAdmin(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = RegraAdmin
    fields = ['descricao', 'horario_inicio', 'horario_fim', 'valor_minimo', 'valor_maximo', 'controlador']
    template_name = 'paginasweb/formadminsenha.html'
    success_url = reverse_lazy('adminindex')
    extra_context = {
    'titulo': 'Cadastro regra',
    'botao': 'Cadastrar'
    }
    success_message = "Regra atualizada com sucesso!"

class LeituraUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Leitura
    fields = ['tipo_sensor', 'valor', 'data', 'sensor', 'alerta']
    template_name = 'paginasweb/form.html'
    success_url = reverse_lazy('index')
    extra_context = {
    'titulo': 'Cadastro de leitura',
    'botao': 'Cadastrar'
    }
    success_message = "Leitura atualizada com sucesso!"

class SobreAdminUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = SobreAdmin
    fields = ['titulo', 'conteudo']
    template_name = 'paginasweb/formadminsenha.html'
    sucess_url = reverse_lazy('sobreadmin')
    extra_context = {
        'botao': 'Salvar'
    }
    success_message = "Sobre atualizado com sucesso!"

    ####################################################################################

class CadastroDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
     model = Cadastro
     template_name = 'paginasweb/formadminsenha.html'
     success_url = reverse_lazy('adminindex')
     extra_context = {
          'titulo': 'Excluir cadastro de cliente',
          'botao': 'Excluir'
     }
     success_message = "Cadastro deletado com sucesso!"

class ControladorDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
        model = Controlador
        template_name = 'paginasweb/form.html'
        success_url = reverse_lazy('index')
        extra_context = {
        'titulo': 'Excluir controlador',
        'botao': 'Excluir',
        }
        success_message = "Controlador deletado com sucesso!"

class ControladorDeleteAdmin(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
        model = ControladorAdmin
        template_name = 'paginasweb/formadminsenha.html'
        success_url = reverse_lazy('adminindex')
        extra_context = {
        'titulo': 'Excluir controlador',
        'botao': 'Excluir',
        }
        success_message = "Controlador deletado com sucesso!"

class RegraDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
        model = Regra
        template_name = 'paginasweb/form.html'
        success_url = reverse_lazy('index')
        extra_context = {
        'titulo': 'Excluir regra',
        'botao': 'Excluir'
        }
        success_message = "Regra deletada com sucesso!"

class RegraDeleteAdmin(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
        model = RegraAdmin
        template_name = 'paginasweb/formadminsenha.html'
        success_url = reverse_lazy('adminindex')
        extra_context = {
        'titulo': 'Excluir regra',
        'botao': 'Excluir'
        }
        success_message = "Regra deletada com sucesso!"

class LeituraDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
        model = Leitura
        template_name = 'paginasweb/form.html'
        success_url = reverse_lazy('index')
        extra_context = {
        'titulo': 'Excluir leitura',
        'botao': 'Excluir'
            }
        success_message = "Leitura deletada com sucesso!"

class SobreAdminDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = SobreAdmin
    template_name = 'paginasweb/formadminsenha.html'
    success_url = reverse_lazy('sobreadmin')
    extra_context = {
        'titulo': 'Excluir sobre',
        'botao': 'Excluir'
    }
    success_message = "Sobre deletado com sucesso!"
        

######################################################


class CadastroView(SuccessMessageMixin, LoginRequiredMixin, ListView):
     model = Cadastro
     template_name = 'paginasweb/clientescadastro.html'

class ControladorView(SuccessMessageMixin, LoginRequiredMixin, ListView):
     model = Controlador
     template_name = 'paginasweb/controlador.html'

     def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)

         # Pega os dois conjuntos de controladores
         controladores_admin = ControladorAdmin.objects.all()
         listar_controlador = Controlador.objects.all()
         
         # Tabela vermelha: junta admin + clientes
         context['object_list'] = list(listar_controlador) + list(controladores_admin)

         return context


class ControladorViewAdmin(SuccessMessageMixin, LoginRequiredMixin, ListView):
     model = ControladorAdmin
     template_name = 'paginasweb/controladorcadastro.html'

class RegraViewAdmin(SuccessMessageMixin, LoginRequiredMixin, ListView):
     model = RegraAdmin
     template_name = 'paginasweb/regracadastro.html'

class RegraView(SuccessMessageMixin, LoginRequiredMixin, ListView):
     model = Regra
     template_name = 'paginasweb/regra.html'

     def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['regras_admin'] = RegraAdmin.objects.all()  # regras do admin
        return context

class LeituraView(SuccessMessageMixin, LoginRequiredMixin, ListView):
     model = Leitura
     template_name = 'paginasweb/leitura.html'

########################################################## Teste user permitido


def redirecionar_para_adminindex(request):
    if request.method == 'POST':
        return redirect('adminindex')  # redireciona para a página principal do admin
    
def redirecionar_para_login(request):
        return redirect('cadastrar-cadastro')  # redireciona para a página inícial (login)


#unir tabelas de controlador e regra do admin com cliente
    
class ControladorAdminComClienteView(LoginRequiredMixin, TemplateView):
    template_name = 'paginasweb/controladorcadastro_completo.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['controladores_admin'] = ControladorAdmin.objects.all()
        context['listar_controlador'] = Controlador.objects.all()
        return context

class RegraAdminComClienteView(LoginRequiredMixin, TemplateView):
    template_name = 'paginasweb/regrascadastro_completo.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['regras_admin'] = RegraAdmin.objects.all()
        context['listar_regra'] = Regra.objects.all()
        return context