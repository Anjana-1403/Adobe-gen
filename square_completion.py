import cv2
import numpy as np

def complete_square(image):
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image

    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    edges = cv2.Canny(blurred, 50, 150)

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    completed_image = np.zeros_like(gray)

    for contour in contours:
        if cv2.contourArea(contour) < 100: 
            continue

        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, False)

        x, y, w, h = cv2.boundingRect(approx)

        cv2.rectangle(completed_image, (x, y), (x+w, y+h), 255, 2)

        cv2.drawContours(completed_image, [contour], -1, 255, 1)

    return completed_image

image = cv2.imread(r"C:\Users\ANJANA\OneDrive\Pictures\Screenshots\Screenshot 2024-08-10 225327.png", cv2.IMREAD_GRAYSCALE)

result = complete_square(image)

cv2.imshow("Completed Shape", result)
cv2.waitKey(0)
cv2.destroyAllWindows()