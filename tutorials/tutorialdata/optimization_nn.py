from keras import backend as K
print(K.tensorflow_backend._get_available_gpus())

from keras import models
from keras import layers
from keras.optimizers import Adam, RMSprop, SGD
from keras.utils.np_utils import to_categorical
from keras.callbacks import EarlyStopping
from keras import regularizers
from keras.layers import Dropout
from keras.layers.core import Dense, Dropout, Activation
from keras import backend as K

from sklearn.metrics import f1_score
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split

from hyperas.distributions import uniform
from hyperopt import Trials, STATUS_OK, tpe
from hyperas import optim
from hyperas.distributions import choice, uniform

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from collections import Counter 

def data():
    
    corpus = pd.read_csv("corpora/wikicorpus_v2.csv")

    vectorizer = TfidfVectorizer()
    vector = vectorizer.fit_transform(corpus["text"])
    labels = LabelEncoder().fit_transform(corpus["category"])
    vocab = vectorizer.vocabulary_
    

    X_train, X_test, y_train, y_test = train_test_split(vector, 
                                                            labels, 
                                                            test_size=0.4, 
                                                            train_size=0.6,
                                                            random_state=42)
    X_val = X_test[:132]
    X_test = X_test[132:]

    y_val = y_test[:132]
    y_test = y_test[132:]

    y_val = to_categorical(y_val)
    y_test = to_categorical(y_test)
    y_train = to_categorical(y_train)
    
    return X_train, y_train, X_val, y_val, X_test, y_test

X_train, y_train, X_val, y_val, X_test, y_test = data()
print(X_train.shape)


def create_model(X_train, y_train, X_val, y_val, X_test, y_test, vocab, labels):
    
    if K.backend() == 'tensorflow':
        K.clear_session()
    
    model = models.Sequential()
    model.add(Dense({{choice([16, 32, 64])}}, input_shape=(len(vocab),)))
    model.add(Activation('relu'))
    model.add(Dropout({{choice([0.2, 0.3])}}))
    model.add(Dense({{choice([16, 32, 64])}}))
    model.add(Activation('relu'))
    model.add(Dropout({{choice([0.2, 0.3])}})) 
    model.add(Dense(len(np.unique(labels))))
    model.add(Activation('softmax'))
    

    model.compile(optimizer='rmsprop',
                  loss="categorical_crossentropy",
                  metrics=["accuracy"])
    
    history = model.fit(X_train,
                        y_train,
                        epochs=10,
                        batch_size=16,
                        validation_data=(X_val, y_val),
                        verbose=2)
              
    validation_acc = np.mean(history.history['val_acc']) 
    
    return {'loss': -validation_acc, 'status': STATUS_OK, 'model':model}


best_run, best_model = optim.minimize(model=create_model,
                                      data=data,
                                      algo=tpe.suggest,
                                      max_evals=5,
                                      trials=Trials())


X_train, y_train, X_val, y_val, X_test, y_test = data()
print("Evalutation of best performing model:" )
print(best_model.evaluate(X_test, y_test))
print("Best performing model chosen hyper-parameters:")
print(best_run)