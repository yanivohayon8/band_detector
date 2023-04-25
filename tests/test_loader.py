import unittest
from src.loader import RdpDataloader
import cv2
import matplotlib.pyplot as plt


class TestRdpLoader(unittest.TestCase):

    def test_rdp_polygon(self):
        csv_path = "data/rdp_segments/group_45/RPf_00368_intact_mesh.csv"
        loader = RdpDataloader(csv_path)
        loader.load()
        polygon_coords = loader.get_polygon_coords()
        poly_x = [coord[0] for coord in polygon_coords]
        poly_y = [coord[1] for coord in polygon_coords]
        plt.plot(poly_x + [poly_x[0]], poly_y + [poly_y[0]],color="red")
        
        img = cv2.imread("data/images/group_45/RPf_00368_intact_mesh.png",cv2.COLOR_BGR2RGB)
        plt.imshow(img)
        plt.show()
        plt.close()


if __name__ == "__main__":
    unittest.main()