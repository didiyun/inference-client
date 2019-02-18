#!/bin/bash
[ ! -d 'gen-protos' ] && mkdir gen-protos
protoc -I../protos --go_out=./gen-protos ../protos/*.proto

