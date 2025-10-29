"""
Tiny TensorFlow demo to show how to train a model and export to TFLite.

This is a minimal example using CIFAR-10 shipped with tf.keras.datasets.
For real usage, replace with domain-specific leaf images and labels, add augmentation,
and improve model/metrics.

Run:
python ai/train_demo.py
"""
import tensorflow as tf
import numpy as np
import os

MODEL_DIR = "ai/models"
os.makedirs(MODEL_DIR, exist_ok=True)

def prepare_data():
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.cifar10.load_data()
    x_train = x_train.astype("float32") / 255.0
    x_test = x_test.astype("float32") / 255.0
    return (x_train, y_train), (x_test, y_test)

def build_model(input_shape=(32,32,3), num_classes=10):
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=input_shape),
        tf.keras.layers.Conv2D(16, 3, activation="relu"),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Conv2D(32, 3, activation="relu"),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(64, activation="relu"),
        tf.keras.layers.Dense(num_classes, activation="softmax"),
    ])
    model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    return model

def train_and_save():
    (x_train, y_train), (x_test, y_test) = prepare_data()
    model = build_model()
    model.fit(x_train[:5000], y_train[:5000], epochs=3, validation_data=(x_test[:1000], y_test[:1000]))
    model_path = os.path.join(MODEL_DIR, "demo_model.h5")
    model.save(model_path)
    print("Saved model to", model_path)

if __name__ == "__main__":
    train_and_save()
