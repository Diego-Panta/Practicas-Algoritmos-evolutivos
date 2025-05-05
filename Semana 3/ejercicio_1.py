import numpy as np

#Estudiante: Panta Piscoche Jose Diego
#Semana 3 05/05/25

#Presupuesto de tipo double
presupuesto = 8.0

#Una dimensión para los precios
precios = np.array([0.10,0.12,0.08])

#Cuántos páginas puede fotocopiar en cada una de las 3 copisterias con sus S/ 8.
max_paginas = np.floor(presupuesto/precios)

#En cuál copisteria obtiene la mayor cantidad de paginas sin pasarse del presupuesto
cant_max = int(max_paginas.max()) #obtenemos la mayor cant de paginas
indice_max = int(max_paginas.argmax()) #obtenemos el indice del mayor

# Nombre de copisterias
nombres = ['A','B','C']

#Bucle donde imprimiremos cada copisteria con sus respectivos precios y cant de paginas que puedo comprar
for i, nombre in enumerate(nombres):
    print(f"La copisteria {nombre}: precio S/{precios[i]} - puedo fotocopiar {int(max_paginas[i])} paginas")

#Imprimimos la mayor cantidad de paginas, el nombre de la copisteria
print(f"\nCon S/ {presupuesto:.2f} obtienes la mayor cantidad de paginas ({cant_max}) en la copisteria {nombres[indice_max]}.")
