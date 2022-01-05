import tensorflow as tf
from keras_cv.layers.preprocessing.cut_mix import CutMix


NUM_CLASSES = 10


class CutMixTest(tf.test.TestCase):
    def test_return_shapes(self):
        xs = tf.ones((2, 512, 512, 3))
        # randomly sample labels
        ys = tf.random.categorical(tf.math.log([[0.5, 0.5]]), 2)
        ys = tf.squeeze(ys)
        ys = tf.one_hot(ys, NUM_CLASSES)

        layer = CutMix(probability=1.0)
        xs, ys = layer(xs, ys)

        self.assertEqual(xs.shape, [2, 512, 512, 3])
        # one hot smoothed labels
        self.assertEqual(ys.shape, [2, 10])
        self.assertEqual(len(ys != 0.0), 2)

    def test_label_smoothing(self):
        xs = tf.ones((2, 512, 512, 3))
        # randomly sample labels
        ys = tf.random.categorical(tf.math.log([[0.5, 0.5]]), 2)
        ys = tf.squeeze(ys)
        ys = tf.one_hot(ys, NUM_CLASSES)

        layer = CutMix(probability=1.0, label_smoothing=0.2)
        xs, ys = layer(xs, ys)
        self.assertNotAllClose(ys, 0.0)
