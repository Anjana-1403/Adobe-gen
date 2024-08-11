import cv2
import numpy as np
import matplotlib.pyplot as plt

def load_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError("Image not found or the path is incorrect")
    return img

def preprocess_image(img):
    blurred = cv2.GaussianBlur(img, (5, 5), 0)
    
    edges = cv2.Canny(blurred, threshold1=50, threshold2=150)
    
    dilated = cv2.dilate(edges, None, iterations=1)
    
    return dilated

def find_and_draw_contours(img):
    contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    contour_img = np.zeros_like(img)
    
    cv2.drawContours(contour_img, contours, -1, (255, 255, 255), 2)
    
    return contour_img

def complete_contours(img):
    kernel = np.ones((5, 5), np.uint8)
    closed = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel, iterations=2)
    
    return closed

def main(image_path):
    img = load_image(image_path)
    
    preprocessed_img = preprocess_image(img)
    
    contour_img = find_and_draw_contours(preprocessed_img)
    
    completed_img = complete_contours(contour_img)
    
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.title("Original Image")
    plt.imshow(img, cmap='gray')
    
    plt.subplot(1, 2, 2)
    plt.title("Completed Image")
    plt.imshow(completed_img, cmap='gray')
    plt.show()

# Path to your image
image_path = r'D:\Adobe-gen\problems\problems\occlusion2_rec.png'

main(image_path)