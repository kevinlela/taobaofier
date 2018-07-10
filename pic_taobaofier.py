#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import fnmatch
import argparse
import errno
import traceback    
import sys
import random
sys.path.append("/Users/Kisecu/Library/Python/2.7/bin")

from skimage import data
from skimage.transform import resize
from skimage import io
from skimage import color as color
from skimage import img_as_float


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
    for root, dirnames, filenames in os.walk(directory):
        print filenames
        subfolder = root[root.find(directory) + len(directory) :]
        print subfolder
        for filename in filenames:
            full_path = os.path.join(root, filename)
            if file_is_match(full_path, pattern):
                matches.append(os.path.join(root, filename))
                subfolders.append(subfolder)
    return matches, subfolders

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def convert_rgb(img):
    nchannel = color.guess_spatial_dimensions(img)
    res = img
    if nchannel == 1 or nchannel == None:
        res = color.gray2rgb(img)
    elif nchannel == 4:
        res = img[:, :, 0:3]
    nchannel = res.shape[2]
    if nchannel == 4:
        res = img[:, :, 0:3]
    print res.shape
    return res

def resize_img(img, short_size):
    width = short_size
    height = short_size
    shape = img.shape
    nrows = shape[0] 
    ncols = shape[1] 
    print nrows, ncols
    if nrows < ncols:
        width = int(float(ncols)/float(nrows) * float(short_size))
    elif nrows > ncols:
        height = int(float(nrows)/float(ncols) * float(short_size))

    return resize(img, (height, width))

def add_water_mark(img, water_mark):
    shape = img.shape
    height = shape[0]
    width = shape[1]
    wm_shape = water_mark.shape
    wm_height = wm_shape[0]
    wm_width = wm_shape[1]

    if height < wm_height - 1 or width < wm_width - 1:
        print "water mark is larger than image"
        return img

    h_pos = random.randint(0, height - wm_height - 1)
    w_pos = random.randint(0, width - wm_width - 1)

    alpha = 0.8

    img = img_as_float(img)
    water_mark = img_as_float(water_mark)

    img[h_pos : h_pos + wm_height, w_pos : w_pos + wm_width, :] = alpha * img[h_pos : h_pos + wm_height, w_pos : w_pos + wm_width, :] + (1 - alpha) * water_mark
    
    return img

def main(folder_path, output_path):
    scale = 700
    all_img_files, subfolders = find_files(folder_path, ["*.jpg", "*.png", ".bmp"])
    
    print "reading warter mark"
    water_mark_img = io.imread("./water_mark/water_mark_0.png")
    wm = convert_rgb(water_mark_img)

    for idx, val in enumerate(all_img_files):
        try:
            img_file = all_img_files[idx]
            # read image
            print "processing: " + img_file + "\n"
            img = io.imread(img_file)

            # convert to 3 channel color image
            img = convert_rgb(img)
            
            
            # modify
            res = resize_img(img, scale)

            # add water mark
            res = add_water_mark(res, wm)

            # save image
            # get image name
            last_slash = img_file.rfind('/')
            last_slash = 0 if last_slash == -1 else last_slash
            img_name = img_file[last_slash:]
            img_dir = output_path + '/' + subfolders[idx]
            mkdir_p(img_dir)
            io.imsave(img_dir + '/' + img_name, res)
        except Exception as e:
            print str(e)
            print traceback.format_exc()
        # break

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='taobaofier')
    parser.add_argument('--input', required=True,
                        help='the path to you want to convert')
    parser.add_argument('--output', required=True,
                        help='the path to you want to store results')
    args = parser.parse_args()
    main(folder_path=args.input, output_path=args.output)

    