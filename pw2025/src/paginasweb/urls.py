from django.urls import path
from .views import *
from .views import LeituraCreateView

from .views import *
from . import views

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
	#path("api/leitura/", LeituraCreateView.as_view(), name="leitura-create"),
    path('login-admin/', redirecionar_para_adminindex, name='login-admin'),  # onde o formulário envia
    path('api/leituras/', views.LeituraCreateView.as_view(), name='leituras_create'),
    path('api/grafico/', views.grafico_dados, name='grafico_dados'),

    path('', IndexView.as_view(), name='index'),  # Página inicial
    path('indexcliente/', IndexClienteView.as_view(), name='indexcliente'), # Página quando o cliente loga
    path('sobre/', SobreView.as_view(), name='sobre'),  # Página sobre
    path('cadastro/', CadastroView.as_view(), name='cadastro'), # Pagina de cadastro de clientes
    path('controlador/', ControladorView.as_view(), name='controlador'), # Pagina de cadastro de controlador
    path('adminindex/', AdminView.as_view(), name='adminindex'), # Página da área do Admin

    path('cadastrar/controlador/', ControladorCreate.as_view(), name='cadastrar-controlador'),
    path('cadastrar/regra/', RegraCreate.as_view(), name='cadastrar-regra'),
    path('cadastrar/cadastro/', CadastroCreate.as_view(), name='cadastrar-cadastro'),

    path('editar/controlador/<int:pk>/', ControladorUpdate.as_view(), name='editar-controlador'),
    path('editar/regra/<int:pk>/', RegraUpdate.as_view(), name='editar-regra'),
    path('editar/cadastro/<int:pk>/', CadastroUpdate.as_view(), name='editar-cadastro'),

    path('excluir/controlador/<int:pk>/', ControladorDelete.as_view(), name='excluir-controlador'),
    path('excluir/regra/<int:pk>/', RegraDelete.as_view(), name='excluir-regra'),
    path('excluir/cadastro/<int:pk>/', CadastroDelete.as_view(), name='excluir-cadastro'),

    path("listar/controlador/", ControladorView.as_view(), name="listar-controlador"),
    path("listar/regra/", RegraView.as_view(), name="listar-regra"),
    path("listar/cadastro/", CadastroView.as_view(), name="listar-clientes-cadastro"),
    


]
