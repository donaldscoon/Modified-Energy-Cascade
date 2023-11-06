import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import cv2
import os
import LAI_functions as LAI
import LAI_canopy as LAI_c
import re
import csv

file_path = "C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/Computer Vision/test_images/"
file_list = LAI.open_images(file_path)
pattern1 = re.compile(r'_A_')
pattern2 = re.compile(r'_T_')
result_path = "C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/Computer Vision/results/"

# Create a dictionary to store the calculated areas with filenames (only the file name) as keys
area_data = {}

########################################################################################################################
############################# CALCULATING THE AREAS ####################################################################
########################################################################################################################

for image in file_list:
    original = cv2.imread(image)
    file_name = os.path.basename(image)  # Get just the file name
    if re.search(pattern1, image):      # this if statement calculates the total leaf area from those images
        # # processing the image
        # red_masked = LAI.remove_red_area(image)
        # non_green_masked = LAI.remove_non_green_area(red_masked)
        # leaf_area, image_result = LAI.calculate_leaf_area(non_green_masked)

        # # saving the results
        # area_data[file_name] = leaf_area
        # processed_image = LAI.display_images(original, image_result, leaf_area)
        # output_path = os.path.join(result_path, file_name)
        # cv2.imwrite(output_path, processed_image)
        # print(f"Total leaf area in {file_name}: {leaf_area} square pixels")
        continue
    elif re.search(pattern2, image):    # this elif statement calculates the total canopy area from those images
        # proccess the image
        non_green_masked = LAI_c.canopy_remove_non_green_area(image)
        canopy_area, image_with_contours, canopy_size = LAI_c.canopy_calculate_leaf_area(non_green_masked)

        # save the results
        area_data[file_name] = canopy_area
        processed_image = LAI.display_images(original, image_with_contours, canopy_area, canopy_size) #CANOPY SIZE??!?!?!?!??!
        output_path = os.path.join(result_path, file_name)
        cv2.imwrite(output_path, processed_image)
        print(f"Total canopy area in {file_name}: {canopy_area} square pixels")

########################################################################################################################
############################# SAVING THE AREAS #########################################################################
########################################################################################################################

# Specify the CSV file path
csv_file_path = os.path.join(result_path, "area_data.csv")

# Save the data to a CSV file
with open(csv_file_path, mode='w', newline='') as csv_file:
    fieldnames = ['Filename', 'Area']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    # Write the header row
    writer.writeheader()

    # Write the data
    for filename, area in area_data.items():
        writer.writerow({'Filename': filename, 'Area': area})

print(f"Area data saved to {csv_file_path}")