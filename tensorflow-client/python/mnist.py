#!/usr/bin/env python
import sys
import numpy as np
import requests
sys.path.append('./gen_protos')
import predict_pb2
from tf_utils import tensor_util
from google.protobuf.json_format import MessageToDict

def sendRequest(url):
    request = predict_pb2.PredictRequest()
    response = predict_pb2.PredictResponse()

    request.model_spec.name = 'mnist'
    request.model_spec.signature_name = 'predict_images'

    array = np.random.ranf(784).reshape(1,784).astype(np.float32)
    request.inputs['images'].CopyFrom(
	tensor_util.make_tensor_proto(array))

    data = request.SerializeToString()

    data_type = "application/proto"
    headers = {
        # !!! set content type 
        'content-type': data_type,
        # !!! replace your token
        'Authorization': "AppCode YOUR_CODE"
    }

    res = requests.post(url, data, headers=headers, verify=False)
    if (res.status_code == 200 and res.headers['Content-Type'] == data_type):
        # print res.content
        response.ParseFromString(res.content)
        print(MessageToDict(response))
    else:
        # handle error msg
        print(res.content)

if __name__ == '__main__':
    url = sys.argv[1]
    sendRequest(url)
