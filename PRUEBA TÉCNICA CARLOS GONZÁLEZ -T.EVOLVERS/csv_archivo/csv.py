import csv

def generar_csv(vel_random:int, timestamp:float):
    f = open('archivo.csv', 'a', newline='')

    fila = (vel_random, timestamp)
    escritor = csv.writer(f)
    escritor.writerow(fila)
    f.close()