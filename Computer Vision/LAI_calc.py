import matplotlib.pyplot as plt
import numpy as np
import cv2
import os
import LAI_functions as LAI


file_path = "Modified-Energy-Cascade/Computer Vision/test_images"

file_list = LAI.open_images(file_path)

for image in file_list:
    # Mask and filter the images
    red_masked = LAI.remove_red_area(image)
    non_green_masked, contours = LAI.remove_non_green_area(red_masked)
    print(contours)
    plot = cv2.drawContours(non_green_masked, contours, -1, (0, 0, 0), 2)
    plt.imshow(plot)
    plt.show()


    leaf_area = LAI.calculate_leaf_area(non_green_masked)
    print(f"Total leaf area in {image}: {leaf_area} square pixels")
