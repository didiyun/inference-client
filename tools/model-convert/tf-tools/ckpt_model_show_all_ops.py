'''
show ckpt model all operations
'''

import sys
import tensorflow as tf
from tensorflow.python.framework import graph_util

def show_all_ops(model_path):
    saver = tf.train.import_meta_graph('./xxx/xxx.meta', clear_devices=True)
    with tf.Session() as sess:
        model_file=tf.train.latest_checkpoint(model_path)
        sess.run(tf.global_variables_initializer())
        saver.restore(sess, model_file)
        for i in tf.get_default_graph().get_operations():
            print(i.name)
if __name__ == '__main__':
    show_all_ops(sys.argv[1])
