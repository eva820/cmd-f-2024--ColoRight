import numpy as np
from skimage import io
from skimage.color import rgb2lab, deltaE_cie76

rgb = io.imread('map2.png')[:,:,0:3]
lab = rgb2lab(rgb)

green = [97,174,253]
magenta = [106, 217, 166]

threshold_green = 50
threshold_magenta = 50

green_3d = np.uint8(np.asarray([[green]]))
magenta_3d = np.uint8(np.asarray([[magenta]]))

dE_green = deltaE_cie76(rgb2lab(green_3d), lab)
dE_magenta = deltaE_cie76(rgb2lab(magenta_3d), lab)

rgb[dE_magenta < threshold_magenta] = np.uint8(np.asarray([[[0,0,0]]]))
io.imshow(rgb)
io.show()
rgb[dE_green < threshold_green] = np.uint8(np.asarray([[[0,0,255]]]))
io.imshow(rgb)
io.show()

