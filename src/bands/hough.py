import cv2
import numpy as np
import math


class HoughLine():
    def __init__(self,theta,rho) -> None:
        self.theta = theta
        self.rho = rho
        self.slope = -1 / np.tan(theta)
        self.bias = rho / np.sin(theta)
        pass
    
    def __repr__(self) -> str:
        return f"theta={self.theta},radius={self.rho}"

    # old - delete when refactoring
    def sample_two_points(self,img_shape):
        left_border_x=0
        up_border_y = img_shape[1] # because of the image size
        right_border_x = img_shape[0]
        down_border_y = 0

        left_border_y = self.get_y(left_border_x)

        if not math.isnan(left_border_y):
            left_border_y = int(left_border_y)

        up_border_x = self.get_x(up_border_y)

        if not math.isnan(up_border_x):
            up_border_x = int(up_border_x)

        right_border_y = self.get_y(right_border_x)

        if not math.isnan(right_border_y):
            right_border_y = int(right_border_y)

        down_border_x = self.get_x(down_border_y)

        if not math.isnan(down_border_x):
            down_border_x = int(down_border_x)
        
        crossing_bounds = [(left_border_x,left_border_y),
                            (up_border_x,up_border_y),
                            (right_border_x,right_border_y),
                            (down_border_x,down_border_y)]
        points = []

        for point in crossing_bounds:

            if point[0] <= img_shape[0] and point[0]>=0:
                if point[1] <= img_shape[1] and point[1]>=0:
                    points.append(point)

        # if it is a noise?
        if len(points)<2:
            raise ("Warning, line must touch the image borders")
        
        return points
                

    def get_y(self,x,bound=7000):
        return (self.rho - x*np.cos(self.theta))/(np.sin(self.theta)+1e-6)
    
    def get_x(self,y,bound=7000):
        return (self.rho - y*np.sin(self.theta))/(np.cos(self.theta)+1e-6)



class HoughBand():

    def __init__(self,line1:HoughLine,line2:HoughLine) -> None:
        self.line1 = line1
        self.line2 = line2
        self.theta = (line1.theta + line2.theta)/2
        self.radius = (line1.radius + line2.radius)/2

    def __repr__(self) -> str:
        return f"{self.theta};{self.radius}"
    
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value,HoughBand):
            radius_diff = abs(__value.radius-self.radius)
            theta_diff = abs(__value.theta-self.theta)
            radius_threshold = 5
            theta_threshold = 1 # because the resolution is 1
            return radius_diff < radius_threshold and theta_diff < theta_threshold
    
    def get_width(self):
        return abs(self.line1.radius - self.line2.radius)
    

def detect_hough_lines_randomly(img:np.ndarray,rho_resolution=1,theta_resolution=1,minimum_votes = 100):

    if img.dtype != np.uint8:
        img_copy = img.astype(np.uint8)
    else:
        img_copy = img

    # set srcn and dstn as 0 to use the classical hough transform algorithm
    lines =  cv2.HoughLinesP(img,rho_resolution,theta_resolution*np.pi/180,minimum_votes,0,0)

    if lines is None:
        return []
    
    lines_two_points = []
    
    for line in lines:
        x1, y1, x2, y2 = line[0]
        lines_two_points.append([(x1,y1),(x2,y2)])
    
    return lines_two_points


def detect_hough_lines(img:np.ndarray,rho_resolution=1,theta_resolution=1,minimum_votes = 100):

    if img.dtype != np.uint8:
        img_copy = img.astype(np.uint8)
    else:
        img_copy = img

    # set srcn and dstn as 0 to use the classical hough transform algorithm
    lines =  cv2.HoughLines(img,rho_resolution,theta_resolution*np.pi/180,minimum_votes,0,0)

    if lines is None:
        return []
    
    hough_lines = []
    
    for line in lines:
        radius,theta = line[0]
        hough_line = HoughLine(theta,radius)
        hough_lines.append(hough_line)
    
    return hough_lines