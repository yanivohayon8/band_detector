import pandas as pd

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
        #return [(y,2064-x) for x,y in zip(xs,ys)]
        return [(y,2000-x) for x,y in zip(xs,ys)]
