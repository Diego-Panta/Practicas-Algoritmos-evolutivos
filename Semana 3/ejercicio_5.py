import numpy as np

#Estudiante: Panta Piscoche Jose Diego
#Semana 3 05/05/25

# Paquete (GB)
paquetes = np.array([1,2,5,10])

#Una dimensión para los precios
precios = np.array([5.0,9.0,20.0,35.0])

#Costo por GB para cada paquete.
costo_paquete_gb = np.floor(precios/paquetes)

#En cuál medio obtiene la mayor cantidad de viajes sin pasarse del presupuesto
costo_min = int(costo_paquete_gb.min()) #obtenemos el paquete mas economico
indice_min = int(costo_paquete_gb.argmin()) #obtenemos el indice del menor

#Bucle donde imprimiremos cada paquete con sus respectivos precios y costo
for i, paquete in enumerate(paquetes):
    print(f"El paquete {paquete}: precio S/{precios[i]} - tiene costo de S/. {int(costo_paquete_gb[i])} por GB.")

#Imprimimos la mayor cantidad de viajes, el nombre del medio
print(f"\nEl paquete mas economico con precio de (S/.{costo_min}) es del paquete {paquetes[indice_min]} GB.")
