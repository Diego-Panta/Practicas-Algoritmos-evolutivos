import numpy as np

#Estudiante: Panta Piscoche Jose Diego
#Semana 2 30/04/25

#Presupuesto de tipo double
presupuesto = 10.0

#Una dimensión para los precios
precios = np.array([2.50,3.00,1.75,2.20])

#Cuántos cafés puede comprar en cada una de las cuatro cafeterías con sus S/ 10.
max_cafe = np.floor(presupuesto/precios)

#En cuál cafetería obtiene la mayor cantidad de cafés sin pasarse del presupuesto
cant_max = int(max_cafe.max()) #obtenemos la mayor cant de cafe
indice_max = int(max_cafe.argmax()) #obtenemos el indice del mayor cafe

#El precio mínimo entre las cuatro cafeterías y el índice (o nombre) de esa cafetería.
precio_min = precios.min() #obtenemos el menor precio de cafe
indice_min = int(precios.argmin()) #obtenemos el indice menor del precio de cafe

# Nombre de cafeterías
nombres = ['A','B','C','D']

#Bucle donde imprimiremos cada cafetería con sus respectivos precios y cant de cafe que puedo comprar
for i, nombre in enumerate(nombres):
    print(f"La cafetería {nombre}: precio S/{precios[i]} - puedo comprar {int(max_cafe[i])} cafes")

#Imprimimos la mayor cantidad de cafe, precio mas bajo y el nombre de la cafetería
print(f"\nCon S/ {presupuesto:.2f} obtienes la mayor cantidad de cafés ({cant_max}) en la cafetería {nombres[indice_max]}.")
print(f"El precio más bajo es S/ {precio_min:.2f} en la cafetería {nombres[indice_min]}.")
