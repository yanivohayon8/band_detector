import glob
import pandas as pd
from src.loader import RdpDataloader
from src.geometry import PolygonWrapper
from PIL import Image


def convert_rdp_folder(src_folder,dst_folder,images_folder,crop_margin = 32, is_compute_convex_hull=False):
    '''
        This functions read the csv files that were outtputted from the RDP module (Sinem) and
        creates a new folder containing the following:
        - piece.csv file containing the coordinates of the pieces (top left corner is the origin)
        - images folder containing the original images cropped to the bounding box cotaining the fragment.

        src_folder - the folder of csv output of the rdp 
        dst_file_path - the path of the puzzle files such as pieces and the images
        images_folder - where are the images
        crop_margin - a space given from all size while preparing the image for the spring mass sfml graphics... 32 is default because the original image is 2000x2000 and Sinem outputs rdp is 2064x2064...
    '''
    pieces_file_path = dst_folder + "/pieces.csv"
    convex_hull_file_path = dst_folder + "/convex_hull.csv"

    fragment_files = glob.glob(src_folder+"/*.csv")
    intact_images_files = glob.glob(images_folder+"/*")

    assert len(fragment_files) == len(intact_images_files)

    xs = []
    ys = []
    ids = []
    convex_hull_xs = []
    convex_hull_ys = []
    convex_hull_ids = []
    fragments_names = []


    for i,file in enumerate(fragment_files):
        fragment_name = file.split("\\")[-1].split(".")[0]
        print(f"Processing fragment {fragment_name}")
        fragments_names.append(fragment_name)
        rdp_loader = RdpDataloader(file)
        rdp_loader.load()
        polygon_coords = rdp_loader.get_polygon_coords()

        x_min = 99999
        y_min = 99999
        x_max = 0
        y_max = 0

        for coord in polygon_coords:

            if coord[0]<x_min:
                x_min = coord[0]

            if coord[0] > x_max:
                x_max = coord[0]

            if coord[1]<y_min:
                y_min = coord[1]
            
            if coord[1] > y_max:
                y_max = coord[1]
        
        for coord in polygon_coords:
            xs.append(coord[0]-x_min)
            ys.append(coord[1]-y_min)
            ids.append(fragment_name)
        
        img = Image.open(intact_images_files[i])
        cropped_img = img.crop((x_min-crop_margin,y_min-crop_margin,x_max+crop_margin,y_max+crop_margin))
        cropped_img.save(f"{dst_folder}/images/{fragment_name}.png")

        #
        # computing convex hull coordinates
        #
        if is_compute_convex_hull:
            polygon = PolygonWrapper(polygon_coords)
            convex_hull = polygon.polygon.convex_hull
            convex_hull_x,convex_hull_y = convex_hull.exterior.xy
            convex_hull_x = convex_hull_x.tolist()
            convex_hull_y = convex_hull_y.tolist()

            for x,y in zip(convex_hull_x,convex_hull_y):
                convex_hull_xs.append(x-x_min)
                convex_hull_ys.append(y-y_min)
                convex_hull_ids.append(i)

    if is_compute_convex_hull:
        df_convex_hull = pd.DataFrame({
                "piece":convex_hull_ids,
                "x":convex_hull_xs,
                "y":convex_hull_ys
            })

        df_convex_hull.to_csv(convex_hull_file_path,index=False)

    # Ofir convention
    df_pieces = pd.DataFrame({
        "piece":ids,
        "x":xs,
        "y":ys
    })
    
    df_pieces.to_csv(pieces_file_path,index=False)

    df_mapping = pd.DataFrame(
        {
        "fragment":fragments_names,
        "ids":range(len(fragment_files))
        }
    )




