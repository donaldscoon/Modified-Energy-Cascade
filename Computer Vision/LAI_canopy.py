
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
    leaf_area = 0
    canopy_size = []

    for contour in contours:
        # Calculate the area of each contour
        area = cv2.contourArea(contour)
        leaf_area += area

        # # Calculate the enclosing circle for each contour
        # (x, y), radius = cv2.minEnclosingCircle(contour)
        # canopy_size.append((int(radius), int(radius)))
        # print(canopy_size)
    return leaf_area, image_with_contours, canopy_size

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


# if __name__ == "__main__":
#     image_path = "C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/Computer Vision/test_images/H5_T_Muir_1.21_03.30.22.JPG"
#     # red_masked = remove_red_area(image_path)
#     non_green_masked = remove_non_green_area(image_path)
#     leaf_area = calculate_leaf_area(non_green_masked)
#     print(f"Total leaf area in {image_path}: {leaf_area} square pixels")