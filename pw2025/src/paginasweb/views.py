from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Controlador, Sensor, Regra, Leitura

from django.urls import reverse_lazy
from django.views import View
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_date, parse_time
from django.utils.timezone import make_aware

from datetime import datetime
from decimal import Decimal, InvalidOperation

from django.shortcuts import redirect
from django.contrib.auth.models import User, Group
from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from django.shortcuts import get_object_or_404
from .forms import UsuarioForm

from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied


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
    

    
# def grafico_dados(request):
#     #ultimos 20 registros ordenados por data decrescente
#     leituras = Leitura.objects.order_by('-data')[:20]

#     #agrupa por tipo de sensor (ex: temperatura, umidade etc.)
#     dados = {}
#     for l in reversed(leituras):  #inverte para mostrar em ordem cronologica
#         if l.sensor not in dados:
#             dados[l.sensor] = []
#         dados[l.sensor].append({
#             "data": l.data.strftime("%H:%M:%S"),
#             "valor": float(l.valor)
#         })

#     return JsonResponse(dados)

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
class ControladorViewAdmin(GroupRequiredMixin, TemplateView):
     group_required = u"Administrador"
     template_name = 'paginasweb/cadastrar/formadminsenha.html'

#Página "Regra" do Admin
class RegraViewAdmin(GroupRequiredMixin, TemplateView):
     group_required = u"Administrador"
     template_name = 'paginasweb/cadastrar/formadminsenha.html'

#Página "Admin"
class AdminView(GroupRequiredMixin, TemplateView):
     group_required = u"Administrador"
     template_name = 'paginasweb/adminindex.html'



class CustomLoginView(LoginView):
    template_name = 'formlogin.html'

    def get_success_url(self):
        if self.request.user.is_superuser:
            return reverse_lazy('adminindex')
        else:
            return reverse_lazy('login')


class UsuarioCreate(SuccessMessageMixin, CreateView):
    template_name = 'paginasweb/form.html'     
    form_class = UsuarioForm
    success_url = reverse_lazy('index')
    extra_context = {
        'titulo': 'Cadastro de Usuário',
        'botao': 'Cadastrar'
    }
    success_message = "Cadastro criado com sucesso!"

    def form_valid(self, form):

        grupo = get_object_or_404(Group, name='Usuário')

        url = super().form_valid(form)  

        self.object.groups.add(grupo)  # Adiciona o usuário ao grupo "Usuário"
        self.object.save()  # Salva o objeto para garantir que as alterações sejam persistidas

        return url


######################################################################################


class ControladorCreate(GroupRequiredMixin, SuccessMessageMixin, LoginRequiredMixin, CreateView):
    group_required = [u"Usuário"]
    model = Controlador
    fields = ['nome', 'descricao']
    template_name = 'paginasweb/form.html'
    success_url = reverse_lazy('listar-controlador')
    extra_context = {
        'titulo': 'Cadastro de controlador',
        'botao': 'Cadastrar'
    }
    success_message = "Controlador criado com sucesso!"

    def form_valid(self, form):
        # Antes do super n foi criado o objeto nem salvo no banco
        form.instance.usuario = self.request.user  # Define o usuário logado como o criador do cadastro
        form.instance.cadastrado_por = self.request.user  # Define o usuário logado como quem cadastrou o controlador
        url = super().form_valid(form)
        return url


class ControladorCreateAdmin(GroupRequiredMixin, SuccessMessageMixin, LoginRequiredMixin, CreateView):
    group_required = [u"Administrador"]
    model = Controlador
    fields = ['nome', 'descricao', 'usuario']
    template_name = 'paginasweb/formadminsenha.html'
    success_url = reverse_lazy('listar-controlador')
    extra_context = {
        'titulo': 'Cadastro de controlador',
        'botao': 'Cadastrar'
    }
    success_message = "Controlador criado com sucesso!"

    def form_valid(self, form):
        form.instance.cadastrado_por = self.request.user  # Define o usuário logado como quem cadastrou o controlador
        url = super().form_valid(form)
        return url


class SensorCreateAdmin(GroupRequiredMixin, SuccessMessageMixin, LoginRequiredMixin, CreateView):
    group_required = [u"Administrador"]
    model = Sensor
    fields = ['numero_serial', 'descricao', 'controlador', 'cadastrado_por']
    template_name = 'paginasweb/formadminsenha.html'
    success_url = reverse_lazy('listar-sensor')
    extra_context = {
        'titulo': 'Cadastro de sensor',
        'botao': 'Cadastrar'
    }
    success_message = "Sensor criado com sucesso!"


class RegraCreate(GroupRequiredMixin, SuccessMessageMixin, LoginRequiredMixin, CreateView):
    group_required = [u"Usuário"]
    model = Regra
    fields = ['descricao', 'horario_inicio', 'horario_fim', 'valor_minimo', 'valor_maximo', 'sensor']
    template_name = 'paginasweb/form.html'
    success_url = reverse_lazy('listar-regra')
    extra_context = {
        'titulo': 'Cadastro regra',
        'botao': 'Cadastrar'
    }
    success_message = "Regra criada com sucesso!"

    # Listar somente os sensores dos controladores que o usuário cadastrou (logado)
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['sensor'].queryset = Sensor.objects.filter(controlador__usuario=self.request.user)
        return form

    def form_valid(self, form):
        # Antes do super n foi criado o objeto nem salvo no banco
        form.instance.usuario = self.request.user  # Define o usuário logado como o criador do cadastro
        form.instance.cadastrado_por = self.request.user  # Define o usuário logado como quem cadastrou a regra
        url = super().form_valid(form)

        return url
    

class RegraCreateAdmin(GroupRequiredMixin, SuccessMessageMixin, LoginRequiredMixin, CreateView):
    group_required = [u"Administrador"]
    model = Regra
    fields = ['descricao', 'horario_inicio', 'horario_fim', 'valor_minimo', 'valor_maximo', 'sensor']
    template_name = 'paginasweb/formadminsenha.html'
    success_url = reverse_lazy('listar-regra')
    extra_context = {
        'titulo': 'Cadastro de regra',
        'botao': 'Cadastrar'
    }
    success_message = "Regra criada com sucesso!"

    # Definir o usuário como o usuário do controlador e não o usuário logado
    def form_valid(self, form):
        form.instance.usuario = form.instance.sensor.controlador.usuario
        form.instance.cadastrado_por = self.request.user
        return super().form_valid(form)


################################################################################


class UserUpdate(GroupRequiredMixin, SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    group_required = [u"Usuário"]
    model = User
    fields = ['first_name', 'last_name','username', 'email']
    template_name = 'paginasweb/form.html'
    success_url = reverse_lazy('index')
    extra_context = {
        'titulo': 'Atualizar meus dados',
        'botao': 'Atualizar'
    }
    success_message = "Cadastro atualizado com sucesso!"

    def get_object(self, queryset=None):
        return self.request.user


class UserUpdateAdmin(GroupRequiredMixin, SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    group_required = [u"Administrador"]
    model = User
    fields = ['first_name', 'last_name','username', 'email']
    template_name = 'paginasweb/form.html'
    success_url = reverse_lazy('index')
    extra_context = {
        'titulo': 'Atualizar meus dados',
        'botao': 'Atualizar'
    }
    success_message = "Cadastro atualizado com sucesso!"

    def get_object(self, queryset=None):
        return get_object_or_404(User, pk=self.kwargs['pk'])


class ControladorUpdate(GroupRequiredMixin, SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    group_required = [u"Usuário"]
    model = Controlador
    fields = ['nome', 'descricao']
    template_name = 'paginasweb/form.html'
    success_url = reverse_lazy('index')
    extra_context = {
    'titulo': 'Atualização de controlador',
    'botao': 'Salvar'
    }
    success_message = "Controlador atualizado com sucesso!"

    # Busca o objeto com a pk e o usuário autenticado
    def get_object(self, queryset=None):
        self.object = get_object_or_404(Controlador, pk=self.kwargs['pk'], usuario=self.request.user)
        return self.object


class ControladorUpdateAdmin(GroupRequiredMixin, SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    group_required = u"Administrador"
    model = Controlador
    fields = ['nome', 'descricao', 'usuario']
    template_name = 'paginasweb/formadminsenha.html'
    success_url = reverse_lazy('adminindex')
    extra_context = {
        'titulo': 'Atualização de controlador',
        'botao': 'Salvar'
    }
    success_message = "Controlador atualizado com sucesso!"


class SensorUpdateAdmin(GroupRequiredMixin, SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    group_required = u"Administrador"
    model = Sensor
    fields = ['nome', 'descricao', 'controlador', 'cadastrado_por']
    template_name = 'paginasweb/formadminsenha.html'
    success_url = reverse_lazy('adminindex')
    extra_context = {
        'titulo': 'Atualização de sensor',
        'botao': 'Salvar'
    }
    success_message = "Sensor atualizado com sucesso!"


class RegraUpdate(GroupRequiredMixin, SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    group_required = [u"Usuário"]
    model = Regra
    fields = ['descricao', 'horario_inicio', 'horario_fim', 'valor_minimo', 'valor_maximo', 'sensor']
    template_name = 'paginasweb/form.html'
    success_url = reverse_lazy('index')
    extra_context = {
    'titulo': 'Atualização de regra',
    'botao': 'Salvar'
    }
    success_message = "Regra atualizada com sucesso!"

    # Listar somente os sensores do usuário
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['sensor'].queryset = Sensor.objects.filter(controlador__usuario=self.request.user)
        return form

    def get_object(self, queryset=None):
        self.object = get_object_or_404(Regra, pk=self.kwargs['pk'], usuario=self.request.user)
        return self.object
    

class RegraUpdateAdmin(GroupRequiredMixin, SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    group_required = [u"Administrador"]
    model = Regra
    fields = ['descricao', 'horario_inicio', 'horario_fim', 'valor_minimo', 'valor_maximo', 'sensor']
    template_name = 'paginasweb/formadminsenha.html'
    success_url = reverse_lazy('listar-regra')
    extra_context = {
        'titulo': 'Cadastro de regra',
        'botao': 'Cadastrar'
    }
    success_message = "Regra criada com sucesso!"

    # Definir o usuário como sendo o usuário que possui o controlador desse sensor
    def form_valid(self, form):
        form.instance.usuario = form.instance.sensor.controlador.usuario
        return super().form_valid(form)
    

class LeituraUpdateAdmin(GroupRequiredMixin, SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    group_required = u"Administrador"
    model = Leitura
    fields = ['valor', 'data', 'sensor']
    template_name = 'paginasweb/formadminsenha.html'
    success_url = reverse_lazy('index')
    extra_context = {
        'titulo': 'Atualização de leitura',
        'botao': 'Salvar'
    }
    success_message = "Leitura atualizada com sucesso!"
    

####################################################################################


class ControladorDelete(GroupRequiredMixin, SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    group_required = [u"Administrador", u"Usuário"]
    model = Controlador
    template_name = 'paginasweb/form.html'
    success_url = reverse_lazy('index')
    extra_context = {
        'titulo': 'Excluir controlador',
        'botao': 'Excluir',
    }
    success_message = "Controlador deletado com sucesso!"

    def get_object(self, queryset=None):
        self.object = get_object_or_404(Controlador, pk=self.kwargs['pk'])
        # Se for o usuário logado ou pertencer ao grupo Administrador...
        if self.object.usuario == self.request.user or self.request.user.groups.filter(name='Administrador').exists():  
            return self.object
        else:
            raise PermissionDenied("Você não tem permissão para acessar este objeto.")


class SensorDeleteAdmin(GroupRequiredMixin, SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    group_required = [u"Administrador"]
    model = Sensor
    template_name = 'paginasweb/form.html'
    success_url = reverse_lazy('index')
    extra_context = {
        'titulo': 'Excluir sensor',
        'botao': 'Excluir',
    }
    success_message = "Sensor deletado com sucesso!"

    # Se o usuário pode excluir, tire o comentário do método abaixo

    # def get_object(self, queryset=None):
    #     self.object = get_object_or_404(Sensor, pk=self.kwargs['pk'])
    #     # Se for o usuário logado ou pertencer ao grupo Administrador...
    #     if self.object.controlador.usuario == self.request.user or self.request.user.groups.filter(name='Administrador').exists():
    #         return self.object
    #     else:
    #         raise PermissionDenied("Você não tem permissão para acessar este objeto.")
        

class RegraDelete(GroupRequiredMixin, SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    group_required = [u"Administrador", u"Usuário"]
    model = Regra
    template_name = 'paginasweb/form.html'
    success_url = reverse_lazy('index')
    extra_context = {
        'titulo': 'Excluir regra',
        'botao': 'Excluir'
    }
    success_message = "Regra deletada com sucesso!"

    def get_object(self, queryset=None):
        self.object = get_object_or_404(Regra, pk=self.kwargs['pk'])
        if self.object.usuario == self.request.user or self.request.user.groups.filter(name='Administrador').exists():
            return self.object
        else:
            raise PermissionDenied("Você não tem permissão para acessar este objeto.")


class LeituraDeleteAdmin(GroupRequiredMixin, SuccessMessageMixin, LoginRequiredMixin, DeleteView):
        group_required = u"Administrador"
        model = Leitura
        template_name = 'paginasweb/form.html'
        success_url = reverse_lazy('index')
        extra_context = {
            'titulo': 'Excluir leitura',
            'botao': 'Excluir'
        }
        success_message = "Leitura deletada com sucesso!"

        def get_object(self, queryset=None):
          self.object = get_object_or_404(Leitura, pk=self.kwargs['pk'])
          return self.object
        

######################################################


class ControladorList(GroupRequiredMixin, SuccessMessageMixin, LoginRequiredMixin, ListView):
    group_required = [u"Administrador", u"Usuário"]
    model = Controlador
    template_name = 'paginasweb/controladorcadastro_completo.html'

    def get_queryset(self):
        queryset = Controlador.objects.all()
        return queryset.filter(usuario=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Se for do grupo do grupo admin, filtra todas, menos as minhas
        if self.request.user.groups.filter(name='Administrador').exists():
            controladores = Controlador.objects.all()
            controladores = controladores.exclude(usuario=self.request.user)
            context['todos_controladores'] = controladores

        return context


class SensorList(GroupRequiredMixin, SuccessMessageMixin, LoginRequiredMixin, ListView):
    group_required = [u"Administrador", u"Usuário"]
    model = Sensor
    template_name = 'paginasweb/sensor.html'

    def get_queryset(self):
        queryset = Sensor.objects.all()
        return queryset.filter(controlador__usuario=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Se for do grupo do grupo admin, filtra todas, menos as minhas
        if self.request.user.groups.filter(name='Administrador').exists():
            sensores = Sensor.objects.all()
            sensores = sensores.exclude(controlador__usuario=self.request.user)
            context['todos_sensores'] = sensores

        return context
    

class RegraList(GroupRequiredMixin, SuccessMessageMixin, LoginRequiredMixin, ListView):
    group_required = [u"Administrador", u"Usuário"]
    model = Regra
    template_name = 'paginasweb/regrascadastro_completo.html'

    def get_queryset(self):
        queryset = Regra.objects.all()
        return queryset.filter(usuario=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Se for do grupo do grupo admin, filtra todas, menos as minhas
        if self.request.user.groups.filter(name='Administrador').exists():
            regras = Regra.objects.all()
            regras = regras.exclude(usuario=self.request.user)
            context['todas_regras'] = regras

        return context


class LeituraList(GroupRequiredMixin, SuccessMessageMixin, LoginRequiredMixin, ListView):
     group_required = u"Administrador"
     model = Leitura
     template_name = 'paginasweb/leitura.html'


class UserList(GroupRequiredMixin, SuccessMessageMixin, LoginRequiredMixin, ListView):
    group_required = [u"Administrador"]
    model = User
    template_name = 'paginasweb/clientescadastro.html'


########################################################## Teste user permitido


def redirecionar_para_adminindex(request):
    if request.method == 'POST':
        return redirect('adminindex')  # redireciona para a página principal do admin
    
def redirecionar_para_login(request):
        return redirect('login')  # redireciona para a página inícial (login)


#unir tabelas de controlador e regra do admin com cliente
    
class ControladorAdminComClienteView(GroupRequiredMixin, LoginRequiredMixin, TemplateView):
    group_required = u"Administrador"
    template_name = 'paginasweb/controladorcadastro_completo.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['controladores_admin'] = ControladorAdmin.objects.all()
        context['listar_controlador'] = Controlador.objects.all()
        return context

class RegraAdminComClienteView(GroupRequiredMixin, LoginRequiredMixin, TemplateView):
    group_required = u"Administrador", u"Usuário"
    template_name = 'paginasweb/regrascadastro_completo.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['regras_admin'] = RegraAdmin.objects.all()
        context['listar_regra'] = Regra.objects.all()
        return context
    


# ======================================================================================

# Teste de gráfico

def grafico_dados(request):
    labels = []
    data = []

    queryset = Leitura.objects.order_by('-data')[:10]  # últimas 10
    for leitura in queryset:
        labels.append(leitura.data.strftime('%d/%m'))  # formato da data
        data.append(leitura.valor)

    return render(request, 'paginasweb/index.html', {
        'labels': labels[::-1],  # inverte para mostrar do mais antigo ao mais recente
        'data': data[::-1]
    })

def grafico_dadosadmin(request):
    labels = []
    data = []

    queryset = Leitura.objects.order_by('-data')[:10]  # últimas 10
    for leitura in queryset:
        labels.append(leitura.data.strftime('%d/%m'))  # formato da data
        data.append(leitura.valor)

    return render(request, 'paginasweb/adminindex.html',  {
        'labels': labels[::-1],  # inverte para mostrar do mais antigo ao mais recente
        'data': data[::-1]
    })
