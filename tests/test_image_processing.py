import unittest
from src.image_processing.processors import IntactProcessor
import matplotlib.pyplot as plt


class TestIntactProcessor(unittest.TestCase):

    intact_images_path = "data/images"

    def test_RPf_00368_preprocessing(self):
        group = 45
        img_name = "RPf_00368_intact_mesh.png"
        img_path = f"{self.intact_images_path}/group_{group}/{img_name}"
        processor = IntactProcessor(img_path)
        processor.load_img()
        img_preprocessed = processor.preprocess()
        edge_map = processor.get_edge_map()

        fig, (ax1,ax2) = plt.subplots(1,2)
        ax1.imshow(img_preprocessed)
        ax2.imshow(edge_map,cmap="gray")

        plt.close()


if __name__ == "__main__":
    unittest.main()