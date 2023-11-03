import cv2
import numpy as np
import matplotlib.pyplot as plt

# def calculate_leaf_area(image):
#     # Create a new blank canvas for displaying images
#     canvas = np.zeros_like(image)

#     # Convert the image to grayscale
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#     # Apply Gaussian blur to reduce noise
#     blurred = cv2.GaussianBlur(gray, (11, 11), 0)

#     # Threshold the image to segment the leaves
#     _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

#     # Convert the image to HSV color space
#     hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

#     # Define your green hue range
#     lower_green = np.array([35, 50, 50])
#     upper_green = np.array([85, 255, 255])

#     # Create a green mask based on the HSV values
#     green_mask = cv2.inRange(hsv, lower_green, upper_green)

#     # Perform a logical OR operation to combine the threshold and green mask
#     combined_mask = cv2.bitwise_or(thresh, green_mask)

#     # Find contours in the combined thresholded image
#     contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#     # Draw the contours on a copy of the original image
#     image_with_contours = image.copy()
#     cv2.drawContours(image_with_contours, contours, -1, (0, 255, 0), 2)  # -1 draws all contours
#     # plt.imshow(image_with_contours)
#     # plt.show()

#     # List to store contours with HSV values outside the green range
#     non_green_contours = []

#     for contour in contours:
#         # Calculate the average HSV values within the contour
#         print(contour)
#         image_with_contour = image.copy()
#         cv2.drawContours(image_with_contour, contour, -1, (0, 255, 0), 2)  # -1 draws all contours
#         plt.imshow(image_with_contour)
#         plt.show()
#         # Get the HSV values within a contout
#         # Print the mean HSV values
#         # print("Average HSV values within the contour: ", average_hsv)

#         # Check if the average HSV values fall outside the green range
#         # if not (lower_green <= average_hsv <= upper_green).all():
#         #     non_green_contours.append(contour)

#     # Remove the non-green contours from the original contours variable


#     # Draw the remaining contours on the image

#     # Optionally, display the image with filtered contours

#     # Calculate and return the total leaf area (contours with green HSV values)
def calculate_leaf_area(image):
    # Create a new blank canvas for displaying images
    canvas = np.zeros_like(image)

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
    # contours = list(contours)

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

    # adjust the 
    non_green_contours = np.array(non_green_contours, dtype=object)

    # Create a new list to store the filtered contours
    filtered_contours = []

    # Iterate through the original contours
    for contour in filtered_contours:
        print(contour)

    # Update the contours variable with the filtered contours
    contours = filtered_contours

    # Draw the remaining contours on the image
    image_with_filtered_contours = image.copy()
    cv2.drawContours(image_with_filtered_contours, non_green_contours, -1, (0, 0, 0), thickness=cv2.FILLED)

    # Optionally, display the image with filtered contours
    cv2.imshow('Image with Filtered Contours', image_with_filtered_contours)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Calculate and return the total leaf area (contours with green HSV values)
    total_area = 0
    for contour in contours:
        area = cv2.contourArea(contour)
        total_area += area

    # return total_area
if __name__ == "__main__":
    image_path = "Modified-Energy-Cascade/Computer Vision/Rex-Leaves.jpg"
    image = cv2.imread(image_path)
    leaf_area = calculate_leaf_area(image)
    print(f"Total leaf area in {image_path}: {leaf_area} square pixels")
