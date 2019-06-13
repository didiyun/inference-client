#include <stdio.h>
#include <iostream>
#include <string>

#include <curl/curl.h>
#include "gen_protos/predict.pb.h"

using tensorflow::serving::PredictRequest;
using tensorflow::serving::PredictResponse;
using tensorflow::serving::ModelSpec;

typedef google::protobuf::Map<std::string, tensorflow::TensorProto> OutMap;

inline const std::vector<float> mnist_sample_28x28() {
  return {
      0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0,
      0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0,
      0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0,
      0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0,
      0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0,
      0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0,
      0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0,
      0    ,0    ,0    ,0    ,0    ,0    ,0.33 ,0.73 ,0.62 ,0.59 ,0.24 ,0.14 ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0,
      0    ,0    ,0    ,0    ,0    ,0    ,0.87 ,1    ,1    ,1    ,1    ,0.95 ,0.78 ,0.78 ,0.78 ,0.78 ,0.78 ,0.78 ,0.78 ,0.78 ,0.67 ,0.2  ,0    ,0    ,0    ,0    ,0    ,0,
      0    ,0    ,0    ,0    ,0    ,0    ,0.26 ,0.45 ,0.28 ,0.45 ,0.64 ,0.89 ,1    ,0.88 ,1    ,1    ,1    ,0.98 ,0.9  ,1    ,1    ,0.55 ,0    ,0    ,0    ,0    ,0    ,0,
      0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0.067,0.26 ,0.055,0.26 ,0.26 ,0.26 ,0.23 ,0.082,0.93 ,1    ,0.42 ,0    ,0    ,0    ,0    ,0    ,0,
      0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0.33 ,0.99 ,0.82 ,0.071,0    ,0    ,0    ,0    ,0    ,0,
      0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0.086,0.91 ,1    ,0.33 ,0    ,0    ,0    ,0    ,0    ,0    ,0,
      0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0.51 ,1    ,0.93 ,0.17 ,0    ,0    ,0    ,0    ,0    ,0    ,0,
      0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0.23 ,0.98 ,1    ,0.24 ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0,
      0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0.52 ,1    ,0.73 ,0.02 ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0,
      0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0.035,0.8  ,0.97 ,0.23 ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0,
      0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0.49 ,1    ,0.71 ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0,
      0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0.29 ,0.98 ,0.94 ,0.22 ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0,
      0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0.075,0.87 ,1    ,0.65 ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0,
      0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0.012,0.8  ,1    ,0.86 ,0.14 ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0,
      0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0.15 ,1    ,1    ,0.3  ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0,
      0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0.12 ,0.88 ,1    ,0.45 ,0.004,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0,
      0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0.52 ,1    ,1    ,0.2  ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0,
      0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0.24 ,0.95 ,1    ,1    ,0.2  ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0,
      0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0.47 ,1    ,1    ,0.86 ,0.16 ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0,
      0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0.47 ,1    ,0.81 ,0.071,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0,
      0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0
    };
}


std::string prepareRequest() {
    using namespace tensorflow;
    TensorProto tensor_proto;
    tensor_proto.set_dtype(DT_FLOAT);
    tensor_proto.mutable_tensor_shape()->add_dim()->set_size(1);
    tensor_proto.mutable_tensor_shape()->add_dim()->set_size(784);

    // for (auto pixel: mnist_sample_28x28()) {
    //   tensor_proto.add_float_val(pixel);
    // }

    // google::protobuf::RepeatedField<float> data(mnist_sample_28x28().begin(), mnist_sample_28x28().end());
    // tensor_proto.mutable_float_val()->Swap(&data);

    *tensor_proto.mutable_float_val() = {mnist_sample_28x28().begin(), mnist_sample_28x28().end()};
    PredictRequest request;

    ModelSpec* spec = request.mutable_model_spec();
    spec->set_name("mnist");
    spec->set_signature_name("predict_images");
    (*request.mutable_inputs())["images"] = tensor_proto;
    assert(request.IsInitialized());
   
    std::string output;
    request.SerializeToString(&output);
    return output;

}


void parseResponse(const std::string &res) {
    PredictResponse response;
    response.ParseFromString(res);
    std::cout << "outputs size is " << response.outputs_size() << std::endl;
    OutMap& map_outputs = *response.mutable_outputs();
    OutMap::iterator iter;
    int output_index = 0;

    // read the response
    for (iter = map_outputs.begin(); iter != map_outputs.end(); ++iter) {
      tensorflow::TensorProto& result_tensor_proto = iter->second;
      std::cout << "number of probabilies " << result_tensor_proto.float_val_size() << std::endl;

      int maxIdx = -1;
      float maxVal = -1;
      for (int i = 0; i < result_tensor_proto.float_val_size(); ++i) {
          float val = result_tensor_proto.float_val(i);
          std::cout << "probability of " << i << " is " << val << std::endl;

          if (maxVal < val) {
            maxVal = val;
            maxIdx = i;
          }
      }
      std::cout << std::endl << "most probably the digit on the image is " << maxIdx << std::endl << std::endl;
      ++output_index;
    }
}

static size_t write_data(void *contents, size_t size, size_t nmemb, void *userp) {
    ((std::string*)userp)->append((char*)contents, size * nmemb);
    return size * nmemb;
}

static size_t header_callback(char *ptr, size_t size, size_t nmemb, void *userp) {
    int r;
    char buf[32] = {0, };
    r = sscanf(ptr, "Content-Type: %s\n", buf);
    if(r) {
        ((std::string*)userp)->append(buf, strlen(buf));
    }

    return size * nmemb;
}

// TODO  auth 
int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::cerr << "Usage: ./serving_client \"http://10.84.164.236:8002/v1/model/tensorflow/predict/\"" << std::endl;
        return -1;
    }
    char* url = argv[1];

    CURL *curl; 
    curl = curl_easy_init();

    if(curl) {
        curl_easy_setopt(curl, CURLOPT_CUSTOMREQUEST, "POST");
        curl_easy_setopt(curl, CURLOPT_URL, url);
        std::string req = prepareRequest();
        std::string res, content_type;
        struct curl_slist *headers = NULL;
        headers = curl_slist_append(headers, "content-type: application/proto");
        headers = curl_slist_append(headers, "Authorization: AppCode YOUR_CODE");

        curl_easy_setopt(curl, CURLOPT_SSL_VERIFYPEER, false);
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, req.c_str());
        curl_easy_setopt(curl, CURLOPT_POSTFIELDSIZE, req.size());
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_data);//设置回调函数
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &res);//设置写数据

        curl_easy_setopt(curl, CURLOPT_HEADERFUNCTION, header_callback);
        curl_easy_setopt(curl, CURLOPT_HEADERDATA, &content_type);

        CURLcode ret = curl_easy_perform(curl);

        if(ret == CURLE_OK) {
            long response_code;
            curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &response_code);
            // 检查 HTTP 返回值和类型
            if (response_code == 200 && content_type == "application/proto") {
                parseResponse(res);
            } else {
                fprintf(stderr, "response error : %s\n", res.c_str());
            }
        } else {
            fprintf(stderr, "curl_easy_perform() failed: %s\n",
                        curl_easy_strerror(ret));
        }
        curl_easy_cleanup(curl);
    }
    return 0;
}
