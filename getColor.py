import numpy as np
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to the image")
args = vars(ap.parse_args())

## Y1 X1 = start, X2 Y2 = end 
## 0=red 1=green 2=blue -1=error
def getColorInRange(image, X1, Y1, X2, Y2):

    #save raw image to file
    raw_rgb = np.array(image)
    cv2.imwrite('color_detect_pic.jpg', raw_rgb)
    image = cv2.imread('color_detect_pic.jpg')

    print("LEFT: " + str(X1) + ", " + str(Y1))
    print("RIGHT: " + str(X2) + ", " + str(Y2))

    red = 0
    green = 0
    blue = 0
    if Y1 <= Y2 and X1 <= X2:
        for i in range(X1, X2):
            for j in range(Y1, Y2):
                h = getColor(image, i, j)
                if h == 0:
                    red += 1
                if h == 1:
                    green += 1
                if h == 2:
                    blue += 1
    
    if red > green and red > blue:
        #print("getColorInRange:0")
        return 0
    if green > red and green > blue:
        #print("getColorInRange:1")
        return 1
    if blue > red and blue > green:
        #print("getColorInRange:2")
        return 2

    #print("getColorInRange:-1")
    return -1

## 0=red 1=green 2=blue -1=error
def getColor(image, X, Y):
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
    # image = cv2.imread(image)
    # Load the pixel 
    pixel = image[Y,X]

    i = 0
    #test the color
    for (lower, upper) in boundaries:
        lower = np.array(lower, dtype = "uint8")
        upper = np.array(upper, dtype = "uint8")

        if inRange(pixel, lower, upper):
            #print (i)
            return i
        i += 1

    #print ("-1")
    return -1

## if color is in Range = true
def inRange(toTest, lower, upper):
    if lower[0] <= toTest[0] <= upper[0]:
        if lower[1] <= toTest[1] <= upper[1]:
            if lower[2] <= toTest[2] <= upper[2]:
                return True
    return False