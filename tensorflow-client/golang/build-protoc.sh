#!/bin/bash

protoc -I./protos --go_out=import_path=./protos:./protos ./protos/*.proto


