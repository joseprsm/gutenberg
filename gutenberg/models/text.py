from typing import List

import tensorflow as tf
import tensorflow_hub as hub

TEXT_MODEL_URL = "https://tfhub.dev/google/universal-sentence-encoder/4"


class TextModel(tf.keras.Model):

    def __init__(self, layer_sizes: List[int] = None):
        super().__init__()
        self._layer_sizes = layer_sizes
        self._model = hub.load(TEXT_MODEL_URL)

        self.use_layer = hub.KerasLayer(self._model, trainable=False)

        self.dense_layers: List[tf.keras.layers.Dense] = [
            tf.keras.layers.Dense(num_units)
            for num_units in self._layer_sizes
        ]

    def call(self, inputs: tf.Tensor, *_):
        x = self.use_layer(inputs)  # (None, 512)
        for layer in self.dense_layers:
            x = layer(x)
        return x

    def get_config(self):
        return {"layer_sizes": self._layer_sizes}
