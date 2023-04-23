import cv2
import numpy as np

class HoughLine():
    def __init__(self,theta,radius) -> None:
        self.theta = theta
        self.radius = radius
        pass
    
    def __repr__(self) -> str:
        return f"theta={self.theta},radius={self.radius}"

    def sample_two_points(self,distance = 1000):
        '''
            hough_theta - the theta that represent the line, according to the hough transform
            hough_radius - the radius that represent the line, according to the hough transform
            distance - the distance between the points
        '''
        a,b = np.cos(self.theta), np.sin(self.theta)
        x0,y0 = a*self.radius, b*self.radius
        x1,y1 = int(x0 + distance * (-b)), int(y0 + distance*a)
        x2,y2 = int(x0 - distance * (-b)), int(y0 - distance*a)
        return (x1,y1),(x2,y2)



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