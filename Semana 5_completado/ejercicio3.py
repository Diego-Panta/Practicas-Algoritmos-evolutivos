import pandas as pd
import random

# Paso 1: Leer el archivo CSV con la matriz de distancias
# Suponiendo que tienes un archivo CSV llamado 'distancias.csv' que tiene la matriz de distancias 10x10
df_distancias = pd.read_csv('labdistances.csv', index_col=0)

# Paso 2: Representación de la solución como permutación
lab_ids = list(df_distancias.index)  # Laboratorios son las filas/columnas del DataFrame
random.shuffle(lab_ids)  # Mezclamos el orden de los laboratorios para iniciar

# Paso 3: Función de costo: calcular la distancia total de la ruta
def calcular_costo(ruta):
    distancia_total = 0
    for i in range(len(ruta) - 1):
        distancia_total += df_distancias.loc[ruta[i], ruta[i + 1]]
    distancia_total += df_distancias.loc[ruta[-1], ruta[0]]  # Regresamos al primer laboratorio
    return distancia_total

# Paso 4: Función de vecindad: intercambiar dos nodos en la ruta
def generar_vecinos(ruta):
    vecinos = []
    for i in range(len(ruta)):
        for j in range(i + 1, len(ruta)):
            nuevo_ruta = ruta.copy()
            nuevo_ruta[i], nuevo_ruta[j] = nuevo_ruta[j], nuevo_ruta[i]  # Intercambiamos los nodos
            vecinos.append(nuevo_ruta)
    return vecinos

# Paso 5: Hill climbing - Búsqueda local
def hill_climbing(iteraciones=1000):
    ruta_actual = lab_ids.copy()
    costo_actual = calcular_costo(ruta_actual)
    
    for _ in range(iteraciones):
        vecinos = generar_vecinos(ruta_actual)
        mejor_vecino = ruta_actual
        mejor_costo = costo_actual
        
        for vecino in vecinos:
            costo_vecino = calcular_costo(vecino)
            if costo_vecino < mejor_costo:
                mejor_vecino = vecino
                mejor_costo = costo_vecino
        
        if mejor_costo < costo_actual:
            ruta_actual = mejor_vecino
            costo_actual = mejor_costo
        else:
            break  # No hay mejora
    
    return ruta_actual, costo_actual

# Paso 6: Ejecutar hill climbing
ruta_optima, costo_optimo = hill_climbing()

# Paso 7: Mostrar resultado
print(f"Ruta óptima de laboratorios (orden de visita): {ruta_optima}")
print(f"Distancia total recorrida: {costo_optimo} metros")