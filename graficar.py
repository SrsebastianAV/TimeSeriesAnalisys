"""
Modulo para representar graficamente series de tiempo inmersas en un DataFrame
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.gridspec import GridSpec
class Graficar:

    def __init__(self, x, y):


        self.x = x
        self.y = y
        self.name_columnsy = y.columns.values.tolist()





    def correlacion(self, corr_matrix,figsizex=10, figsizey=10):
        """
        Devuelve el grafico correlacion entre las variables del la matriz de correlación
        Se debe ingresar la matriz de correlación que resulta del comando df.corr()
        :param dataframe: Matriz de correlaciones
        :param figsizex: tamaño en x del grafico
        :param figsizey: tamaño en Y del grafico
        :return:
        """
        plt.figure(figsize=(figsizex,figsizey))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
        plt.title('Matriz de Correlación')

    def nulos(self):
        pass
    def multiscatter(self, DataFrame):
        #sns.pairplot(DataFrame)
        pass
    def histcatter(self, df_x, df_y):
        """
        Devuelve un scatter plot de los df ingresados, y grafica histogramas en las columnas de cada df
        :param df_x: DataFrame 1
        :param df_y: DataFrame 2
        :return: None - Bibliografia - https://stackabuse.com/matplotlib-scatter-plot-with-distribution-plots-histograms-jointplot/
        """
        fig = plt.figure()
        gs = GridSpec(12,12) #Fila 0 empieza en la parte superior de la figura
        ax_scatter = fig.add_subplot(gs[3:10, 0:9])  #es el subplot principal (gráfico de dispersión) que ocupa las celdas de la fila 2 a la 10 y de la columna 0 a la 9.
        ax_hist_x = fig.add_subplot(gs[0:2, 0:10])
        ax_hist_y = fig.add_subplot(gs[2:10, 10:12])

        ax_scatter.scatter(df_x, df_y)
        ax_hist_x.hist(df_x)
        ax_hist_y.hist(df_y, orientation = 'horizontal')
    def scatter(self,num_figure, num_plots_figure, figsizex=10, figsizey=10):
        """
        La función scatter representa graficamente series de tiempo en una o varias figuras
        :param num_figure: Número de figuras - Es decir, ventanas que se ejecutarán con plt.show()
        :param num_plots_figure: Número de gráficas en una figura o ventana
        :return: None
        """


        try:
            if not isinstance(num_figure, int) or not isinstance(num_plots_figure, int) or  num_figure <= 0 or  num_plots_figure <= 0 or  num_plots_figure > 2:
                raise ValueError(f"Se debe presentar un número entero y mayor a cero en la entrada de la función")
            try:

                if num_figure > len(self.y.columns) or num_plots_figure > len(self.y.columns):
                    raise IndexError(f"El DataFrame no cuenta con variables suficientes para las ventanas o graficos solicitados")

                if num_plots_figure == 2:
                    nombres_columnas = self.y.columns.tolist()
                    # Crear subgraficos
                    fig, axs = plt.subplots(num_figure, figsize=(10, 50))

                    if num_figure == 1: #Se puede mejorar -  si solo vamos a graficar una figura eliminar el ciclo for, ademas poner para graficar como max 3 variables a la vez en la misma figura - ademas, si son varios df crear otra funcion unicamente para esto
                        axs = [axs]
                    # Agregar datos
                    for i in range(num_figure):
                        titulo = nombres_columnas[i]
                        axs[i].scatter(self.x, self.y[nombres_columnas[1]], label = nombres_columnas[1], marker='o', s=20, color='mediumpurple', alpha=0.5)
                        axs[i].scatter(self.x, self.y[nombres_columnas[2]], label = nombres_columnas[2], marker='o', s=20, color='palegreen', alpha=0.5)
                        axs[i].set_title("Gráfico de Dispersión")
                        axs[i].set_xlabel('Fecha')
                        axs[i].set_ylabel('Datos')
                        axs[i].legend()

                    plt.subplots_adjust(hspace=0.5)

                else:

                    fig, ax = plt.subplots(num_figure, figsize=(figsizex, figsizey))
                    # Si solo se solicita una figura, entonces plt.subplots devolverá un solo eje no una lista de ejes
                    if num_figure == 1:
                        ax = [ax]
                    for figure in range(num_figure):
                        ax[figure].scatter(self.x, self.y[self.name_columnsy[figure]], label= self.name_columnsy[figure], marker='o', s=20, color='mediumpurple', alpha=0.5)
                        ax[figure].set_xlabel('Fecha')
                        ax[figure].set_ylabel(self.name_columnsy[figure])
                        ax[figure].set_title(f'Gráfico de Dispersión - Fecha vs {self.name_columnsy[figure]}')
                        ax[figure].legend()
                    plt.subplots_adjust(hspace=0.5)

            except IndexError as e:
                print(e)

        except ValueError as e:
            print(e)


    def histograma(self):
        pass



if __name__ == "__main__":

    #Se crea DF
    data = {'A':[1,2,3,4], 'B':[12,14,16,18], 'C':[1,54,36,8], 'D':[11,14,15,17]}
    df = pd.DataFrame(data)
    #Inicializamos el objeto
    grafica1 = Graficar(df[['A']], df.iloc[:,1:])
    #se grafica un scatter
    grafica1.scatter(num_figure=1, num_plots_figure=2, figsizex=15,figsizey=15)
    grafica1.histcatter(df[['A']], df[['B']])
    plt.show()

    # correlation = df.corr()
    # grafica2 = Graficar(correlation, pd.DataFrame())
    # grafica2.correlacion()
