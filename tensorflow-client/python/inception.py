#!/usr/bin/env python
import sys
import numpy as np
import requests
sys.path.append('./gen_protos')
import predict_pb2
from tf_utils import tensor_util
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
        tensor_util.make_tensor_proto(getImageData(), shape=[1]))
    data = request.SerializeToString()

    data_type = "application/proto"
    headers = {
        # !!! set content type 
        'content-type': data_type,
        # !!! replace your token
        'Authorization': "AppCode YOUR_CODE"
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
        print(res.content)

if __name__ == '__main__':
    url = sys.argv[1]
    sendRequest(url)
