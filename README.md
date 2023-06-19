# Bands Detector

This project is aimed at detecting straight bands on fresco fragments as part of the RePAIR project. These bands are a recurrent visual pattern on fragments from the same decoration, and as such, serve as a hint for future pairwise matching. 

In addition, the project computes the intersection points of the detected bands with the contour - more precisely, the closest vertices on the polygonal representation of it. Utilizing the Hough Transform Algorithm, the scripts compute the lines on the images of the fragment. The lines are represented in a polar coordinate system, and are then clustered into bands based on rho and theta thresholded differences.

> Note: The project includes several other independent mini utilities that you can ignore, such as `convert_rdp_folder` that is designed to convert the CSV format, and `seg_and_edge_map` that preprocesses the input image as the main script does.

The output of the script includes:
- An image that outputs all the detected lines on the fragment. Lines that are close to each other and have small angle perturbations would be considered as a band. The lines of a band would be colored the same way.
- A JSON file containing the following metadata:
  - `representive_line`: A line that represents the center (mean) of a band. It crosses the border of the image, and it is essentially two points close to the borders.
  - `Lines`: A list containing all the lines composing the bands in a polar coordinate system. These lines were computed using OpenCV. They contain small JSONs of rho and theta.
  - `Width`: The width of the band. It is computed as `max_rho - min_rho` among the computed lines of the bands.
  - `Average_color`: In RGB format.
  - `closest_vertices_on_contour`: Contains two metadata: the coordinates in the image plane as well as its indices of the vertices in the polygonal representation of the fragment.

If you use debug mode, you can plot the polygonal representation of the image and the segmentation results. These images would be saved.

<img src="https://github.com/yanivohayon8/band_detector/assets/38216201/434820ee-fe13-4274-9784-cec3b3365872" width="500">
## Installation

You should install the following dependencies:
1) Matplotlib
2) Pandas
3) OpenCV
4) Pillow
5) NumPy
6) Shapely
7) Scikit-learn

## Usage

The script has the following parameters:
1) `img_path`: The path of the image of the input fragment
2) `csv_path`: The path of the polygonal representation of the input fragment
3) `dst_folder`: The path of the folder to save the new files

Optional parameters of the algorithm:
1) `minimum_votes`: The minimum number of votes for  Hough Transform algorithm to detect a line
2) `rho_diff`: Lines under this parameter would be considered under the same band
3) `theta_diff`: Lines under this parameter would be considered under the same band

Example of command line execution:
```bash
python main.py --img_path "data/group_39/intact_images\\RPf_00319_intact_mesh.png" --csv_path "data/rdp_segments/group_39\\RPf_00319_intact_mesh.csv" --dst_folder "data/group_39/bands/" --is_debug
```

## Known Issues
No known issues as of the latest update.

## Relevant Publications
No relevant publications as of the latest update.


