# Estudiante: Panta Piscoche Jose Diego
# Semana 2 30/04/25

# Presupuesto de tipo float
presupuesto = 10.0

# Precios de café en cada cafetería
precios = [2.50, 3.00, 1.75, 2.20]

# Calcular cuántos cafés se pueden comprar en cada cafetería (redondeo hacia abajo sin librerías)
max_cafe = [int(presupuesto // precio) for precio in precios]

# Obtener la mayor cantidad de cafés y su índice
cant_max = max_cafe[0]
indice_max = 0
for i in range(1, len(max_cafe)):
    if max_cafe[i] > cant_max:
        cant_max = max_cafe[i]
        indice_max = i

# Obtener el precio mínimo y su índice
precio_min = precios[0]
indice_min = 0
for i in range(1, len(precios)):
    if precios[i] < precio_min:
        precio_min = precios[i]
        indice_min = i

# Nombres de cafeterías
nombres = ['A', 'B', 'C', 'D']

# Mostrar resultados individuales por cafetería
for i in range(len(nombres)):
    print(f"La cafetería {nombres[i]}: precio S/{precios[i]} - puedo comprar {max_cafe[i]} cafés")

# Imprimir resultados finales
print(f"\nCon S/ {presupuesto:.2f} obtienes la mayor cantidad de cafés ({cant_max}) en la cafetería {nombres[indice_max]}.")
print(f"El precio más bajo es S/ {precio_min:.2f} en la cafetería {nombres[indice_min]}.")