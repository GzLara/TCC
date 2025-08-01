from django.urls import path
from .views import *
from .views import LeituraCreateView

from .views import *
from . import views

from django.contrib.auth import views as auth_views


urlpatterns = [

    # Criar rota para página de login
    path('cadastrar/cadastro/', CustomLoginView.as_view(
       template_name = 'paginasweb/formlogin.html',
       extra_context = {
          'titulo': 'Login',
          'botao': 'Entrar',
     }
   ), name='cadastrar'),

   path('senha/', auth_views.PasswordChangeView.as_view(
       template_name = 'paginasweb/form.html',
       extra_context = {
          'titulo': 'Atualizar senha',
          'botao': 'Salvar',
     }
   ), name='senha'),

    path('senhaadmin/', auth_views.PasswordChangeView.as_view(
       template_name = 'paginasweb/formadminsenha.html',
       extra_context = {
          'titulo': 'Atualizar senha',
          'botao': 'Salvar',
     }
   ), name='senhaadmin'),

   # Criar rota de logout
   path('logout/', auth_views.LogoutView.as_view(), name ='logout'),

    #parte tcc
	#path("api/leitura/", LeituraCreateView.as_view(), name="leitura-create"),
    path('login-admin/', redirecionar_para_adminindex, name='login-admin'),  # onde o formulário envia
    path('api/leituras/', views.LeituraCreateView.as_view(), name='leituras_create'),
    path('api/grafico/', views.grafico_dados, name='grafico_dados'),
    path('controladores-completo/', ControladorAdminComClienteView.as_view(), name='controladores-completo'),
    path('regras-completo/', RegraAdminComClienteView.as_view(), name='regras-completo'),

    path('', redirecionar_para_login, name='redirecionar-login'),  # Página inicial
    path('index/', IndexView.as_view(), name='index'), # Página quando o cliente loga
    path('sobre/', SobreView.as_view(), name='sobre'),  # Página sobre
    path('cadastro/', CadastroView.as_view(), name='cadastro'), # Pagina de cadastro de clientes
    path('controlador/', ControladorView.as_view(), name='controlador'), # Pagina de cadastro de controlador
    path('adminindex/', AdminView.as_view(), name='adminindex'), # Página da área do Admin
    path('regras/', RegraView.as_view(), name='regras'), # Página de regras
    path('sobreadmin/', SobreViewAdmin.as_view(), name='sobreadmin'),  # Página sobre do admin

    path('cadastrar/controladoradmin/', ControladorCreateAdmin.as_view(), name='cadastrar-controlador-admin'),
    path('cadastrar/regraadmin/', RegraCreateAdmin.as_view(), name='cadastrar-regra-admin'),
    path('cadastrar/controlador/', ControladorCreate.as_view(), name='cadastrar-controlador'),
    path('cadastrar/regra/', RegraCreate.as_view(), name='cadastrar-regra'),
    path('cadastrar/cadastro/', CadastroCreate.as_view(), name='cadastrar-cadastro'),
    path('cadastrar/sobreadmin/', SobreAdminCreate.as_view(), name='cadastrar-sobreadmin'),
    path('registrar/', UsuarioCreate.as_view(), name='registrar'),

    path('editar/controladoradmin/<int:pk>/', ControladorUpdateAdmin.as_view(), name='editar-controlador-admin'),
    path('editar/regraadmin/<int:pk>/', RegraUpdateAdmin.as_view(), name='editar-regra-admin'),
    path('editar/controlador/<int:pk>/', ControladorUpdate.as_view(), name='editar-controlador'),
    path('editar/regra/<int:pk>/', RegraUpdate.as_view(), name='editar-regra'),
    path('editar/cadastro/<int:pk>/', CadastroUpdate.as_view(), name='editar-cadastro'),
    path('editar/sobreadmin/<int:pk>/', SobreAdminUpdate.as_view(), name='editar-sobreadmin'),

    path('excluir/controladoradmin/<int:pk>/', ControladorDeleteAdmin.as_view(), name='excluir-controlador-admin'),
    path('excluir/regraadmin/<int:pk>/', RegraDeleteAdmin.as_view(), name='excluir-regra-admin'),
    path('excluir/controlador/<int:pk>/', ControladorDelete.as_view(), name='excluir-controlador'),
    path('excluir/regra/<int:pk>/', RegraDelete.as_view(), name='excluir-regra'),
    path('excluir/cadastro/<int:pk>/', CadastroDelete.as_view(), name='excluir-cadastro'),
    path('excluir/sobreadmin/<int:pk>/', SobreAdminDelete.as_view(), name='excluir-sobreadmin'),

    path("listar/controladoradmin/", ControladorListViewAdmin.as_view(), name="listar-controlador-admin"),
    path("listar/regraadmin/", RegraListViewAdmin.as_view(), name="listar-regra-admin"),
    path("listar/controlador/", ControladorListView.as_view(), name="listar-controlador"),
    path("listar/regra/", RegraListView.as_view(), name="listar-regra"),
    path("listar/cadastro/", CadastroListView.as_view(), name="listar-clientes-cadastro"),
    
    


]
