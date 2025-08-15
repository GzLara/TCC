from django.db import models
from django.contrib.auth.models import User

# Todas as classes DEVEM ter a herança para a classe Model que está dentro de "models"
# class SuaClasse(models.Model):
#   atributo = models.TipoDeAtributo(propriedade1=valor1, p2="v2", p3=v3)

# Depois de criar as classes, defina os atributos e seus tipos
# https://docs.djangoproject.com/pt-br/4.2/ref/models/fields/#field-types

# Cada campo tem suas propriedades, que estão disponíveis em
# https://docs.djangoproject.com/pt-br/4.2/ref/models/fields/#field-options

    
class Controlador(models.Model):
    nome = models.CharField(max_length=255, verbose_name="Nome", default="Controlador Padrão")
    descricao = models.CharField(max_length=255, verbose_name="Descrição")
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    
    cadastrado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name='controladores')
    cadastrado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nome}"
    
    class Meta:
        ordering = ['nome', 'cadastrado_em']
    

class Sensor(models.Model):
    numero_serial = models.CharField(max_length=255, verbose_name="Número Serial")
    descricao = models.CharField(max_length=255, verbose_name="Descrição")
    controlador = models.ForeignKey(Controlador, on_delete=models.CASCADE)
    
    cadastrado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sensores')
    cadastrado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.numero_serial} - {self.descricao} - {self.controlador.nome}"
    
    class Meta:
        ordering = ['descricao', 'cadastrado_em']


class Leitura(models.Model):
    valor = models.FloatField()
    data = models.DateTimeField()
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, null=True)
    
    cadastrado_por = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='leituras')
    cadastrado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.valor} - {self.data} - {self.sensor.numero_serial} - {self.sensor.descricao}"
    
    class Meta:
        ordering = ['sensor', 'cadastrado_em']
    

class Regra(models.Model):
    descricao = models.CharField(max_length=255, verbose_name="Descrição")
    
    horario_inicio = models.TimeField(verbose_name="Horário de Início")
    horario_fim = models.TimeField(verbose_name="Horário de Fim")
    
    valor_minimo = models.FloatField(verbose_name="Valor Mínimo")
    valor_maximo = models.FloatField(verbose_name="Valor Máximo")
    
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    cadastrado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name='regras')
    cadastrado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.descricao} - {self.sensor} - {self.usuario}"

    class Meta:
        ordering = ['descricao', 'sensor', 'cadastrado_em']
