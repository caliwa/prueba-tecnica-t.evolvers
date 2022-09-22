import asyncio
import json
import random
from datetime import datetime
from conexion_redis import redis
from csv_archivo.csv import generar_csv


async def metricas_dispositivo(ciclo: int):
    tarea2 = asyncio

    for i in range(ciclo):
        dt = datetime.now()
        timestamp = round(datetime.timestamp(dt), 2)  # debe ir acá para que sea dinámico, redondeo de 2
        vel_random = random.randint(15, 90)
        metricas = json.dumps({
            "radar_velocidad": vel_random,
            "timestamp": timestamp
        })

        generar_csv(vel_random, timestamp) #para construir el csv

        try: #tarea1
            asyncio.create_task(envio_eventos_consumers_fastapi(json.loads(metricas)) ) #consumer fastapi
            if vel_random > 50:
                tarea2 = asyncio.create_task(envio_eventos_consumers_noti(json.loads(metricas)) ) #consumer alertas
                await tarea2
            await asyncio.sleep(2)
        except Exception as e:  # se crea subrutina para enviar las métricas al consumer de almacenamiento
            raise SystemExit(e)


async def envio_eventos_consumers_noti(metricas: dict):
    redis.xadd('umbral_mayor_50', metricas, '*')


async def envio_eventos_consumers_fastapi(metricas: dict):
    redis.xadd('almacenamiento_metricas', metricas, '*')


def main():
    ciclo = 0
    #redis.flushall()
    while ciclo < 10 or ciclo > 100:
        ciclo = int(input("Ingrese el rango de captación del radar (10 - 100): "))
    asyncio.run(metricas_dispositivo(ciclo))


if __name__ == '__main__':
    main()
