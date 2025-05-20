import pandas as pd
import random

# Paso 1: Leer el archivo CSV con la información de proyectos
df_proyectos = pd.read_csv('projects.csv')

# Paso 2: Representación de la solución como un bitstring (longitud 8)
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

# Paso 4: Generar vecinos (voltear un bit)
def generar_vecinos(bitstring):
    vecinos = []
    for i in range(len(bitstring)):
        vecino = bitstring.copy()
        vecino[i] = 1 - vecino[i]
        vecinos.append(vecino)
    return vecinos

# Paso 5: Hill climbing
def hill_climbing(iteraciones=1000):
    bitstring_actual = [random.randint(0, 1) for _ in range(8)]
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
            break
    
    return bitstring_actual, aptitud_actual

# Paso 6: Ejecutar hill climbing
bitstring_optimo, beneficio_optimo = hill_climbing()

# Paso 7: Mostrar resultado
print(f"Proyectos seleccionados (bitstring): {bitstring_optimo}")
print(f"Beneficio total: {beneficio_optimo} S/")

# Paso 8: Filtrar proyectos con pandas sin numpy, creando una lista booleana
filtro_booleano = [bool(b) for b in bitstring_optimo]

proyectos_seleccionados = df_proyectos[filtro_booleano]

print("Proyectos seleccionados:")
print(proyectos_seleccionados[['ProjectID', 'Cost_Soles', 'Benefit_Soles']])