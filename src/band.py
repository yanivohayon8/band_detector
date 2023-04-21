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


class Band():

    def __init__(self,first_line:HoughLine,second_line:HoughLine) -> None:
        self.first_line = first_line
        self.second_line = second_line
        self.theta = (first_line.theta + second_line.theta)/2
        self.radius = (first_line.radius + second_line.radius)/2

    def __repr__(self) -> str:
        return f"{self.theta};{self.radius}"
    
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value,Band):
            radius_diff = abs(__value.radius-self.radius)
            theta_diff = abs(__value.theta-self.theta)
            radius_threshold = 5
            theta_threshold = 1 # because the resolution is 1
            return radius_diff < radius_threshold and theta_diff < theta_threshold
    
    def get_width(self):
        return abs(self.first_line.radius - self.second_line)
            

        return False