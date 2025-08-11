"""
Modulo para imputar, graficar y analizar las diferentes tecnicas de imputación y con ello definir el DF de entrada de las medidas estadisticas
"""
from graficar import Graficar
from missing import Missingvalues
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import kstest
import seaborn as sns
import numpy as np
# ---------------------------------PASO 1--------------------------------------------------
#-------------------------------EXTRACCIÓN-------------------------------------------------
df_meteo = pd.read_excel("C:/Users/SebastiánAguirre/PycharmProjects/SeriesTiemporTesis/datosmeteo.xlsx")
df_v180 = pd.read_excel("C:/Users/SebastiánAguirre/PycharmProjects/SeriesTiemporTesis/lambda_paso_1_v180.xlsx")
#df_v90 = pd.read_excel("C:/Users/SebastiánAguirre/PycharmProjects/SeriesTiemporTesis/lambda_paso_1_v90.xlsx")
df_meteo['fecha'] = pd.to_datetime(df_meteo['fecha'])
df_v180['fecha'] = pd.to_datetime(df_v180['fecha'])
df_meteo = df_meteo.drop(index=[0,1])
# df_meteo.set_index('Fecha', inplace=True)
# df_v180.set_index('fecha', inplace=True)
# df_v90.set_index('fecha', inplace=True)
#-----------------------------------------------------------------------------------------

#-----------------------------TRANSFORMACIÓN-----------------------------------------------
df180 = pd.merge(df_v180, df_meteo, on='fecha' ,how='right')
#df90 = pd.merge(df_v90, df_meteo, how='outer', left_index=True, right_index = True)
df180.set_index('fecha', inplace=True)
# print(df180.iloc[1290:1300,:])
# print(len(df180))
# df180 = df180.drop(columns=['lambda_d_urbano_1','lambda_urbano_1'])
# df90 = df90.drop(columns=['lambda_d_urbano_1','lambda_urbano_1'])
indiceinicial = df180.index[1220] #EN JULIO DE 2022 HACEN FALTA UNOS DÍAS EN LA TASA DE FALLAS, POR TAL MOTIVO SE REALIZA EL CALCULO DE VALORES FALTANTES EN ESTOS DIAS PARA PROSEGUIR CON DROPNA Y ELIMINAR LOS DATOS ANTERIORES AL DIA INICIAL SEGUN LA VENATANA SELECCIONADA
indicefinal = df180.index[1370]
nulls_df180 = Missingvalues(df180.loc[indiceinicial:indicefinal,:])
df180_mean_imp, df180_fbf_imp, df180_lin_imp, df180_knn_imp, df180_mice_imp = nulls_df180.set()
df180.loc[indiceinicial:indicefinal,:] = df180_mice_imp
df180= df180.dropna(subset=['lambda_bavaria_1']) #SE ELIMINA LOS VALORES NULOS DE DF180 QUE CONTIENE LA VARIABLE X
#df90= df90.dropna(subset=['lambda_sur_1'])
copia_df180 = df180.copy()
#-----------------------------COMENTAR - SE GRAFICA EL % DE NULLS DE VARIABLES METEO EN LA TESIS--------------------------------

nulls_final = Missingvalues(df180)
porcentage_final = nulls_final.howmany(df180)
no_null = [100-nulls for nulls in porcentage_final]
#print("Porcentage valores faltantes antes de tratamiento:")
#print(porcentage_final)
porcentage_final = porcentage_final[10:]
no_null = no_null[10:]
# Crear un DataFrame
df = pd.DataFrame(porcentage_final)
data = {
    'Company': df180.iloc[:, 10:].columns.tolist(),
    'Nulos': porcentage_final,
    'No Nulos': no_null
}
# Crear DataFrame
df = pd.DataFrame(data)
## Posición de las barras
#bar_width = 0.2
#index = np.arange(len(df['Company']))
## Configuración del gráfico
#plt.figure(figsize=(14, 10))
## Barras
#plt.bar(index, df['No Nulos'], bar_width, label='No Nulos', color='lightskyblue', edgecolor='black')   #--------------------------------------------------------------------------------------------------------------------------------
#plt.bar(index + bar_width, df['Nulos'], bar_width, label='Nulos', color='lightcoral', edgecolor='black')
## Títulos y etiquetas
#plt.title('Valores Faltantes y No Faltantes')
#plt.xlabel('Parámetros Climáticos')
#plt.ylabel('Porcentaje (%)')
#plt.xticks(index + bar_width / 2, df['Company'], rotation=90)
#plt.legend()
## Mostrar gráfico
#plt.tight_layout()
##plt.savefig("valoresfaltantesv3.png") #----------------------SE GRAFICA EL % DE NULLS DE VARIABLES METEO EN LA TESIS----------------------------------------------------------------------------------------------------------------


#--------------------------------EDA-------------------------------------------------------
#-------------------------LIMPIEZA DE DATOS------------------------------------------------
#-------------------------VALORES FALTANTES------------------------------------------------
#En las siguientes líneas se desarrollara ciertas graficas indispensable para el análisis, sin embargo,
#cuando se finalice el análisis, estás líneas serán comentadas para evitar su ejecución
#----------------------------------df180---------------------------------------------------

#ANALISIS 1/5 DE LOS DATOS
indiceinicial = df180.index[0]
indicefinal = df180.index[303]
# grafica1 = Graficar(df180[['VVMXAG_CON@21115020']].loc[indiceinicial:indicefinal,:].index, df180[['VVMXAG_CON@21115020']].loc[indiceinicial:indicefinal,:])
# grafica1.scatter(num_figure=1, num_plots_figure=1)
# plt.show()
nulls_df180 = Missingvalues(df180.loc[indiceinicial:indicefinal,:])
porcentage_nulls = nulls_df180.howmany(df180.loc[indiceinicial:indicefinal,:]) #Cuantos valores faltantes existen
#print(porcentage_nulls) #SE DEBE COMENTAR
df180_mean_imp, df180_fbf_imp, df180_lin_imp, df180_knn_imp, df180_mice_imp = nulls_df180.set()
#Se gráfica y se analiza cual técnica respeta en mayor porcentaje la distribución original de los datos. Además, se tiene en cuenta las pruebas de hipotesis de comparación de distribuciones
#-------------------------SE COMENTAN DESPUES DEL ANALISIS PARA NO SATURAR-----------------------------
#df180_knn_imp.hist()
# df180.loc[indiceinicial:indicefinal,:].hist()
# df180_mice_imp.hist()
# grafica1 = Graficar(df180_lin_imp[['VVMXAG_CON@21115020']].index, df180_lin_imp[['VVMXAG_CON@21115020']])
# grafica1.scatter(num_figure=1, num_plots_figure=1)
#plt.show()
# SE IMPUTA LOS VALORES DE LA TECNICA SELECCIONADA
df180.loc[indiceinicial:indicefinal,:] = df180_knn_imp


#ANALISIS 2/5 DE LOS DATOS
indiceinicial = df180.index[303]
indicefinal = df180.index[606]


nulls_df180 = Missingvalues(df180.loc[indiceinicial:indicefinal,:])
porcentage_nulls = nulls_df180.howmany(df180.loc[indiceinicial:indicefinal,:]) #Cuantos valores faltantes existen
#print(porcentage_nulls) #SE DEBE COMENTAR
df180_mean_imp, df180_fbf_imp, df180_lin_imp, df180_knn_imp, df180_mice_imp = nulls_df180.set()
#Se gráfica y se analiza cual técnica respeta en mayor porcentaje la distribución original de los datos. Además, se tiene en cuenta las pruebas de hipotesis de comparación de distribuciones
#-------------------------SE COMENTAN DESPUES DEL ANALISIS PARA NO SATURAR-----------------------------
# df180.loc[indiceinicial:indicefinal,:].hist()
# df180_knn_imp.hist()
# df180_mice_imp.hist()
# grafica1 = Graficar(df180[['VVMXAG_CON@21115020']].loc[indiceinicial:indicefinal,:].index, df180[['VVMXAG_CON@21115020']].loc[indiceinicial:indicefinal,:]) #SE DEBE COMENTAR
# grafica1.scatter(num_figure=1, num_plots_figure=1)
# grafica2 = Graficar(df180_knn_imp[['VVMXAG_CON@21115020']].index, df180_knn_imp[['VVMXAG_CON@21115020']])
# grafica2.scatter(num_figure=1, num_plots_figure=1)
# grafica3 = Graficar(df180_mice_imp[['VVMXAG_CON@21115020']].index, df180_mice_imp[['VVMXAG_CON@21115020']])
# grafica3.scatter(num_figure=1, num_plots_figure=1)
# plt.show()
# SE IMPUTA LOS VALORES DE LA TECNICA SELECCIONADA
#df180.loc[indiceinicial:indicefinal,:] = df180_knn_imp


#ANALISIS 3/5 DE LOS DATOS
indiceinicial = df180.index[606]
indicefinal = df180.index[909]

nulls_df180 = Missingvalues(df180.loc[indiceinicial:indicefinal,:])
porcentage_nulls = nulls_df180.howmany(df180.loc[indiceinicial:indicefinal,:]) #Cuantos valores faltantes existen

df180_mean_imp, df180_fbf_imp, df180_lin_imp, df180_knn_imp, df180_mice_imp = nulls_df180.set()
#Se gráfica y se analiza cual técnica respeta en mayor porcentaje la distribución original de los datos. Además, se tiene en cuenta las pruebas de hipotesis de comparación de distribuciones
#-------------------------SE COMENTAN DESPUES DEL ANALISIS PARA NO SATURAR-----------------------------
# df180.loc[indiceinicial:indicefinal,:].hist()
# df180_knn_imp.hist()
# df180_mice_imp.hist()
# grafica1 = Graficar(df180[['VVMXAG_CON@21115020']].loc[indiceinicial:indicefinal,:].index, df180[['VVMXAG_CON@21115020']].loc[indiceinicial:indicefinal,:]) #SE DEBE COMENTAR
# grafica1.scatter(num_figure=1, num_plots_figure=1)
# grafica2 = Graficar(df180_knn_imp[['VVMXAG_CON@21115020']].index, df180_knn_imp[['VVMXAG_CON@21115020']])
# grafica2.scatter(num_figure=1, num_plots_figure=1)
# grafica3 = Graficar(df180_mice_imp[['VVMXAG_CON@21115020']].index, df180_mice_imp[['VVMXAG_CON@21115020']])
# grafica3.scatter(num_figure=1, num_plots_figure=1)
# plt.show()
# SE IMPUTA LOS VALORES DE LA TECNICA SELECCIONADA
df180.loc[indiceinicial:indicefinal,:] = df180_mice_imp
# df180.hist() #SE COMENTA
# plt.show()

#ANALISIS 4/5 DE LOS DATOS
indiceinicial = df180.index[909]
indicefinal = df180.index[1212]


nulls_df180 = Missingvalues(df180.loc[indiceinicial:indicefinal,:])
porcentage_nulls = nulls_df180.howmany(df180.loc[indiceinicial:indicefinal,:]) #Cuantos valores faltantes existen
df180_mean_imp, df180_fbf_imp, df180_lin_imp, df180_knn_imp, df180_mice_imp = nulls_df180.set()
#Se gráfica y se analiza cual técnica respeta en mayor porcentaje la distribución original de los datos. Además, se tiene en cuenta las pruebas de hipotesis de comparación de distribuciones
#-------------------------SE COMENTAN DESPUES DEL ANALISIS PARA NO SATURAR-----------------------------
# df180.loc[indiceinicial:indicefinal,:].hist()
# df180_knn_imp.hist()
# df180_mice_imp.hist()
# grafica1 = Graficar(df180[['VV_10_MEDIA_D@21115170']].loc[indiceinicial:indicefinal,:].index, df180[['VV_10_MEDIA_D@21115170']].loc[indiceinicial:indicefinal,:]) #SE DEBE COMENTAR
# grafica1.scatter(num_figure=1, num_plots_figure=1)
# grafica2 = Graficar(df180_knn_imp[['VV_10_MEDIA_D@21115170']].index, df180_knn_imp[['VV_10_MEDIA_D@21115170']])
# grafica2.scatter(num_figure=1, num_plots_figure=1)
# grafica3 = Graficar(df180_mice_imp[['VV_10_MEDIA_D@21115170']].index, df180_mice_imp[['VV_10_MEDIA_D@21115170']])
# grafica3.scatter(num_figure=1, num_plots_figure=1)
# plt.show()
# SE IMPUTA LOS VALORES DE LA TECNICA SELECCIONADA
df180.loc[indiceinicial:indicefinal,:] = df180_mice_imp
# df180.hist()
# plt.show()


#ANALISIS 5/5 DE LOS DATOS
indiceinicial = df180.index[1212]
#indicefinal = df180.index[1212]


nulls_df180 = Missingvalues(df180.loc[indiceinicial:,:])
porcentage_nulls = nulls_df180.howmany(df180.loc[indiceinicial:,:]) #Cuantos valores faltantes existen
df180_mean_imp, df180_fbf_imp, df180_lin_imp, df180_knn_imp, df180_mice_imp = nulls_df180.set()

#Se gráfica y se analiza cual técnica respeta en mayor porcentaje la distribución original de los datos. Además, se tiene en cuenta las pruebas de hipotesis de comparación de distribuciones
#-------------------------SE COMENTAN DESPUES DEL ANALISIS PARA NO SATURAR-----------------------------
# df180.loc[indiceinicial:,:].hist()
# df180_knn_imp.hist()
# df180_mice_imp.hist()
# grafica1 = Graficar(df180[['VV_10_MEDIA_D@21115170']].loc[indiceinicial:,:].index, df180[['VV_10_MEDIA_D@21115170']].loc[indiceinicial:,:]) #SE DEBE COMENTAR
# grafica1.scatter(num_figure=1, num_plots_figure=1)
# correlation_matrix1 = df180.loc[indiceinicial:,:].corr()
# grafica1.correlacion(correlation_matrix1)
# grafica2 = Graficar(df180_knn_imp[['VV_10_MEDIA_D@21115170']].index, df180_knn_imp[['VV_10_MEDIA_D@21115170']])
# grafica2.scatter(num_figure=1, num_plots_figure=1)
# correlation_matrix2 = df180_knn_imp.corr()
# grafica2.correlacion(correlation_matrix2)
# grafica3 = Graficar(df180_mice_imp[['VV_10_MEDIA_D@21115170']].index, df180_mice_imp[['VV_10_MEDIA_D@21115170']])
# grafica3.scatter(num_figure=1, num_plots_figure=1)
# correlation_matrix3 = df180_mice_imp.corr()
# grafica3.correlacion(correlation_matrix3)
#plt.show()
# SE IMPUTA LOS VALORES DE LA TECNICA SELECCIONADA
df180.loc[indiceinicial:,:] = df180_mice_imp
# grafica1 = Graficar(df180[['VV_10_MEDIA_D@21115170']].index, df180[['VV_10_MEDIA_D@21115170']]) #SE DEBE COMENTAR
# grafica1.scatter(num_figure=1, num_plots_figure=1)
# df180.hist()
# plt.show()



# EN EL INTERVALO 2/5 SE OBSERVA QUE LAQ PENULTIMA VARIABLE PRESENTA 99% DE VALORES FALTANTES, POR LO TANTO, SE DECIDE IMPUTAR EL RESTO DE INTERVALOS
# Y AL FINAL REALIZAR EL ALGORITMO MICE EN TODO EL CONJUNTO PARA PREDECIR DICHO INTERVALO CON MAYOR PROYECCION
#ANALISIS RESTANTES DE LOS DATOS

nulls_df180 = Missingvalues(df180)
porcentage_nulls = nulls_df180.howmany(df180) #Cuantos valores faltantes existen
df180_mean_imp, df180_fbf_imp, df180_lin_imp, df180_knn_imp, df180_mice_imp = nulls_df180.set()

#Se gráfica y se analiza cual técnica respeta en mayor porcentaje la distribución original de los datos. Además, se tiene en cuenta las pruebas de hipotesis de comparación de distribuciones
#-------------------------SE COMENTAN DESPUES DEL ANALISIS PARA NO SATURAR-----------------------------
# df180.hist()
# df180_knn_imp.hist()
# df180_mice_imp.hist()
# grafica1 = Graficar(df180[['VV_10_MEDIA_D@21115170']].index, df180[['VV_10_MEDIA_D@21115170']]) #SE DEBE COMENTAR
# grafica1.scatter(num_figure=1, num_plots_figure=1)
# correlation_matrix1 = df180.corr()
# grafica1.correlacion(correlation_matrix1)
# grafica2 = Graficar(df180_knn_imp[['VV_10_MEDIA_D@21115170']].index, df180_knn_imp[['VV_10_MEDIA_D@21115170']])
# grafica2.scatter(num_figure=1, num_plots_figure=1)
# correlation_matrix2 = df180_knn_imp.corr()
# grafica2.correlacion(correlation_matrix2)
# grafica3 = Graficar(df180_mice_imp[['VV_10_MEDIA_D@21115170']].index, df180_mice_imp[['VV_10_MEDIA_D@21115170']])
# grafica3.scatter(num_figure=1, num_plots_figure=1)
# correlation_matrix3 = df180_mice_imp.corr()
# grafica3.correlacion(correlation_matrix3)
# plt.show()
# SE IMPUTA LOS VALORES DE LA TECNICA SELECCIONADA
df180 = df180_mice_imp  #--------------------BASE DE DATOS FINALLLLL-------------------------------
# grafica1 = Graficar(df180[['VV_10_MEDIA_D@21115170']].index, df180[['VV_10_MEDIA_D@21115170']]) #SE DEBE COMENTAR
# grafica1.scatter(num_figure=1, num_plots_figure=1)
#df180.hist()
#plt.show()

#SE VERIFICA EL NUMNERO DE FALTANTES FINALES -  DEBERIAN SER 0
nulls_final = Missingvalues(df180)
porcentage_final = nulls_final.howmany(df180)
#print("Porcentage valores faltantes despues de tratamiento:")
#print(porcentage_final)
#plt.savefig("figura_300dpi.png")
#SE REALIZA UNA PRUEBA PARA VERIFICAR LA SIMILITUD DE LA DISTRIBUCIÓN FINAL CON LA DISTRIBUCIÓN ORIGINAL
original_df180_flat = copia_df180['VVMXAG_CON@21115020'].dropna().values.flatten()

# Eliminar filas con NaNs en el DataFrame original para la comparación
final_flat = df180['VVMXAG_CON@21115020'].values.flatten()
# Se calcula el KS test comparando cada método con el DataFrame original
ks_tests = {
    "f_fill": kstest(original_df180_flat, final_flat),
            }
#SE ELIMINA LAS COLUMNAS QUE NO SE VAN A UTILIZAR EN EL ANALISIS

df180 = df180.drop(columns=['lambda_d_termales_1','lambda_d_bavaria_1','lambda_d_granjas_1','lambda_mtto_granjas_d','lambda_mtto_bavaria_d','lambda_mtto_granjas_d.1'])
df180.to_excel('df180.xlsx')
#---------------------------------------------ANALISIS DE VARIABLES REDUNDANTES----------------------------------------------------
from sklearn.preprocessing import StandardScaler
variables = df180.iloc[:,:] #[:,6:]
print(variables.columns)
scaler = StandardScaler()
variables_estandarizadas = scaler.fit_transform(variables)
variables_estandarizadas_df = pd.DataFrame(variables_estandarizadas, columns=variables.columns)
cov_matrix_estandarizadas = variables_estandarizadas_df.cov()
eigenvalues, eigenvectors = np.linalg.eig(cov_matrix_estandarizadas)
if __name__ == "__main__":

    ##-----------SE COMENTA DESDE AQUI PARA NO VER TODOS LOS GRAFICOS PLOTTING---------------------------
    import seaborn as sns
    plt.figure(figsize=(8, 6))
    sns.heatmap(cov_matrix_estandarizadas, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Matriz de Covarianzas estandarizada")
    ##-----------SE COMENTA HASTA AQUI PARA NO VER TODOS LOS GRAFICOS PLOTTING---------------------------

    ##-----------SE COMENTA DESDE AQUI PARA NO VER TODOS LOS GRAFICOS PLOTTING---------------------------
    #Escoge un valor propio específico (por ejemplo, el primero)
    plt.figure(figsize=(8, 6))
    idx = 7
    valor_propio = eigenvalues[idx]
    vector_propio = eigenvectors[:, idx]
    # Crear un gráfico de los valores del vector propio
    plt.plot(vector_propio, marker='o', linestyle='-', color='b')
    # Etiquetas y título
    plt.title(f'Valores del Vector Propio Asociado al Valor Propio: {valor_propio:.2f}')
    plt.xlabel('Variable')
    plt.ylabel('Valor')
    # Mostrar el gráfico
    plt.grid(True)
    plt.savefig("vectorpropiov1.png")
    plt.figure(figsize=(10, 7))
    plt.bar(range(len(eigenvalues)), eigenvalues, color='#87CEEB', edgecolor='black')  # Azul rey mate con borde negro
    # Añadir etiquetas a cada barra para mostrar el valor de cada eigenvalue
    for i, val in enumerate(eigenvalues):
        plt.text(i, val + 0.05, f'{val:.2f}', ha='center', fontsize=12)
    # Mejorar el diseño
    plt.title("Valores Propios - (Eigenvalues)", fontsize=16, fontweight='bold')
    plt.xlabel("Componente", fontsize=14)
    plt.ylabel("Valor Propio", fontsize=14)
    plt.grid(axis='y', linestyle='--', alpha=0.7)  # Grilla sutil solo en el eje
    # Mostrar el gráfico
    plt.tight_layout()
    plt.savefig("valorespropiosv1.png")

    plt.figure(figsize=(8, 6))
    sns.heatmap(eigenvectors, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Matriz de vectores propios")

    plt.show()
    #df180 = df180.drop('PT_10_TT_D@21097070', axis=1)

    ##-----------SE COMENTA HASTA AQUI PARA NO VER TODOS LOS GRAFICOS PLOTTING---------------------------

# Imprime los resultados del KS test
# for method, ks_result in ks_tests.items():
#     print(f"{method}: KS test statistic = {ks_result.statistic}, p-value = {ks_result.pvalue}")

# SE DEBE VERIFICAR QUE NO SE IMPUTEN VALORES NEGATIVOS DEBIDO A LA NATURALEZA DE LOS DATOS




#sns.pairplot(df90_mice_imp.iloc[:,8:])

# df90.hist(edgecolor='black')
# df90_mice_imp.hist(edgecolor='red')
#
# correlation_matrix1 = df90_mice_imp.corr()
# grafica1 = Graficar(df90_mice_imp.index, df90_mice_imp)
# grafica1.correlacion(correlation_matrix1)
# plt.show()
# correlation_matrix2 = df90.corr()
# grafica2 = Graficar(df90_mice_imp.index, df90_mice_imp)
# grafica2.correlacion(correlation_matrix2)
#
#
# correlation_matrix3 = df90_knn_imp.corr()
# grafica3 = Graficar(df90_mice_imp.index, df90_mice_imp)
# grafica3.correlacion(correlation_matrix3)
# plt.show()
#     #Inicializamos el objeto
#grafica1 = Graficar(df[['Fecha']], df.iloc[:,1:]) # Si se desea graficar 2 variables en una figura se debe pasar un df con variable 1 en la posicion 0 y variable 2 en posicion 1 del df
#     #se grafica un scatter
#grafica1.scatter(num_figure=1, num_plots_figure=2, figsizex=20,figsizey=15)




# correlation_matrix1 = df180.corr()
# valores_faltantes = Missingvalues(df180)
# vf = valores_faltantes.howmany()
# a = valores_faltantes.set()
# correlation_matrix2 = a.corr()
# print(vf)
# b = valores_faltantes.howmany()
# print(b)
#
# df180 = df180.drop(df180.index[:180])
# df180 = df180.drop(df180.index[1524:])
#
# a = a.drop(a.index[:180])
# a = a.drop(a.index[1524:])
#
# # grafica1 = Graficar(df180.index, df180.iloc[:,16:20])
# # grafica1.scatter(num_figure=3, num_plots_figure=1, figsizex=15,figsizey=15)
# # grafica1.correlacion(correlation_matrix1)
# grafica2 = Graficar(a.index, a.iloc[:,16:20])
# grafica2.scatter(num_figure=3, num_plots_figure=1, figsizex=15,figsizey=15)
# grafica2.histcatter(df180[['PTPM_CON@21110400']], df180[['VVMXAG_CON@21115020']])
# grafica2.correlacion(correlation_matrix2)
#
# df180.hist()
#
# plt.show()






