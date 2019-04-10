#!/bin/bash
[ ! -d './gen_protos' ] && mkdir ./gen_protos
protoc -I ../protos/ --python_out=./gen_protos/ ../protos/*.proto
