import cv2
from src.image_processing import utils
import numpy as np

class IntactProcessor():

    def __init__(self,img_path) -> None:
        self.img_path = img_path
        self.img = None
        self.img_color_segmented = None

    
    def load_img(self):
        self.img = cv2.imread(self.img_path)
        self.img = cv2.cvtColor(self.img,cv2.COLOR_BGR2RGB)
        return self.img
    
    def preprocess(self):
        img_smoothed = utils.run_bilateral_filter(self.img)
        img_normelized = img_smoothed/255.0 # put this inside the segment kmeans function (make a copy within it)
        img_segmented = utils.segment_kmeans(img_normelized)
        self.img_color_segmented = (img_segmented*255).astype(np.uint8)
        return self.img_color_segmented
    
    def get_edge_map(self,rho1=70,rho2=150):
        img_segmented_gray = cv2.cvtColor(self.img_color_segmented,cv2.COLOR_RGB2GRAY)
        return utils.canny(img_segmented_gray,rho1=rho1,rho2=rho2)