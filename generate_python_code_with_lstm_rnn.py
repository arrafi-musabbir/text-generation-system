# -*- coding: utf-8 -*-
"""generate python code with LSTM-RNN

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xluNyXDZgf06wFsYoMugxcP-A1TBU-VX
"""

from google.colab import drive
drive.mount('/content/drive')

"""## Necessary imports"""

import numpy as np
import tensorflow as tf
import pandas as pd
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import LSTM
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.utils import to_categorical
import sys

"""## Loading text file to train"""

# load ascii text and covert to lowercase
filename = "data.txt"
raw_text = open(filename, 'r', encoding='utf-8').read()
raw_text = raw_text.lower()

"""## preparing the data"""

# create mapping of unique chars to integers
chars = sorted(list(set(raw_text)))
char_to_int = dict((c, i) for i, c in enumerate(chars))

n_chars = len(raw_text)
n_vocab = len(chars)
print("Total Characters: ", n_chars)
print("Total Vocab: ", n_vocab)

"""## Finding patters in the data"""

...
# prepare the dataset of input to output pairs encoded as integers
seq_length = 100
dataX = []
dataY = []
for i in range(0, n_chars - seq_length, 1):
	seq_in = raw_text[i:i + seq_length]
	seq_out = raw_text[i + seq_length]
	dataX.append([char_to_int[char] for char in seq_in])
	dataY.append(char_to_int[seq_out])
n_patterns = len(dataX)
print("Total Patterns: ", n_patterns)

"""## Data normalization with one hot encoding"""

...
# reshape X to be [samples, time steps, features]
X = np.reshape(dataX, (n_patterns, seq_length, 1))
# normalize
X = X / float(n_vocab)
# one hot encode the output variable
y = to_categorical(dataY)

"""## Building the LSTM model"""

...
# define the LSTM model
model = Sequential()
model.add(LSTM(256, input_shape=(X.shape[1], X.shape[2]), return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(256))
model.add(Dropout(0.2))
model.add(Dense(y.shape[1], activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics = ['accuracy'],)

model.summary()

"""## Defining early stopping monitoring validation loss"""

early_stopping = EarlyStopping(
    monitor='val_loss',
    min_delta=0.001,
    patience=4,
    restore_best_weights=True)

"""## Defining the checkpoints and the callback function"""

...
# define the checkpoint
filepath="/content/drive/MyDrive/RNN-lstm/weights-improvement-{epoch:02d}-{loss:.4f}.hdf5"
# define the callback function
checkpoint = ModelCheckpoint(filepath, monitor='val_loss', verbose=1, save_best_only=True, mode='min')
callbacks_list = [checkpoint, early_stopping]

"""## Training the model"""

history = model.fit(X, y, epochs=100, batch_size=128, validation_split=0.1, callbacks=callbacks_list)

"""## Ploting traning vs validation loss"""

history_df = pd.DataFrame(history.history)

plt.plot(history_df.loc[:, ['loss']], "#6daa9f", label='Training loss')
plt.plot(history_df.loc[:, ['val_loss']],"#774571", label='Validation loss')
plt.title('Training and Validation loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend(loc="best")

plt.show()

"""## Ploting traning vs validation accuracy"""

history_df = pd.DataFrame(history.history)

plt.plot(history_df.loc[:, ['accuracy']], "#6daa9f", label='Training accuracy')
plt.plot(history_df.loc[:, ['val_accuracy']],"#774571", label='Validation accuracy')
plt.title('Training vs Validation accuracy')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend(loc="best")

plt.show()

"""## Load the trained model"""

...
# load the network weights
filename = "/content/drive/MyDrive/RNN-lstm/weights-improvement-23-1.2212.hdf5"
model.load_weights(filename)
model.compile(loss='categorical_crossentropy', optimizer='adam')

...
int_to_char = dict((i, c) for i, c in enumerate(chars))

"""## Generating text with trained LSTM model"""

...
# pick a random seed
start = np.random.randint(0, len(dataX)-1)
pattern = dataX[start]
print("Generating fake Python code (functions, etc.):\n")
print("\"", ''.join([int_to_char[value] for value in pattern]), "\"")
# generate characters
for i in range(1000):
	x = np.reshape(pattern, (1, len(pattern), 1))
	x = x / float(n_vocab)
	prediction = model.predict(x, verbose=0)
	index = np.argmax(prediction)
	result = int_to_char[index]
	seq_in = [int_to_char[value] for value in pattern]
	sys.stdout.write(result)
	pattern.append(index)
	pattern = pattern[1:len(pattern)]
print("\n\nDone.")