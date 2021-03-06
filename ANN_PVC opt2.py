# -*- coding: utf-8 -*-
"""Artificial Neural Network

# This code is generated by Dr. Kazi Monzure Khoda

### Importing the libraries
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from sklearn.metrics import mean_squared_error
from keras.callbacks import EarlyStopping

tf.__version__

"""## Part 1 - Data Preprocessing

### Importing the dataset
"""

dataset = pd.read_excel('PVC Load 2.xlsx')
datasetTest = pd.read_excel('X_given_PVC2.xlsx')
X = dataset.iloc[:, :-1].values
y = dataset.iloc[:, -1].values

X_given=datasetTest.iloc[:, :-1].values

# # Taking care of missing data
# from sklearn.impute import SimpleImputer 
# imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
# imputer = imputer.fit(X[:, 0:7])
# X[:, 0:7] = imputer.transform(X[:, 0:7])

"""### Splitting the dataset into the Training set and Test set"""

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 1)


## Part 2 - Building the ANN
ann = tf.keras.models.Sequential()
ann.add(tf.keras.layers.Dense(units=500, activation='relu', input_dim = 3))
ann.add(tf.keras.layers.Dense(units=500, activation='relu'))
ann.add(tf.keras.layers.Dense(units=500, activation='relu'))
ann.add(tf.keras.layers.Dense(units=500, activation='relu'))
ann.add(tf.keras.layers.Dense(units=500, activation='relu'))
ann.add(tf.keras.layers.Dense(units=1))
ann.compile(optimizer = 'adam', loss = 'mean_squared_error')

"""### Training the ANN model on the Training set"""

#ann.fit(X_train, y_train, batch_size = 32, epochs = 10000)
"""### Training the ANN model on the Training set"""
early_stopping_monitor = EarlyStopping(monitor='val_loss', patience=5000)  # ignored
history_mse = ann.fit(X_train, y_train, batch_size = 256, epochs = 10000, callbacks = [early_stopping_monitor], verbose = 0, validation_split = 0.2)

print('Loss:    ', history_mse.history['loss'][-1], '\nVal_loss: ', history_mse.history['val_loss'][-1])

# EVALUATE MODEL IN THE TEST SET
score_mse_test = ann.evaluate(X_test, y_test)
print('Test Score:', score_mse_test)

# EVALUATE MODEL IN THE TRAIN SET
score_mse_train = ann.evaluate(X_train, y_train)
print('Train Score:', score_mse_train)


#batch seize 32 is working better
ann.save('my_model_PP5')

"""### Predicting the results of the Test set"""

 
# y_pred = ann.predict(np.array([[0.07, 0.06, .139, 0.765, 28, 440, 15.7, 0.1390, 39.6 ]]))
#y_pred = ann.predict(np.array([[12.95, 0.35, 13.30, 0.8, 35.8, 700, 20, 30 ]]))

y_pred = ann.predict(X_given)

fig = plt.figure(figsize=(10,6))
plt.plot(X[94:193,2], y[94:193],color='green', linestyle='dashed', label = '10%')
plt.plot(X[194:288,2], y[194:288], color = 'red', linestyle='dashed', label = '20%')
plt.plot( X_given[:,2],y_pred, color = 'blue', label = 'ANN model')
plt.title('Load-Displacement Curve')
plt.xlabel('Displacement (mm)')
plt.ylabel('Load (kN)')
plt.legend()
plt.show()
