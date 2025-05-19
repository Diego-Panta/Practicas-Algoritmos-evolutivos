import pandas as pd
import random

# Cargar datos desde el CSV
df = pd.read_csv('tesistas.csv')

# Paso 1: Inicializar variables
salas = [f"S{i+1}" for i in range(6)]  # 6 salas disponibles
franjas = [f"F{i+1}" for i in range(6)]  # 6 franjas disponibles

# Asignación inicial de tesistas a franjas y salas secuencialmente
def asignacion_inicial(df):
    asignacion = {}
    for idx, row in df.iterrows():
        tesista = row['TesistaID']
        for i, f in enumerate(franjas):
            if row[f] == 1:
                sala = salas[i % len(salas)]  # Asignación cíclica de salas
                asignacion[tesista] = (sala, f)
                break
    return asignacion

# Paso 2: Función de costo
def calcular_costo(asignacion):
    solapamientos = 0
    huecos = 0
    # Para cada sala, verificamos los solapamientos y huecos
    for sala in salas:
        franjas_ocupadas = [f for tesista, (s, f) in asignacion.items() if s == sala]
        if len(franjas_ocupadas) > 1:  # Si hay más de un tesista en la sala
            franjas_ocupadas.sort()
            # Contamos solapamientos
            for i in range(len(franjas_ocupadas) - 1):
                if franjas_ocupadas[i+1] == franjas_ocupadas[i]:  # Solapamiento en la misma franja
                    solapamientos += 1
        # Verificamos los huecos (espacios vacíos entre franjas ocupadas)
        franjas_ocupadas = sorted(set(franjas_ocupadas))
        # Verificamos los huecos (espacios vacíos entre franjas ocupadas)
        for i in range(1, len(franjas_ocupadas)):
            if franjas_ocupadas[i] != franjas_ocupadas[i-1]:  # Espacio entre franjas ocupadas
                huecos += 1

        # Verificamos que no haya más de 4 horas continuas de uso
        franjas_ocupadas = sorted(franjas_ocupadas)
        if len(franjas_ocupadas) > 4:
            return float('inf')  # Penalizamos excesos de horas continuas
    
    return solapamientos + huecos

# Paso 3: Vecindad (mover un tesista a otra sala/franja)
def generar_vecinos(asignacion, df):
    vecinos = []
    for tesista in asignacion:
        asignacion_vecino = asignacion.copy()
        sala, franja = asignacion[tesista]
        # Cambiar la franja de este tesista
        franjas_disponibles = [f for f in franjas if f != franja and df.loc[df['TesistaID'] == tesista, f].values[0] == 1]
        if franjas_disponibles:
            nueva_franja = random.choice(franjas_disponibles)
            asignacion_vecino[tesista] = (sala, nueva_franja)
            vecinos.append(asignacion_vecino)
    return vecinos

# Paso 4: Hill climbing (iteraciones)
def hill_climbing(df, iteraciones=1000):
    asignacion_actual = asignacion_inicial(df)
    costo_actual = calcular_costo(asignacion_actual)
    
    for _ in range(iteraciones):
        vecinos = generar_vecinos(asignacion_actual, df)
        mejor_vecino = asignacion_actual
        mejor_costo = costo_actual
        
        for vecino in vecinos:
            costo_vecino = calcular_costo(vecino)
            if costo_vecino < mejor_costo:  # Queremos minimizar el costo
                mejor_vecino = vecino
                mejor_costo = costo_vecino
        
        if mejor_costo < costo_actual:
            asignacion_actual = mejor_vecino
            costo_actual = mejor_costo
        else:
            break  # No hay mejora
    
    return asignacion_actual, costo_actual

# Ejecutar hill climbing
asignacion_optima, costo_optimo = hill_climbing(df)

# Paso 5: Mostrar los resultados
print("Asignación final:")
for tesista, (sala, franja) in asignacion_optima.items():
    print(f"{tesista} -> {sala}, {franja}")

print(f"Costo final (solapamientos y huecos): {costo_optimo}")