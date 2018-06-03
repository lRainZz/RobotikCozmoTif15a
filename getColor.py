import numpy as np
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to the image")
args = vars(ap.parse_args())

## 0=red 1=green 2=blue -1=error
def getColor(image, Y, X):
    #red, green. blue
    boundaries = [
	    ([0, 0, 100], [100, 130, 255]),
	    ([0, 100, 0], [130, 255, 100]),
	    ([100, 0, 0], [255, 100, 130]),
    ]
    #red = [([0, 0, 100], [100, 130, 255])]
    #green = [([0, 100, 0], [130, 255, 100])]
    #blue = [([100, 0, 0], [255, 100, 130])]
    
    # load the image
    image = cv2.imread(image)
    # Load the pixel    
    pixel = image[Y,X]

    i = 0
    #test the color
    for (lower, upper) in boundaries:
        lower = np.array(lower, dtype = "uint8")
        upper = np.array(upper, dtype = "uint8")

        if inRange(pixel, lower, upper):
            print (i)
            return i
        i += 1

    print ("-1")
    return -1

## if color is in Range = true
def inRange(toTest, lower, upper):
    if lower[0] <= toTest[0] <= upper[0]:
        if lower[1] <= toTest[1] <= upper[1]:
            if lower[2] <= toTest[2] <= upper[2]:
                return True
    return False




getColor(args["image"], 10, 10)