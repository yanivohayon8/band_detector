import unittest
from src.image_processing.processors import IntactProcessor
from src.image_processing.utils import line_pixels
import matplotlib.pyplot as plt
import cv2
import numpy as np

class TestIntactProcessor(unittest.TestCase):

    intact_images_path = "data/images"

    def test_RPf_00368_preprocessing(self):
        group = 45
        img_name = "RPf_00368_intact_mesh.png"
        img_path = f"{self.intact_images_path}/group_{group}/{img_name}"
        processor = IntactProcessor(img_path)
        processor.load_img()
        img_preprocessed,labels = processor.preprocess()
        edge_map = processor.get_edge_map()

        fig, (ax1,ax2) = plt.subplots(1,2)
        ax1.imshow(img_preprocessed)
        ax2.imshow(edge_map,cmap="gray")

        plt.close()

    def test_RPf_00368_mask(self):
        group = 45
        img_name = "RPf_00368_intact_mesh.png"
        img_path = f"{self.intact_images_path}/group_{group}/{img_name}"
        processor = IntactProcessor(img_path)
        processor.load_img()
        img_preprocessed,img_labels = processor.preprocess()

        labels_unique = [0,1,2] #np.unique(labels)
        masked_imgs = []
        for label in labels_unique:
            mask = (label==img_labels) #np.where(labels==label,1,0)

            masked_img = np.zeros_like(processor.img)
            masked_img[mask] = processor.img[mask]
            masked_imgs.append(masked_img)
        
        fig,ax = plt.subplots(1,3)
        [ax[i].imshow(masked_imgs[i]) for i in range(len(labels_unique))]
        plt.show()
        plt.waitforbuttonpress()
            

class TestUtils(unittest.TestCase):

    def test_line_pixels(self):
        simple_img_path = "data/images/simple_example.png"
        img = cv2.imread(simple_img_path)
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        pixels = line_pixels(img, (100, 100), (150,150))

        print(np.mean(pixels,axis=0))


if __name__ == "__main__":
    unittest.main()