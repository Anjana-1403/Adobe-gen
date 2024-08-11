import cv2
import numpy as np

def detect_shape(contour):
    approx = cv2.approxPolyDP(contour, 0.04 * cv2.arcLength(contour, True), True)
    shape = "Unidentified"
    
    if len(approx) == 2:
        shape = "Straight Line"
    elif len(approx) == 3:
        shape = "Triangle"
    elif len(approx) == 4:
        (x, y, w, h) = cv2.boundingRect(approx)
        aspect_ratio = w / float(h)
        if 0.95 <= aspect_ratio <= 1.05:
            shape = "Square"
        else:
            shape = "Rectangle"
    elif len(approx) >= 5:
        area = cv2.contourArea(contour)
        (x, y), radius = cv2.minEnclosingCircle(contour)
        circle_area = np.pi * (radius ** 2)
        if abs(area - circle_area) < 0.1 * circle_area:
            shape = "Circle"
        else:
            ellipse = cv2.fitEllipse(contour)
            shape = "Ellipse"
    else:
        hull = cv2.convexHull(approx)
        if len(approx) == len(hull):
            shape = "Regular Polygon"
        else:
            shape = "Star"

    return shape

image = cv2.imread(r'problems\problems\occlusion2_rec.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(blurred, 50, 150)

contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for contour in contours:
    shape = detect_shape(contour)
    print(f"Detected shape: {shape}")
    
    cv2.drawContours(image, [contour], -1, (0, 255, 0), 2)
    cv2.putText(image, shape, (contour[0][0][0] - 10, contour[0][0][1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

cv2.imshow("Detected Shapes", image)
cv2.waitKey(0)
cv2.destroyAllWindows()