# -*- coding: utf-8 -*-
import os
import fnmatch
import argparse
import errno
import traceback    
import sys

def file_is_match(full_path, patterns):
    result = False
    for pattern in patterns:
        result = result or fnmatch.filter([full_path], pattern)
    return result

def find_files(directory, pattern=[]):
    if not os.path.exists(directory):
        raise ValueError("Directory not found {}".format(directory))

    matches = []
    subfolders = []
    all_file_names = []
    for root, dirnames, filenames in os.walk(directory):
        print filenames
        subfolder = root[root.find(directory) + len(directory) :]
        print subfolder
        for filename in filenames:
            full_path = os.path.join(root, filename)
            if file_is_match(full_path, pattern):
                matches.append(os.path.join(root, filename))
                subfolders.append(subfolder)
                all_file_names.append(filename)
    return matches, subfolders, all_file_names

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise