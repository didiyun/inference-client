# inference-client


[![Build Status](https://img.shields.io/github/stars/didiyun/inference-client.svg)](https://github.com/didiyun/inference-client)
[![Build Status](https://img.shields.io/github/forks/didiyun/inference-client.svg)](https://github.com/didiyun/inference-client)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)



# 简介
`inference-client` 是滴滴云推理服务的 `HTTP` 客户端示例代码

# 安装运行
从 [didiyun](https://app.didiyun.com/#/api/authtoken) 获取token, 替换代码中的 token , 然后运行：


## 例子: Tensorflow Python Client Demo
```shell
cd tensorflow-client/python
pip install -r requirements.txt
sh build-protoc.sh
python mnist.py https://ip:port/v1/model/tensorflow/predict
```

## 例子: Pytorch Python Client Demo
```shell
cd pytorch-client/python
pip install -r requirements.txt
sh build-protoc.sh
python resnet_demo.py https://ip:port/v1/model/pytorch/predict
```


