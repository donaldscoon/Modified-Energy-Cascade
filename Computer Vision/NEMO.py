import matplotlib.pyplot as plt
import numpy as np
import cv2

# https://realpython.com/python-opencv-color-spaces/

nemo = cv2.imread('C:/Users/donal/Documents/GitHub/Computer Vision Class/NEMO EX/nemo0.jpg')
nemo = cv2.cvtColor(nemo, cv2.COLOR_BGR2RGB)

plt.imshow(nemo)
plt.show()

hsv_nemo = cv2.cvtColor(nemo, cv2.COLOR_RGB2HSV)

plt.imshow(hsv_nemo)
plt.show()

light_orange = (1, 190, 200)
dark_orange = (18, 255, 255)

mask = cv2.inRange(hsv_nemo, light_orange, dark_orange)
plt.imshow(mask)

result = cv2.bitwise_and(nemo, nemo, mask=mask)

plt.subplot(1,2,1)
plt.imshow(mask, cmap="gray")
plt.subplot(1,2,2)
plt.imshow(result)
plt.show()

light_white = (0, 0, 200)
dark_white = (145, 60, 255)
mask_white = cv2.inRange(hsv_nemo, light_white, dark_white)
result_white = cv2.bitwise_and(nemo, nemo, mask=mask_white)
plt.subplot(1, 2, 1)
plt.imshow(mask_white, cmap="gray")
plt.subplot(1, 2, 2)
plt.imshow(result_white)
plt.show()
final_mask = mask + mask_white
final_result = cv2.bitwise_and(nemo, nemo, mask=final_mask)
plt.subplot(1, 2, 1)
plt.imshow(final_mask, cmap="gray")
plt.subplot(1, 2, 2)
plt.imshow(final_result)
plt.show()
