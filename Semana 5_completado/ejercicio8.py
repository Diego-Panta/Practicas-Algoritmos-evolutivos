import pandas as pd
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error
from deap import base, creator, tools, algorithms
import matplotlib.pyplot as plt

# --- Datos ---
df = pd.read_csv("houseprices.csv")

X = df[['Rooms', 'Area_m2']].values
y = df['Price_Soles'].values

# --- DEAP setup ---

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))  # Minimizar RMSE
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
# El gen: α real entre 0.001 y 10 (rango común para α en Ridge)
toolbox.register("attr_float", np.random.uniform, 0.001, 10.0)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=1)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Función de evaluación
def eval_ridge(individual):
    alpha = individual[0]
    model = Ridge(alpha=alpha)
    model.fit(X, y)
    y_pred = model.predict(X)
    rmse = np.sqrt(mean_squared_error(y, y_pred))
    return (rmse,)

toolbox.register("evaluate", eval_ridge)

# Sin cruce
toolbox.register("mate", lambda ind1, ind2: None)

# Mutación gaussiana pequeña, sigma=0.1, prob mut 1 para que siempre muta
def mut_gauss(individual, mu=0, sigma=0.1, indpb=1.0):
    for i in range(len(individual)):
        if np.random.rand() < indpb:
            individual[i] += np.random.normal(mu, sigma)
            # Mantener α positivo y en rango
            if individual[i] < 0.001:
                individual[i] = 0.001
            elif individual[i] > 10:
                individual[i] = 10
    return (individual,)

toolbox.register("mutate", mut_gauss)

# Selección greedy: reemplazar solo si mejora (se implementa manualmente abajo)

# --- Algoritmo Hill Climbing con población ---
def main():
    pop = toolbox.population(n=20)
    # Evaluar población inicial
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    best_fits = []
    best_ind = tools.selBest(pop, 1)[0]
    best_fit = best_ind.fitness.values[0]

    NGEN = 100
    for gen in range(NGEN):
        for i, ind in enumerate(pop):
            # Generar vecino por mutación
            mutant = toolbox.clone(ind)
            toolbox.mutate(mutant)
            del mutant.fitness.values

            # Evaluar vecino
            fit_mut = toolbox.evaluate(mutant)

            # Reemplazar solo si mejora
            if fit_mut[0] < ind.fitness.values[0]:
                pop[i] = mutant
                pop[i].fitness.values = fit_mut

                # Actualizar mejor global
                if fit_mut[0] < best_fit:
                    best_fit = fit_mut[0]
                    best_ind = mutant

        best_fits.append(best_fit)
        print(f"Gen {gen+1} - Mejor RMSE: {best_fit:.4f} con α={best_ind[0]:.4f}")

    return best_ind, best_fits

if __name__ == "__main__":
    best_solution, convergence = main()

    print("\n== Resultado final ==")
    print(f"α óptimo: {best_solution[0]:.4f}")
    print(f"RMSE mínimo: {convergence[-1]:.4f}")

    # Curva de convergencia
    import matplotlib.pyplot as plt
    plt.plot(convergence, label="Mejor RMSE")
    plt.xlabel("Generación")
    plt.ylabel("RMSE")
    plt.title("Curva de convergencia - Hill Climbing DEAP")
    plt.legend()
    plt.show()