import pandas as pd

#Estudiante: Panta Piscoche Jose Diego
#Semana 3 05/05/25

#Construcción de diccionario
datos = {'Estudiante': ['Rosa','David','Elena','Mario','Paula'],
         'Dias_prestamo':[7,10,5,12,3]}

#convertimos el dicionario en dataframe
df = pd.DataFrame(datos)

#calcular el maximo de dias de prestamo
max_dias  = df['Dias_prestamo'].max()

#Mostrar dataframe completo
print("DataFrame de uso de laboratorio")
print(df)

#calcular estadisticas descriptiva
stats = df['Dias_prestamo'].describe()
print("\nEstadísticas de Dias de prestamo")
print(stats)

#Filtrar filas
df_mayor_8 = df[df['Dias_prestamo']>8]

#Imprimimos el gasto promedio y la lista de estudiantes  que retuvieron > 8 dias
dias_promedio = stats['mean']
lista_altos = df_mayor_8['Estudiante'].tolist()

#imprimimos el maximo y promedio de dias de prestamo
print(f"\nLos dias promedios por estudiante fue de {dias_promedio:.2f} dias, redondeando a {round(dias_promedio):.2f}.")
print(f"\nEl maximo de dias de prestamo fue de {max_dias:.2f} dias.")
#imprimimos el gasto promedio por estudiante como los estudiantes que retuvieron más de 8
print("Estudiantes que retuvieron más de 8 dias:")
for alumno in lista_altos:
 print(f" - {alumno}")
