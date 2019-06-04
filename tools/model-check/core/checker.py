#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os

class TFModelDirChecker(object):
    def __call__(self, model_path):
        #压缩包第一级路径必须有且只有1个目录
        for root, dirs, files in os.walk(model_path):
            if root == model_path:
                if not (len(dirs) == 1):
                    print("more than one dirs in compress file")
                    raise RuntimeError("Invalid model dir structure")
                top_dir=dirs[0]
                #self.compress_dir = top_dir
                print("model check top dir: %s pass"%top_dir)
                break
            else:
                print("root dir check fail")
                raise RuntimeError("Invalid model dir structure")

        walk_dir = os.path.join(model_path, top_dir)
        #第一级目录必须有且只有1个数字目录
        for root, dirs, files in os.walk(walk_dir):
            if root.split('/')[-1] == top_dir:
                if not (len(dirs) == 1):
                    print("more than one dirs in top dir")
                    raise RuntimeError("Invalid model dir structure")
                second_dir=dirs[0]
                if not second_dir.isdigit():
                    print("second dir must be all numbers")
                    raise RuntimeError("Invalid model dir structure")
                print("model check second: %s pass"%second_dir)
                break
            else:
                print("second dir check fail")
                raise RuntimeError("Invalid model dir structure")
        
        walk_dir = os.path.join(walk_dir, second_dir)
        #self.saved_model_dir = walk_dir
        #第二级目录下包含一个.pb文件，variables文件夹可有可无
        for root, dirs, files in os.walk(walk_dir):
            if root.split('/')[-1] == second_dir:
                check_pb_file = False
                for file_name in files:
                    if (file_name == "saved_model.pbtxt"):
                        check_pb_file = True
                        pb_name = file_name
                    if (file_name == "saved_model.pb"):
                        check_pb_file = True
                        pb_name = file_name
                if not check_pb_file:
                    print("can't find *pb file")
                    raise RuntimeError("Invalid model dir structure")

                print("model check third: %s pass"%(pb_name))
                break
            else:
                print("model check third dir fail")
                raise RuntimeError("Invalid model dir structure")


class PytorchModelDirChecker(object):
    def __call__(self, model_path):
        #压缩包第一级路径必须有且只有1个目录
        for root, dirs, files in os.walk(model_path):
            if root == model_path:
                if not (len(dirs) == 1):
                    print("more than one dirs in tar file")
                    raise RuntimeError("Invalid model dir structure")
                top_dir=dirs[0]
                #self.compress_dir = top_dir
                print("model check top dir: %s pass"%top_dir)
                break
            else:
                print("model check top dir fail")
                raise RuntimeError("Invalid model dir structure")

        walk_dir = os.path.join(model_path, top_dir)
        #第一级目录必须有且只有1个数字目录
        for root, dirs, files in os.walk(walk_dir):
            if root.split('/')[-1] == top_dir:
                if not (len(dirs) == 1):
                    print("more than one dirs in top dir")
                    raise RuntimeError("Invalid model dir structure")
                second_dir=dirs[0]
                if not second_dir.isdigit():
                    print("dir must be all numbers")
                    raise RuntimeError("Invalid model dir structure")
                print("model check second: %s pass"%second_dir)
                break
            else:
                print("second dir check fail")
                raise RuntimeError("Invalid model dir structure")

        walk_dir = os.path.join(walk_dir, second_dir)
        #self.saved_model_dir = walk_dir
        #第二级目录下有且只有一个.pt文件
        for root, dirs, files in os.walk(walk_dir):
            if root.split('/')[-1] == second_dir:
                if not (len(files) == 1):
                    print("more than one file in third dir")
                    raise RuntimeError("Invalid model dir structure")
                pt_file_name=files[0]
                postfix = os.path.splitext(pt_file_name)[1]
                if postfix != ".pt":
                    print("can't find *pt file")
                    raise RuntimeError("Invalid model dir structure")
                print("model check third: %s pass"%(pt_file_name))
                break
            else:
                print("model check third dir fail")
                raise RuntimeError("Invalid model dir structure")
        return

def dirCheckerFactory(stype="tensorflow"):
    """The factory method"""
    dircheckers = dict(tensorflow=TFModelDirChecker, pytorch=PytorchModelDirChecker)
    return dircheckers[stype]()


