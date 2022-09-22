from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import HashModel
from conexion_redis import redis

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)

#Modelo de la tabla en ba se de datos redis (HASHMODEL)
class Medidor(HashModel):
    radar_velocidad: int
    timestamp: float

    class Meta:
        database = redis

# CRUD Métricas

@app.get('/medidor')
def all():
    return [formato(pk) for pk in Medidor.all_pks()]


def formato(pk: str):
    medidor = Medidor.get(pk)
    return {
        "ID": medidor.pk,
        "velocidad": medidor.radar_velocidad,
        "timestamp": medidor.timestamp,
    }

@app.post('/medidor') #esta parte del CRUD es la que se llama para almacenar métricas
def create(medidor: Medidor):
    return medidor.save()


@app.get('/medidor/{pk}')
def get(pk: str):
    return Medidor.get(pk)


@app.delete('/medidor/{pk}')
def delete(pk: str):
    return Medidor.delete(pk)

# Fin CRUD Métricas
