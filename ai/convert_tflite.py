"""
Convert saved Keras model to TFLite for on-device inference.

Run:
python ai/convert_tflite.py ai/models/demo_model.h5 ai/models/demo_model.tflite
"""
import tensorflow as tf
import sys

def convert(keras_path, tflite_path):
    model = tf.keras.models.load_model(keras_path)
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    tflite_model = converter.convert()
    with open(tflite_path, "wb") as f:
        f.write(tflite_model)
    print("Wrote tflite model to", tflite_path)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python convert_tflite.py <model.h5> <out.tflite>")
        sys.exit(1)
    convert(sys.argv[1], sys.argv[2])
