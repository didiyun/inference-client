import tensorflow as tf
import numpy as np

with tf.Session() as sess:
    tf.saved_model.loader.load(sess, [tf.saved_model.tag_constants.SERVING], "./model")

    '''
    generate inputs here, example:

    array_1 = np.array(xxx).reshape(x,x).astype(np.float32)
    array_2 = np.array(xxx).reshape(x,x).astype(np.float32)
    '''

    '''
    get tensor_name for sess_run, example:

    input_1  = sess.graph.get_tensor_by_name('xxx:x')
    input_2  = sess.graph.get_tensor_by_name('xxx:x')
    output_1 = sess.graph.get_tensor_by_name('xxx:x')
    '''

    var = sess.run(output_1, feed_dict={input_1:array_1, input_2:array_2})
    print("var", var)
