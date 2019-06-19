#!/usr/bin/env python
import sys
import numpy as np
import tensorflow as tf
import requests
from tensorflow_serving.apis import predict_pb2
from google.protobuf.json_format import MessageToDict

def getImageData():
    with open('./test.jpg', 'r') as f:
        return f.read()

def sendRequest(url):
    request = predict_pb2.PredictRequest()
    response = predict_pb2.PredictResponse()

    request.model_spec.name = 'inception'
    request.model_spec.signature_name = 'predict_images'

    request.inputs['images'].CopyFrom(
        tf.make_tensor_proto(getImageData(), shape=[1]))
    data = request.SerializeToString()

    data_type = "application/proto"

    #Add Appcode here
    token = "YOUR_CODE"

    headers = {
        # !!! set content type
        'content-type': data_type,
        # !!! replace your token
        'Authorization': "AppCode " + token
    }

    res = requests.post(url, data, headers=headers)

    if (res.status_code == 200 and res.headers['Content-Type'] == data_type):
        # print res.content
        response.ParseFromString(res.content)
        le = len(response.outputs["classes"].string_val)
        for i in range(le):
            print("{}  score: {}".format(response.outputs["classes"].string_val[i],
                                        response.outputs["scores"].float_val[i]))

    else:
        # handle error msg
	print(res.headers['X-Ddy-Error-Message'])
        print(res.content)

if __name__ == '__main__':
    url = sys.argv[1]
    sendRequest(url)
