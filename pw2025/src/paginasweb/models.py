from django.db import models
from django.contrib.auth.models import User

# Todas as classes DEVEM ter a herança para a classe Model que está dentro de "models"
# class SuaClasse(models.Model):
#   atributo = models.TipoDeAtributo(propriedade1=valor1, p2="v2", p3=v3)

# Depois de criar as classes, defina os atributos e seus tipos
# https://docs.djangoproject.com/pt-br/4.2/ref/models/fields/#field-types

# Cada campo tem suas propriedades, que estão disponíveis em
# https://docs.djangoproject.com/pt-br/4.2/ref/models/fields/#field-options

class IndexCliente(models.Model):
    descricao = models.CharField(max_length=255, verbose_name="Descrição")


class TipoSensor(models.Model):
    numero_serial = models.CharField(max_length=255, verbose_name="Número Serial")
    descricao = models.CharField(max_length=255, verbose_name="Descrição")

    def __str__(self):
        return f"{self.numero_serial}"

    
class Admin(models.Model):
    nome = models.CharField(max_length=30, verbose_name="Nome")
    email = models.EmailField(max_length=255, verbose_name="E-mail")
    senha = models.CharField(max_length=255, verbose_name="Senha")
    cadastrado_em = models.DateTimeField(max_length=30, auto_now_add=True)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin')

    def __str__(self):
        return f"{self.nome}"

class Cadastro(models.Model):
    nome = models.CharField(max_length=30, verbose_name="Nome")
    email = models.EmailField(max_length=255, verbose_name="E-mail")
    senha = models.CharField(max_length=255, verbose_name="Senha")
    cadastrado_em = models.DateTimeField(max_length=30, auto_now_add=True)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cadastro')

    def __str__(self):
        return f"{self.nome}"
    
class Controlador(models.Model):
    cadastro_cliente = models.ForeignKey(Cadastro, on_delete=models.PROTECT, null=True, blank=True)
    nome = models.CharField(max_length=255, verbose_name="Nome", default="Controlador Padrão")
    descricao = models.CharField(max_length=255, verbose_name="Descrição")

    def __str__(self):
        return f"{self.nome}"


class Sensor(models.Model):
    descricao = models.CharField(max_length=255, verbose_name="Descrição")
    controlador = models.ForeignKey(Controlador, on_delete=models.PROTECT)
    tipo_sensor = models.ForeignKey(TipoSensor, on_delete=models.PROTECT)


class Regra(models.Model):
    descricao = models.CharField(max_length=255, verbose_name="Descrição")
    horario_inicio = models.CharField(
        max_length=10,
        verbose_name="Horário de Início"
    )
    horario_fim = models.CharField(
        max_length=10,
        verbose_name="Horário de Fim"
    )
    valor_minimo = models.FloatField()
    valor_maximo = models.FloatField()
    controlador = models.ForeignKey(Controlador, on_delete=models.PROTECT,  null=True, blank=True)


class Leitura(models.Model):
    tipo_sensor = models.ForeignKey(TipoSensor, on_delete=models.PROTECT)
    valor = models.FloatField()
    data = models.DateTimeField()
    temperatura = models.DecimalField(max_digits=5, decimal_places=2)
    sensor = models.ForeignKey(Sensor, on_delete=models.PROTECT)
    alerta = models.ForeignKey(
        Regra, on_delete=models.SET_NULL, null=True, blank=True
    )
