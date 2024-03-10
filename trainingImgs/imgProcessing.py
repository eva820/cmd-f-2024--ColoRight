import cv2
import numpy as np
import matplotlib.colors as mcolors
from skimage import io
from skimage.color import rgb2lab, deltaE_cie76

for i in range(4,5):
    filepath = f'map{i}.png'
    image = cv2.imread(filepath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Find Canny edges
    edged = cv2.Canny(gray, 10,20)
    cv2.waitKey(0)
    contours, hierarchy = cv2.findContours(edged,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    min_area = image.size//3000
    max_area = image.size//30
    max_epsilon = 0.03

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

    image = cv2.imread(filepath)
    img = image[box[0]:box[1], box[2]:box[3]]

    if img.shape[0]>img.shape[1]:
        # colorLine = np.mean(img,axis = 1).astype(int)
        colorLine = img[:,img.shape[1]//2,:]
        print(colorLine)
    else:
        # colorLine = np.mean(img,axis = 0).astype(int)
        colorLine = img[img.shape[0]//2,:,:]
        print(colorLine)

    samples = 19
    newcolor = []
    i = 0
    while(sum(colorLine[i])>=253*3):
        i=i+1
        print(i)
    newcolor.append(colorLine[i])
    j = i
    for i in range(samples):
        newcolor.append(colorLine[int(len(colorLine)/samples*(i+1))-1])
    # newcolor.append(colorLine[len(colorLine)-1])
    newcolor.append(colorLine[len(colorLine)-1])
    newcolor.append(newcolor[19])
    colorLine = newcolor
    def rgb_to_hex(rgb):
        r = max(0, min(255, int(rgb[0])))
        g = max(0, min(255, int(rgb[1])))
        b = max(0, min(255, int(rgb[2])))
        return "#{:02x}{:02x}{:02x}".format(r, g, b)
    def hex_to_rgb(hex_color):
        """Convert a hexadecimal color code to RGB."""
        # Remove the '#' prefix if present
        hex_color = hex_color.lstrip('#')
        # Convert the hexadecimal string to RGB components
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return [r, g, b]

    colorHex = list(dict.fromkeys([rgb_to_hex(x) for x in colorLine]))
    colorLine = [hex_to_rgb(x) for x in colorHex]
    print(colorLine)

    def jet_colormap(n,palet):
        if palet == 0:
            colors = [(0,[0.35,0.7,0.9]),(0.5,[0,0.6,0.5]),(0.75,[0.95,0.9,0.25]),(1,[0.9,0.6,0])]
        elif palet == 1:
            colors = [(0, [0,0,1]), (1, [1,0,0])]
        cmap = mcolors.LinearSegmentedColormap.from_list("jet_custom", colors, N=n)
        colors_list = [list([int(x*255) for x in cmap(i)[0:3]]) for i in np.linspace(0, 1, n)]
        return colors_list

    cmap = jet_colormap(len(colorHex),0)

    rgb = io.imread(filepath)[:,:,0:3]
    lab = rgb2lab(rgb)

    for i in range(0,len(colorLine)):
        color3d = np.uint8(np.asarray([[colorLine[i][::-1]]]))
        if i == 0:
            print(colorLine[i])
            colorPrev = np.uint8(np.asarray([[colorLine[i+1][::-1]]]))
        else:
            colorPrev = np.uint8(np.asarray([[colorLine[i-1][::-1]]]))
        thres = deltaE_cie76(rgb2lab(colorPrev),rgb2lab(color3d))*3//4
        colorDist = deltaE_cie76(rgb2lab(color3d), lab)
        if sum(colorLine[i])<250*3:
            rgb[colorDist<thres] = cmap[i]

    whiteDist = deltaE_cie76(rgb2lab([[[255, 255, 255]]]), lab)
    rgb[whiteDist<30] = [255,255,255]
    io.imshow(rgb)
    io.show()

'''

def rgb_to_hex(rgb):
    r = max(0, min(255, int(rgb[0])))
    g = max(0, min(255, int(rgb[1])))
    b = max(0, min(255, int(rgb[2])))
    return "#{:02x}{:02x}{:02x}".format(r, g, b)

colorLine = list(dict.fromkeys([rgb_to_hex(x) for x in colorLine]))

def jet_colormap(n,palet):
    if palet !=1:
        colors = [(0, [0,0,1]), (1, [1,0,0])]
    cmap = mcolors.LinearSegmentedColormap.from_list("jet_custom", colors, N=n)
    colors_list = [list([int(x*255) for x in cmap(i)[0:3]]) for i in np.linspace(0, 1, n)]
    print(colors_list)
    return colors_list

cmap = jet_colormap(len(colorLine),0)

color_mapping = dict(zip(colorLine,cmap))

# Define the mapping function
def map_color(pixel):
    if pixel in color_mapping:
        return color_mapping[pixel]
    else:
        return pixel  # No modification

img = cv2.imread(f'map{i}.png')
for y in range(img.shape[0]):
    for x in range(img.shape[1]):
        hh = rgb_to_hex(img[y][x][:])
        if hh in color_mapping:
            img[y][x][:] = color_mapping[hh]

cv2.imshow('Rectangular Contours', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

'''