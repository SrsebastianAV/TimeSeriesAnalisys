"""
Modulo para obtener las medidas estadisticas de un df
bibliografia-scipy-pandas documentation
"""
from graficar import Graficar
from missing import Missingvalues
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import kstest
import scipy.stats as ss
from scipy.stats import kurtosis
from pandas.core import window
class Medidas():
    def __init__(self, dataframe):
        self.df = dataframe
        self.estadisticas = pd.DataFrame()
    def mean(self):
        """
        SE CALCULA LA MEDIA DE CADA VARIABLE DEL DATAFRAME
        :return: MEAN - ES UN DF CON LAS MEDIAS DE CADA VARIABLE
        """
        mean = self.df.mean()
        return mean

    def median(self):
        """
        SE CALCULA LA MEDIANA DE CADA VARIABLE DEL DATAFRAME
        :return: MEDIAN - ES UN DF CON LAS MEDIANAS DE CADA VARIABLE
        """
        median = self.df.median()
        return median
    def std(self):
        std = self.df.std()
        return std
    def var(self):
        var = self.df.var()
        return var
    def cv(self):
        """
        Es una medida de variabilidad relativa que no depende de las unidades de medida (Evalua la variabilidad en relación con su media). Se emplea para comparar la variabilidad de distintas variables
        EJ: Permite comparar la variabilidad de conjuntos de datos con distintas magnitudes o unidades. Por ejemplo, la dispersión relativa puede comparar la variabilidad de ingresos en dos países diferentes, donde los ingresos absolutos pueden ser muy distintos.
        A diferencia de las medidas absolutas de dispersión (como la desviación estándar), que indican cuánto varían los datos en unidades concretas, la dispersión relativa normaliza esta variabilidad en función de la magnitud de los datos
        Lo normaliza dividiendo la std entre la media.
        :return:
        """
        cv = ss.variation(self.df)*100
        return pd.DataFrame(cv, columns=["CV"], index = self.df.columns)
    def skewness(self):
        skew = self.df.skew()#(skew - sesgar, obluco asimetrico)
        return skew
    def kurt(self):
        kurt = kurtosis(self.df, fisher=False)

        return pd.DataFrame(kurt, columns=["kurt"], index = self.df.columns)
    def observations(self, mean, median, cv, skew, kurt):
        observation = ''
        if (mean-(mean*0.1)) <= median <= (mean+(mean*0.1)):
            observation += 'La media es buen indicador del centro de los datos-'
        else:
            observation += 'la media no es una buena medida del centro de los datos (asimetría, atípicos, heterogeneidad)-'
        if kurt > 7.0:
            observation += 'Heterogeneidad por pocos atípicos muy alejados del resto-'
        elif kurt <=2:
            observation += 'Heterogeneidad por mezcla de dos poblaciones (Distribución bimodal)- '
        if kurt < 3:
            observation += 'Distribución platicurtica - '
        elif kurt > 3:
            observation += 'Distribución leptocurtica - '
        if -1 <= skew <= 1:
            observation += 'Distribución simetrica o con asimetria moderada-'
        elif skew > 1:
            observation += 'Distribución altamente asimetrica positivamente- '
        elif skew < -1:
            observation += 'Distribución altamente asimetrica ngeativamente-'
        return observation

    def descriptive(self):
        #ANALISIS INICIAL CONVIENE MEDIDAS DE CENTRALIDAD DE DATOS
        mean, median, std, var, cv, skew, kurtosis = self.mean(), self.median(), self.cv(), self.var() ,self.std(), self.skewness(), self.kurt()
        descriptive1 = pd.concat([mean, median, cv,var, std, skew,kurtosis], axis=1)
        descriptive1.columns = ['Mean','Median', 'std', 'VAR','CV' , 'skew', 'kurt']
        df = pd.DataFrame(descriptive1)
        df.to_excel('estad.xlsx')
        print(f"Medidas de los Datos:")
        print(descriptive1)
        for index, row in descriptive1.iterrows(): #Index ilustra los indices de las filas, row devuelve serie de pandas con cada valor contenido en cada columna j de la fila de estudio
            variable = index
            mean_variable, median_variable, cv_variable, skew_variable, kurtosis_variable  = row['Mean'], row['Median'], row['CV'], row['skew'], row['kurt']
            observation = self.observations(mean_variable, median_variable, cv_variable, skew_variable, kurtosis_variable)
            print(f"{variable} - {observation}")

    def outlier(self, columns_analysis): #INTERQUARTILE RANGE METHOD - the outlier data points are the ones falling below Q1–1.5 IQR or above Q3 + 1.5 IQR.
        """
        Recibe los nombres de las columnas a las cuales se desea realizar el tratamiento de atípicos mediante el interquartile range method
        :param columns_analysis:
        :return: dataframe de estudio con variables ajustadas
        """
        for column in columns_analysis:
            q1 = self.df[column].quantile(0.25)
            q3 = self.df[column].quantile(0.75)
            IQR = q3-q1
            outlier = self.df[column][((self.df[column]<(q1-1.5*IQR)) | (self.df[column]>(q3+1.5*IQR)))]
            self.df[column] = self.df[column].apply(lambda x: q1 if x < (q1-1.5*IQR) else x)
            self.df[column] = self.df[column].apply(lambda x: q1 if x > (q3+1.5*IQR) else x)

        return self.df
    def rolling_mean(self, columns_analysis):
        for column in columns_analysis:
            moving_avg = self.df[column].rolling(window=30).mean()
            print(moving_avg)
            fig, ax = plt.subplots()
            ax.plot(moving_avg, color='mediumpurple')
            ax.plot(self.df[column], color='palegreen')

if __name__ == "__main__":
    #Se crea df de prueba
    data = {'A':[100,3,3,2,3,3,2,3,1],'B':[9,9,11,13,12,12,11,13,12], 'C':[1,1,1,1,9,9,1,9,9]}
    df = pd.DataFrame(data)
    #data = {'A': [1.2, -0.5, 0.8, -0.3, 0.5, -0.2, 0.7, -0.4, 1.0, -0.6, 0.9, -0.1, 0.3, -0.7, 0.4, -0.8, 0.6, -1.0, 0.2, -0.9]}
    import numpy as np
    #data = np.random.normal(size=1500)
    #df = pd.DataFrame(data)
    #df.hist()
    #print(df.kurt())
    #Inicializo la instancia de la clase
    medidas_df = Medidas(df)
    medidas_df.descriptive()
    columnas_con_atipicos = ['A','B']
    medidas_df.outlier(columnas_con_atipicos)
    medidas_df.rolling_mean(columnas_con_atipicos)
    plt.show()
    # np.random.seed(0)  # Fijar semilla para reproducibilidad
    # data = np.random.normal(size=200000000)  # Generar 20 valores de una distribución normal estándar







