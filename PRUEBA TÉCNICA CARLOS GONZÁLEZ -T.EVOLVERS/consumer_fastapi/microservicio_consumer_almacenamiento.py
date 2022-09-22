import requests, asyncio, json
from simulador.conexion_redis import redis

key = 'almacenamiento_metricas'
group = 'almacenamiento'

url = "http://127.0.0.1:8000/medidor" #URL de la conexión @app.post('/medidor') de fastapi

headers = {
    'Content-Type': 'application/json'
}

try:
    redis.xgroup_create(key, group)
except:
    pass
    #print("Grupo existente")

async def ingreso_metricas_redis(headers: dict):
    cont = 0
    while True:
        metricas = redis.xreadgroup(group, key, {key: '>'}, None)# > significa tomar todos los eventos

        contenido = ' '.join(str(e) for e in metricas) #se mira si hay caracteres en la lista
        if len(contenido) != 0:
            cont+=1
            metricas = metricas[0][1][0][1] #es una lista, al acceder al dato exacto del {}, pasa a ser
            print(f'{cont}. {metricas}')                 #un diccionario, ya que las variables son dinámicas en python
            #json.dumps es un metodo para convertir el diccionario en formato json
            requests.request("POST", url, headers=headers, data=json.dumps(metricas) )  # envio a redisDB


asyncio.run(ingreso_metricas_redis(headers))
