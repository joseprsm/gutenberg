import tensorflow as tf


class UserModel(tf.keras.Model):

    def __init__(self, input_dim: int, embedding_dim: int = 32, **kwargs):
        super().__init__(**kwargs)
        self._input_dim = input_dim
        self._embedding_dim = embedding_dim

        self.hashing_layer = tf.keras.layers.Hashing(input_dim)
        self.embedding_layer = tf.keras.layers.Embedding(input_dim, embedding_dim)

    def call(self, inputs, *_):
        x = self.hashing_layer(inputs)  # (None, 1)
        x = self.embedding_layer(x)  # (None, 32)
        return x

    def get_config(self):
        return {
            'input_dim': self._input_dim,
            'embedding_dim': self._embedding_dim
        }
