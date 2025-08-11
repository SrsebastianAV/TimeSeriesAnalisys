"""
Modulo que implementa una red neuronal para predecir los valores de tasa de fallas
bibliografia-pytorch documentation
"""
from data180 import df180
from window import DataWindow
import torch
import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
from sklearn.model_selection import TimeSeriesSplit
from sklearn.preprocessing import StandardScaler
import datetime

import numpy as np
import pandas as pd
import seaborn as sns
import tensorflow as tf
import matplotlib.pyplot as plt
from data180 import scaler
from tensorflow.keras import Model, Sequential

from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.losses import MeanSquaredError
from tensorflow.keras.metrics import MeanAbsoluteError

from tensorflow.keras.layers import Dense, Conv1D, LSTM, Lambda, Reshape, RNN, LSTMCell

import warnings
warnings.filterwarnings('ignore')


print(torch.__version__)
#SELECCIONAMOS LAS VARIABLES DE INTERES
variables = ['lambda_granjas_1','lambda_mtto_granjas_f', 'VVMXAG_CON@21115020','PTPM_CON@21115020']

class NN():
    def __init__(self, dataset, window, seed):
        self.window = window
        self.seed = seed
        self.data = dataset

    def modeling(self):
        model = tf.keras.models.Sequential([
            tf.keras.layers.Dense(128, input_shape=[self.window], activation="relu"),
            tf.keras.layers.Dense(64, activation="relu"),
            tf.keras.layers.Dense(90)
        ])
        model.compile(loss="mse", optimizer=tf.keras.optimizers.SGD(learning_rate=1e-3, momentum=0.9),
              metrics=['mae', 'mse'])
        history = model.fit(self.data, epochs=500, verbose=0)

        return history, model







if __name__ == "__main__":
    #-----DATA-----
    variable_prediction = "lambda_granjas_1"
    scaler = StandardScaler()
    variables_estandar = scaler.fit_transform(df180[[variable_prediction]])
    df180 = pd.DataFrame(variables_estandar, columns=df180[[variable_prediction]].columns)

    Train_split = int(0.6 * len(df180))
    Val_split = int(0.8 * len(df180))
    X_train = df180[:Train_split]
    X_val = df180[Train_split:Val_split]
    X_test = df180[Val_split:]
    time_train = df180.index[:Train_split]
    time_train = df180.index[:Train_split]
    time_train = df180.index[:Train_split]


    #--------------
    #----WINDOW----
    window_size = 90
    dataset1 = DataWindow(window_width=window_size, label_width=90,train_data=X_train[variable_prediction], val_data=X_val[variable_prediction], test_data=X_test)
    dataset = dataset1.train
    #--------------
    #---MODELING---
    nn1 = NN(dataset=dataset, window=window_size, seed=42)
    history, model = nn1.modeling()
    print(model.summary())
    loss = history.history['loss']
    epochs = range(len(loss))
    plt.plot(epochs, loss, 'b', label='Training Loss')
    plt.show()
    #--VALIDATION--

    dataset_val = dataset1.val
    val_loss, val_mae, val_mse = model.evaluate(dataset_val)
    print(f'Validation Loss (MSE): {val_loss}, Validation MAE: {val_mae}, Validation MSE: {val_mse}')
    result = model.evaluate(dataset_val)
    print(result)
    #------------
    #-PREDICTION-

    forecast = []
    dataset_val = dataset1.val
    predictions = model.predict(dataset_val)
    print(predictions) #Este me da el resultado de todas las ventanas
    print(len(predictions))
    # --El siguiente ejercicio se desarrolla con el fin de predecir y graficar los resultados por las ventanas
    # Inicializar listas para las etiquetas y las predicciones
    input = []
    val_labels = []
    predictions = []

    # Iterar sobre el dataset de validación por ventanas
    for window in dataset1.val:
        inputs, labels = window  # Inputs (X) y labels (y)
        val_labels.append(labels.numpy())  # Guardar las etiquetas verdaderas
        input.append(inputs.numpy())
        pred = model.predict(inputs)  # Predecir los valores con el modelo entrenado
        # print("validation data", inputs)
        # print("labels", labels)
        # print("predictions", pred)
        predictions.append(pred)

    particular_val = 50
    print("Entrada:")
    print(np.array(input[particular_val]))
    print("Validation values:")
    print(np.array(val_labels[particular_val]))
    print("Predictions values:")
    print(predictions[particular_val])

    x_input = np.arange(1, input[particular_val].shape[1]+1)
    x_pred = np.arange(input[particular_val].shape[1]+1, input[particular_val].shape[1]+1 + predictions[particular_val].shape[1])

    plt.figure(figsize=(10,10))
    plt.plot(x_input, input[particular_val].squeeze())
    plt.plot(x_pred, val_labels[particular_val].squeeze())
    plt.plot(x_pred, predictions[particular_val].squeeze())
    plt.show()

    entrada_original = scaler.inverse_transform(np.array(input[particular_val]))
    entrada_original = entrada_original.reshape(-1, 1)
    entrada_originales_df = pd.DataFrame(entrada_original, columns=df180[[variable_prediction]].columns)

    predictions_original = scaler.inverse_transform(predictions[particular_val])
    predictions_original = predictions_original.reshape(-1, 1)
    predictions_originales_df = pd.DataFrame(predictions_original, columns=df180[[variable_prediction]].columns)

    print("Entrada:")
    print(entrada_originales_df)
    print("Validation values:")
    print(np.array(val_labels[particular_val]))
    print("Predictions values:")
    print(predictions_originales_df)

    plt.figure(figsize=(10, 10))
    plt.plot(x_input, entrada_originales_df)
    #plt.plot(x_pred, val_labels[particular_val].squeeze())
    plt.plot(x_pred, predictions_originales_df)
    plt.show()
    # Initialize a list
    forecast = []

    # Reduce the original series
    forecast_series = df180[Train_split - window_size:]

    # Use the model to predict data points per window size
    for time in range(len(forecast_series) - window_size):
        forecast.append(model.predict(forecast_series[time:time + window_size][np.newaxis]))

    # Convert to a numpy array and drop single dimensional axes
    results = np.array(forecast).squeeze()

    # Plot the results
    plot_series(time, (x_valid, results))



