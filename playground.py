import matplotlib.pyplot as plt
import skimage
from skimage import io
from skimage import filters
import numpy as np

import matplotlib
matplotlib.rcParams['xtick.major.size'] = 0
matplotlib.rcParams['ytick.major.size'] = 0
matplotlib.rcParams['xtick.labelsize'] = 0
matplotlib.rcParams['ytick.labelsize'] = 0

original_image = skimage.img_as_float(io.imread("../test_in/IMG_20180407_153328.jpg"))

plt.imshow(original_image)
plt.show()