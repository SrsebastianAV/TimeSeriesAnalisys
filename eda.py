"""


#SE OBTIENE LA BASE DE DATOS SIN VALORES FALTANTES
"""
import pandas as pd

from data180 import df180 #SE OBTIENE LA BASE DE DATOS SIN VALORES FALTANTES
from medidas import Medidas
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime, timedelta
#SE OBSERVA LA DISTRIBUCION DE LOS DATOS CON UN HISTOGRAMA
# df180.hist(bins=25)
#SE OBTIENEN LAS MEDIDAS NECESARIAS PARA
medidas1 = Medidas(df180)
medidas1.descriptive()
from statsmodels.tsa.seasonal import STL
# from statsmodels.tsa.seasonal import seasonal_decompose
# descomposition = seasonal_decompose(df180['lambda_mtto_norte_f'], model='multiplicative')
# descomposition.plot()
# decomposition = STL(df180['lambda_mtto_norte_f'], period=182, robust=True, seasonal=13).fit() #Decompose the series using the STL function. The period is equal to
#                                                                       #the frequency m. Since we have monthly data, the period is 12.
#
# fig, (ax1, ax2, ax3, ax4) = plt.subplots(nrows=4, ncols=1, sharex=True, figsize=(10,8))
#
# ax1.plot(decomposition.observed)
# ax1.set_ylabel('Observed')
#
# ax2.plot(decomposition.trend)
# ax2.set_ylabel('Trend')
#
# ax3.plot(decomposition.seasonal)
# ax3.set_ylabel('Seasonal')
#
# ax4.plot(decomposition.resid)
# ax4.set_ylabel('Residuals')
# #plt.xticks(np.arange(0, 145, 12), np.arange(1949, 1962, 1))
# fig.autofmt_xdate()
# plt.tight_layout()

#plt.savefig('figures/CH08_F04_peixeiro.png', dpi=300)


#GRACIAS AL ANALISIS, SE OBSERVA QUE LAS ULTIMAS DOS VARIABLES PRESENTAN ATIPICOS QUE NO SE DESEAN EN EL ANALISIS, POR LO TANTO SE REALIZA SU TRATAMIENTO
#SE CREA UNA FUNCION EN MEDIDAS PARA TRATAR LAS VARIABLES QUE SE ESPECIFIQUEN, YA QUE NO SE DESEA TRATAR TODAS LAS VARIABLES DEBIDO A SU NATURALEZA
variables_con_atipicos = ['lambda_granjas_1','VVMXAG_CON@21115020']
df180 = medidas1.outlier(variables_con_atipicos)

fig, axes = plt.subplots(2, figsize=(25, 10))
SIZE_DEFAULT = 20
SIZE_LARGE = 20
plt.rc("font", weight="normal")  # controls default font
plt.rc("font", size=SIZE_DEFAULT)  # controls default text sizes
plt.rc("xtick", labelsize=SIZE_DEFAULT)  # fontsize of the tick labels
plt.rc("ytick", labelsize=SIZE_DEFAULT)
variables_a_graficar = ['lambda_termales_1','lambda_bavaria_1', 'lambda_granjas_1']
colors = ["#8D99AE", "#EF233C","blue"] #"#2B2F42",
for variable, color in zip(variables_a_graficar, colors):
    axes[0].plot(df180[['lambda_granjas_1']].index,df180[[variable]], label=variable, color = color)
    axes[0].text(
        df180['lambda_granjas_1'].index[-1]+ timedelta(days=1),
        df180[variable].iloc[-1],
        variable,
        color=color,
        fontweight="bold",
        horizontalalignment="left",
        verticalalignment="center",
    )

axes[0].spines["right"].set_visible(False)
axes[0].spines["top"].set_visible(False)

axes[0].tick_params(axis='both', which='major', labelsize=18)
axes[0].set_title("Tasas de Fallas", fontsize=24)
axes[0].set_ylabel("Tasa de Fallas (Fallas/Día)", fontsize=21)
axes[0].set_xlabel("Fecha", fontsize=21)
variables_a_graficar = ['lambda_mtto_termal_f','lambda_mtto_bavaria_f', 'lambda_mtto_granjas_f']
colors = ["#8D99AE", "#EF233C","blue"]
for variable, color in zip(variables_a_graficar, colors):
    axes[1].plot(df180[['lambda_granjas_1']].index,df180[[variable]], label=variable, color = color)
    axes[1].text(
        df180['lambda_granjas_1'].index[-1]+ timedelta(days=1),
        df180[variable].iloc[-1],
        variable,
        color=color,
        fontweight="bold",
        horizontalalignment="left",
        verticalalignment="center",
    )

axes[1].spines["right"].set_visible(False)
axes[1].spines["top"].set_visible(False)

axes[1].tick_params(axis='both', which='major', labelsize=18)
axes[1].set_title("Tasas de Fallas Mantenimiento", fontsize=24)
axes[1].set_ylabel("Tasa de Fallas (Fallas/Día)", fontsize=21)
axes[1].set_xlabel("Fecha", fontsize=21)
plt.subplots_adjust(hspace=0.5)
plt.savefig("tasadefallasv1.png", dpi=300, bbox_inches='tight')#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



medidas2 = Medidas(df180)
medidas2.descriptive()
#---------SE GRAFICA LAS TASAS DE FALLAS POR MES EN EL PERIODO DE ESTUDIO-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
variable = 'PTPM_CON@21115020'
copy_df180 = df180.copy()
copy_df180['Mes'] = copy_df180.index.month #CREO UNA COLUMNA CON EL NUMERO DEL MES DE LA FECHA              #sumas = copy_df180['PTPM_CON@21115020'].resample('M').sum().reset_index()
mean_per_month = copy_df180.groupby('Mes')[[variable]].mean() #AGRUPAMOS POR LA VARIABLE MES CREADA ANTERIORMENTE LA VARIABLE PTPM Y CALCULAMOS LA MEDIA POR MES
mean_per_month_tf2 = copy_df180.groupby('Mes')[['lambda_granjas_1']].mean()
mean_per_month_tf3 = copy_df180.groupby('Mes')[['lambda_bavaria_1']].mean()
mean_per_month_tf4 = copy_df180.groupby('Mes')[['lambda_termales_1']].mean()
mean_per_month.index = ['Ene','Feb', 'Mar', 'Abr','May' , 'Jun', 'Jul','Agos','Sept', 'Oct', 'Nov','Dic']

mean_per_month_tf2.index = ['Ene','Feb', 'Mar', 'Abr','May' , 'Jun', 'Jul','Agos','Sept', 'Oct', 'Nov','Dic']
mean_per_month_tf3.index = ['Ene','Feb', 'Mar', 'Abr','May' , 'Jun', 'Jul','Agos','Sept', 'Oct', 'Nov','Dic']
mean_per_month_tf4.index = ['Ene','Feb', 'Mar', 'Abr','May' , 'Jun', 'Jul','Agos','Sept', 'Oct', 'Nov','Dic']


# fig, axes = plt.subplots(1, 4, figsize=(20, 10))
# Primer heatmap
# sns.heatmap(mean_per_month_tf4, annot=True, linewidths=0.5, linecolor='gray', annot_kws={"size": 12}, cmap="Blues", ax=axes[0])
# axes[0].set_title("lambda_norte Promedio Por Mes", fontsize=16)
# axes[0].set_ylabel("Mes", fontsize=12)
# axes[0].set_xlabel("(mm)", fontsize=12)
#
# # Segundo heatmap
# sns.heatmap(mean_per_month_tf2, annot=True, linewidths=0.5, linecolor='gray', annot_kws={"size": 12}, cmap="Blues", ax=axes[1])
# axes[1].set_title("lambda_sur Promedio Por Mes", fontsize=16)
# axes[1].set_ylabel("Mes", fontsize=12)
# axes[1].set_xlabel("(mm)", fontsize=12)
#
# sns.heatmap(mean_per_month_tf3, annot=True, linewidths=0.5, linecolor='gray', annot_kws={"size": 12}, cmap="Blues", ax=axes[2])
# axes[2].set_title("lambda_riv Promedio Por Mes", fontsize=16)
# axes[2].set_ylabel("Mes", fontsize=12)
# axes[2].set_xlabel("(mm)", fontsize=12)



plt.savefig("tasadefallaspormesv1.png") #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------SE GRAFICA LAS LLUVIAS POR MES EN EL PERIODO DE ESTUDIO-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
plt.figure(figsize=(20,10))
sns.heatmap(mean_per_month.T,annot=True, linewidths=0.5, linecolor='gray', annot_kws={"size": 12}, cmap="Blues")
plt.title("Precipitaciones Por Mes", fontsize=24)
plt.xlabel("Mes del año", fontsize=21)
plt.ylabel("Día pluviométrico estación AEROPUERTO (mm)", fontsize=18)
plt.savefig("precipitacionespormesv1.png")

#------- SE GRAFICA POR AÑO LA VARIABLE I --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

v2019 = df180[variable].loc['2019-01-01' : '2019-12-31']
v2020 = df180[variable].loc['2020-01-01' : '2020-12-31']
v2021 = df180[variable].loc['2021-01-01' : '2021-12-31']
v2022 = df180[variable].loc['2022-01-01' : '2022-12-31']
v2023 = df180[variable].loc['2023-01-01' : '2023-12-31']

t2019 = range(181,181+len(v2019))
t2020 = range(1,len(v2020)+1)
t2021 = range(1,len(v2021)+1)
t2022 = range(1,len(v2022)+1)
t2023 = range(1,len(v2023)+1)

plt.figure(figsize=(20,10))
plt.scatter(t2019,v2019, color="yellow", linewidth=2, linestyle="-", label="2019", alpha=0.5, marker='+')
plt.scatter(t2020,v2020, color="blue", linewidth=1, linestyle="-", label="2020", alpha=0.5, marker='^')
plt.scatter(t2021,v2021, color="m", linewidth=1, linestyle="-", label="2021", alpha=0.5, marker='s')
plt.scatter(t2022,v2022,color="deepskyblue", linewidth=1, linestyle="-", label="2022", alpha=0.5, marker='o')
plt.scatter(t2023,v2023,color="lawngreen", linewidth=1, linestyle="-", label="2023", alpha=0.5, marker='*')

plt.axvline(45,color="black",linewidth = 1, linestyle = "dashed")
plt.axvline(135,color="black",linewidth = 1, linestyle = "dashed")
plt.axvline(274,color="black",linewidth = 1, linestyle = "dashed")

plt.annotate("Lluvias Frecuentes ", (320, 100), fontsize=13)
plt.annotate("Sequía", (200, 100), fontsize=13)
plt.annotate("Lluvias Intermitentes", (70, 100), fontsize=13)
plt.annotate("Sequía Transitoria", (-1, 100), fontsize=13)

plt.legend(fontsize=13)
plt.title('Precipitaciones por año', fontsize=24)
plt.xlabel('Día del año', fontsize=21)
plt.ylabel(f'Día pluviométrico estación AEROPUERTO (mm)', fontsize=18)
plt.savefig("precipitacionesporañov1.png")

fig, axes = plt.subplots(2, 3, figsize=(18, 12))  # -----------------------------------------------------------------------------------------------------HISTOGRAMA LAMBDA

# Aplanar el array de ejes para iterar fácilmente
axes = axes.flatten()
colors = ["#8D99AE", "#EF233C","#8D99AE", "#EF233C","blue","blue", 'lightcoral', 'lightblue', 'lightpink']

# Iterar sobre las primeras seis columnas y los ejes para crear los histogramas
for i, ax in enumerate(axes):
    df180.iloc[:, i].hist(bins=25, ax=ax, color=colors[i])
    ax.set_ylabel('Frecuencia', fontsize=12)  # Tamaño de la fuente ajustado
    ax.set_title(df180.columns[i], fontsize=14)  # Tamaño de la fuente ajustado
    ax.tick_params(axis='x', labelsize=10)
    ax.tick_params(axis='y', labelsize=10)
# Ajustar el espacio entre los subplots
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.subplots_adjust(hspace=0.3, wspace=0.3)
plt.savefig("histlambdav1.png")

#--------------------------------------------------------------------------------------------------------------------------------LAMBDA POR AÑO
variable ='lambda_granjas_1'
v2019 = df180[variable].loc['2019-01-01' : '2019-12-31']
v2020 = df180[variable].loc['2020-01-01' : '2020-12-31']
v2021 = df180[variable].loc['2021-01-01' : '2021-12-31']
v2022 = df180[variable].loc['2022-01-01' : '2022-12-31']
v2023 = df180[variable].loc['2023-01-01' : '2023-12-31']

t2019 = range(181,181+len(v2019))
t2020 = range(1,len(v2020)+1)
t2021 = range(1,len(v2021)+1)
t2022 = range(1,len(v2022)+1)
t2023 = range(1,len(v2023)+1)

fig, axes = plt.subplots(2, figsize=(20, 10))

SIZE_DEFAULT = 20
SIZE_LARGE = 20
plt.rc("font", weight="normal")  # controls default font
plt.rc("font", size=SIZE_DEFAULT)  # controls default text sizes
plt.rc("xtick", labelsize=SIZE_DEFAULT)  # fontsize of the tick labels
plt.rc("ytick", labelsize=SIZE_DEFAULT)

axes[0].plot(t2019,v2019, color="teal", linewidth=1.3, linestyle="-", label="2019", alpha=0.5)
axes[0].plot(t2020,v2020, color="blue", linewidth=1, linestyle="-", label="2020", alpha=0.5)
axes[0].plot(t2021,v2021, color="purple", linewidth=1, linestyle="-", label="2021", alpha=0.5)
axes[0].plot(t2022,v2022,color="red", linewidth=1, linestyle="-", label="2022", alpha=0.5)
axes[0].plot(t2023,v2023,color="black", linewidth=1, linestyle="-", label="2023", alpha=0.5)

axes[0].spines["right"].set_visible(False)
axes[0].spines["top"].set_visible(False)

axes[0].axvline(45,color="black",linewidth = 1, linestyle = "dashed")
axes[0].axvline(135,color="black",linewidth = 1, linestyle = "dashed")
axes[0].axvline(274,color="black",linewidth = 1, linestyle = "dashed")

axes[0].annotate("Lluvias Frecuentes ", (320, 0.061), fontsize=13)
axes[0].annotate("Sequía", (200, 0.061), fontsize=13)
axes[0].annotate("Lluvias Intermitentes", (70, 0.061), fontsize=13)
axes[0].annotate("Sequía Transitoria", (-1, 0.061), fontsize=13)

axes[0].tick_params(axis='both', which='major', labelsize=18)
axes[0].legend(loc='lower right', fontsize=12)
axes[0].set_title(f'{variable} por año', fontsize=24)
axes[0].set_xlabel('Día del año', fontsize=21)
axes[0].set_ylabel(f'Fallas/Día', fontsize=21)

month_tf1 = copy_df180.groupby('Mes')[['lambda_granjas_1']]
meses = ['Ene','Feb', 'Mar', 'Abr','May' , 'Jun', 'Jul','Agos','Sept', 'Oct', 'Nov','Dic']
c = 0
columns= []
for name, month in month_tf1:
    #LA ESTRATEGIA ANTERIOR GRAFICA CADA MES EN UNA MIS MA FIGURA Y LOS CONCATENA DESDE 0 HASTA 11 EN ORDEN, EN ESTE CASO SE CONSIDERA QUE NO SIRVE PORQUE CADA GRAFICO TIENE SU PROPIA ESCALA Y SE QUIERE UNA ESCALA PARA TODOS
    # month.plot(kind='box', ax = axs[c])
    columns.append(month['lambda_granjas_1'])
    c+=1

box = axes[1].boxplot(columns, patch_artist=True)
axes[1].set_title(f'Diagrama de Cajas - {variable} - Mensual', fontsize=22)  # Tamaño de la fuente ajustado
axes[1].set_ylabel("Fallas/Día", fontsize=21)
axes[1].set_xlabel("Mes", fontsize=21)
axes[1].set_xticklabels(meses[:len(columns)])
axes[1].grid(True, linestyle='--', alpha=0.7)
axes[1].tick_params(axis='x', labelsize=15)
axes[1].tick_params(axis='y', labelsize=15)
#colors = ['#191970', '#0000CD', '#00008B', '#1E90FF', '#87CEFA', '#87CEEB', '#F5FFFA', '#E0FFFF', '#ADD8E6', '#4169E1', '#0000FF', '#000080']  #ADD8E6 (0.68, 0.85, 0.90)

colors = [(0, 0, 0.5), (0, 0, 0.8), (0.1, 0.2, 0.5), (0, 0, 0.8), (0.0, 0.5, 1.0), (0.68, 0.85, 0.90), (0.95, 0.95, 1.0), (0.68, 0.9, 0.95), (0.0, 0.65, 1.0), (0.0, 0.5, 1.0), (0, 0, 0.8), (0, 0, 0.7)]
for patch, color in zip(box['boxes'], colors[:len(columns)]):
    patch.set_facecolor(color)
plt.subplots_adjust(hspace=0.5)

plt.savefig("lambdaporañov1.png",dpi=300)


#--------------------------------------------------------------------------------------------------------------------------------LAMBDA mtto POR AÑO

variable ='lambda_mtto_granjas_f'
v2019 = df180[variable].loc['2019-01-01' : '2019-12-31']
v2020 = df180[variable].loc['2020-01-01' : '2020-12-31']
v2021 = df180[variable].loc['2021-01-01' : '2021-12-31']
v2022 = df180[variable].loc['2022-01-01' : '2022-12-31']
v2023 = df180[variable].loc['2023-01-01' : '2023-12-31']

t2019 = range(181,181+len(v2019))
t2020 = range(1,len(v2020)+1)
t2021 = range(1,len(v2021)+1)
t2022 = range(1,len(v2022)+1)
t2023 = range(1,len(v2023)+1)

fig, axes = plt.subplots(2, figsize=(20, 10))
SIZE_DEFAULT = 20
SIZE_LARGE = 20
plt.rc("font", weight="normal")  # controls default font
plt.rc("font", size=SIZE_DEFAULT)  # controls default text sizes
plt.rc("xtick", labelsize=SIZE_DEFAULT)  # fontsize of the tick labels
plt.rc("ytick", labelsize=SIZE_DEFAULT)

axes[0].plot(t2019,v2019, color="teal", linewidth=1.3, linestyle="-", label="2019", alpha=0.5)
axes[0].plot(t2020,v2020, color="blue", linewidth=1, linestyle="-", label="2020", alpha=0.5)
axes[0].plot(t2021,v2021, color="purple", linewidth=1, linestyle="-", label="2021", alpha=0.5)
axes[0].plot(t2022,v2022,color="red", linewidth=1, linestyle="-", label="2022", alpha=0.5)
axes[0].plot(t2023,v2023,color="black", linewidth=1, linestyle="-", label="2023", alpha=0.5)

axes[0].spines["right"].set_visible(False)
axes[0].spines["top"].set_visible(False)

axes[0].tick_params(axis='both', which='major', labelsize=18)
axes[0].legend(fontsize=13)
axes[0].set_title(f'{variable} por año', fontsize=24)
axes[0].set_xlabel('Día del año', fontsize=21)
axes[0].set_ylabel(f'Fallas/Día', fontsize=21)

axes[0].axvline(45,color="black",linewidth = 1, linestyle = "dashed")
axes[0].axvline(135,color="black",linewidth = 1, linestyle = "dashed")
axes[0].axvline(274,color="black",linewidth = 1, linestyle = "dashed")

axes[0].annotate("Lluvias Frecuentes ", (320, 0.041), fontsize=13)
axes[0].annotate("Sequía", (200, 0.041), fontsize=13)
axes[0].annotate("Lluvias Intermitentes", (70, 0.041), fontsize=13)
axes[0].annotate("Sequía Transitoria", (-1, 0.041), fontsize=13)

copy_df180 = df180.copy()
copy_df180['Mes'] = copy_df180.index.month #CREO UNA COLUMNA CON EL NUMERO DEL MES DE LA FECHA
month_tf1 = copy_df180.groupby('Mes')[['lambda_mtto_granjas_f']]
meses = ['Ene','Feb', 'Mar', 'Abr','May' , 'Jun', 'Jul','Agos','Sept', 'Oct', 'Nov','Dic']
c = 0
columns= []
for name, month in month_tf1:
    #LA ESTRATEGIA ANTERIOR GRAFICA CADA MES EN UNA MIS MA FIGURA Y LOS CONCATENA DESDE 0 HASTA 11 EN ORDEN, EN ESTE CASO SE CONSIDERA QUE NO SIRVE PORQUE CADA GRAFICO TIENE SU PROPIA ESCALA Y SE QUIERE UNA ESCALA PARA TODOS
    # month.plot(kind='box', ax = axs[c])
    columns.append(month['lambda_mtto_granjas_f'])
    c+=1

box = axes[1].boxplot(columns, patch_artist=True)
axes[1].set_title(f'Diagrama de Cajas - {variable} - Mensual', fontsize=22)  # Tamaño de la fuente ajustado
axes[1].set_ylabel("Fallas/Día", fontsize=21)
axes[1].set_xlabel("Mes", fontsize=21)
axes[1].set_xticklabels(meses[:len(columns)])
axes[1].grid(True, linestyle='--', alpha=0.7)
axes[1].tick_params(axis='x', labelsize=15)
axes[1].tick_params(axis='y', labelsize=15)
#colors = ['#191970', '#0000CD', '#00008B', '#1E90FF', '#87CEFA', '#87CEEB', '#F5FFFA', '#E0FFFF', '#ADD8E6', '#4169E1', '#0000FF', '#000080']  #ADD8E6 (0.68, 0.85, 0.90)

colors = [(0, 0, 0.5), (0, 0, 0.8), (0.1, 0.2, 0.5), (0, 0, 0.8), (0.0, 0.5, 1.0), (0.68, 0.85, 0.90), (0.95, 0.95, 1.0), (0.68, 0.9, 0.95), (0.0, 0.65, 1.0), (0.0, 0.5, 1.0), (0, 0, 0.8), (0, 0, 0.7)]
for patch, color in zip(box['boxes'], colors[:len(columns)]):
    patch.set_facecolor(color)
plt.subplots_adjust(hspace=0.5)

plt.savefig("lambdamttoporañov1.png",dpi=300)
#---------------------------------------------------------------------------------------------------------------------------------------BOXPLOT
# EN LA LINEA 108 SE CREA UNA COLUMNA CON EL MES EN COPY.DF180
month_tf1 = copy_df180.groupby('Mes')[['lambda_mtto_granjas_f']]
meses = ['Ene','Feb', 'Mar', 'Abr','May' , 'Jun', 'Jul','Agos','Sept', 'Oct', 'Nov','Dic']
c = 0
columns= []
for name, month in month_tf1:
    #LA ESTRATEGIA ANTERIOR GRAFICA CADA MES EN UNA MIS MA FIGURA Y LOS CONCATENA DESDE 0 HASTA 11 EN ORDEN, EN ESTE CASO SE CONSIDERA QUE NO SIRVE PORQUE CADA GRAFICO TIENE SU PROPIA ESCALA Y SE QUIERE UNA ESCALA PARA TODOS
    # month.plot(kind='box', ax = axs[c])
    columns.append(month['lambda_mtto_granjas_f'])
    c+=1

fig, axs = plt.subplots()
box = axs.boxplot(columns, patch_artist=True)
axs.set_title('Diagrama de Cajas Mensual', fontsize=24)  # Tamaño de la fuente ajustado
axs.set_ylabel("Fallas/Día", fontsize=21)
axs.set_xlabel("Mes", fontsize=21)
axs.set_xticklabels(meses[:len(columns)])
axs.grid(True, linestyle='--', alpha=0.7)
axs.tick_params(axis='x', labelsize=15)
axs.tick_params(axis='y', labelsize=15)
#colors = ['#191970', '#0000CD', '#00008B', '#1E90FF', '#87CEFA', '#87CEEB', '#F5FFFA', '#E0FFFF', '#ADD8E6', '#4169E1', '#0000FF', '#000080']  #ADD8E6 (0.68, 0.85, 0.90)
decimal = 1
colors = [(0, 0, 0.5), (0, 0, 0.8), (0.1, 0.2, 0.5), (0, 0, 0.8), (0.0, 0.5, 1.0), (0.68, 0.85, 0.90), (0.95, 0.95, 1.0), (0.68, 0.9, 0.95), (0.0, 0.65, 1.0), (0.0, 0.5, 1.0), (0, 0, 0.8), (0, 0, 0.7)]
for patch, color in zip(box['boxes'], colors[:len(columns)]):
    patch.set_facecolor(color)
# fig, axs = plt.subplots(2,2, figsize=(12,6))
# axs = axs.flatten()
# v2019.plot(kind='box', ax = axs[0])
# v2020.plot(kind='box', ax=axs[1])
# v2021.plot(kind='box', ax = axs[2])
# v2022.plot(kind='box', ax=axs[3])
#----------------RECONOCIMIENTO DE PATRONES EN SERIES TEMPORALES-------------------------------
#-------------POR AHORA SE REALIZA EL GRAFICO DE LA MEDIA MOVIL -------------------
#------A LA ESPERA DE DESARROLLAR LA ESTRUCTURA DEL ANALISIS ----------------
# variables_tiempo = ['VV_10_MEDIA_D@21115170','VVMXAG_CON@21115020']
# medidas2.rolling_mean(variables_tiempo)
# #SE PUEDEN DETECTAR TENDENCIAS A LO LARGO DEL TIEMPO, CORRELACIONES LINEALES (DIFERENCIA ENTRE MATRIZ DE CORRELACION Y MATRIZ DE COVARIANZAS), PCA
# #-------------
variable = 'lambda_granjas_1'
copy_df180 = df180.copy()
copy_df180 = copy_df180[[variable]]
WINDOW_SIZE = 90
copy_df180['rolling_mean'] = copy_df180[variable].rolling(window=WINDOW_SIZE).mean()
copy_df180['rolling_std'] = copy_df180[variable].rolling(window=WINDOW_SIZE).std()
copy_df180.plot(title='Moving Mean and Standard Deviation')
plt.tight_layout()
plt.xlabel('Date (Day)')
plt.ylabel('Failure Rate (Failures/Unit*Hour)')

transitoria_2019 = df180.loc['2019-01-01' : '2019-02-15']
transitoria_2020 = df180.loc['2020-01-01' : '2020-02-15']
transitoria_2021 = df180.loc['2021-01-01' : '2021-02-15']
transitoria_2022 = df180.loc['2022-01-01' : '2022-02-15']
transitoria_2023 = df180.loc['2023-01-01' : '2023-02-15']
transitoria = pd.concat([transitoria_2019,transitoria_2020, transitoria_2021, transitoria_2022, transitoria_2023])
lluviasi_2019 = df180.loc['2019-02-16' : '2019-05-16']
lluviasi_2020 = df180.loc['2019-02-16' : '2020-05-16']
lluviasi_2021 = df180.loc['2019-02-16' : '2021-05-16']
lluviasi_2022 = df180.loc['2019-02-16' : '2022-05-16']
lluviasi_2023 = df180.loc['2019-02-16' : '2023-05-16']
lluviasi = pd.concat([lluviasi_2019,lluviasi_2020, lluviasi_2021, lluviasi_2022, lluviasi_2023])
sequia_2019 = df180.loc['2019-05-17' : '2019-10-01']
sequia_2020 = df180.loc['2020-05-17' : '2020-10-01']
sequia_2021 = df180.loc['2021-05-17' : '2021-10-01']
sequia_2022 = df180.loc['2022-05-17' : '2022-10-01']
sequia_2023 = df180.loc['2023-05-17' : '2023-10-01']
sequia = pd.concat([sequia_2019,sequia_2020, sequia_2021, sequia_2022, sequia_2023])
lluviasf_2019 = df180.loc['2019-10-02' : '2019-12-31']
lluviasf_2020 = df180.loc['2020-10-02' : '2020-12-31']
lluviasf_2021 = df180.loc['2021-10-02' : '2021-12-31']
lluviasf_2022 = df180.loc['2022-10-02' : '2022-12-31']
lluviasf_2023 = df180.loc['2023-10-02' : '2023-12-31']
lluviasf = pd.concat([lluviasf_2019,lluviasf_2020, lluviasf_2021, lluviasf_2022, lluviasf_2023])
from sklearn.preprocessing import StandardScaler
#Sequía Transitoria
scaler = StandardScaler()
variables_estandarizadas = scaler.fit_transform(transitoria)
variables_estandarizadas_df = pd.DataFrame(variables_estandarizadas, columns=transitoria.columns)
cov_matrix_estandarizadas = variables_estandarizadas_df.cov()
import seaborn as sns
plt.figure(figsize=(10, 8))
# Graficar la matriz de covarianza estandarizada (puedes reemplazarla con tu propia matriz)
sns.heatmap(cov_matrix_estandarizadas, annot=True, cmap="coolwarm", fmt=".2f", annot_kws={"size": 8},
            cbar_kws={'shrink': 0.8}) #, fmt=".2f"
# Ajustar el título largo dividiéndolo en dos líneas
plt.title("Matriz de Covarianza en Sequía Transitoria", fontsize=16, pad=20)
# Ajustar el tamaño de las etiquetas del eje x e y
plt.xticks(rotation=45, ha='right', fontsize=10)
plt.yticks(rotation=0, ha='right',fontsize=8)
# Ajustar el espaciado y mostrar el gráfico
plt.tight_layout()
plt.savefig("cov_sequiat.png")
#Sequía
scaler = StandardScaler()
variables_estandarizadas = scaler.fit_transform(sequia)
variables_estandarizadas_df = pd.DataFrame(variables_estandarizadas, columns=sequia.columns)
cov_matrix_estandarizadas = variables_estandarizadas_df.cov()
print(cov_matrix_estandarizadas)
import seaborn as sns
plt.figure(figsize=(10, 8))
# Graficar la matriz de covarianza estandarizada (puedes reemplazarla con tu propia matriz)
sns.heatmap(cov_matrix_estandarizadas, annot=True, cmap="coolwarm", fmt=".2f", annot_kws={"size": 8},
            cbar_kws={'shrink': 0.8})
# Ajustar el título largo dividiéndolo en dos líneas
plt.title("Matriz de Covarianza en Sequía", fontsize=16, pad=20)
# Ajustar el tamaño de las etiquetas del eje x e y
plt.xticks(rotation=45, ha='right', fontsize=10)
plt.yticks(rotation=0, fontsize=10)
# Ajustar el espaciado y mostrar el gráfico
plt.tight_layout()
plt.savefig("cov_sequia.png")
#Lluvias Intermitentes
scaler = StandardScaler()
variables_estandarizadas = scaler.fit_transform(lluviasi)
variables_estandarizadas_df = pd.DataFrame(variables_estandarizadas, columns=lluviasi.columns)
cov_matrix_estandarizadas = variables_estandarizadas_df.cov()
print(cov_matrix_estandarizadas)
import seaborn as sns
plt.figure(figsize=(10, 8))
# Graficar la matriz de covarianza estandarizada (puedes reemplazarla con tu propia matriz)
sns.heatmap(cov_matrix_estandarizadas, annot=True, cmap="coolwarm", fmt=".2f", annot_kws={"size": 8},
            cbar_kws={'shrink': 0.8})
# Ajustar el título largo dividiéndolo en dos líneas
plt.title("Matriz de Covarianza en Lluvias Intermitentes", fontsize=16, pad=20)
# Ajustar el tamaño de las etiquetas del eje x e y
plt.xticks(rotation=45, ha='right', fontsize=10)
plt.yticks(rotation=0, fontsize=10)
# Ajustar el espaciado y mostrar el gráfico
plt.tight_layout()
plt.savefig("cov_lluviasi.png")
#Lluvias Frecuentes
scaler = StandardScaler()
variables_estandarizadas = scaler.fit_transform(lluviasf)
variables_estandarizadas_df = pd.DataFrame(variables_estandarizadas, columns=lluviasf.columns)
cov_matrix_estandarizadas = variables_estandarizadas_df.cov()
print(cov_matrix_estandarizadas)
import seaborn as sns
plt.figure(figsize=(10, 8))
# Graficar la matriz de covarianza estandarizada (puedes reemplazarla con tu propia matriz)
sns.heatmap(cov_matrix_estandarizadas, annot=True, cmap="coolwarm", fmt=".2f", annot_kws={"size": 8},
            cbar_kws={'shrink': 0.8})
# Ajustar el título largo dividiéndolo en dos líneas
plt.title("Matriz de Covarianza en Lluvias Frecuentes", fontsize=16, pad=20)
# Ajustar el tamaño de las etiquetas del eje x e y
plt.xticks(rotation=45, ha='right', fontsize=10)
plt.yticks(rotation=0, fontsize=10)
# Ajustar el espaciado y mostrar el gráfico
plt.tight_layout()
plt.savefig("cov_lluviasf.png")
plt.show()

# for index, row in df180.iterrows():
#     print(row)



