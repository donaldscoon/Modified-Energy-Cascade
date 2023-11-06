import matplotlib.pyplot as plt
import numpy as np
import cv2
import os
import LAI_functions as LAI
import LAI_canopy as LAI_c
import re


file_path = "Modified-Energy-Cascade/Computer Vision/test_images"
file_list = LAI.open_images(file_path)

# # Create a window to display images
# window_name = 'Input Output Comparison'
# cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

# # Set the initial size of the window
# window_width = 800  # Adjust the width as needed
# window_height = 600  # Adjust the height as needed
# cv2.resizeWindow(window_name, window_width, window_height)
pattern1 = re.compile(r'_A_')
pattern2 = re.compile(r'_T_')

for image in file_list:
    if re.search(pattern1, image):
        # # Mask and filter the images
        # display = cv2.imread(image)
        # red_masked = LAI.remove_red_area(image)
        # non_green_masked = LAI.remove_non_green_area(red_masked)
        # leaf_area, image_with_contours = LAI.calculate_leaf_area(non_green_masked)
        # print(f"Total leaf area in {image}: {leaf_area} square pixels")
        continue
    elif re.search(pattern2, image):
        display = cv2.imread(image)
        non_green_masked = LAI_c.canopy_remove_non_green_area(image)
        leaf_area, image_with_contours = LAI_c.canopy_calculate_leaf_area(non_green_masked)
        print(f"Total canopy area in {image}: {leaf_area} square pixels")
        plt.imshow(non_green_masked)
        plt.show()

#     # Stack the images horizontally
#     stacked_images = np.hstack((display, image_with_contours))

#     # Resize the stacked images to fit within the window
#     scale_percent = 1.0  # Set to 1.0 to fit within the window size
#     width = int(window_width * scale_percent)
#     height = int(window_height * scale_percent)
#     stacked_images = cv2.resize(stacked_images, (width, height))

#     # Display all images in the window
#     cv2.imshow(window_name, stacked_images)

#     # Add a delay between images to see the changes
#     cv2.waitKey(2000)  # Adjust the delay (milliseconds) as needed

# # Close the window when done
# cv2.destroyAllWindows()
