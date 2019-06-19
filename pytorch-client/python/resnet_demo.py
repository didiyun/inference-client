# -*- coding: utf-8 -*
import sys
import numpy as np
import requests
sys.path.append("./gen_protos")
import caffe2_service_pb2
import utils


def sendRequest(url):
    spec = caffe2_service_pb2.ModelSpec()
    spec.name = 'resnet'

    request = caffe2_service_pb2.PredictRequest()
    response = caffe2_service_pb2.PredictResponse()
    request.model_spec.CopyFrom(spec)

    array = np.ones(1*3*224*224).reshape(1,3,224,224).astype(np.float32)
    request.inputs['input_1'].CopyFrom(utils.NumpyArrayToCaffe2Tensor(array))
    data = request.SerializeToString()

    data_type = "application/proto"

    #!!! Add Appcode here
    token = "YOUR_CODE"

    headers = {
        # !!! set content type
        'content-type': data_type,
        # !!! replace your token
        'Authorization': "AppCode " + token
    }

    res = requests.post(url=url,
                        data=data,
                        headers=headers)
    if (res.status_code == 200 and res.headers['Content-Type'] == data_type):
        response.ParseFromString(res.content)
        print(response)
    else:
	print(res.headers['X-Ddy-Error-Message'])
	print(res.content)

if __name__ == '__main__':
    #url https://ip:port/v1/model/pytorch/predict
    url = sys.argv[1]
    sendRequest(url)
