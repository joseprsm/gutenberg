from typing import List

import tensorflow as tf

from gutenberg.models.text import TextModel


class ItemModel(tf.keras.Model):

    def __init__(self,
                 activation_fn: str = None,
                 layer_sizes: List[int] = None):
        super().__init__()
        self._layer_sizes = layer_sizes or [512, 256, 64]

        self.name_model = TextModel()
        self.description_model = TextModel()

        self.dense_layers = [
            tf.keras.layers.Dense(num_units, activation=activation_fn)
            for num_units in self._layer_sizes
        ]

    def call(self, inputs):
        name_embedding = self.name_model(inputs['item_name'])  # (None, 512)
        description_embedding = self.description_model(inputs['item_description'])  # (None, 512)
        x = tf.concat([name_embedding, description_embedding], axis=1)  # (None, 1024)
        for layer in self.dense_layers:
            x = layer(x)
        return x

    @staticmethod
    def get_config():
        return {}
