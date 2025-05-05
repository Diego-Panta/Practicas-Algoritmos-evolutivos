# Estudiante: Panta Piscoche Jose Diego
# Semana 2 30/04/25

paga = 2

# Construcción de datos
estudiantes = ['Ana', 'Luis', 'Maria', 'Juan', 'Carla']
horas_usadas = [3, 5, 2, 4, 1]

# Calculamos el costo total por estudiante
costo_total = []
for horas in horas_usadas:
    costo_total.append(paga * horas)

# Mostrar tabla
print("DataFrame de uso de laboratorio")
print(f"{'Estudiante':<10} {'Horas_usadas':<15} {'Costo_total'}")
for i in range(len(estudiantes)):
    print(f"{estudiantes[i]:<10} {horas_usadas[i]:<15} S/ {costo_total[i]:.2f}")

# Calcular estadísticas descriptivas del costo_total
n = len(costo_total)
suma = sum(costo_total)
media = suma / n

# Ordenar para percentiles
ordenados = sorted(costo_total)
minimo = ordenados[0]
maximo = ordenados[-1]
mediana = ordenados[n // 2] if n % 2 != 0 else (ordenados[n // 2 - 1] + ordenados[n // 2]) / 2

# Mostrar estadísticas
print("\nEstadísticas de Costo_total")
print(f"Cantidad: {n}")
print(f"Promedio: S/ {media:.2f}")
print(f"Mínimo: S/ {minimo:.2f}")
print(f"Mediana: S/ {mediana:.2f}")
print(f"Máximo: S/ {maximo:.2f}")

# Filtrar estudiantes con costo > 6.00
lista_altos = []
for i in range(n):
    if costo_total[i] > 6.0:
        lista_altos.append(estudiantes[i])

# Imprimir resultados finales
print(f"\nEl gasto promedio por estudiante fue de S/ {media:.2f}.")
print("Estudiantes que gastaron más de S/ 6.00:")
for alumno in lista_altos:
    print(f" - {alumno}")