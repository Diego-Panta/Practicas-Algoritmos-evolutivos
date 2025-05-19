import pandas as pd

# Paso 1: Leer el archivo
df = pd.read_csv('grades.csv')

# Asegurarnos de trabajar solo con columnas numéricas (e.g., 'Parcial1', 'Parcial2', 'Parcial3')
df_numerico = df.select_dtypes(include='number').astype(float)

# Paso 2: Función de aptitud
def calcular_aptitud(df, offset):
    df_offset = df + offset
    promedios = df_offset.mean(axis=1)
    promedio_general = promedios.mean()
    porcentaje_aprobados = (promedios >= 11).mean()

    if promedio_general > 14:
        return 0  # Penalización
    return porcentaje_aprobados

# Paso 3: Hill climbing
offset_actual = 0
mejor_aptitud = calcular_aptitud(df_numerico, offset_actual)
paso = 0.5
mejor_offset = offset_actual

while True:
    vecinos = [offset_actual + paso, offset_actual - paso]
    vecinos = [o for o in vecinos if -5 <= o <= 5]
    mejora = False

    for vecino in vecinos:
        aptitud_vecino = calcular_aptitud(df_numerico, vecino)
        if aptitud_vecino > mejor_aptitud:
            mejor_aptitud = aptitud_vecino
            offset_actual = vecino
            mejor_offset = vecino
            mejora = True
            break  # Primera mejora

    if not mejora:
        break  # No hay mejora → detener

# Paso 4: Resultados
df_final = df_numerico + mejor_offset
promedios_finales = df_final.mean(axis=1)
porcentaje_final = (promedios_finales >= 11).mean() * 100
promedio_general_final = promedios_finales.mean()

print(f"Offset óptimo: {mejor_offset}")
print(f"Porcentaje de aprobados: {porcentaje_final:.2f}%")
print(f"Promedio general de la clase: {promedio_general_final:.2f}")