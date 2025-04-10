from keras.models import Sequential # type: ignore
from keras.layers import Dense # type: ignore

def ann():
    model = Sequential()
    model.add(Dense(30, input_dim=32, activation='relu', kernel_initializer='random_uniform'))
    model.add(Dense(10, activation='relu'))
    model.add(Dense(5, activation='softmax'))  # 5 classes
    model.compile(loss="categorical_crossentropy", optimizer='adam', metrics=['accuracy'])
    return model