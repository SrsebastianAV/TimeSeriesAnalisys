"""
Este modulo presenta, describe e imputa los valores faltantes en el DataFrame
"""
from graficar import Graficar
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from fancyimpute import IterativeImputer
from scipy.stats import kstest
from sklearn.experimental import enable_iterative_imputer  # Para habilitar IterativeImputer en versiones recientes de sklearn
from sklearn.impute import IterativeImputer
class Missingvalues:

    def __init__(self, X):

        self.X = X
        self.columns = self.X.columns.values
        self.null_values_percentage = []

    def howmany(self, dataframe):
        """
        Metodo que calcula el porcentaje de valores nulos en el DataFrame de entrada X
        :return: Retorna los valores nulos en porcentaje de cada columna del DataFrame
        """
        # null_values_percentage = []
        # null_values = self.X.isnull().sum()
        # self.null_values_percentage = [int(100*null_values.iloc[i]/len(self.X)) for i in range(len(null_values))]
        # return self.null_values_percentage
        self.null_values_percentage = []
        null_values = dataframe.isnull().sum()
        self.null_values_percentage = [int(100 * null_values.iloc[i] / len(dataframe)) for i in range(len(null_values))]
        return self.null_values_percentage

    def mean_imputation(self, dataframe):
        """
        Metodo que imputa la media a un DataFrame en los datos faltantes
        :param Dataframe: Ingresa DataFrame al cual se le imputa la media
        :return: Devuelve el DataFrame con los valores imputados
        """
        return dataframe.fillna(dataframe.mean())
    def b_fill(self, dataframe):
        """
        Metodo que realiza el relleno hacia atras (backfill) a un DataFrame en los datos faltantes
        :param Dataframe: Entrada es un DataFrame
        :return: Devuelve el DataFrame con los valores imputados
        """
        return dataframe.fillna(dataframe.bfill())
    def f_fill(self, dataframe):
        """
        Metodo que realiza el relleno hacia adelante (forwardfill) a un DataFrame en los datos faltantes
        :param Dataframe: Entrada es un DataFrame
        :return: Devuelve el DataFrame con los valores imputados
        """
        return dataframe.fillna(dataframe.ffill())
    def linear_interpolation(self, dataframe):
        """
        Metodo que realiza la imputación de valores faltantes con la interpolación lineal a un DataFrame
        :param Dataframe: Entrada es un DataFrame
        :return: Devuelve el DataFrame con los valores imputados
        """
        return dataframe.interpolate(method='linear')

    def knn_imputation(self, dataframe):
        """
        Metodo que realiza el relleno hacia adelante (forwardfill) a un DataFrame en los datos faltantes
        :param Dataframe: Entrada es un DataFrame
        :return: Devuelve el DataFrame con los valores imputados
        """
        imputer = KNNImputer(n_neighbors=7, weights='uniform')
        knnimputation = pd.DataFrame(imputer.fit_transform(dataframe), columns=dataframe.columns, index=dataframe.index)
        return knnimputation
    def MICE_imputation(self, dataframe):
        """
        Metodo que realiza el relleno hacia adelante (forwardfill) a un DataFrame en los datos faltantes
        :param Dataframe: Entrada es un DataFrame
        :return: Devuelve el DataFrame con los valores imputados
        """
        # imputer = IterativeImputer(max_iter=1000, random_state=20)
        # MICEimputation = pd.DataFrame(imputer.fit_transform(dataframe), columns=dataframe.columns, index=dataframe.index)
        imputer = IterativeImputer(random_state=10) #, sample_posterior=True
        df_imputed = imputer.fit_transform(dataframe)

        # Convertir el resultado de vuelta a un DataFrame
        MICEimputation = pd.DataFrame(df_imputed, columns=dataframe.columns, index=dataframe.index)
        return MICEimputation
    def set(self):
        mean_imp = self.X.copy()
        for i in range(len(self.null_values_percentage)):
            if self.null_values_percentage[i] <= 10:
                 mean_imp[self.columns[i]]= self.mean_imputation(self.X[[self.columns[i]]])

        #Se copia el DataFrame original
        fbf_imp, lin_imp, knn_imp, mice_imp = [self.X.copy() for _ in range(4)]
        #Se llaman los metodos de imputación en los DataFrame copia
        fbf_imp, lin_imp, knn_imp, mice_imp = self. f_fill(fbf_imp), self.linear_interpolation(lin_imp), self.knn_imputation(knn_imp), self.MICE_imputation(mice_imp)
        fbf_imp = self.b_fill(fbf_imp)
        lin_imp = self.mean_imputation(lin_imp)
        #SI UN VALOR ES MENOR A CERO ENTONCES SE ASIGNA CERO
        #.MAP Aplica una función a cada elemento del DataFrame
        #max(x, 0): Devuelve el valor mayor entre x y 0
        #Si x es -5, max(-5, 0) devolverá 0.
        #Si x es 3, max(3, 0) devolverá 3
        fbf_imp, lin_imp, knn_imp, mice_imp = fbf_imp.map(lambda x: max(x, 0)), lin_imp.map(lambda x: max(x, 0)), knn_imp.map(lambda x: max(x, 0)), mice_imp.map(lambda x: max(x, 0))

        assert not fbf_imp.isnull().values.any(), "Forward-Backward fill resulted in NaNs"
        assert not lin_imp.isnull().values.any(), "Backfill resulted in NaNs"
        assert not knn_imp.isnull().values.any(), "KNN imputation resulted in NaNs"
        assert not mice_imp.isnull().values.any(), "MICE imputation resulted in NaNs"

        fbf_imp_flat = fbf_imp.values.flatten()
        lin_imp_flat = lin_imp.values.flatten()
        knn_imp_flat = knn_imp.values.flatten()
        mice_imp_flat = mice_imp.values.flatten()

        # Eliminar filas con NaNs en el DataFrame original para la comparación
        original_flat = self.X.dropna().values.flatten()

        # Se calcula el KS test comparando cada método con el DataFrame original
        ks_tests = {
            "f_fill": kstest(original_flat, fbf_imp_flat),
            "lin_fill": kstest(original_flat, lin_imp_flat),
            "knn_imputation": kstest(original_flat, knn_imp_flat),
            "MICE_imputation": kstest(original_flat, mice_imp_flat),
        }

        # Imprime los resultados del KS test
        # for method, ks_result in ks_tests.items(): #SE COMENTA PORQUE YA TERMINA EL ANALISIS DE IMPUTACION
        #     print(f"{method}: KS test statistic = {ks_result.statistic}, p-value = {ks_result.pvalue}")

        return mean_imp, fbf_imp, lin_imp, knn_imp, mice_imp


if __name__ == "__main__":
    # Se crea DF
    data = {'A': [1, 2, np.nan, 4], 'B': [12, 14, np.nan, np.nan], 'C': [np.nan, 54, 36, 8], 'D': [11, 14, 15, 17]}
    df = pd.DataFrame(data)
    # Inicializamos el objeto
    missing1 = Missingvalues(df)
    missing1.howmany(dataframe=df)
    missing1.set()

    # EValuar la distribución de lso datos, yo quiero que los datos imputados no cambien mi distribución
    #Evaluar si se preserva la correlacion de las variables