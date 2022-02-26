from typing import List

import tensorflow as tf
import tensorflow_recommenders as tfrs

from gutenberg.models.text import TextModel
from gutenberg.models.query import QueryModel


class Recommender(tfrs.Model):

    def __init__(self,
                 nb_users: int,
                 prediction_layer_sizes: List[int] = None,
                 rating_layer_sizes: List[int] = None,
                 rating_activation_fn: str = 'relu'):
        super().__init__()
        self._nb_users = nb_users
        self._rating_activation_fn = rating_activation_fn
        self._rating_layer_sizes = rating_layer_sizes or [128, 64, 32]
        self._prediction_layer_sizes = prediction_layer_sizes or [256, 128, 64]

        self.query_model = QueryModel(nb_users)
        self.prediction_model = TextModel(layer_sizes=self._prediction_layer_sizes)

        self.rating_model = tf.keras.Sequential([
            tf.keras.layers.Dense(num_units, activation=rating_activation_fn)
            for num_units in self._rating_layer_sizes
        ])

        self.rating_model.add(tf.keras.layers.Dense(1))

    def compute_loss(self, inputs, training: bool = False) -> tf.Tensor:
        ratings = inputs.pop('rating')
        query_embeddings, candidate_embeddings, rating_predictions = self(inputs)
        rating_loss = self.rating_task(labels=ratings, predictions=rating_predictions)
        retrieval_loss = self.retrieval_task(query_embeddings, candidate_embeddings)
        return self.rating_weight * rating_loss + self.retrieval_weight * retrieval_loss

    def call(self, inputs, *_):
        query_embeddings = self.query_model(inputs)  # (None, 64)
        candidate_embeddings = self.prediction_model(inputs['prediction'])  # (None, 64)
        x = tf.concat([query_embeddings, candidate_embeddings], axis=1)  # (None, 128)
        rating_predictions = self.rating_model(x)  # (None, 1)
        return query_embeddings, candidate_embeddings, rating_predictions

    def get_config(self):
        return {
            'nb_users': self._nb_users,
            'rating_layer_sizes': self._rating_layer_sizes,
            'rating_activation_fn': self._rating_activation_fn,
        }
