from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import TipoSensor, Controlador, Sensor, Regra, Leitura, Cadastro
from django.views import View
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_date, parse_time
from django.utils.timezone import make_aware
from datetime import datetime
from decimal import Decimal, InvalidOperation

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
            temperatura_str = request.POST.get("temperatura")

            if not all([data_str, hora_str, temperatura_str]):
                return HttpResponseBadRequest("Campos obrigatórios: data, hora, temperatura")

            data_parsed = parse_date(data_str)
            hora_parsed = parse_time(hora_str)
            if not data_parsed or not hora_parsed:
                return HttpResponseBadRequest("Data ou hora inválida")

            datahora = datetime.combine(data_parsed, hora_parsed)
            datahora_aware = make_aware(datahora)

            try:
                temperatura = Decimal(temperatura_str)
            except InvalidOperation:
                return HttpResponseBadRequest("Temperatura inválida")

            leitura = Leitura.objects.create(data=datahora_aware, temperatura=temperatura)

            return JsonResponse({"status": "sucesso", "id": leitura.id})

        except Exception as e:
            return HttpResponseBadRequest(f"Erro inesperado: {str(e)}")



# Página inicial
class IndexView(TemplateView):
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

# Views de cadastro (CreateView)

class CadastroCreate(CreateView):
     model = Cadastro
     fields = ['nome', 'email', 'senha']
     template_name = 'paginasweb/cadastro.html'
     success_url = reverse_lazy('listar-clientes-cadastro')
     extra_context = {
          'titulo': 'Cadastro de cliente',
          'botao': 'Cadastrar'
     }

class TipoSensorCreate(CreateView):
    model = TipoSensor
    fields = ['numero_serial', 'descricao']
    template_name = 'paginasweb/form.html'
    success_url = reverse_lazy('listar-tipo-sensor')
    extra_context = {
        'titulo': 'Cadastro de tipo de sensor',
        'botao': 'Cadastrar'
    }

class ControladorCreate(CreateView):
    model = Controlador
    fields = ['cadastro_cliente', 'nome', 'descricao']
    template_name = 'paginasweb/form.html'
    success_url = reverse_lazy('listar-controlador')
    extra_context = {
        'titulo': 'Cadastro de controlador',
        'botao': 'Cadastrar'
    }

class SensorCreate(CreateView):
    model = Sensor
    fields = ['descricao', 'controlador', 'tipo_sensor']
    template_name = 'paginasweb/form.html'
    success_url = reverse_lazy('listar-sensor')
    extra_context = {
        'titulo': 'Cadastro de sensor',
        'botao': 'Cadastrar'
    }


class RegraCreate(CreateView):
    model = Regra
    fields = ['descricao', 'horario_inicio', 'horario_fim', 'valor_minimo', 'valor_maximo', 'tipo_sensor']
    template_name = 'paginasweb/form.html'
    success_url = reverse_lazy('listar-regra')
    extra_context = {
        'titulo': 'Cadastro regra',
        'botao': 'Cadastrar'
    }

class LeituraCreate(CreateView):
    model = Leitura
    fields = ['tipo_sensor', 'valor', 'data', 'sensor', 'alerta']
    template_name = 'paginasweb/form.html'
    success_url = reverse_lazy('listar-leitura')
    extra_context = {
    'titulo': 'Cadastro de leitura',
    'botao': 'Cadastrar'
    }

################################################################################

class CadastroUpdate(UpdateView):
     model = Cadastro
     fields = ['nome', 'email', 'senha']
     template_name = 'paginasweb/form.html'
     success_url = reverse_lazy('index')
     extra_context = {
          'titulo': 'Cadastro de cliente',
          'botao': 'Cadastrar'
     }

class TipoSensorUpdate(UpdateView):
    model = TipoSensor
    fields = ['numero_serial', 'descricao']
    template_name = 'paginasweb/form.html'
    success_url = reverse_lazy('index')
    extra_context = {
        'titulo': 'Cadastro de tipo de sensor',
        'botao': 'Cadastrar'
    }

class ControladorUpdate(UpdateView):
    model = Controlador
    fields = ['cadastro_cliente', 'nome', 'descricao']
    template_name = 'paginasweb/form.html'
    success_url = reverse_lazy('index')
    extra_context = {
    'titulo': 'Cadastro de controlador',
    'botao': 'Cadastrar'
    }

class SensorUpdate(UpdateView):
    model = Sensor
    fields = ['descricao', 'controlador', 'tipo_sensor']
    template_name = 'paginasweb/form.html'
    success_url = reverse_lazy('index')

class RegraUpdate(UpdateView):
    model = Regra
    fields = ['descricao', 'horario_inicio', 'horario_fim', 'valor_minimo', 'valor_maximo', 'tipo_sensor']
    template_name = 'paginasweb/form.html'
    success_url = reverse_lazy('index')
    extra_context = {
    'titulo': 'Cadastro regra',
    'botao': 'Cadastrar'
    }

class LeituraUpdate(UpdateView):
    model = Leitura
    fields = ['tipo_sensor', 'valor', 'data', 'sensor', 'alerta']
    template_name = 'paginasweb/form.html'
    success_url = reverse_lazy('index')
    extra_context = {
    'titulo': 'Cadastro de leitura',
    'botao': 'Cadastrar'
    }

    ####################################################################################

class CadastroDelete(DeleteView):
     model = Cadastro
     template_name = 'paginasweb/form.html'
     success_url = reverse_lazy('index')
     extra_context = {
          'titulo': 'Excluir cadastro de cliente',
          'botao': 'Excluir'
     }

class TipoSensorDelete(DeleteView):
        model = TipoSensor
        template_name = 'paginasweb/form.html'
        success_url = reverse_lazy('index')
        extra_context = {
        'titulo': 'Excluir tipo de sensor',
        'botao': 'Excluir'
        }

class ControladorDelete(DeleteView):
        model = Controlador
        template_name = 'paginasweb/form.html'
        success_url = reverse_lazy('index')
        extra_context = {
        'titulo': 'Excluir controlador',
        'botao': 'Excluir',
        }

class SensorDelete(DeleteView):
        model = Sensor
        template_name = 'paginasweb/form.html'
        success_url = reverse_lazy('index')
        extra_context = {
        'titulo': 'Excluir sensor',
        'botao': 'Excluir sensor'
        }

class RegraDelete(DeleteView):
        model = Regra
        template_name = 'paginasweb/form.html'
        success_url = reverse_lazy('index')
        extra_context = {
        'titulo': 'Excluir regra',
        'botao': 'Excluir'
        }

class LeituraDelete(DeleteView):
        model = Leitura
        template_name = 'paginasweb/form.html'
        success_url = reverse_lazy('index')
        extra_context = {
        'titulo': 'Excluir leitura',
        'botao': 'Excluir'
            }
        

######################################################

class TipoSensorView(ListView):
     model = TipoSensor
     template_name = 'paginasweb/tiposensor.html'


class CadastroView(ListView):
     model = Cadastro
     template_name = 'paginasweb/clientescadastro.html'

class ControladorView(ListView):
     model = Controlador
     template_name = 'paginasweb/controlador.html'

class SensorView(ListView):
     model = Sensor
     template_name = 'paginasweb/sensor.html'

class RegraView(ListView):
     model = Regra
     template_name = 'paginasweb/regra.html'

class LeituraView(ListView):
     model = Leitura
     template_name = 'paginasweb/leitura.html'