package main

import (
	"bytes"
	"crypto/tls"
	"flag"
	"fmt"
	"io/ioutil"
	"net/http"

	caffe2 "./gen-protos"
	"github.com/golang/protobuf/proto"
)

func httpDo(url string) {
	var proto_req caffe2.PredictRequest
	var proto_res caffe2.PredictResponse
	model_name := "resnet"
	signature_name := "predict_images"
	proto_req.ModelSpec = &caffe2.ModelSpec{Name: &model_name, SignatureName: &signature_name}
	proto_req.Inputs = make(map[string]*caffe2.TensorProto)
	var fake_image []float32
	for i := 0; i < 3*224*224; i++ {
		fake_image = append(fake_image, float32(1.0))
	}
	input_1_type := caffe2.TensorProto_FLOAT
	proto_req.Inputs["input_1"] = &caffe2.TensorProto{
		FloatData: fake_image,
		DataType:  &input_1_type,
		Dims:      []int64{1, 3, 224, 224}}
	pbdata, err := proto.Marshal(&proto_req)
	if err != nil {
		fmt.Println("pb marshal error: ", err)
		// handle error
	}
	client := &http.Client{
		Transport: &http.Transport{
			TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
		}}

	req, err := http.NewRequest("POST", url, bytes.NewBuffer(pbdata))
	if err != nil {
		// handle error
	}

	req.Header.Set("Content-Type", "application/proto")
	req.Header.Set("Authorization", "AppCode YOUR_CODE")

	resp, err := client.Do(req)

	defer resp.Body.Close()

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		// handle error
	}

	if resp.StatusCode == http.StatusOK &&
		resp.Header.Get("Content-Type") == "application/proto" {
		err = proto.Unmarshal(body, &proto_res)
		if err != nil {
			panic(err)
		}
		fmt.Println(proto_res)
	} else {
		fmt.Println(resp.Header.Get("Content-Type"))
		fmt.Println(string(body))
	}

}

func main() {
	address := flag.String("url", "https://ip:port/v1/model/pytorch/predict", "serving url")
	flag.Parse()
	httpDo(*address)
}
