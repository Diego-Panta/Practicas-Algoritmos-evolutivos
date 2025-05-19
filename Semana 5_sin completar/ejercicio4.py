import pandas as pd
import random
import numpy as np

# Paso 1: Leer el archivo CSV con la información de proyectos
# Suponemos que el archivo CSV tiene las columnas: 'ProjectID', 'Cost_Soles', 'Benefit_Soles'
df_proyectos = pd.read_csv('projects.csv')

# Paso 2: Representación de la solución como un bitstring
# El bitstring tendrá longitud 8, ya que hay 8 proyectos.
bitstring_actual = [random.randint(0, 1) for _ in range(8)]

# Paso 3: Función de aptitud
def calcular_aptitud(bitstring):
    costo_total = 0
    beneficio_total = 0
    for i, bit in enumerate(bitstring):
        if bit == 1:
            costo_total += df_proyectos.iloc[i]['Cost_Soles']
            beneficio_total += df_proyectos.iloc[i]['Benefit_Soles']
    
    if costo_total > 10000:
        return -float('inf')
    
    return beneficio_total

# Paso 4: Función de vecindad (volteamos un bit)
def generar_vecinos(bitstring):
    vecinos = []
    for i in range(len(bitstring)):
        vecino = bitstring.copy()
        vecino[i] = 1 - vecino[i]  # Volteamos el bit
        vecinos.append(vecino)
    return vecinos

# Paso 5: Hill climbing - Búsqueda local
def hill_climbing(iteraciones=1000):
    bitstring_actual = [random.randint(0, 1) for _ in range(8)]  # Iniciar aleatoriamente
    aptitud_actual = calcular_aptitud(bitstring_actual)
    
    for _ in range(iteraciones):
        vecinos = generar_vecinos(bitstring_actual)
        mejor_vecino = bitstring_actual
        mejor_aptitud = aptitud_actual
        
        for vecino in vecinos:
            aptitud_vecino = calcular_aptitud(vecino)
            if aptitud_vecino > mejor_aptitud:
                mejor_vecino = vecino
                mejor_aptitud = aptitud_vecino
        
        if mejor_aptitud > aptitud_actual:
            bitstring_actual = mejor_vecino
            aptitud_actual = mejor_aptitud
        else:
            break  # No hay mejora
    
    return bitstring_actual, aptitud_actual

# Paso 6: Ejecutar hill climbing
bitstring_optimo, beneficio_optimo = hill_climbing()

# Paso 7: Mostrar resultado
print(f"Proyectos seleccionados (bitstring): {bitstring_optimo}")
print(f"Beneficio total: {beneficio_optimo} S/")

# Paso 8: Mostrar los proyectos seleccionados usando el bitstring
# Convertimos el bitstring a un array booleano para filtrar los proyectos
bitstring_optimo = np.array(bitstring_optimo, dtype=bool)
proyectos_seleccionados = df_proyectos[bitstring_optimo]

print("Proyectos seleccionados:")
print(proyectos_seleccionados[['ProjectID', 'Cost_Soles', 'Benefit_Soles']])