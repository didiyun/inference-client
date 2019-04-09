#!/bin/bash
[ ! -d './gen_protos' ] && mkdir ./gen_protos
protoc -I ../protos --go_out=import_path=./gen_protos:./gen_protos ../protos/*.proto
