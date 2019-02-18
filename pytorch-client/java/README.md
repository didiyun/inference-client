## Java Demo

how to build:

```
mvn clean package assembly:single
```

run:

```
java -cp target/eis-java-example-1.0-SNAPSHOT-jar-with-dependencies.jar com.didiyun.eis.ResnetClientDemo https://ip:port/v1/model/pytorch/predict
```
