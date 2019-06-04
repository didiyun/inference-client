#! /usr/bin/env python
# -*- coding: utf-8 -*-
import util
import os

class HttpGetter(object):
    def __call__(self, source, path):
        try:
            url = source['url']
            print("start to download model from http url(%s) to (%s)"% (url,path))
            util.wget(path, url)
            print("end to download model from http url(%s) to (%s)"% (url,path))
        except Exception as e:
            print(e)
            raise RuntimeError('Invalid url(wget from url fail reason(%s))' % e.message)

class WarpperGetter(object):
    def __init__(self, getter):
        self.getter = getter

    def __call__(self, source, path, file_name, force_clear=True):
        if force_clear:
            util.rm_dir(path)

        self.getter(source, path)

        for _, _, files in os.walk(path):
            for name in files:
                tmp_name = name

        source_path = os.path.join(path, tmp_name)
        dest_path = os.path.join(path, file_name)
        util.rename(source_path, dest_path)

def getterFactory(stype="http"):
    """The factory method"""
    getters = dict(http=HttpGetter)
    return WarpperGetter(getters[stype]())

