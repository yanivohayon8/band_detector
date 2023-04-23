intact_images_path = "data/images"
from src.image_processing.processors import IntactProcessor
import matplotlib.pyplot as plt
from src.bands import hough
from src.bands import two_points
import cv2
from src.intact_surface_detectors import StraightBandsDetector
from src import DEBUG_COLORS
from src.loader import RdpDataloader


def detect_straight_line_bands(group,img_name,rdp_csv_path,is_debug=False):
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
    
    band_detector = StraightBandsDetector(hough_lines)
    bands = band_detector.detect()
    bands_as_lines = [band.get_representive_line() for band in bands]

    rdp_loader = RdpDataloader(rdp_csv_path)
    rdp_loader.load()
    polygon_coords = rdp_loader.get_polygon_coords()



    if is_debug:
        img_ = img.copy()
        
        # for line in two_point_lines:
        #     cv2.line(img_,line.point1,line.point2,(255,0,255),2)

        for i,band in enumerate(bands):
            for line in band.hough_lines:
                points = line.sample_two_points(edge_map.shape)
                cv2.line(img_,points[0],points[1],DEBUG_COLORS[i%len(DEBUG_COLORS)],2)


        poly_x = [coord[0] for coord in polygon_coords]
        poly_y = [coord[1] for coord in polygon_coords]

        fig, axs = plt.subplots(2,2)
        axs[0,0].imshow(img_preprocessed)
        axs[0,1].imshow(edge_map,cmap="gray")
        axs[1,0].imshow(img_)
        axs[1,1].set_aspect("equal",adjustable='box')
        axs[1,1].plot(poly_x + [poly_x[0]], poly_y + [poly_y[0]],color="red")

        plt.show()
        plt.close()
    
    


