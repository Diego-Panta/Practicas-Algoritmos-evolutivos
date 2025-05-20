import pandas as pd
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from deap import base, creator, tools
import random
import matplotlib.pyplot as plt
import warnings
from sklearn.exceptions import ConvergenceWarning

warnings.filterwarnings("ignore", category=ConvergenceWarning)

# --- Datos ---
df = pd.read_csv("enrollments.csv")

X = df[['Credits','Prev_GPA','Extracurricular_hours']].values
y_raw = df['Category'].values

# Codificar categorías (Alta=0, Media=1, Baja=2 o similar)
le = LabelEncoder()
y = le.fit_transform(y_raw)

# Escalar features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# División train-test
X_train, X_val, y_train, y_val = train_test_split(X_scaled, y, test_size=0.3, random_state=42)

# --- DEAP setup ---

creator.create("FitnessMax", base.Fitness, weights=(1.0,))  # Maximizar accuracy
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

# Genotipo: [num_capas(1-3), neuronas_capa1(1-50), neuronas_capa2(0-50), neuronas_capa3(0-50), learning_rate(0.0001-0.1)]
# neuronas capa 2 y 3 pueden ser 0 si capa no existe

def create_individual():
    n_layers = random.randint(1,3)
    neurons = [random.randint(1,50) for _ in range(n_layers)]
    # completar hasta 3 capas con ceros
    neurons += [0]*(3 - n_layers)
    lr = random.uniform(0.0001, 0.1)
    return [n_layers] + neurons + [lr]

toolbox.register("individual", tools.initIterate, creator.Individual, create_individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Evaluar fitness (accuracy) entrenando MLP 20 epochs
def eval_nn(individual):
    n_layers = int(individual[0])
    neurons = [int(n) for n in individual[1:1+n_layers]]
    lr = individual[-1]

    # Configurar hidden_layer_sizes según capas activas
    hidden_layer_sizes = tuple(neurons)

    try:
        mlp = MLPClassifier(hidden_layer_sizes=hidden_layer_sizes,
                            learning_rate_init=lr,
                            max_iter=20,
                            random_state=42)
        mlp.fit(X_train, y_train)
        preds = mlp.predict(X_val)
        acc = accuracy_score(y_val, preds)
    except Exception as e:
        # Si algo falla (p.ej. capa con 0 neuronas), asignar fitness muy bajo
        acc = 0.0

    return (acc,)

toolbox.register("evaluate", eval_nn)

# Mutación: muta una variable (entero o float) con pequeño cambio
def mutate_individual(individual):
    idx = random.randint(0, len(individual)-1)
    if idx == 0:  # num capas (int)
        individual[0] = max(1, min(3, individual[0] + random.choice([-1,1])))
        # Ajustar neuronas capas si capas cambian
        n_layers = individual[0]
        # Si hay más capas que antes, asignar neuronas aleatorias
        for i in range(1,1+n_layers):
            if individual[i] == 0:
                individual[i] = random.randint(1,50)
        # Si menos capas, poner a 0 neuronas capas extras
        for i in range(1+n_layers,4):
            individual[i] = 0

    elif 1 <= idx <= 3:  # neuronas (int)
        if individual[idx] > 0:
            change = random.choice([-5, -1, 1, 5])
            individual[idx] = max(0, min(50, individual[idx] + change))
            # Si neuronas pasa a 0 y capa es activa, reducir capa
            if individual[idx] == 0 and idx <= individual[0]:
                individual[0] = idx - 1  # reducir capas activas si capa queda sin neuronas
        else:
            # Si es 0, posibilidad de activar con random
            if random.random() < 0.3:
                individual[idx] = random.randint(1,50)

    else:  # tasa aprendizaje (float)
        change = np.random.normal(0, 0.01)
        individual[idx] = max(0.0001, min(0.1, individual[idx] + change))

    return (individual,)

toolbox.register("mutate", mutate_individual)

# Sin cruce
toolbox.register("mate", lambda ind1, ind2: None)

# Hill climbing local (mutar y aceptar solo si mejora)
def hill_climb(pop, ngen=30):
    best_fits = []
    best_ind = tools.selBest(pop,1)[0]
    best_fit = best_ind.fitness.values[0]

    for gen in range(ngen):
        for i, ind in enumerate(pop):
            mutant = toolbox.clone(ind)
            toolbox.mutate(mutant)
            del mutant.fitness.values
            fit_mut = toolbox.evaluate(mutant)
            if fit_mut[0] > ind.fitness.values[0]:
                pop[i] = mutant
                pop[i].fitness.values = fit_mut
                if fit_mut[0] > best_fit:
                    best_fit = fit_mut[0]
                    best_ind = mutant
        best_fits.append(best_fit)
        print(f"Generación {gen+1}, Mejor Accuracy: {best_fit:.4f}")

    return best_ind, best_fits

def main():
    pop = toolbox.population(n=20)
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    best_ind, fitness_hist = hill_climb(pop, ngen=30)

    print("\nArquitectura óptima:")
    print(f"Número capas: {best_ind[0]}")
    print("Neurona(s) por capa:", [int(n) for n in best_ind[1:1+int(best_ind[0])]])
    print(f"Tasa aprendizaje: {best_ind[-1]:.5f}")
    print(f"Accuracy final: {best_ind.fitness.values[0]:.4f}")

    # Graficar evolución accuracy
    plt.plot(fitness_hist)
    plt.xlabel("Generación")
    plt.ylabel("Accuracy")
    plt.title("Curva de convergencia Accuracy")
    plt.show()

if __name__ == "__main__":
    main()