import unittest
from src.intact_surface_detectors import StraightBandsDetector
from src.bands import hough

class TestStraightBandsDetector(unittest.TestCase):
    def test_toy_example(self):
        
        hough_lines = [hough.HoughLine(50,1),hough.HoughLine(50.5,4),hough.HoughLine(90.02,9)]
        detector = StraightBandsDetector(hough_lines)
        detector.detect()
    

if __name__ == "__main__":
    unittest.main()