from typing import Dict, List

import tensorflow as tf

from gutenberg.models.item import ItemModel
from gutenberg.models.user import UserModel
from gutenberg.models.text import TextModel


class QueryModel(tf.keras.Model):

    def __init__(self,
                 nb_users: int,
                 user_embedding_dim: int = 8,
                 activation_fn: str = None,
                 layer_sizes: List[int] = None):

        self._nb_users = nb_users
        self._user_embedding_dim = user_embedding_dim
        self._layer_sizes = layer_sizes or [128, 64]

        self.user_model = UserModel(nb_users, user_embedding_dim)
        self.item_model = ItemModel()
        self.prompt_model = TextModel()

        self.dense_layers: List[tf.keras.layers.Dense] = [
            tf.keras.layers.Dense(num_units, activation=activation_fn)
            for num_units in self.dense_layers
        ]

    def call(self, inputs: Dict[str, tf.Tensor], *_):
        user_embedding = self.user_model(inputs['user_id'])  # (None, 32)
        item_embedding = self.item_model(inputs)  # (None, 64)
        prompt_embedding = self.prompt_model(inputs['prompt'])  # (None, 128)

        x = tf.concat([user_embedding, item_embedding, prompt_embedding], axis=1)  # (None, 224)

        for layer in self.dense_layers:
            x = layer(x)

        return x

    def get_config(self):
        return {
            'nb_users': self._nb_users,
            'user_embedding_dim': self._user_embedding_dim,
            'layer_sizes': self._layer_sizes
        }
