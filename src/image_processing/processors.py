import cv2
from src.image_processing import utils
import numpy as np

class Processor():

    def __init__(self,img_path) -> None:
        self.img_path = img_path
        self.img = None
        self.img_color_segmented = None
        self.img_labels = None
        self.masked_img = None

    
    def load_img(self):
        self.img = cv2.imread(self.img_path)
        self.img = cv2.cvtColor(self.img,cv2.COLOR_BGR2RGB)
        return self.img

class IntactProcessor(Processor):
    
    def preprocess(self,n_clusters=3):
        img_smoothed = utils.run_bilateral_filter(self.img)
        img_normelized = img_smoothed/255.0 # put this inside the segment kmeans function (make a copy within it)
        img_segmented,self.img_labels = utils.segment_kmeans(img_normelized,n_clusters=n_clusters) #The clusters: background\fragment background\ theme
        self.img_color_segmented = (img_segmented*255).astype(np.uint8)
        return self.img_color_segmented,self.img_labels
    
    def masked_image(self,label_segment):
        mask = (label_segment==self.img_labels) #np.where(labels==label,1,0)
        masked_img = np.zeros_like(self.img)
        masked_img[mask] = self.img[mask]
        self.masked_img = masked_img
        return masked_img
    
    def get_edge_map(self,img,rho1=70,rho2=150):
        # img_segmented_gray = cv2.cvtColor(self.img_color_segmented,cv2.COLOR_RGB2GRAY)
        img_segmented_gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
        return utils.canny(img_segmented_gray,rho1=rho1,rho2=rho2)
    
class BamboolinesProcessor(Processor):

    def get_edge_map(self,rho1=70,rho2=140):
        img_gray = cv2.cvtColor(self.img,cv2.COLOR_RGB2GRAY)
        return utils.canny(img_gray,rho1=rho1,rho2=rho2)