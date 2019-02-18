
## build
* go get github.com/golang/protobuf/{proto,protoc-gen-go}
* ./build-protoc.sh 
* go build client.go


## run test
* 增加 token
* ./client --url=https://ip:port/v1/model/tensorflow/predict
