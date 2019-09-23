"""
    Utility functions for image matching task.
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import cv2
import math
from sklearn.cluster import KMeans
from skimage import measure
from config import config as cfg
import pandas as pd

class RGBPreprocess:
    def __init__(self):
        self.tw, self.th, self.bw, self.bh = cfg.CROP_DIMS

    def process_img(self, image):
        """
            Process the green channel of the rgb image to get the plants information.
            1. Crop the petri dish from the image.
            2. Median blur the image to remove the small noises in the image.
            3. Locate the plants in the grid on the petri dish.
            4. Apply k means clustering to each grid and find the features of each plant.
        """
        # Resize image to detect the contours easily.
        self.h, self.w = 600, 600
        image = cv2.resize(image, (self.h, self.w))
        img = image[self.th:self.bh, self.tw:self.bw]
        # plt.imshow(img)
        # plt.show()

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        height, width, _ = img.shape
        
        # grid dimensions
        GRIDW = cfg.GRIDW
        GRID_RANGE_W = math.ceil(width / GRIDW)

        GRIDH = cfg.GRIDH
        GRID_RANGE_H = math.ceil(height / GRIDH)

        # canvas for output labels
        canvas = np.zeros_like(img[:,:,0])

        count = 0
        grid_no, centroid_list, region_ar_list = [], [], []

        '''
            Apply kmeans clustering for finding labels of each grid. Select the actual plant label by pixel voting.
            Grid is numbered from left to right, top to bottom starting from 1.
            Format -
            1 2  3  4
            5 6  7  8
            9 10 11 12
        '''
        for h in range(0, height-1, GRID_RANGE_H):
            for w in range(0, width-1, GRID_RANGE_W):
                count+=1
                grid_no.append(count)

                image = img[h:h+GRID_RANGE_H, w:w+GRID_RANGE_W]                    
                image = cv2.medianBlur(image, 5)                
                h1, w1, d = image.shape
                image = image.reshape((h1*w1, -1))

                # kmeans clustering
                kmeans = KMeans(n_clusters = 2, n_init=30, max_iter=100, n_jobs=-1, tol=1e-1, algorithm="full")
                kmeans.fit(image)
                cluster_cntr = kmeans.cluster_centers_

                label_image = kmeans.labels_.reshape(h1, w1)
                label_count = np.bincount(np.array([label_image[0,0], label_image[0,GRID_RANGE_W-1], label_image[GRID_RANGE_H-1,0], label_image[GRID_RANGE_H-1, GRID_RANGE_W-1]]))
                label = np.argmin(label_count)
                if len(label_count)==1:
                    label = 1 if label_image[0,0]==0 else 0
                
                clustered_image = np.zeros_like(label_image)
                clustered_image[label_image==label]=count

                thresh = cv2.threshold(clustered_image.astype(np.uint8), 0, 255, cv2.THRESH_BINARY)[1]
                props = measure.regionprops(clustered_image)
                
                # find the center and area of labeled region.
                try:
                    region_centroid = [prop.centroid for prop in props][0]
                    centroid_list.append(region_centroid)
                    region_area = [prop.area for prop in props][0] 
                    region_ar_list.append(region_area)                    
                    # print("Grid information: {}".format(count))
                    # print("Center: ({}, {})".format(region_centroid[0]+h, region_centroid[1]+w))
                    # print("Region area: ", region_area)
                except:
                    print("Contaminated region. Grid number: ", count)

                data = {'Grid No' : grid_no, 'Center' : centroid_list, 'Region area (no of pixels)' : region_ar_list}
                df = pd.DataFrame(data)
                canvas[h:h+GRID_RANGE_H, w:w+GRID_RANGE_W] = clustered_image

        return canvas, df
    