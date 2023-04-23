import pandas as pd

# import cv2

# class ImageLoader:

#     def __init__(self,img_path) -> None:
#         self.img_path = img_path

#     def load(self,type="rgb"):
#         if type == "rgb":
#             return cv2.imread(self.img_path,cv2.COLOR_BGR2RGB)
#         if type == "gray":
#             return 

IMAGE_WIDTH = 2064
IMAGE_HEIGHT = 2064

class RdpDataloader():

    def __init__(self,csv_path) -> None:
        self.csv_path = csv_path
        self.df = None
    
    def load(self):
        self.df = pd.read_csv(self.csv_path)
    
    def get_polygon_coords(self):
        xs = self.df["start_point_x"].values.tolist()
        ys = self.df["start_point_y"].values.tolist()

        # Workaround rdp module bug
        return [(y,IMAGE_HEIGHT-x) for x,y in zip(xs,ys)]
