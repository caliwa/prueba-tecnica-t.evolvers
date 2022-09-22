import asyncio
from simulador.conexion_redis import redis

key = 'umbral_mayor_50'
group = 'notificacion'

resultados = {}

try:
    redis.xgroup_create(key, group)
except:
    pass

async def metodo_notificar():
    i = 1
    while True:
        try:
            resultados = redis.xreadgroup(group, key, {key: '>'}, None)  # > significa tomar todos los eventos
            if len(resultados) != 0:
                print("ALERTA, UMBRAL DE 50km/h SUPERADO!")
                print(f"#{i}. {resultados}")
                i += 1
                redis.xgroup_delconsumer(key, group)
                #redis.xgroup_destroy(key, group) #evento consumido, eliminado de la lista de consumidor
                # eliminando el grupo con 1 item y volviendolo a crear
        except Exception as e:
            print("Fin de notificación")
            #print(str(e))

asyncio.run(metodo_notificar())