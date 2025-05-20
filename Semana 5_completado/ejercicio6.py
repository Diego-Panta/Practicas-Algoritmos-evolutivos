import pandas as pd
import random

# Cargar datos
df = pd.read_csv('examquestions.csv')

# Constantes
NUM_PREGUNTAS = len(df)
TIEMPO_MAX = 90
DIFICULTAD_MIN = 180
DIFICULTAD_MAX = 200

# Función para evaluar una solución
def evaluar(solucion):
    seleccionadas = df[solucion == 1]
    total_tiempo = seleccionadas['Time_min'].sum()
    total_dificultad = seleccionadas['Difficulty'].sum()
    
    if total_tiempo > TIEMPO_MAX:
        return 1000 + (total_tiempo - TIEMPO_MAX) * 10  # Penalización fuerte
    if total_dificultad < DIFICULTAD_MIN:
        return 500 + (DIFICULTAD_MIN - total_dificultad) * 5
    if total_dificultad > DIFICULTAD_MAX:
        return 500 + (total_dificultad - DIFICULTAD_MAX) * 5
    return 0  # Costo 0 si está dentro del rango

# Generar una solución inicial válida (puede requerir intentos)
def generar_solucion_inicial():
    for _ in range(1000):  # Intentos máximos para evitar bucles infinitos
        solucion = pd.Series([random.randint(0, 1) for _ in range(NUM_PREGUNTAS)])
        if evaluar(solucion) == 0:
            return solucion
    return pd.Series([0] * NUM_PREGUNTAS)  # Fallback

# Generar vecinos cambiando un bit
def generar_vecinos(solucion):
    vecinos = []
    for i in range(NUM_PREGUNTAS):
        vecino = solucion.copy()
        vecino[i] = 1 - vecino[i]
        vecinos.append(vecino)
    return vecinos

# Algoritmo Hill Climbing
def hill_climbing(iter_max=1000):
    actual = generar_solucion_inicial()
    mejor_costo = evaluar(actual)
    
    for _ in range(iter_max):
        vecinos = generar_vecinos(actual)
        mejora = False
        for vecino in vecinos:
            costo = evaluar(vecino)
            if costo < mejor_costo:
                actual = vecino
                mejor_costo = costo
                mejora = True
                break  # Usamos "first improvement"
        if not mejora:
            break  # No mejora encontrada, detener
    return actual, mejor_costo

# Ejecutar
solucion, costo_final = hill_climbing()
seleccionadas = df[solucion == 1]

# Mostrar resultados
print("Preguntas seleccionadas:")
print(seleccionadas)
print("\nNúmero de preguntas:", len(seleccionadas))
print("Tiempo total:", seleccionadas['Time_min'].sum())
print("Dificultad total:", seleccionadas['Difficulty'].sum())
print("Costo final:", costo_final) #Esto indica que no hay penalizaciones ni por tiempo ni por dificultad.