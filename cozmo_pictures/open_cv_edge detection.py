import cv2
import numpy as np
from matplotlib import pyplot as plt
import os
import time

os.mkdir("./edges")
for file in os.listdir("."):
    if file.endswith(".jpg"):
        print(os.path.join("/mydir", file))
        img = cv2.imread(file, 0)
        edges = cv2.Canny(img, 100, 200)

        #plt.subplot(121), plt.imshow(img, cmap='gray')
        #plt.title('Original Image'), plt.xticks([]), plt.yticks([])
        #plt.subplot(122), plt.imshow(edges, cmap='gray')
        #plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
        cv2.imwrite("./edges/" + file, edges)
        time.sleep(1)
