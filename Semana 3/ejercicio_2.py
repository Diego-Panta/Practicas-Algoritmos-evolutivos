import numpy as np

#Estudiante: Panta Piscoche Jose Diego
#Semana 3 05/05/25

#Presupuesto de tipo double
presupuesto = 15.0

#Una dimensión para los precios
precios = np.array([2.50,3.00,1.80])

#Cuántos viajes puede disponer en cada una de los 3 medios con sus S/ 8.
max_viajes = np.floor(presupuesto/precios)

#En cuál medio obtiene la mayor cantidad de viajes sin pasarse del presupuesto
cant_max = int(max_viajes.max()) #obtenemos la mayor cant de viajes
indice_max = int(max_viajes.argmax()) #obtenemos el indice del mayor

# Nombre de medios de transporte
nombres = ['Bus','Combi','Tren']

#Bucle donde imprimiremos cada medio con sus respectivos precios y cant de viajes que puedo comprar
for i, nombre in enumerate(nombres):
    print(f"El medio {nombre}: precio S/{precios[i]} - puedo comprar {int(max_viajes[i])} viajes")

#Imprimimos la mayor cantidad de viajes, el nombre del medio
print(f"\nCon S/ {presupuesto:.2f} obtienes la mayor cantidad de viajes ({cant_max}) en el medio de {nombres[indice_max]}.")
