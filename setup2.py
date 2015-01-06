#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2015 Vladimir Strackovski vlado@nv3.org
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, dis-
# tribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the fol-
# lowing conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABIL-
# ITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#

"""
  backup setup tool
  ~~~~~~~~~~~~~~~~~~
    Simple backup tool
    Author: Vladimir Strackovski <vlado@nv3.org>
"""

__author__ = 'vstrackovski'

import json
import os
import sys


def prompt_user():
    source = raw_input("Absolute path to source dir: ")
    source_name = os.path.basename(os.path.normpath(source))
    config = {}
    destinations = {}
    local_destinations = []
    s3_buckets = []
    config['source'] = source
    config['source_name'] = source_name

    local = raw_input('Absolute path to local destination dir: ')
    if len(local) > 0:
        local_destinations.append(local)
        while query_yes_no("Add another local destination?", "no"):
            local_destinations.append(raw_input("Path: "))

    s3_bucket = raw_input('S3 Bucket name: ')
    if len(s3_bucket) > 0:
        s3_buckets.append(s3_bucket)
        while query_yes_no("Add another bucket?", "no"):
            s3_buckets.append(raw_input("Bucket: "))

    destinations['local'] = local_destinations
    destinations['s3'] = s3_buckets
    config['destinations'] = destinations

    return config


def query_yes_no(question, default="yes"):
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


configs = []
config = prompt_user()
configs.append(config)
while query_yes_no("Add another source?", "no"):
    configs.append(prompt_user())

print configs

configFile = open('config2.json', 'w')
json.dump(configs, configFile, ensure_ascii=True)