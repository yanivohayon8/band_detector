import glob
import pandas as pd
from src.loader import RdpDataloader
from src.geometry import PolygonWrapper
import numpy as np


def convert_rdp_folder(src_folder,dst_folder,factor=3,use_convex_hull=False):
    '''
        src_folder - the folder of csv output of the rdp 
        dst_file_path - the path of the final csv of the pieces
        mapping_file - file that maps betwen name to the num order....
    '''
    pieces_file_path = dst_folder + "pieces.csv"
    mapping_file = dst_folder +"mapping.csv"
    convex_hull_file_path = dst_folder + "convex_hull.csv"

    fragment_files = glob.glob(src_folder+"/*.csv")
    fragment2num = {}
    xs = []
    ys = []
    ids = []
    convex_hull_xs = []
    convex_hull_ys = []
    convex_hull_ids = []
    fragments_names = []


    for i,file in enumerate(fragment_files):
        fragment_name = file.split("\\")[-1].split(".")[0]
        fragments_names.append(fragment_name)
        rdp_loader = RdpDataloader(file)
        rdp_loader.load()
        polygon_coords = rdp_loader.get_polygon_coords()

        #
        # computing convex hull coordinates
        #
        polygon = PolygonWrapper(polygon_coords)
        convex_hull = polygon.polygon.convex_hull
        convex_hull_x,convex_hull_y = convex_hull.exterior.xy
        convex_hull_x = convex_hull_x.tolist()
        convex_hull_y = convex_hull_y.tolist()
        x_mean = np.mean(convex_hull_x)
        y_mean = np.mean(convex_hull_y)

        for x,y in zip(convex_hull_x,convex_hull_y):
            #convex_hull_xs.append((x-x_mean)*factor)
            #convex_hull_ys.append((y-y_mean)*factor)
            convex_hull_xs.append(x)
            convex_hull_ys.append(y)
            convex_hull_ids.append(i)
        

        #
        # computing polygon coordinates
        #

        x_min = 99999
        y_min = 99999

        for coord in polygon_coords:

            if coord[0]<x_min:
                x_min = coord[0]
            if coord[1]<y_min:
                y_min = coord[1]
        
        for coord in polygon_coords:
            #xs.append((coord[0]-x_mean)*factor)
            #ys.append((coord[1]-y_mean)*factor)
            xs.append(coord[0]-x_min)
            ys.append(coord[1]-y_min)
            #ids.append(i)
            ids.append(fragment_name)
    

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

    df_mapping.to_csv(mapping_file,index=False)



