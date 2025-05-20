import pandas as pd
import numpy as np
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
from deap import base, creator, tools
import matplotlib.pyplot as plt

# --- Datos ---
df = pd.read_csv("emails.csv")

X = df[['Feature1','Feature2','Feature3','Feature4','Feature5']].values
y = df['Spam'].values

# División en train y validación para evaluar fitness
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.3, random_state=42)

# --- DEAP setup ---

creator.create("FitnessMax", base.Fitness, weights=(1.0,))  # Maximizar F1-score
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
# Genotipo: 6 floats (umbral + 5 pesos), inicializados uniformemente en rango [0,1]
toolbox.register("attr_float", np.random.uniform, 0, 1)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=6)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Función para predecir con un individuo
def predict_spam(individual, X):
    threshold = individual[0]
    weights = np.array(individual[1:])
    scores = X.dot(weights)
    return (scores >= threshold).astype(int)

# Fitness: calcular F1-score en validación
def eval_f1(individual):
    y_pred = predict_spam(individual, X_val)
    return (f1_score(y_val, y_pred),)

toolbox.register("evaluate", eval_f1)

# Mutación gaussiana pequeña
def mut_gauss(individual, mu=0, sigma=0.1, indpb=0.5):
    for i in range(len(individual)):
        if np.random.rand() < indpb:
            individual[i] += np.random.normal(mu, sigma)
            # Mantener pesos y umbral en rango [0,1]
            if individual[i] < 0:
                individual[i] = 0
            elif individual[i] > 1:
                individual[i] = 1
    return (individual,)

toolbox.register("mutate", mut_gauss)

# Sin cruce
toolbox.register("mate", lambda ind1, ind2: None)

# Selección greedy con hill climbing local
def hill_climb(pop):
    best_fits = []
    best_ind = tools.selBest(pop, 1)[0]
    best_fit = best_ind.fitness.values[0]

    NGEN = 100
    for gen in range(NGEN):
        for i, ind in enumerate(pop):
            mutant = toolbox.clone(ind)
            toolbox.mutate(mutant)
            del mutant.fitness.values
            fit_mut = toolbox.evaluate(mutant)

            # Reemplaza solo si mejora
            if fit_mut[0] > ind.fitness.values[0]:
                pop[i] = mutant
                pop[i].fitness.values = fit_mut

                if fit_mut[0] > best_fit:
                    best_fit = fit_mut[0]
                    best_ind = mutant

        best_fits.append(best_fit)
        print(f"Gen {gen+1}: Mejor F1-score = {best_fit:.4f}")

    return best_ind, best_fits

def main():
    pop = toolbox.population(n=20)
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    best_ind, fitness_history = hill_climb(pop)

    print("\nMejores pesos encontrados:")
    print(f"Umbral: {best_ind[0]:.4f}")
    for i,w in enumerate(best_ind[1:], 1):
        print(f"Peso Feature{i}: {w:.4f}")

    # Graficar F1-score por generación
    plt.plot(fitness_history, label="Mejor F1-score")
    plt.xlabel("Generación")
    plt.ylabel("F1-score")
    plt.title("Curva de convergencia F1-score")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()