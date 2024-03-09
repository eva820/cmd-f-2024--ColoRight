import cv2
import numpy as np
# for i in range(1,6):
i = 1
image = cv2.imread(f'map{i}.png')
# cv2.imshow('current image',img)
# cv2.waitKey()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Find Canny edges
edged = cv2.Canny(gray, 10,20)
cv2.waitKey(0)

# Finding Contours
# Use a copy of the image e.g. edged.copy()
# since findContours alters the image
contours, hierarchy = cv2.findContours(edged,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

# Filter contours that are closely aligned to rectangles
min_area = image.size//3000 # Minimum area threshold for the contour
max_area = image.size//30  # Maximum area threshold for the contour
max_epsilon = 0.03  # Maximum approximation accuracy for the polygon (adjust as needed)

rect_contours = []
for contour in contours:
    area = cv2.contourArea(contour)
    if min_area < area < max_area:
        perimeter = cv2.arcLength(contour, True)
        epsilon = max_epsilon * perimeter
        approx = cv2.approxPolyDP(contour, epsilon, True)
        if len(approx) == 4:  # Check if the contour is a quadrilateral
            dist1 = np.linalg.norm(approx[1]-approx[2])
            dist2 = np.linalg.norm(approx[0]-approx[3])
            dist3 = np.linalg.norm(approx[0]-approx[1])
            dist4 = np.linalg.norm(approx[2]-approx[3])
            if abs(dist2-dist1)<=dist1*0.4 and abs(dist4-dist3)<=dist4*0.4:
                rect_contours.append(approx)
                break

cv2.drawContours(image, rect_contours, -1, (0, 255, 0), 2)
resized_image = cv2.resize(image, (image.shape[1] // 2, image.shape[0] // 2))
cv2.imshow('Rectangular Contours', resized_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# show the cropped color bar
grid = rect_contours[0]
box = [np.min(grid[:,0,1]), np.max(grid[:,0,1]),np.min(grid[:,0,0]),np.max(grid[:,0,0])]

image = cv2.imread(f'map{i}.png')
img = image[box[0]:box[1], box[2]:box[3]]

cv2.imshow('Rectangular Contours', img)
cv2.waitKey(0)
cv2.destroyAllWindows()