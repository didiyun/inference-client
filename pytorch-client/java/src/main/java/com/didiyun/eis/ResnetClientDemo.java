package com.didiyun.eis;

import org.apache.http.HttpResponse;
import org.apache.http.HttpStatus;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.conn.ssl.NoopHostnameVerifier;
import org.apache.http.conn.ssl.SSLConnectionSocketFactory;
import org.apache.http.conn.ssl.TrustSelfSignedStrategy;
import org.apache.http.entity.ByteArrayEntity;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.ssl.SSLContextBuilder;
import org.apache.http.util.EntityUtils;
import caffe2.Caffe2;
import caffe2.Caffe2Service;

import java.util.Map;


public class ResnetClientDemo {

    private String url;
    public ResnetClientDemo(String url) {
        this.url = url;
    }

    /**
     * predict from thrift server
     */
    public void predict() {
        Caffe2.TensorProto imageTensor = createImageTensor(getMockImage());
        requestService(imageTensor);
    }

    // mock image
    private float[][][] getMockImage() {
        return new float[3][224][224];
    }

    /**
     * Create image tensor from image content
     *
     * @param image image content
     * @return image tensor
     */
    private Caffe2.TensorProto createImageTensor(float[][][] image) {
        try {
            Caffe2.TensorProto.Builder imageTensorBuilder = Caffe2.TensorProto.newBuilder();
            imageTensorBuilder.setDataType(Caffe2.TensorProto.DataType.FLOAT);
            imageTensorBuilder.addDims(1);
            imageTensorBuilder.addDims(3);
            imageTensorBuilder.addDims(224);
            imageTensorBuilder.addDims(224);

            for (int a = 0; a < 3; ++a) {
                for (int i = 0; i < 224; ++i) {
	 	    for (int j = 0; j < 224; ++j) {
                        imageTensorBuilder.addFloatData(1);
		    }
	        }
            }
            return imageTensorBuilder.build();
        } catch (Exception e) {
            e.printStackTrace();
            throw new Error(e);
        }
    }

    /**
     * Request mnist classification eis
     *
     * @param requestTensor request image tensor
     */
    private void requestService(Caffe2.TensorProto requestTensor) {
        try {
            SSLContextBuilder builder = new SSLContextBuilder();
            builder.loadTrustMaterial(null, new TrustSelfSignedStrategy());
            SSLConnectionSocketFactory sslsf = new SSLConnectionSocketFactory(
                    builder.build(), NoopHostnameVerifier.INSTANCE);
            CloseableHttpClient client = HttpClients.custom().
                    setSSLSocketFactory(sslsf).build();
            HttpPost post = new HttpPost(url);
            post.setHeader("Content-Type", "application/proto");
            // replace YOUR_TOKEN with didiyun api token
            post.setHeader("Authorization", "AppCode YOUR_CODE");
            post.setEntity(new ByteArrayEntity(generateCaffe2RequestBody(requestTensor)));
            HttpResponse response = client.execute(post);
            if (response.getStatusLine().getStatusCode() == HttpStatus.SC_OK 
                    && "application/proto".equals(response.getFirstHeader("Content-Type").getValue())) {
                // get result tensor
                byte[] raw = EntityUtils.toByteArray(response.getEntity());
                Caffe2Service.PredictResponse res = Caffe2Service.PredictResponse.parseFrom(raw);
                Map<String, Caffe2.TensorProto> outputMap = res.getOutputsMap();
                for (Caffe2.TensorProto tensor : outputMap.values()) {
                    System.out.println("number of probabilities " + tensor.getFloatDataCount());
                    int maxIdx = -1;
                    float maxVal = -1f;
                    for (int i = 0; i < tensor.getFloatDataCount(); i++) {
                        float value = tensor.getFloatData(i);
                        System.out.println("probability of " + i + " is " + value);
                        if (maxVal < value) {
                            maxIdx = i;
                            maxVal = value;
                        }
                    }
                    System.out.println("most probably the index of the image is " + maxIdx);
                }
            } else {
                // print error message
                String msg = EntityUtils.toString(response.getEntity(), "UTF-8");
                System.err.println("error msg is " + msg);
            }
        } catch (Exception e) {
            e.printStackTrace();
            throw new Error(e);
        }
    }

    private byte[] generateCaffe2RequestBody(Caffe2.TensorProto tensor) {
        // generate tf request body
        Caffe2Service.ModelSpec modelSpec = Caffe2Service.ModelSpec.newBuilder()
                .setName("resnet")
                .setSignatureName("predict_images")
                .build();
        Caffe2Service.PredictRequest request = Caffe2Service.PredictRequest.newBuilder()
                .setModelSpec(modelSpec)
                .putInputs("images", tensor)
                .build();
        return request.toByteArray();
    }

    public static void main(String[] args) {
        // replace with your url, like https://${ip}:${port}/v1/model/pytorch/predict
        new ResnetClientDemo(args[0]).predict();
    }
}
