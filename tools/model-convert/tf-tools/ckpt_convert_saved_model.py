'''
convert ckpt model to saved_model
'''
import tensorflow as tf
from tensorflow.python.framework import graph_util
from tensorflow.python.saved_model import signature_constants
from tensorflow.python.saved_model import tag_constants

def saved_graph(input_checkpoint):

    saver = tf.train.import_meta_graph(input_checkpoint + '.meta', clear_devices=True)

    builder = tf.saved_model.builder.SavedModelBuilder('./saved_model')
    sigs = {}
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        saver.restore(sess, input_checkpoint)

        g = tf.get_default_graph()
	'''
	add inputs&outputs here:
	example: 
	inputs_1 = g.get_tensor_by_name("xxx/xxx/xxx:0")	
	outputs_1 = g.get_tensor_by_name("xxx/xxx/xxx:0")	
	'''

        sigs[signature_constants.DEFAULT_SERVING_SIGNATURE_DEF_KEY] = \
            tf.saved_model.signature_def_utils.build_signature_def(
                inputs={
	'''
	build input tensor info here
	example:
	'inputs_1':tf.saved_model.utils.build_tensor_info(inputs_1),
	'''
        },
            outputs = {
	'''
	build input tensor info here
	example:
	'outputs_1':tf.saved_model.utils.build_tensor_info(outputs_1),
	'''
    },
         method_name = tf.saved_model.signature_constants.PREDICT_METHOD_NAME   
        )

        builder.add_meta_graph_and_variables(sess,
                                             [tag_constants.SERVING],
                                             signature_def_map=sigs)

    builder.save()

if __name__ == '__main__':
    input_checkpoint='/xxx/xxx/ckpt_model_path'
    saved_graph(input_checkpoint)
