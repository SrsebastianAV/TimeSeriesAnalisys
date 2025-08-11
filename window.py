"""
Modulo que implementa una red neuronal para predecir los valores de tasa de fallas
coursera time series documentation
"""
import pandas as pd
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from data180 import df180
from sklearn.preprocessing import StandardScaler
variables = ['lambda_termales_1','lambda_mtto_termal_f', 'VVMXAG_CON@21115020']
df180 = df180[variables]

variables = df180
scaler = StandardScaler()
variables_estandarizadas = scaler.fit_transform(variables)
df180s = pd.DataFrame(variables_estandarizadas, columns=variables.columns)

#CREATING A TRAIN/TEST SPLIT
Train_split = int(0.5*len(df180s))
Val_split = int(0.75*len(df180s))
X_train = df180s[:Train_split]
X_val = df180s[Train_split:Val_split]
X_test = df180s[Val_split:]



variable_prediction = "lambda_termales_1"



def plot_predictions(train_data=X_train, val_data=X_val, test_data=X_test, predictions=None):
    """

    :param train_data:
    :param val_data:
    :param test_data:
    :param predictions:
    :return:
    """
    plt.figure(figsize=(10,8))
    plt.scatter(train_data.index, train_data[variable_prediction], s=7, label='Entrenamiento', color='blue', marker='o', linestyle='-', alpha=0.7) #plot train data
    plt.scatter(val_data.index, val_data[variable_prediction], s=7, label='Validación', color='green', marker='s', linestyle='-', alpha=0.7) #Plot validation data
    plt.scatter(test_data.index, test_data[variable_prediction], s=7, label='Prueba', color='orange', marker='D', linestyle='-', alpha=0.7) #Plot test data
    if predictions is not None:
        plt.scatter(predictions.index, predictions[variable_prediction], label='Test Data', color='orange', marker='D', linestyle='-', alpha=0.7)
    plt.title('Tasa de Fallas: lambda_granjas_1', fontsize=18, weight='bold')
    plt.xlabel('Tiempo (Días)', fontsize=14, weight='bold')
    plt.ylabel('lambda_granjas_1', fontsize=14, weight='bold')

    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)
    plt.legend(loc='upper right', fontsize=12, frameon=True, fancybox=True, shadow=True)
    plt.tight_layout()
    plt.savefig("tvtdata.png")
    plt.show()

class DataWindow():
    def __init__(self, window_width, label_width, train_data=X_train[variable_prediction], val_data=X_val[variable_prediction], test_data=X_test):
        """

        :param window_width:
        :param label_width:
        :param train_data:
        :param val_data:
        :param test_data:
        """
        self.window_width = window_width
        self.label_width = label_width
        self.train_data = train_data
        self.val_data = val_data
        self.test_data = test_data

    def windowed_dataset(self, series, shuffle_buffer):
        """

        :param series:
        :return:
        """
        dataset = tf.data.Dataset.from_tensor_slices(series)
        dataset = dataset.window(self.window_width+self.label_width, shift=1, drop_remainder=True)
        dataset = dataset.flat_map(lambda windows: windows.batch(self.window_width+self.label_width)) #Aplano los datos en un nuevo formato (tensor) para tener un mejor formato
        dataset = dataset.map(lambda windows: (windows[:-self.label_width], windows[-self.label_width:])) #tuple
        dataset = dataset.shuffle(shuffle_buffer) #Se barajan con el total de ventanas creadas representado por la variable shuffle
        dataset = dataset.batch(32).prefetch(1)
        # for x,y in dataset:
        #     print(x.numpy(), y.numpy())
        # for window in dataset: #para ver el contenido de dataset
        #     print(len(window))
        #     for val in window:
        #         print(val.numpy(), end=" ")
        #     print()
        return dataset
    def window_sinbatch(self, series):
        """

        :param series:
        :return:
        """
        dataset = tf.data.Dataset.from_tensor_slices(series)
        dataset = dataset.window(self.window_width+self.label_width, shift=1, drop_remainder=True)
        dataset = dataset.flat_map(lambda windows: windows.batch(self.window_width+self.label_width)) #Aplano los datos en un nuevo formato (tensor) para tener un mejor formato
        dataset = dataset.map(lambda windows: (windows[:-self.label_width], windows[-self.label_width:])) #tuple
        dataset = dataset.batch(1)
        return dataset
    @property
    def train(self):
        shuffle = (len(self.train_data) - self.window_width) // 1 + 1  # shift es 1
        return self.windowed_dataset(self.train_data, shuffle_buffer=shuffle)

    @property
    def val(self):
        return self.window_sinbatch(self.val_data)

    @property
    def test(self):
        shuffle = (len(self.test_data) - self.window_width) // 1 + 1  # shift es 1
        return self.windowed_dataset(self.test_data, shuffle_buffer=shuffle)
if __name__ == "__main__":
    plot_predictions()
    plt.show()
    window_size = 90
    dataset1 = DataWindow(window_width=window_size, label_width=90)
    dataset = dataset1.train
    for windows in dataset.take(1):
        print(f'data type: {type(windows)}')
        print(f'number of elements in the tuple: {len(windows)}')
        print(f'shape of first element: {windows[0].shape}')
        print(f'shape of second element: {windows[1].shape}')

    l0 = tf.keras.layers.Dense(90, input_shape=[window_size])
    model = tf.keras.models.Sequential([l0])
    model.compile(loss="mse", optimizer=tf.keras.optimizers.SGD(learning_rate=1e-6, momentum=0.9),
              metrics=['mae', 'mse'])
    history = model.fit(dataset,epochs=10)
    print(format(l0.get_weights()))

    loss = history.history['loss']
    epochs = range(len(loss))
    plt.plot(epochs, loss, 'b', label='Training Loss')
    # plt.show()
    dataset_val = dataset1.val
    val_loss, val_mae, val_mse = model.evaluate(dataset_val)
    print(f'Validation Loss (MSE): {val_loss}, Validation MAE: {val_mae}, Validation MSE: {val_mse}')
    result = model.evaluate(dataset_val)
    print(result)


    # # Initialize a list
    # forecast = []
    # dataset_val = dataset1.val
    # predictions = model.predict(dataset_val)
    # # Inicializar listas para las etiquetas y las predicciones
    # input = []
    # val_labels = []
    # predictions = []
    #
    # # Iterar sobre el dataset de validación por ventanas
    # for window in dataset1.val:
    #     inputs, labels = window  # Inputs (X) y labels (y)
    #     val_labels.append(labels.numpy())  # Guardar las etiquetas verdaderas
    #     input.append(inputs.numpy())
    #     pred = model.predict(inputs)  # Predecir los valores con el modelo entrenado
    #     # print("validation data", inputs)
    #     # print("labels", labels)
    #     # print("predictions", pred)
    #     predictions.append(pred)
    #
    # particular_val = 50
    # print(np.array(input[particular_val]))
    # print(np.array(val_labels[particular_val]))
    # print(predictions[particular_val])
    #
    # x_input = np.arange(1, input[particular_val].shape[1]+1)
    # x_pred = np.arange(input[particular_val].shape[1]+1, input[particular_val].shape[1]+1 + predictions[particular_val].shape[1])
    #
    # plt.figure(figsize=(10,10))
    # plt.scatter(x_input, input[particular_val])
    # plt.scatter(x_pred, val_labels[particular_val])
    # plt.scatter(x_pred, predictions[particular_val])
    # plt.show()








    # # Convertir las predicciones a un DataFrame si es necesario
    # predictions_df = pd.DataFrame(predictions, columns=["Predicted_lambda_norte_1"])
    # print(predictions_df)
    # # Convertir las predicciones a un DataFrame si es necesario (dependiendo de cómo hayas estructurado tus datos)
    # predictions_df = pd.DataFrame(predictions, columns=["Predicted_lambda_norte_1"])
    # #predictions_df.index = dataset.val.map(lambda x: x[0]).index  # Esto puede variar según cómo obtengas el índice
    # print(predictions_df)













