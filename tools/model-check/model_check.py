#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import json
import sys
import argparse
import base64
import traceback
import tempfile

sys.path.append("./core/")
import checker
import getter
import util

class ModelChecker(object):
    def __init__(self, url, local_path, framework):
        self.model_type = framework
        self.source = {}
        self.source["url"] = url
        self.pkg_name = ""
        self.model_path = local_path
        self.type = "http"

    def run(self):
        # download model-pkg from http or s3
        from sys import version_info
        if version_info.major == 2:
            from urlparse import urlparse
            parsed_result=urlparse(self.source["url"])
        else:
            from urllib import parse
            parsed_result=parse.urlparse(self.source["url"])
        print("%s"% str(parsed_result))
        self.pkg_name = parsed_result.path.split('/')[-1]

        getter.getterFactory(self.type)(self.source,
                                               self.model_path,
                                               self.pkg_name)
        # uncompress model-pkg to model_path
        util.uncompress(os.path.join(self.model_path, self.pkg_name), self.model_path)

        # filter hidden files or MAC special dirs
        util.filter(self.model_path)

        # check dir structure
        checker.dirCheckerFactory(self.model_type)(self.model_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', required=True, help='model package s3 url')
    parser.add_argument("--framework", required=True, help="pytorch or tensorflow")
    args = parser.parse_args()
    print(args)

    try:
        p = ModelChecker(args.url, tempfile.mkdtemp(), args.framework)
        p.run()
        print("model check success")

    except Exception as e:
        msg = traceback.format_exc()
        print(e)
        print("model check fail")
        print("Trace : %s", msg)
