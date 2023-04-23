import unittest
from src.intact_surface_detectors import StraightBandsDetector


# class TestStraightBandsDetector(unittest.TestCase):
#     def detect_lines_fragment(self,img_path,img_name):

#         detector = StraightBandsDetector(img_path)
#         detector.load_img()
#         detector.preprocess()
#         detector.detect_hough_lines(minimum_votes=300)
#         bands = detector.detect_bands()
    
#     def test_detect_lines_RPf_00279(self):
#         img_name = "RPf_00279"
#         img_path = f"data/images/obj_images/{img_name}"
#         self.detect_lines_fragment(img_path)

if __name__ == "__main__":
    unittest.main()