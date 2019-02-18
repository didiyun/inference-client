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
import org.tensorflow.framework.DataType;
import org.tensorflow.framework.TensorProto;
import org.tensorflow.framework.TensorShapeProto;
import tensorflow.serving.Model;
import tensorflow.serving.Predict;

import java.util.Map;


public class MnistClientDemo {

    private String url;

    public MnistClientDemo(String url) {
        this.url = url;
    }

    /**
     * predict from thrift server
     */
    public void predict() {
        TensorProto imageTensor = createImageTensor(getMockImage());
        requestService(imageTensor);
    }

    // mock image
    private int[][] getMockImage() {
        return new int[28][28];
    }

    /**
     * Create image tensor from image content
     *
     * @param image image content
     * @return image tensor
     */
    private TensorProto createImageTensor(int[][] image) {
        try {
            TensorShapeProto.Dim featuresDim1 = TensorShapeProto.Dim.newBuilder()
                    .setSize(1).build();
            TensorShapeProto.Dim featuresDim2 = TensorShapeProto.Dim.newBuilder()
                    .setSize(image.length * image.length).build();
            TensorShapeProto imageFeatureShape = TensorShapeProto.newBuilder()
                    .addDim(featuresDim1).addDim(featuresDim2).build();

            TensorProto.Builder imageTensorBuilder = TensorProto.newBuilder();
            imageTensorBuilder.setDtype(DataType.DT_FLOAT).setTensorShape(imageFeatureShape);

            for (int i = 0; i < image.length; ++i) {
                for (int j = 0; j < image.length; ++j) {
                    imageTensorBuilder.addFloatVal(image[i][j]);
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
    private void requestService(TensorProto requestTensor) {
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
            post.setHeader("Authorization", "Bearer YOUR_TOKEN");
            post.setEntity(new ByteArrayEntity(generateTFRequestBody(requestTensor)));
            HttpResponse response = client.execute(post);
            if (response.getStatusLine().getStatusCode() == HttpStatus.SC_OK 
                    && "application/proto".equals(response.getFirstHeader("Content-Type").getValue())) {
                // get result tensor
                byte[] raw = EntityUtils.toByteArray(response.getEntity());
                Predict.PredictResponse res = Predict.PredictResponse.parseFrom(raw);
                Map<String, TensorProto> outputMap = res.getOutputsMap();
                for (TensorProto tensor : outputMap.values()) {
                    System.out.println("number of probabilities " + tensor.getFloatValCount());
                    int maxIdx = -1;
                    float maxVal = -1f;
                    for (int i = 0; i < tensor.getFloatValCount(); i++) {
                        float value = tensor.getFloatVal(i);
                        System.out.println("probability of " + i + " is " + value);
                        if (maxVal < value) {
                            maxIdx = i;
                            maxVal = value;
                        }
                    }
                    System.out.println("most probably the digit on the image is " + maxIdx);
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

    private byte[] generateTFRequestBody(TensorProto tensor) {
        // generate tf request body
        Model.ModelSpec modelSpec = Model.ModelSpec.newBuilder()
                .setName("mnist")
                .setSignatureName("predict_images")
                .build();
        Predict.PredictRequest request = Predict.PredictRequest.newBuilder()
                .setModelSpec(modelSpec)
                .putInputs("images", tensor)
                .build();
        return request.toByteArray();
    }

    public static void main(String[] args) {
        // replace with your url, like https://${ip}:${port}/v1/model/tensorflow/predict
        new MnistClientDemo(args[0]).predict();
    }
}
