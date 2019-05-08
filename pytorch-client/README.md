## python和c++语言的client需要先安装protoc工具，安装方法如下：

### Mac OS X

If you have Homebrew (which you can get from https://brew.sh), just run:

`brew install protobuf`

If you see any error messages, run brew doctor, follow any recommended fixes, and try again. If it still fails, try instead:

`brew upgrade protobuf`

Alternately, run the following commands:

```
PROTOC_ZIP=protoc-3.5.1-osx-x86_64.zip
curl -OL https://github.com/google/protobuf/releases/download/v3.5.1/$PROTOC_ZIP
sudo unzip -o $PROTOC_ZIP -d /usr/local bin/protoc
rm -f $PROTOC_ZIP
```


### Linux
Run the following commands:

```
PROTOC_ZIP=protoc-3.5.1-linux-x86_64.zip
curl -OL https://github.com/google/protobuf/releases/download/v3.5.1/$PROTOC_ZIP
sudo unzip -o $PROTOC_ZIP -d /usr/local bin/protoc
rm -f $PROTOC_ZIP
```

Alternately, manually download and install protoc from here:
[protobuf-v3.5.1](https://github.com/protocolbuffers/protobuf/releases?after=v3.5.1)
`https://github.com/protocolbuffers/protobuf/releases?after=v3.5.1`
