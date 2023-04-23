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



    # def pair_parallel_lines(self,lines:list=None,max_theta_diff = 0.06):
    #     '''
    #         This method return a list of pairs of lines indecies that are parallel
    #         to one another. 
    #     '''

    #     if lines is None:
    #         lines = self.hough_lines

    #     pairs = [] # will contain indexes from out_lines
    #     for line_i in range(len(lines)):
    #         for line_j in range(len(lines)):

    #             if line_i == line_j:
    #                 continue
                    
    #             # check for duplicates
    #             if (line_j,line_i) in pairs or (line_i,line_j) in pairs:
    #                 continue

    #             theta_diff = abs(lines[line_i].theta-lines[line_j].theta)
    #             if  theta_diff <= max_theta_diff:
    #                 pairs.append((line_i,line_j))
        
    #     return pairs
    
    # def pair_close_lines(self,lines:list=None,min_radius_diff = 100):
    #     '''
    #         Returns list of lines that their distance between them is lower than a threshold
    #     '''

    #     if lines is None:
    #         lines = self.hough_lines

    #     pairs = [] # will contain indexes from out_lines
    #     for line_i in range(len(lines)):
    #         for line_j in range(len(lines)):

    #             if line_i == line_j:
    #                 continue
                    
    #             # check for duplicates
    #             if (line_j,line_i) in pairs or (line_i,line_j) in pairs:
    #                 continue

    #             radius_diff = abs(lines[line_i].radius-lines[line_j].radius)
    #             if  radius_diff <= min_radius_diff:
    #                 pairs.append((line_i,line_j))
        
    #     return pairs    

    # def detect_bands(self)->list:
    #     parallel_lines_pairs = self.pair_parallel_lines()
    #     close_lines_pairs = self.pair_close_lines(min_radius_diff=100)
    #     potential_lines_pairs = [pair for pair in parallel_lines_pairs if not pair in close_lines_pairs]

    #     bands_with_duplicates = [HoughBand(self.hough_lines[pair[0]],self.hough_lines[pair[1]]) for pair in potential_lines_pairs]
    #     bands = []
    #     for band in bands_with_duplicates:
    #         if band in bands:
    #             continue
            
    #         # if band.get_width() > 500:
    #         #     continue

    #         bands.append(band)

    #     return bands




    
        


