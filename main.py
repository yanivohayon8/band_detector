import matplotlib.pyplot as plt
from src.band_detectors import StraightBandsDetector
import src.visualize as vs
import numpy as np


if  __name__ == "__main__":
    # img_name = "RPf_00368_intact_mesh.png"
    # img_path = f"data/images/group_45/{img_name}"
    img_name = "RPf_00333_opposite_filtered.png"
    img_path = f"data/images/{img_name}"

    detector = StraightBandsDetector(img_path)
    detector.load_img()
    detector.preprocess()
    detector.detect_hough_lines(minimum_votes=300)
    bands = detector.detect_bands()

    # regular_lines = []
    # distance_between_points = 1000
    # for band in bands:
    #     line1_point1,line1_point2 = band.first_line.sample_two_points(distance_between_points)
    #     line2_point1,line2_point2 = band.second_line.sample_two_points(distance_between_points)
    #     regular_lines.append((line1_point1,line1_point2))
    #     regular_lines.append((line2_point1,line2_point2))



    img_seg = detector.img.copy()
    np.random.seed(0)
    for band in bands:
        color = np.random.randint(0, 255, size=(3, ))
        color = ( int (color [ 0 ]), int (color [ 1 ]), int (color [ 2 ])) ##convert data types int64 to int
        vs.draw_band(img_seg,band,color,thickness=10)

    #vs.draw_lines(img_seg,regular_lines)
    plt.imshow(img_seg)
    plt.close()
    print("finish")


