import pandas as pd
import random
import copy

# Cargar datos
df = pd.read_csv('students.csv')

# Constantes
NUM_EQUIPOS = 5
TAM_EQUIPO = 4
TOTAL_ESTUDIANTES = NUM_EQUIPOS * TAM_EQUIPO
PENALIZACION_SKILL = 10  # Puedes ajustar este peso

# Representación inicial: asignación aleatoria a equipos
def generar_solucion_inicial():
    indices = list(range(TOTAL_ESTUDIANTES))
    random.shuffle(indices)
    equipos = [indices[i*TAM_EQUIPO:(i+1)*TAM_EQUIPO] for i in range(NUM_EQUIPOS)]
    return equipos

# Evaluación: varianza de GPA + penalización por desbalance de skills
def evaluar(equipos):
    varianza_gpa_total = 0
    penalizacion_skills = 0

    for equipo in equipos:
        sub_df = df.loc[equipo]
        varianza_gpa_total += sub_df['GPA'].var()

        # Penalización por desbalance de habilidades en el equipo
        counts = sub_df['Skill'].value_counts()
        max_count = counts.max()
        min_count = counts.min() if len(counts) > 1 else max_count
        penalizacion_skills += (max_count - min_count) * PENALIZACION_SKILL

    return varianza_gpa_total + penalizacion_skills

# Generar vecinos por swap entre dos equipos distintos
def generar_vecinos(equipos):
    vecinos = []
    for i in range(NUM_EQUIPOS):
        for j in range(i+1, NUM_EQUIPOS):
            for idx_i in range(TAM_EQUIPO):
                for idx_j in range(TAM_EQUIPO):
                    nuevo = copy.deepcopy(equipos)
                    # Intercambio
                    nuevo[i][idx_i], nuevo[j][idx_j] = nuevo[j][idx_j], nuevo[i][idx_i]
                    vecinos.append(nuevo)
    return vecinos

# Hill climbing
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
                break  # First improvement
        if not mejora:
            break
    return actual, mejor_costo

# Ejecutar
solucion, costo_final = hill_climbing()
print(f"\nCosto final: {costo_final:.2f}\n")

# Mostrar equipos
for i, equipo in enumerate(solucion):
    sub_df = df.loc[equipo].reset_index(drop=True)
    print(f"\nEquipo {i+1}")
    print(sub_df)
    print(f"GPA promedio: {sub_df['GPA'].mean():.2f}")
    counts = sub_df['Skill'].value_counts()
    skill_dict = {k: int(v) for k, v in counts.items()}
    print("Skills:", skill_dict)