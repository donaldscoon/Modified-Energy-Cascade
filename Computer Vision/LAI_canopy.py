
import matplotlib.pyplot as plt
import numpy as np
import cv2
import os
    
def canopy_calculate_leaf_area(image):

    # # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (11, 11), 0)

    # Threshold the image to segment the leaves
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Convert the image to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define your green hue range
    lower_green = np.array([35, 50, 50])
    upper_green = np.array([85, 255, 255])

    # Create a green mask based on the HSV values
    green_mask = cv2.inRange(hsv, lower_green, upper_green)

    # Perform a logical OR operation to combine the threshold and green mask
    combined_mask = cv2.bitwise_or(thresh, green_mask)

    # Find contours in the combined thresholded image
    contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw the contours on a copy of the original image
    image_with_contours = image.copy()
    cv2.drawContours(image_with_contours, contours, -1, (0, 255, 0), 2)  # -1 draws all contours

    # Stack the original image, thresholded image, green mask, and canvas horizontally
    stacked_images = np.hstack((image, image_with_contours))

    # # Resize the stacked images to a smaller ratio
    # scale_percent = 50  # Adjust this percentage as needed
    # width = int(stacked_images.shape[1] * scale_percent / 100)
    # height = int(stacked_images.shape[0] * scale_percent / 100)
    # stacked_images = cv2.resize(stacked_images, (width, height))

    # # Display all images in the same window
    # cv2.imshow('Images Comparison', stacked_images)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    leaf_area = 0

    for contour in contours:
        # Calculate the area of each contour
        area = cv2.contourArea(contour)
        leaf_area += area

    return leaf_area, image_with_contours

# def remove_red_area(image_path):
#     # Read the image
#     image = cv2.imread(image_path)

#     # Convert the image to the HSV color space
#     hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

#     # Define your red hue range
#     lower_red = np.array([0, 100, 100])  # Lower range of red hue
#     upper_red = np.array([10, 255, 255])  # Upper range of red hue

#     # Create a mask for the red color
#     red_mask = cv2.inRange(hsv, lower_red, upper_red)

#     # Invert the mask to keep non-red areas
#     non_red_mask = cv2.bitwise_not(red_mask)

#     # Bitwise-AND the original image with the non-red mask to remove red regions
#     red_masked = cv2.bitwise_and(image, image, mask=non_red_mask)

#     return red_masked

def canopy_remove_non_green_area(image_path):
    #Read the image
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (11, 11), 0)
    
    # Convert the image to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define your green hue range
    lower_green = np.array([35, 50, 50])
    upper_green = np.array([85, 255, 255])

    # Create a green mask based on the HSV values
    green_mask = cv2.inRange(hsv, lower_green, upper_green)
    # plt.imshow(green_mask)
    # plt.show()

    # Find contours in the combined thresholded image
    contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # contours2 = list(contours)
    
    # Create a black canvas of the same size as the original image
    black_canvas = np.zeros_like(image)

    # Draw filled contours on the black canvas
    cv2.drawContours(black_canvas, contours, -1, (255, 255, 255), thickness=cv2.FILLED)

    # Use a bitwise AND operation to combine the black canvas with the original image
    non_green_masked = cv2.bitwise_and(image, black_canvas)
    # plt.imshow(non_green_masked)
    # plt.show()


    return non_green_masked

def canopy_open_images(path):
    folder_path = path

    # Ensure the folder path is valid
    if os.path.exists(folder_path):
        file_list = []
        
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            
            # Check if it's a file (not a subdirectory)
            if os.path.isfile(file_path):
                file_list.append(file_path)
        
        # Now, file_list contains the paths to all files in the specified folder.

    else:
        print(f"The folder path '{folder_path}' does not exist.")
    
    return file_list

if __name__ == "__main__":
    image_path = "C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/Computer Vision/test_images/H5_T_Muir_1.21_03.30.22.JPG"
    # red_masked = remove_red_area(image_path)
    non_green_masked = remove_non_green_area(image_path)
    leaf_area = calculate_leaf_area(non_green_masked)
    print(f"Total leaf area in {image_path}: {leaf_area} square pixels")