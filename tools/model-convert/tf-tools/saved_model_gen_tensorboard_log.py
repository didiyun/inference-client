import tensorflow as tf
import numpy as np
import time

with tf.Session() as sess:
  tf.saved_model.loader.load(sess, [tf.saved_model.tag_constants.SERVING], "./model")
  summaryWriter = tf.summary.FileWriter('log/', tf.get_default_graph())
