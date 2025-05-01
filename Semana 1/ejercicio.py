import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations

# Coeficientes de la función objetivo: Z = 50x + 80y
def objetivo(x, y):
    return 50 * x + 80 * y

# Restricciones (como funciones implícitas): Ax + By <= C
def restriccion1(x):  # 2x + 3y <= 120 → y <= (120 - 2x) / 3
    return (120 - 2 * x) / 3

def restriccion2(x):  # y >= 5
    return np.full_like(x, 5)

def restriccion3():   # x >= 10
    return 10

# Intersección entre dos líneas: Ax + By = C
def interseccion(a1, b1, c1, a2, b2, c2):
    A = np.array([[a1, b1], [a2, b2]])
    b = np.array([c1, c2])
    if np.linalg.det(A) == 0:
        return None  # Líneas paralelas
    sol = np.linalg.solve(A, b)
    return sol

# Lista de restricciones como (A, B, C) para Ax + By <= C
restricciones = [
    (2, 3, 120),     # 2x + 3y <= 120
    (0, -1, -5),     # y >= 5 → -y <= -5
    (-1, 0, -10),    # x >= 10 → -x <= -10
]

# Buscar intersecciones válidas entre pares de restricciones
puntos_factibles = []
for (r1, r2) in combinations(restricciones, 2):
    punto = interseccion(*r1, *r2)
    if punto is not None:
        x, y = punto
        # Verificar si cumple TODAS las restricciones
        cumple = all(a * x + b * y <= c + 1e-5 for a, b, c in restricciones)
        if cumple:
            puntos_factibles.append((x, y))

# También evaluar puntos extremos de intersección con los ejes si están dentro
# Agregar vértices límites si forman parte del polígono
x_vals = np.linspace(0, 80, 400)
y1 = restriccion1(x_vals)
y2 = restriccion2(x_vals)
x_min = restriccion3()

# Graficar región factible
plt.figure(figsize=(10, 6))
plt.plot(x_vals, y1, label="2x + 3y ≤ 120", color="red")
plt.axhline(5, color="green", linestyle="--", label="y ≥ 5")
plt.axvline(10, color="blue", linestyle="--", label="x ≥ 10")

# Rellenar región factible (visual, no cálculo)
x_fill = np.linspace(10, 60, 400)
y1_fill = np.minimum((120 - 2 * x_fill) / 3, 50)
y2_fill = np.full_like(x_fill, 5)
plt.fill_between(x_fill, y2_fill, y1_fill, where=(y1_fill >= y2_fill), color='gray', alpha=0.3, label='Región factible')

# Evaluar Z en cada punto factible
valores = [(x, y, objetivo(x, y)) for x, y in puntos_factibles]

# Buscar el máximo
mejor = max(valores, key=lambda t: t[2])
x_opt, y_opt, z_opt = mejor

# Graficar los puntos factibles
for x, y, z in valores:
    plt.plot(x, y, 'ko')
    plt.text(x + 0.5, y + 0.5, f"Z={z:.0f}", fontsize=8)

# Marcar solución óptima
plt.plot(x_opt, y_opt, 'go', label="Óptimo")
plt.text(x_opt + 1, y_opt + 1, f"Máx Z = {z_opt:.0f}", fontsize=10, color='green')

# Configurar gráfico
plt.xlabel("Cantidad de artesanías A (x)")
plt.ylabel("Cantidad de artesanías B (y)")
plt.title("Optimización Dinámica de Ganancia")
plt.grid(True)
plt.legend()
plt.xlim(0, 80)
plt.ylim(0, 50)
plt.show()