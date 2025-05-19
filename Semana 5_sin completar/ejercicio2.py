import pandas as pd

# Paso 1: Leer el archivo CSV
df = pd.read_csv('mentoravailability.csv')

# Extraemos las columnas de slots
slots = df.columns[1:]

# Paso 2: Función para generar los bloques de 2 horas consecutivas donde hay disponibilidad
def generar_bloques_disponibles(row):
    bloques = []
    for i in range(len(row) - 1):
        if row[i] == 1 and row[i+1] == 1:
            bloques.append((slots[i], slots[i+1]))
    return bloques

# Paso 3: Función de asignación de bloques iniciales para cada mentor
def asignar_bloques_iniciales():
    asignaciones = {}
    for idx, row in df.iterrows():
        bloques_disponibles = generar_bloques_disponibles(row[1:])
        if bloques_disponibles:
            asignaciones[row['MentorID']] = bloques_disponibles[0]  # Tomamos el primer bloque disponible
    return asignaciones

# Paso 4: Calcular el costo (choques) dado un conjunto de asignaciones
def calcular_choques(asignaciones):
    # Contamos cuántos mentores están asignados a cada slot
    slots_ocupados = pd.Series(0, index=slots)
    for bloque in asignaciones.values():
        slots_ocupados[bloque[0]] += 1
        slots_ocupados[bloque[1]] += 1
    choques = sum(slots_ocupados > 1)  # Contamos cuántos slots tienen más de 1 mentor
    return choques

# Paso 5: Función de búsqueda local (vecindad) - Cambiar 1 bloque de un mentor
def generar_vecinos(asignaciones):
    vecinos = []
    for mentor, bloque in asignaciones.items():
        # Obtener los bloques disponibles para este mentor
        mentor_row = df[df['MentorID'] == mentor].iloc[0]
        bloques_disponibles = generar_bloques_disponibles(mentor_row[1:])
        for nuevo_bloque in bloques_disponibles:
            if nuevo_bloque != bloque:
                nueva_asignacion = asignaciones.copy()
                nueva_asignacion[mentor] = nuevo_bloque
                vecinos.append(nueva_asignacion)
    return vecinos

# Paso 6: Hill climbing - Búsqueda local
def hill_climbing():
    asignaciones_actuales = asignar_bloques_iniciales()
    costo_actual = calcular_choques(asignaciones_actuales)
    
    while True:
        vecinos = generar_vecinos(asignaciones_actuales)
        mejor_vecino = asignaciones_actuales
        mejor_costo = costo_actual
        
        for vecino in vecinos:
            costo_vecino = calcular_choques(vecino)
            if costo_vecino < mejor_costo:
                mejor_vecino = vecino
                mejor_costo = costo_vecino
        
        # Si no hay mejora, terminamos
        if mejor_costo == costo_actual:
            break
        
        # Actualizamos la solución con el mejor vecino encontrado
        asignaciones_actuales = mejor_vecino
        costo_actual = mejor_costo
    
    return asignaciones_actuales, costo_actual

# Paso 7: Ejecutar hill climbing
asignaciones_finales, choques_finales = hill_climbing()

# Paso 8: Mostrar el resultado
print("Asignación final de bloques:")
for mentor, bloque in asignaciones_finales.items():
    print(f"{mentor}: {bloque}")
print(f"Choques finales: {choques_finales+1}")