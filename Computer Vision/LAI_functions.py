
import matplotlib.pyplot as plt
import numpy as np
import cv2
import os
    
def calculate_leaf_area(image):

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

    # Create a black canvas of the same size as the original image
    black_canvas = np.zeros_like(image)

    # Draw the detected contours (leaves) on the black canvas
    cv2.drawContours(black_canvas, contours, -1, (255, 255, 255), thickness=cv2.FILLED)

    # Use a bitwise AND operation to combine the black canvas with the original image
    result_image = cv2.bitwise_and(image, black_canvas)
    # plt.imshow(result_image)
    # plt.show()

    leaf_area = 0

    for contour in contours:
        # Calculate the area of each contour
        area = cv2.contourArea(contour)
        leaf_area += area

    return leaf_area, result_image

def remove_red_area(image_path):
    # Read the image
    image = cv2.imread(image_path)
    # plt.imshow(image)
    # plt.show()

    # Convert the image to the HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define your red hue range
    lower_red = np.array([0, 100, 100])  # Lower range of red hue
    upper_red = np.array([10, 255, 255])  # Upper range of red hue

    # Create a mask for the red color
    red_mask = cv2.inRange(hsv, lower_red, upper_red)

    # Invert the mask to keep non-red areas
    non_red_mask = cv2.bitwise_not(red_mask)

    # Bitwise-AND the original image with the non-red mask to remove red regions
    red_masked = cv2.bitwise_and(image, image, mask=non_red_mask)

    return red_masked

def remove_non_green_area(red_masked):
    #Read the image
    image = red_masked
    
    # Convert the image to grayscale
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
    # contours2 = list(contours)

    # Draw the contours on a copy of the original image
    image_with_contours = image.copy()
    cv2.drawContours(image_with_contours, contours, -1, (0, 255, 0), 2)  # -1 draws all contours

    # List to store contours with HSV values outside the green range
    non_green_contours = []

    for contour in contours:
        # Calculate the average HSV values within the contour
        mask = np.zeros_like(gray)  # Create a single-channel grayscale mask
        cv2.drawContours(mask, [contour], -1, 255, thickness=cv2.FILLED)
        masked_hsv = cv2.bitwise_and(hsv, hsv, mask=mask)
        # plt.imshow(masked_hsv)
        # plt.show()

        # Calculate the mean HSV values within the contour
        non_zero_pixels = cv2.findNonZero(mask)
        if non_zero_pixels is not None:
            total_hsv = np.zeros(3)
            for pixel in non_zero_pixels:
                x, y = pixel[0]
                total_hsv += masked_hsv[y, x]
            average_hsv = total_hsv / len(non_zero_pixels)
        else:
            average_hsv = np.array([0, 0, 0])

        # Print the mean HSV values
        # print("Average HSV values within the contour: ", average_hsv)
        if not lower_green[1] <= average_hsv[1] <= upper_green[1]:
            # print(average_hsv, "out of range")
            non_green_contours.append(contour)

    # convert the non_green contours to an array
    non_green_contours = np.array(non_green_contours, dtype=object)
    
    # Create a black canvas of the same size as the original image
    black_canvas = np.zeros_like(image)


    # Draw the remaining contours on the image
    image_with_filtered_contours = image.copy()
    non_green_masked = cv2.drawContours(image_with_filtered_contours, non_green_contours, -1, (0, 0, 0), thickness=cv2.FILLED)
    # plt.imshow(non_green_masked)
    # plt.show()

    return non_green_masked

def open_images(path):
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

def display_images(original, result, area, canopy_size=None):
    # Create a subplot with two columns
    plt.figure(figsize=(12, 6))

    # Display the original image on the left
    plt.subplot(1, 2, 1)
    plt.imshow(cv2.cvtColor(original, cv2.COLOR_BGR2RGB))
    plt.title("Original Image")

    # Display the result image on the right
    plt.subplot(1, 2, 2)

    # Add the area to the top right corner of the result image
    text = f"Area: {area} square pixels"
    cv2.putText(result, text, (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 5, (255, 255, 255), 8)
    # if canopy_size is not None:
    #     # Draw a bounding circle based on the canopy size
    #     (x, y), radius = canopy_size
    #     cv2.circle(result, (int(x), int(y)), int(radius), (0, 0, 255), 5)  # Red circle

    plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
    plt.title("Processed Image")

    # Capture the processed image
    processed_image = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)

    # plt.show()

    return processed_image

def bounding_box(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply a binary threshold
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)

    # Find contours in the binary image
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # plt.imshow(contours)
    # plt.show()

    # Iterate through contours and find the bounding box for the largest contour
    max_contour = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(max_contour)

    # Draw a rectangle around the plant
    boxed = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 6)

    # Write the values of w and h on the image
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(boxed, f'Width: {w}', (x, y - 10), font, 4, (0, 0, 255), 6)
    # cv2.putText(boxed, f'Height: {h}', (x, y - 30), font, 4, (0, 0, 255), 6)

    # Write height vertically
    text_height = f'Height: {h}'
    for i, char in enumerate(text_height):
        cv2.putText(boxed, char, (x + w + 10, y + i * 100), font, 4, (0, 0, 255), 6, cv2.LINE_AA)

    # Display the result
    # plt.imshow(boxed)
    # plt.show()

    return boxed, w, h

# if __name__ == "__main__":
#     image_path = "C:/Users/donal/Documents/GitHub/Modified-Energy-Cascade/Computer Vision/Rex-Leaves.jpg"
#     red_masked = remove_red_area(image_path)
#     non_green_masked = remove_non_green_area(red_masked)
#     leaf_area, result_image = calculate_leaf_area(non_green_masked)
#     print(f"Total leaf area in {image_path}: {leaf_area} square pixels")