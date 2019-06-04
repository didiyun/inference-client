#! /usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import os
import tarfile
import zipfile

def rm_dir(path):
    print("start to rm dir %s"%path)
    cmd="rm -rf %s" % path
    out=subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
    print("rm dir success %s" %(out))

def wget(path, url):
    cmd="wget -c -P '%s' '%s'" %(path, url)
    print("start to %s"%cmd)
    out=subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
    print("wget pkg success %s" %(out))

def rename(source,dest):
    if source != dest:
        cmd="mv '%s' '%s'" %(source, dest)
        print("start to %s"%cmd)
        out=subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
        print("mv pkg success %s" %(out))
    else:
        print("mv pkg success same dir(%s)"%source)

def compress(work_dir, compress_file_name, compress_dir):
    print("start to compress pkg (%s,%s,%s) ..." %(work_dir,\
                                                compress_file_name,\
                                                compress_dir))

    cmd = "cd '%s' &&  tar zcvf '%s'  '%s'"%(work_dir,\
                                            compress_file_name,\
                                            compress_dir)
    print("start to %s"%cmd)
    try:
        out=subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
    except Exception as e:
        print(e)
        raise RuntimeError('Internal error reason(compress fail)')
    print("compress pkg success %s" %(out))

"""
filter rules
1. dir name match "__MACOSX"
2. file name math ".*"
"""
def filter(path):
    filter_files = []
    filter_dirs = []
    for root, dirs, files in os.walk(path):
        for dir_name in dirs:
            print(os.path.join(root, dir_name))
            if dir_name == "__MACOSX":
                print("match dir(%s)"%os.path.join(root, dir_name))
                filter_dirs.append(os.path.join(root, dir_name))
        for file_name in files:
            print(os.path.join(root, file_name))
            if file_name.startswith('.'):
                print("match file(%s)"%os.path.join(root, file_name))
                filter_files.append(os.path.join(root, file_name))

    for del_dir in filter_dirs:
        print("delete dir(%s)"%del_dir)
        rm_dir(del_dir)
    for del_file in filter_files:
        print("delete file(%s)"%del_file)
        rm_dir(del_file)

def uncompress(pkg_name, path):
    """
    support 
    1/X.tar.gz X.tgz 
    2/X.tar.bz2 
    3/X.zip
    4/X.tar
    """
    print("start to uncompress model %s, %s ..."%(path, pkg_name))
    unsupported = False
    root = os.path.splitext(pkg_name)[0]
    postfix = os.path.splitext(pkg_name)[1]
    try:
        if postfix == ".tar":
            tar = tarfile.open(pkg_name, "r")
            tar.extractall(path=path)
            tar.close()
        elif postfix == ".tgz":
            tar = tarfile.open(pkg_name, "r:gz")
            tar.extractall(path=path)
            tar.close()
        elif postfix == ".zip":
            zipf = zipfile.ZipFile(pkg_name)
            zipf.extractall(path)
            zipf.close()
        elif postfix == ".bz2" and os.path.splitext(root)[1] == ".tar":
            tar = tarfile.open(pkg_name, "r:bz2")
            tar.extractall(path=path)
            tar.close()
        elif postfix == ".gz" and os.path.splitext(root)[1] == ".tar":
            tar = tarfile.open(pkg_name, "r:gz")
            tar.extractall(path=path)
            tar.close()
        else:
            unsupported = True
    except Exception as e:
        print(e)
        raise RuntimeError('Invalid compress type reason(%s)' % e.message)

    if unsupported:
        raise RuntimeError('Unsupported compress type (%s)' %(pkg_name))

    print("uncompress model success")

def list_bucket(target):
    from minio import Minio
    minioClient = Minio(target["url"],
                    access_key=target["accessKey"],
                    secret_key=target["secretKey"],
                    region=target["region"],
                    secure=target["secure"])
    ss= minioClient.list_objects(target["bucketName"],recursive=True)
    for s in ss:
        print(s.object_name)
