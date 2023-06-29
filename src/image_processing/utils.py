import cv2
from sklearn.cluster import KMeans
import numpy as np


def run_bilateral_filter(img, diameter = 50,sigma_color = 200, sigma_space = 200):
    return cv2.bilateralFilter(img,diameter,sigma_color,sigma_space)

def segment_kmeans(img, n_clusters=3,colors_pool=None,random_state=0):
    '''
        This function gets an images and color each pixel to the cluster it belongs according to the results of the kmeans algorithm
        img  - numpy array representing the images. You should pass it as normalized image, i.e., divide by 255.0 to set it with values from 0 to 1
        n_clusteres - the number of cluster of the kmeans. Imagine that each segment is the a node in adjacency graph. set this value so this graph will be k-edge-colorable...
    '''
    #img_normalized = img/255.0
    #img_n = img_normalized.reshape(img_normalized.shape[0]*img_normalized.shape[1], img_normalized.shape[2]) # transform to 2d array
    img_as_vector = img.reshape(img.shape[0]*img.shape[1], img.shape[2]) # transform to 2d array
    kmeans = KMeans(n_clusters=n_clusters,random_state=random_state).fit(img_as_vector)
    if colors_pool is None:
        colors_pool = np.array([
            [255,77,0],
            [30,144,255],
            [173,255,47],        
            [255,0,0],
            [0,0,0],
            [255,255,255],
            [255,4,0]
            
        ])

    len_ = colors_pool.shape[0]
    segments_colors = np.array([colors_pool[i%len_] for i in range(len(kmeans.cluster_centers_))])
    img_segmented = segments_colors[kmeans.labels_]
    img_segmented = img_segmented.reshape(img.shape[0],img.shape[1],img.shape[2])
    img_labels = kmeans.labels_.reshape(img.shape[0],img.shape[1])
    return img_segmented,img_labels

def canny(img,rho1=70,rho2=150):
    return cv2.Canny(img,rho1,rho2)

def line_pixels(img,start,end):
    dx, dy = end[0] - start[0], end[1] - start[1]
    length = max(abs(dx), abs(dy))
    diagonal_pixels = [img[
                        round(start[1]+dy*t/length),
                        round(start[0]+dx*t/length)
                      ] for t in range(length)]
    
    return diagonal_pixels