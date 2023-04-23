intact_images_path = "data/images"
from src.image_processing.processors import IntactProcessor
import matplotlib.pyplot as plt
from src.bands import hough
from src.bands import two_points
import cv2

def detect_straight_line_bands(group,img_name,is_debug=False):
    img_path = f"{intact_images_path}/group_{group}/{img_name}"
    processor = IntactProcessor(img_path)
    img = processor.load_img()
    img_preprocessed = processor.preprocess()
    edge_map = processor.get_edge_map()
    
    hough_lines = hough.detect_hough_lines(edge_map,minimum_votes=100)
    two_point_lines = []

    for line in hough_lines:
        points = line.sample_two_points(edge_map.shape)
        two_point_lines.append(two_points.TwoPointsLine(points[0],points[1]))
    
    if is_debug:
        img_ = img.copy()
        for line in two_point_lines:
            cv2.line(img_,line.point1,line.point2,(255,0,255),2)

        fig, axs = plt.subplots(1,3)
        axs[0].imshow(img_preprocessed)
        axs[1].imshow(edge_map,cmap="gray")
        axs[2].imshow(img_)
        plt.show()
        plt.close()
    
    
    plt.close()


