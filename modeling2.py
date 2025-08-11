import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
from data180 import df180
import torch
import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
from sklearn.model_selection import TimeSeriesSplit

import datetime

import numpy as np
import pandas as pd
import seaborn as sns
import tensorflow as tf
import matplotlib.pyplot as plt

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
variables = ['lambda_norte_1','lambda_mtto_norte_f', 'VVMXAG_CON@21115020','PTPM_CON@21115020']
df180 = df180[variables]
#CREATING A TRAIN/TEST SPLIT
Train_split = int(0.7*len(df180))
Val_split = int(0.85*len(df180))
X_train = df180[:Train_split]
X_val = df180[Train_split:Val_split]
X_test = df180[Val_split:]

# tscv = TimeSeriesSplit(n_splits=20)
#
# for train_index, test_index in tscv.split(X_train):
#     print(train_index, "N",test_index)

class DataWindow(Dataset):
    def __init__(self, input_width, label_width, shift, train_df, val_df, test_df, label_columns=None, stride=1):
        self.train_df = train_df
        self.val_df = val_df
        self.test_df = test_df

        self.label_columns = label_columns
        if label_columns is not None:
            self.label_columns_indices = {name: i for i, name in enumerate(label_columns)}
        self.column_indices = {name: i for i, name in enumerate(train_df.columns)}

        self.input_width = input_width
        self.label_width = label_width
        self.shift = shift
        self.stride = stride  # Agregar el stride

        self.total_window_size = input_width + shift

    def __len__(self):
        # Ajustar el tamaño del dataset según el stride
        return (len(self.train_df) - self.total_window_size) // self.stride + 1

    def __getitem__(self, idx):
        # Calcular el índice de inicio de la ventana considerando el stride
        start_idx = idx * self.stride
        inputs = self.train_df[start_idx:start_idx + self.input_width].values
        labels = self.train_df[start_idx + self.label_width - 1:start_idx + self.total_window_size].values

        if self.label_columns is not None:
            labels = np.stack([labels[:, self.column_indices[name]] for name in self.label_columns], axis=-1)

        return torch.tensor(inputs, dtype=torch.float32), torch.tensor(labels, dtype=torch.float32)

    def make_dataloader(self, batch_size=32):
        return DataLoader(self, batch_size=batch_size, shuffle=True)


# Ejemplo de uso
train_df = X_train  # Reemplaza esto con tu DataFrame de entrenamiento
val_df = X_val  # Reemplaza esto con tu DataFrame de validación
test_df = X_test  # Reemplaza esto con tu DataFrame de prueba

# Crea instancias de DataWindow
single_step_window = DataWindow(input_width=1, label_width=1, shift=1, train_df=train_df, val_df=val_df,
                                test_df=test_df, label_columns=['lambda_norte_1'], stride=1)
wide_window = DataWindow(input_width=24, label_width=24, shift=1, train_df=train_df, val_df=val_df, test_df=test_df,
                         label_columns=['lambda_norte_1'], stride=1)

# Crear dataloaders
train_loader = single_step_window.make_dataloader(batch_size=32)
wide_loader = wide_window.make_dataloader(batch_size=32)

# Iterar sobre el DataLoader
for inputs, labels in train_loader:
    print(f'Inputs: {inputs.shape}, Labels: {labels.shape}')