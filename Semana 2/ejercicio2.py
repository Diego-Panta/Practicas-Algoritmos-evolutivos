import pandas as pd

#Estudiante: Panta Piscoche Jose Diego
#Semana 2 30/04/25

paga = 2
#Construcción de diccionario
datos = {'Estudiante': ['Ana','Luis','Maria','Juan','Carla'],
         'Horas_usadas':[3,5,2,4,1]}

#convertimos el dicionario en dataframe
df = pd.DataFrame(datos)

df['Costo_total']  = paga*df['Horas_usadas'] 

#Mostrar dataframe completo
print("DataFrame de uso de laboratorio")
print(df)

#calcular estadisticas descriptiva
stats = df['Costo_total'].describe()
print("\nEstadísticas de Costo_total")
print(stats)

#Filtrar filas
df_mayor_6 = df[df['Costo_total']>6.0]

#Imprimimos el gasto promedio y la lista de estudiantes con gasto > S/6.00
gasto_promedio = stats['mean']
lista_altos = df_mayor_6['Estudiante'].tolist()

#imprimimos tanto el gasto promedio por cada estudiante comolos que gastaron más de 6
print(f"\nEl gasto promedio por estudiante fue de S/ {gasto_promedio:.2f}.")
print("Estudiantes que gastaron más de S/ 6.00:")
for alumno in lista_altos:
 print(f" - {alumno}")
