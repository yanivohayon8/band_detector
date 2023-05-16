#images_path = "data/images"

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import transforms
from scipy import ndimage
from src.image_processing.processors import BamboolinesProcessor
import cv2
from src.bands import hough
from src.loader import RdpDataloader
from src.geometry import PolygonWrapper
import pandas as pd


def detect_bamboo_lines(img_path,rdp_csv_path,output_path,is_debug=False):
    #img_path = f"{images_path}/group_{group}/{img_name}"
    processor = BamboolinesProcessor(img_path)
    img = processor.load_img()
    edge_map = processor.get_edge_map(rho1=70,rho2=140)

    #plt.imshow(edge_map,cmap="gray")
    lines = hough.detect_hough_lines(edge_map,minimum_votes=150)


    for line in lines:
        points = line.sample_two_points(img.shape)
        cv2.line(img,points[0],points[1],(0,255,0),thickness=2)

    band = hough.HoughBand(lines)
    theta_radians = band.get_theta()
    if theta_radians is None:
        print("Note: we didn't not find any bamboos")
        theta_radians = 0
    degrees = np.rad2deg(theta_radians)
    rotation_options = [0,degrees,-(180-degrees),(90+degrees),-(90-degrees)]
    images_rotated = [ndimage.rotate(img,rot,mode='constant') for rot in rotation_options]

    #if is_debug:
    ax = plt.subplot()
    ax.set_axis_off()
    ax.imshow(img)

    fig, axs = plt.subplots(2,2)
    axs[0,0].set_axis_off()
    axs[0,1].set_axis_off()
    axs[1,0].set_axis_off()
    axs[1,1].set_axis_off()
    # rotation_degrees = 30
    # tr = transforms.Affine2D().rotate_deg(rotation_degrees)
    # ax1.imshow(img,transform=tr+ax1.transData)
    axs[0,0].imshow(images_rotated[1])
    axs[0,1].imshow(images_rotated[2])
    axs[1,0].imshow(images_rotated[3])
    axs[1,1].imshow(images_rotated[4])
    #plt.show()
    plt.waitforbuttonpress()
    plt.close()

    rdp_loader = RdpDataloader(rdp_csv_path)
    rdp_loader.load()
    polygon_coords = rdp_loader.get_polygon_coords()
    polygon = PolygonWrapper(polygon_coords)

    choice = input("Enter Choice of rotation between 0-4 where 0 is not rotating:")
    print("Choice: " + choice)

    polygon_rotated = polygon.rotated(rotation_options[int(choice)])

    xs,ys = polygon_rotated.get_coords_separated()
    df = pd.DataFrame({
        "x":xs,
        "y":ys
    })

    df.to_csv(output_path,index=False)    

