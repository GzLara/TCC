import os
import sys
import django
import random
import time
from datetime import datetime
from django.utils.timezone import make_aware

# Caminho absoluto até a pasta onde está o manage.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, "src")  # onde está o código do projeto

# Garante que o Python ache a pasta do projeto
sys.path.append(SRC_DIR)

# Configura o Django para usar as configurações corretas
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pw2025.settings")  # ajuste se o nome do projeto não for pw2025

django.setup()

from paginasweb.models import Leitura, Sensor  # ajuste se o modelo estiver em outro app

def get_or_create_sensor(nome):
    sensor, _ = Sensor.objects.get_or_create(tipo_sensor=nome)
    return sensor

def gerar_leitura():
    agora = make_aware(datetime.now())

    # Cria ou obtém os sensores
    sensor_temp = get_or_create_sensor("Temperatura")
    sensor_umid = get_or_create_sensor("Umidade")

    # Gera valores aleatórios
    temperatura = round(random.uniform(18.0, 35.0), 1)
    umidade = round(random.uniform(30.0, 90.0), 1)

    # Salva no banco
    Leitura.objects.create(data=agora, sensor=sensor_temp, valor=temperatura)
    Leitura.objects.create(data=agora, sensor=sensor_umid, valor=umidade)

    print(f"[{agora.strftime('%H:%M:%S')}] Temperatura={temperatura}°C, Umidade={umidade}% (salvo no banco)")

if __name__ == "__main__":
    print("Simulador de Arduino rodando! Pressione Ctrl+C para parar.")
    try:
        while True:
            gerar_leitura()
            time.sleep(3)
    except KeyboardInterrupt:
        print("\nSimulador encerrado.")
