package main

import (
	"bytes"
	"crypto/tls"
	"flag"
	"fmt"
	"io/ioutil"
	"net/http"

	tf "./gen_protos"
	"github.com/golang/protobuf/proto"
)

func httpDo(url string) {
	var proto_req tf.PredictRequest
	var proto_res tf.PredictResponse
	proto_req.ModelSpec = &tf.ModelSpec{Name: "mnist", SignatureName: "predict_images"}
	proto_req.Inputs = make(map[string]*tf.TensorProto)
	var fake_image []float32
	for i := 0; i < 784; i++ {
		fake_image = append(fake_image, float32(1.0))
	}
	proto_req.Inputs["images"] = &tf.TensorProto{
		FloatVal: fake_image,
		Dtype:    tf.DataType_DT_FLOAT,
		TensorShape: &tf.TensorShapeProto{
			Dim: []*tf.TensorShapeProto_Dim{&tf.TensorShapeProto_Dim{Size: int64(1)}, &tf.TensorShapeProto_Dim{Size: int64(784)}}}}
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
	req.Header.Set("Authorization", "Bearer YOUR_TOKEN")

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
	address := flag.String("url", "https://ip:port/v1/model/tensorflow/predict", "serving url")
	flag.Parse()
	httpDo(*address)
}
