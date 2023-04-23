import cv2
import src.image_processing.utils as pr
import numpy as np
from src.bands.hough import HoughBand,HoughLine

class StraightBandsDetector():

    def __init__(self,hough_lines:list[HoughLine]) -> None:
        self.hough_lines = hough_lines #

    def detect(self,theta_diff=1,rho_diff = 200)->list[HoughBand]:
        bands = []
        
        for line in self.hough_lines:
            is_assigned = False

            for band in bands:
                if abs(band.get_theta()-line.theta)<theta_diff and abs(band.get_rho()-line.rho) < rho_diff:
                    is_assigned = True
                    band.insert(line)
                    break
            
            if not is_assigned:
                bands.append(HoughBand([line]))

        return bands
