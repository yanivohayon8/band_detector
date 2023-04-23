import unittest
from src.bands import hough,two_points
from src.geometry import PolygonWrapper
import cv2
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import MultiPoint,Point


class TestHoughSimpleExamples(unittest.TestCase):

    simple_img_path = "data/images/simple_example.png"

    def test_lines(self):
        img = cv2.imread(self.simple_img_path,0)
        lines = hough.detect_hough_lines(img,minimum_votes=400)
        img = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)

        for line in lines:
            point1,point2 = line.sample_two_points(distance=50)
            cv2.line(img,point1,point2,(255,0,0))

        plt.imshow(img,cmap="gray")
        plt.close()
        pass

    def test_bands(self):
        img = cv2.imread(self.simple_img_path,0)
        lines = hough.detect_hough_lines(img,minimum_votes=400)
        band = hough.HoughBand(lines[0],lines[1])
        print(repr(band))
        print(band.get_width())


class TestTwoPointsLinesSimpleExamples(unittest.TestCase):
    simple_img_path = "data/images/simple_example.png"

    def run_toy_example(self,line_coords,polygon_coords):
        line = two_points.TwoPointsLine(line_coords[0],line_coords[1])
        polygon = PolygonWrapper(polygon_coords)

        # fig, (ax1,ax2) = plt.subplots(1,2)
        ax1 = plt.subplot()
        line.plot(ax1)
        # line.plot(ax2)
        polygon.plot(ax1)
        # polygon.plot(ax2)

        intersection = polygon.find_intersection(line.line_string)

        if isinstance(intersection,MultiPoint):
            intersection_points = [vertex for vertex in list(intersection.geoms)]
            intersection_x = [coord.x for coord in intersection_points]
            intersection_y = [coord.y for coord in intersection_points]
        if isinstance(intersection,Point):
            intersection_x,intersection_y = intersection.xy
        ax1.scatter(intersection_x, intersection_y, color='green', label='Intersection Points')
        
        edges = polygon.find_edges_touching_points(intersection)
        closest_x = []
        closest_y  = []

        for edge in edges:
            x,y = edge.xy
            closest_x= closest_x + x.tolist()
            closest_y= closest_y + y.tolist()

        # closest_x = [coord.x for point in  ]
        # closest_y = [coord.y for coord in closest_vertices]
        #closest_x,closest_y = edges.xy
        ax1.scatter(closest_x, closest_y, color='purple', label='closest vertices')

        ax1.legend()
        # ax2.legend()
        plt.show()
        plt.close()

    def test_example_1(self):
        line_coords = [(6, 6), (-2, -1)]
        polygon_coords = [(0, 0), (0, 2), (2, 2), (2, 0)]
        self.run_toy_example(line_coords,polygon_coords)

    def test_example_2(self):
        line_coords = [(5, 6), (-2, -6)]
        polygon_coords = [(0, 0), (0, 2), (2, 2), (2, 0)]
        self.run_toy_example(line_coords,polygon_coords)



if __name__ == "__main__":
    unittest.main()