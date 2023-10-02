from PIL import Image

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2

# Importing image data into Numpy arrays
# img = np.asarray(Image.open("Modified-Energy-Cascade/Computer Vision/test_foreground.jpg"))
# print(repr(img)) # prints the raw aray
# plt.imshow(img) # plots the "array image"

# # Applying pseudocolor schemes to image plots
# lum_img = img[:, :, 0] 
# plt.imshow(lum_img, cmap="hot") # there are many cmaps, type one that doesn't exist and it give you a list of them!

# imgplot = plt.imshow(lum_img)
# imgplot.set_cmap('nipy_spectral')
# plt.colorbar()
# plt.show()

# # Examining a specific data range
# plt.hist(lum_img.ravel(), bins=range(256), fc="k", ec="k") #.ravel() Return a contiguous flattened array.
# # plt.imshow(lum_img, clim=(0, ###))
# plt.show()


# read image in BGR
img = cv2.imread('Modified-Energy-Cascade/Computer Vision/test_foreground.jpg')
plt.subplot(1,2,1)
plt.imshow(img)


# convert to LAB space
# Applying a threshold to detect green color can be performed quite easily using LAB color space.
# check out https://stackoverflow.com/questions/47483951/how-can-i-define-a-threshold-value-to-detect-only-green-colour-objects-in-an-ima
lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

# store the a-channel
a_channel = lab[:,:,1]

# Automate threshold using Otsu method
th = cv2.threshold(a_channel,127,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)[1]

# Mask the result with the original image
masked = cv2.bitwise_and(img, img, mask = th)

plt.subplot(1,2,2)
plt.imshow(masked)
plt.show()


