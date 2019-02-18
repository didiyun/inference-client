// Copyright (c) 2014 Baidu, Inc.
// 
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
// 
//     http://www.apache.org/licenses/LICENSE-2.0
// 
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

// A client sending requests to server by multiple threads.

#include <stdio.h>
#include <iostream>
#include <string>
#include <curl/curl.h>

#include <gflags/gflags.h>
#include "protos/caffe2_service.pb.h"
typedef google::protobuf::Map<std::string, caffe2::TensorProto> OutMap;

std::string prepareRequest() {
    using namespace caffe2;
    srand (time(NULL));
    caffe2::TensorProto tensor_proto;
    tensor_proto.set_data_type(caffe2::TensorProto::FLOAT);
    tensor_proto.add_dims(1);
    tensor_proto.add_dims(3);
    tensor_proto.add_dims(224);
    tensor_proto.add_dims(224);

    //mock input
    for (int i=0; i<3*224*224; i++) {
      tensor_proto.add_float_data(1);
    }
    
    caffe2::PredictRequest request;
    caffe2::ModelSpec* spec = request.mutable_model_spec();
    spec->set_name("resnet");
    (*request.mutable_inputs())["input_1"] = tensor_proto;
    assert(request.IsInitialized());

    std::string output;
    request.SerializeToString(&output);
    return output;
}


void parseResponse(const std::string &res) {
    caffe2::PredictResponse response;
    response.ParseFromString(res);
    std::cout << "outputs size is " << response.outputs_size() << std::endl;
    OutMap& map_outputs = *response.mutable_outputs();
    OutMap::iterator iter;
    int output_index = 0;

    for (iter = map_outputs.begin(); iter != map_outputs.end(); ++iter) {
        caffe2::TensorProto& result_tensor_proto = iter->second;
        std::cout << "number of probabilies " << result_tensor_proto.float_data_size() << std::endl;

        int maxIdx = -1;
        float maxVal = -1;
        for (int i = 0; i < result_tensor_proto.float_data_size(); ++i) {
            float val = result_tensor_proto.float_data(i);
            std::cout << "probability of " << i << " is " << val << std::endl;

            if (maxVal < val) {
              maxVal = val;
              maxIdx = i;
            }
        }   
        std::cout << std::endl << "most probably the index of the image is " << maxIdx << std::endl << std::endl;
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



int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::cerr << "Usage: ./serving_client \"http://10.84.164.236:8002/v1/model/pytorch/predict/\"" << std::endl;
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
        headers = curl_slist_append(headers, "Authorization: Bearer YOUR_TOKEN");

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

