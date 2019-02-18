## Java Demo

how to build:

```
mvn clean package assembly:single
```

run:

```
java -cp target/eis-java-example-1.0-SNAPSHOT-jar-with-dependencies.jar com.didiyun.eis.MnistClientDemo https://ip:port/v1/model/tensorflow/predict
```
