import pandas as pd

#Estudiante: Panta Piscoche Jose Diego
#Semana 3 05/05/25

#Construcción de diccionario
datos = {'Dias':['Lunes','Martes','Miercoles','Jueves','Viernes'],
 'Gasto':[4.0, 3.5, 5.0, 4.2, 3.8]}

#convertimos el dicionario en dataframe
df = pd.DataFrame(datos)

#calcular el maximo de dias de prestamo
gasto_total  = df['Gasto'].sum()

#Mostrar dataframe completo
print("DataFrame de uso de laboratorio")
print(df)

#calcular gasto medio de la semana
gasto_medio = df['Gasto'].mean()

#Identificar los días en que gastó más que el promedio.
df_mas_medio = df[df['Gasto']>gasto_medio]
lista_dias_gasto = df_mas_medio['Dias'].tolist()

#imprimimos el gasto total y promedio de la semana
print(f"\nEl gasto medio de Ana fue de S/.{gasto_medio:.2f}.")
print(f"El gasto total de Ana a la semana fue de S/.{gasto_total:.2f}.")
#imprimimos el gasto promedio por estudiante como los estudiantes que retuvieron más de 8
print("Dias que Ana gastó más que el promedio:")
for dias in lista_dias_gasto:
 print(f" - {dias}")
