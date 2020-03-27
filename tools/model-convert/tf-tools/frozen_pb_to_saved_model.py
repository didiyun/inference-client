import tensorflow as tf 
from tensorflow.python.framework import graph_util
from tensorflow.python.saved_model import signature_constants
from tensorflow.python.saved_model import tag_constants


def write_saved_model(frozen_graph_filename):
    sigs = {}
    with tf.Session() as sess:
    	with tf.gfile.GFile(frozen_graph_filename, "rb") as f:
                graph_def = tf.GraphDef()
        	graph_def.ParseFromString(f.read())
   	with tf.Graph().as_default() as graph:
        	tf.import_graph_def(
              	graph_def,
            	input_map=None,
            	return_elements=None,
            	name="",
            	producer_op_list=None
        	)
        builder = tf.saved_model.builder.SavedModelBuilder('./saved_model')

	'''
        add inputs&outputs here:
        example: 
        inputs_1 = graph.get_tensor_by_name("xxx/xxx/xxx:0")    
        outputs_1 = graph.get_tensor_by_name("xxx/xxx/xxx:0")    
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
    input_frozen_pb='./frozen_inference_graph.pb'
    write_saved_model(input_frozen_pb)


