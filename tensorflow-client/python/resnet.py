#!/usr/bin/env python
import sys
import numpy as np
import tensorflow as tf
import requests
from tensorflow_serving.apis import predict_pb2
from google.protobuf.json_format import MessageToDict

def sendRequest(url):
    request = predict_pb2.PredictRequest()
    response = predict_pb2.PredictResponse()

    request.model_spec.name = 'resnet'
    request.model_spec.signature_name = 'predict'

    array = np.ones(224*224*3).reshape(224,224,3).astype(np.float32)

    request.inputs['input'].CopyFrom(
        tf.make_tensor_proto(array, shape=[1, 224,224,3]))

    data = request.SerializeToString()

    data_type = "application/proto"
    headers = {
        # !!! set content type 
        'content-type': data_type,
        # !!! replace your token
        'Authorization': "AppCode TOKEN"
    }

    res = requests.post(url, data, headers=headers, verify=False)
    if (res.status_code == 200 and res.headers['Content-Type'] == data_type):
        # print res.content
        response.ParseFromString(res.content)
        print(response)
    else:
        # handle error msg
        print(res)

if __name__ == '__main__':
    url = sys.argv[1]
    sendRequest(url)
