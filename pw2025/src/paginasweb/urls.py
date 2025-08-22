from django.urls import path
from .views import *
from .views import LeituraCreateView

from .views import *

from django.contrib.auth import views as auth_views


urlpatterns = [

    # Criar rota para página de login
    path('login/', CustomLoginView.as_view(
        template_name = 'paginasweb/formlogin.html',
        extra_context = {
          'titulo': 'Login',
          'botao': 'Entrar',
        }
    ), name='login'),

   path('senha/', auth_views.PasswordChangeView.as_view(
        template_name = 'paginasweb/form.html',
        extra_context = {
            'titulo': 'Atualizar senha',
            'botao': 'Salvar',
        }
    ), name='senha'),

    path('alterar-senha/', auth_views.PasswordChangeView.as_view(
        template_name = 'paginasweb/formadminsenha.html',
        extra_context = {
            'titulo': 'Atualizar senha',
            'botao': 'Salvar',
        }
    ), name='senhaadmin'),
    
    # Criar rota de logout
    path('logout/', auth_views.LogoutView.as_view(), name ='logout'),

    # Registo de usuário no sistema
    path('registrar/', UsuarioCreate.as_view(), name='registrar'),

    path('api/leituras/', LeituraCreateView.as_view(), name='leituras_create'),

    #parte tcc
    # path('login-admin/', redirecionar_para_adminindex, name='login-admin'),  # onde o formulário envia
    path("api/leitura/", LeituraCreateView.as_view(), name="leitura-create"),
    # path('index/', grafico_dados, name='grafico'),
    # path('adminindex/', grafico_dadosadmin, name='graficoadmin'),
    # path('controladores-completo/', ControladorAdminComClienteView.as_view(), name='controladores-completo'),
    # path('regras-completo/', RegraAdminComClienteView.as_view(), name='regras-completo'),


    # path('', redirecionar_para_login, name='redirecionar-login'),  # Página inicial
    path('', IndexView.as_view(), name='index'), # Página quando o cliente loga
    path('sobre/', SobreView.as_view(), name='sobre'),  # Página sobre
    # path('cadastro/', CadastroView.as_view(), name='cadastro'), # Pagina de cadastro de clientes
    # path('controlador/', ControladorView.as_view(), name='controlador'), # Pagina de cadastro de controlador
    # path('adminindex/', AdminView.as_view(), name='adminindex'), # Página da área do Admin
    # path('regras/', RegraView.as_view(), name='regras'), # Página de regras


    # Views ajustadas para usuário e administrador
    path('meus-dados/', UserUpdate.as_view(), name='meus-dados'),

    path('administrador/cadastrar/controlador/', ControladorCreateAdmin.as_view(), name='cadastrar-controlador-admin'),
    path('administrador/cadastrar/sensor/', SensorCreateAdmin.as_view(), name='cadastrar-sensor-admin'),
    path('administrador/cadastrar/regra/', RegraCreateAdmin.as_view(), name='cadastrar-regra-admin'),

    path('cadastrar/controlador/', ControladorCreate.as_view(), name='cadastrar-controlador'),
    path('cadastrar/regra/', RegraCreate.as_view(), name='cadastrar-regra'),

    path('editar/controlador/<int:pk>/', ControladorUpdate.as_view(), name='editar-controlador'),
    path('editar/regra/<int:pk>/', RegraUpdate.as_view(), name='editar-regra'),
    
    path('administrador/editar/user/<int:pk>/', UserUpdateAdmin.as_view(), name='editar-user-admin'),
    path('administrador/editar/controlador/<int:pk>/', ControladorUpdateAdmin.as_view(), name='editar-controlador-admin'),
    path('administrador/editar/sensor/<int:pk>/', SensorUpdateAdmin.as_view(), name='editar-sensor-admin'),
    path('administrador/editar/regra/<int:pk>/', RegraUpdateAdmin.as_view(), name='editar-regra-admin'),
    path('administrador/editar/leitura/<int:pk>/', LeituraUpdateAdmin.as_view(), name='editar-leitura-admin'),

    path('administrador/excluir/user/<int:pk>/', UserDelete.as_view(), name='excluir-user-admin'),
    path('administrador/excluir/sensor/<int:pk>/', SensorDeleteAdmin.as_view(), name='excluir-sensor-admin'),
    path('administrador/excluir/leitura/<int:pk>/', LeituraDeleteAdmin.as_view(), name='excluir-leitura-admin'),

    path('excluir/controlador/<int:pk>/', ControladorDelete.as_view(), name='excluir-controlador'),
    path('excluir/regra/<int:pk>/', RegraDelete.as_view(), name='excluir-regra'),

    path("listar/controlador/", ControladorList.as_view(), name="listar-controlador"),
    path("listar/regra/", RegraList.as_view(), name="listar-regra"),
    path("listar/sensor/", SensorList.as_view(), name="listar-sensor"),
    path("listar/leitura/", LeituraList.as_view(), name="listar-leitura"),

    path('administrador/listar/usuarios/', UserList.as_view(), name='listar-user'),



]
