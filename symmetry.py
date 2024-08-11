import cv2
import numpy as np
import matplotlib.pyplot as plt

def find_center_of_shapes(contours):
    # Find the bounding box that encompasses all contours
    x_min, y_min, x_max, y_max = float('inf'), float('inf'), 0, 0
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        x_min = min(x_min, x)
        y_min = min(y_min, y)
        x_max = max(x_max, x + w)
        y_max = max(y_max, y + h)
    
    # Calculate the center of the bounding box
    center_x = (x_min + x_max) // 2
    center_y = (y_min + y_max) // 2
    
    return center_x, center_y

def draw_vertical_line(image, x):
    # Draw a vertical line at x position
    h, w = image.shape
    cv2.line(image, (x, 0), (x, h), (255, 255, 255), 2)

def check_symmetry(image, center_x):
    # Split the image into left and right halves
    left_half = image[:, :center_x]
    right_half = image[:, center_x:]
    
    # Flip the right half horizontally
    right_half_flipped = cv2.flip(right_half, 1)
    
    # Resize the halves to be the same size
    if left_half.shape[1] != right_half_flipped.shape[1]:
        min_width = min(left_half.shape[1], right_half_flipped.shape[1])
        left_half = left_half[:, :min_width]
        right_half_flipped = right_half_flipped[:, :min_width]
    
    # Calculate the absolute difference between the halves
    difference = cv2.absdiff(left_half, right_half_flipped)
    _, difference_thresh = cv2.threshold(difference, 30, 255, cv2.THRESH_BINARY)
    
    # Calculate the sum of differences
    difference_sum = np.sum(difference_thresh)
    symmetry_score = 1 - (difference_sum / (image.shape[0] * center_x * 255))
    
    return symmetry_score > 0.90, symmetry_score

IMG = r'D:\Adobe-gen\symmetry_check.png'
thresh = cv2.imread(IMG, 0)

if thresh is None:
    print(f"Error: File {IMG} not found or could not be read.")
else:
    # Find contours of the shapes
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    print(f"Number of contours found: {len(contours)}")
    
    # Find the center of the shapes
    center_x, center_y = find_center_of_shapes(contours)
    print(f"Center of shapes: ({center_x}, {center_y})")
    
    # Draw vertical line through the center
    draw_vertical_line(thresh, center_x)
    
    # Check symmetry
    symmetric, score = check_symmetry(thresh, center_x)
    print(f"Symmetric: {symmetric}")
    print(f"Symmetry Score: {score:.6f}")
    
    # Display the result
    plt.imshow(thresh, cmap='gray')
    plt.title(f"Symmetry Score: {score:.6f}")
    plt.show()