import unittest
from src.geometry import PolygonWrapper
import matplotlib.pyplot as plt

class TestPolygonWrapper(unittest.TestCase):
    
    def test_polygon_rotation(self):
        triangle_coords_1 = [(0,0),(1,1),(2,0)]
        triangle = PolygonWrapper(triangle_coords_1)
        x,y = triangle.get_coords_separated()
        new_triangle = triangle.rotated(90)
        x_new,y_new = new_triangle.get_coords_separated()
        fig , (ax1,ax2) = plt.subplots(1,2)
        ax1.plot(x+[x[0]],y+[y[0]])
        ax2.plot(x_new+[x_new[0]],y_new+[y_new[0]])
        plt.show()
        plt.waitforbuttonpress()
        plt.close()





if __name__ == "__main__":
    unittest.main()