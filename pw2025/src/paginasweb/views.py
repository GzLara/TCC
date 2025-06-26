from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import TipoSensor, Controlador, Sensor, Regra, Leitura, Cadastro, Admin, IndexCliente
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

API_SECRET_KEY = "Projeto1MC"

@method_decorator(csrf_exempt, name='dispatch')  # Desativa CSRF para chamadas externas
class LeituraCreateView(View):
     def post(self, request):
        # Verifica chave de API no header
        auth_header = request.headers.get("X-API-KEY")
        if auth_header != API_SECRET_KEY:
            return HttpResponseForbidden("Chave de API inválida")

        try:
            data_str = request.POST.get("data")
            hora_str = request.POST.get("hora")
            sensor_str = request.POST.get("sensor")
            valor_str = request.POST.get("valor")

            if not all([data_str, hora_str, sensor_str, valor_str]):
                return HttpResponseBadRequest("Campos obrigatórios: data, hora, sensor, valor")

            data_parsed = parse_date(data_str)
            hora_parsed = parse_time(hora_str)
            if not data_parsed or not hora_parsed:
                return HttpResponseBadRequest("Data ou hora inválida")

            datahora = datetime.combine(data_parsed, hora_parsed)
            datahora_aware = make_aware(datahora)

            try:
                valor = Decimal(valor_str)
            except InvalidOperation:
                return HttpResponseBadRequest("Valor inválido")

            # Certifique-se de que seu modelo Leitura tenha os campos: sensor (CharField) e valor (DecimalField)
            leitura = Leitura.objects.create(
                data=datahora_aware,
                sensor=sensor_str,
                valor=valor
            )

            return JsonResponse({"status": "sucesso", "id": leitura.id})

        except Exception as e:
            return HttpResponseBadRequest(f"Erro inesperado: {str(e)}")
        

# Página inicial
class IndexView(TemplateView):
    template_name = 'paginasweb/index.html'

# Página inicial quando o cliente faz login

class IndexClienteView(TemplateView):
    template_name = 'paginasweb/index.html'

# Página "sobre"
class SobreView(TemplateView):
    template_name = 'paginasweb/sobre.html'

# Página "Tipo de Sensor"
class TipoSensorView(TemplateView):
    template_name = 'paginasweb/cadastrar/form.html'

# Página "Cadastro"
class CadastroView(TemplateView):
     template_name = 'paginasweb/cadastro.html'

#Página "Controlador"
class ControladorView(TemplateView):
     template_name = 'paginasweb/cadastrar/form.html'

#Página "Sensor"
class SensorView(TemplateView):
     template_name = 'paginasweb/cadastrar/form.html' 

#Página "Regra"
class RegraView(TemplateView):
     template_name = 'paginasweb/cadastrar/form.html'

#Página "Leitura"
class LeituraView(TemplateView):
     template_name = 'paginasweb/cadastrar/form.html' 

#Página "Admin"
class AdminView(TemplateView):
     template_name = 'paginasweb/adminindex.html'

# Views de cadastro (CreateView)

class IndexClienteCreate(LoginRequiredMixin, CreateView):
     model: IndexCliente
     fields = ['descricao']
     template_name = 'paginasweb/index.html'
     success_url = reverse_lazy('index')


class AdminCreate(LoginRequiredMixin, CreateView):
     model = Admin
     fields = ['nome', 'email', 'senha']
     template_name = 'paginasweb/adminindex.html'
     success_url = reverse_lazy('adminindex')
     extra_context = {
          'titulo': 'Cadastro de cliente',
          'botao': 'Cadastrar'
     }

class CadastroCreate(LoginRequiredMixin, CreateView):
     model = Cadastro
     fields = ['nome', 'email', 'senha']
     template_name = 'paginasweb/cadastro.html'
     success_url = reverse_lazy('index')
     extra_context = {
          'titulo': 'Cadastro de cliente',
          'botao': 'Cadastrar'
     }

class TipoSensorCreate(LoginRequiredMixin, CreateView):
    model = TipoSensor
    fields = ['numero_serial', 'descricao']
    template_name = 'paginasweb/form.html'
    success_url = reverse_lazy('listar-tipo-sensor')
    extra_context = {
        'titulo': 'Cadastro de tipo de sensor',
        'botao': 'Cadastrar'
    }

class ControladorCreate(LoginRequiredMixin, CreateView):
    model = Controlador
    fields = ['cadastro_cliente', 'nome', 'descricao']
    template_name = 'paginasweb/form.html'
    success_url = reverse_lazy('listar-controlador')
    extra_context = {
        'titulo': 'Cadastro de controlador',
        'botao': 'Cadastrar'
    }

class SensorCreate(LoginRequiredMixin, CreateView):
    model = Sensor
    fields = ['descricao', 'controlador', 'tipo_sensor']
    template_name = 'paginasweb/form.html'
    success_url = reverse_lazy('listar-sensor')
    extra_context = {
        'titulo': 'Cadastro de sensor',
        'botao': 'Cadastrar'
    }


class RegraCreate(LoginRequiredMixin, CreateView):
    model = Regra
    fields = ['descricao', 'horario_inicio', 'horario_fim', 'valor_minimo', 'valor_maximo', 'tipo_sensor']
    template_name = 'paginasweb/form.html'
    success_url = reverse_lazy('listar-regra')
    extra_context = {
        'titulo': 'Cadastro regra',
        'botao': 'Cadastrar'
    }

class LeituraCreate(LoginRequiredMixin, CreateView):
    model = Leitura
    fields = ['tipo_sensor', 'valor', 'data', 'sensor', 'alerta']
    template_name = 'paginasweb/form.html'
    success_url = reverse_lazy('listar-leitura')
    extra_context = {
    'titulo': 'Cadastro de leitura',
    'botao': 'Cadastrar'
    }

################################################################################

class CadastroUpdate(LoginRequiredMixin, UpdateView):
     model = Cadastro
     fields = ['nome', 'email', 'senha']
     template_name = 'paginasweb/formadmin.html'
     success_url = reverse_lazy('adminindex')
     extra_context = {
          'titulo': 'Cadastro de cliente',
          'botao': 'Cadastrar'
     }

class TipoSensorUpdate(LoginRequiredMixin, UpdateView):
    model = TipoSensor
    fields = ['numero_serial', 'descricao']
    template_name = 'paginasweb/form.html'
    success_url = reverse_lazy('index')
    extra_context = {
        'titulo': 'Cadastro de tipo de sensor',
        'botao': 'Cadastrar'
    }

class ControladorUpdate(LoginRequiredMixin, UpdateView):
    model = Controlador
    fields = ['cadastro_cliente', 'nome', 'descricao']
    template_name = 'paginasweb/form.html'
    success_url = reverse_lazy('index')
    extra_context = {
    'titulo': 'Cadastro de controlador',
    'botao': 'Cadastrar'
    }

class SensorUpdate(LoginRequiredMixin, UpdateView):
    model = Sensor
    fields = ['descricao', 'controlador', 'tipo_sensor']
    template_name = 'paginasweb/form.html'
    success_url = reverse_lazy('index')

class RegraUpdate(LoginRequiredMixin, UpdateView):
    model = Regra
    fields = ['descricao', 'horario_inicio', 'horario_fim', 'valor_minimo', 'valor_maximo', 'tipo_sensor']
    template_name = 'paginasweb/form.html'
    success_url = reverse_lazy('index')
    extra_context = {
    'titulo': 'Cadastro regra',
    'botao': 'Cadastrar'
    }

class LeituraUpdate(LoginRequiredMixin, UpdateView):
    model = Leitura
    fields = ['tipo_sensor', 'valor', 'data', 'sensor', 'alerta']
    template_name = 'paginasweb/form.html'
    success_url = reverse_lazy('index')
    extra_context = {
    'titulo': 'Cadastro de leitura',
    'botao': 'Cadastrar'
    }

    ####################################################################################

class CadastroDelete(LoginRequiredMixin, DeleteView):
     model = Cadastro
     template_name = 'paginasweb/formadmin.html'
     success_url = reverse_lazy('adminindex')
     extra_context = {
          'titulo': 'Excluir cadastro de cliente',
          'botao': 'Excluir'
     }

class TipoSensorDelete(LoginRequiredMixin, DeleteView):
        model = TipoSensor
        template_name = 'paginasweb/form.html'
        success_url = reverse_lazy('index')
        extra_context = {
        'titulo': 'Excluir tipo de sensor',
        'botao': 'Excluir'
        }

class ControladorDelete(LoginRequiredMixin, DeleteView):
        model = Controlador
        template_name = 'paginasweb/form.html'
        success_url = reverse_lazy('index')
        extra_context = {
        'titulo': 'Excluir controlador',
        'botao': 'Excluir',
        }

class SensorDelete(LoginRequiredMixin, DeleteView):
        model = Sensor
        template_name = 'paginasweb/form.html'
        success_url = reverse_lazy('index')
        extra_context = {
        'titulo': 'Excluir sensor',
        'botao': 'Excluir sensor'
        }

class RegraDelete(LoginRequiredMixin, DeleteView):
        model = Regra
        template_name = 'paginasweb/form.html'
        success_url = reverse_lazy('index')
        extra_context = {
        'titulo': 'Excluir regra',
        'botao': 'Excluir'
        }

class LeituraDelete(LoginRequiredMixin, DeleteView):
        model = Leitura
        template_name = 'paginasweb/form.html'
        success_url = reverse_lazy('index')
        extra_context = {
        'titulo': 'Excluir leitura',
        'botao': 'Excluir'
            }
        

######################################################

class TipoSensorView(LoginRequiredMixin, ListView):
     model = TipoSensor
     template_name = 'paginasweb/tiposensor.html'


class CadastroView(LoginRequiredMixin, ListView):
     model = Cadastro
     template_name = 'paginasweb/clientescadastro.html'

class ControladorView(LoginRequiredMixin, ListView):
     model = Controlador
     template_name = 'paginasweb/controlador.html'

class SensorView(LoginRequiredMixin, ListView):
     model = Sensor
     template_name = 'paginasweb/sensor.html'

class RegraView(LoginRequiredMixin, ListView):
     model = Regra
     template_name = 'paginasweb/regra.html'

class LeituraView(LoginRequiredMixin, ListView):
     model = Leitura
     template_name = 'paginasweb/leitura.html'

########################################################## Teste user permitido


def redirecionar_para_adminindex(request):
    if request.method == 'POST':
        return redirect('adminindex')  # redireciona para a página principal do admin