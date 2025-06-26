from django.urls import path
from .views import *
from .views import LeituraCreateView

from .views import *

from django.contrib.auth import views as auth_views


urlpatterns = [

    # Criar rota para página de login
   path('cadastrar/cadastro/', auth_views.LoginView.as_view(
       template_name = 'paginasweb/formadmin.html',
       extra_context = {
          'titulo': 'Login',
          'botao': 'Entrar',
     }
   ), name='cadastro'),

   path('senha/', auth_views.PasswordChangeView.as_view(
       template_name = 'paginasweb/form.html',
       extra_context = {
          'titulo': 'Atualizar senha',
          'botao': 'Salvar',
     }
   ), name='senha'),

   # Criar rota de logout
   path('logout/', auth_views.LogoutView.as_view(), name ='logout'),

    #parte tcc
	path("api/leitura/", LeituraCreateView.as_view(), name="leitura-create"),
    path('login-admin/', redirecionar_para_adminindex, name='login-admin'),  # onde o formulário envia

    path('', IndexView.as_view(), name='index'),  # Página inicial
    path('indexcliente/', IndexClienteView.as_view(), name='indexcliente'), # Página quando o cliente loga
    path('sobre/', SobreView.as_view(), name='sobre'),  # Página sobre
    path('tiposensor/', TipoSensorView.as_view(), name='tiposensor'), #Página tipo de sensor
    path('cadastro/', CadastroView.as_view(), name='cadastro'), # Pagina de cadastro de clientes
    path('controlador/', ControladorView.as_view(), name='controlador'), # Pagina de cadastro de controlador
    path('adminindex/', AdminView.as_view(), name='adminindex'), # Página da área do Admin

    path('cadastrar/tiposensor/', TipoSensorCreate.as_view(), name='cadastrar-tipo-sensor'),
    path('cadastrar/controlador/', ControladorCreate.as_view(), name='cadastrar-controlador'),
    path('cadastrar/sensor/', SensorCreate.as_view(), name='cadastrar-sensor'),
    path('cadastrar/regra/', RegraCreate.as_view(), name='cadastrar-regra'),
    path('cadastrar/leitura/', LeituraCreate.as_view(), name='cadastrar-leitura'),
    path('cadastrar/cadastro/', CadastroCreate.as_view(), name='cadastrar-cadastro'),

    path('editar/tiposensor/<int:pk>/', TipoSensorUpdate.as_view(), name='editar-tipo-sensor'),
    path('editar/controlador/<int:pk>/', ControladorUpdate.as_view(), name='editar-controlador'),
    path('editar/sensor/<int:pk>/', SensorUpdate.as_view(), name='editar-sensor'),
    path('editar/regra/<int:pk>/', RegraUpdate.as_view(), name='editar-regra'),
    path('editar/leitura/<int:pk>/', LeituraUpdate.as_view(), name='editar-leitura'),
    path('editar/cadastro/<int:pk>/', CadastroUpdate.as_view(), name='editar-cadastro'),

    path('excluir/tiposensor/<int:pk>/', TipoSensorDelete.as_view(), name='excluir-tipo-sensor'),
    path('excluir/controlador/<int:pk>/', ControladorDelete.as_view(), name='excluir-controlador'),
    path('excluir/sensor/<int:pk>/', SensorDelete.as_view(), name='excluir-sensor'),
    path('excluir/regra/<int:pk>/', RegraDelete.as_view(), name='excluir-regra'),
    path('excluir/leitura/<int:pk>/', LeituraDelete.as_view(), name='excluir-leitura'),
    path('excluir/cadastro/<int:pk>/', CadastroDelete.as_view(), name='excluir-cadastro'),

    path("listar/tiposensor/", TipoSensorView.as_view(), name="listar-tipo-sensor"),
    path("listar/controlador/", ControladorView.as_view(), name="listar-controlador"),
    path("listar/sensor/", SensorView.as_view(), name="listar-sensor"),
    path("listar/regra/", RegraView.as_view(), name="listar-regra"),
    path("listar/leitura/", LeituraView.as_view(), name="listar-leitura"),
    path("listar/cadastro/", CadastroView.as_view(), name="listar-clientes-cadastro"),
    


]
