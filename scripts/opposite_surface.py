#images_path = "data/images"


import matplotlib.pyplot as plt
from src.image_processing.processors import BamboolinesProcessor
import cv2
from src.bands import hough

def detect_bamboo_lines(img_path,is_debug=False):
    #img_path = f"{images_path}/group_{group}/{img_name}"
    processor = BamboolinesProcessor(img_path)
    img = processor.load_img()
    edge_map = processor.get_edge_map(rho1=70,rho2=140)

    #plt.imshow(edge_map,cmap="gray")
    lines = hough.detect_hough_lines(edge_map,minimum_votes=150)


    for line in lines:
        points = line.sample_two_points(img.shape)
        cv2.line(img,points[0],points[1],(0,255,0),thickness=2)

    fig, (ax1,ax2) = plt.subplots(1,2)
    ax1.imshow(edge_map,cmap="gray")
    ax2.imshow(img)
    #plt.show()
    plt.waitforbuttonpress()
    plt.close()