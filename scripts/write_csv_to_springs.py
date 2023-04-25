import glob
import pandas as pd
from src.loader import RdpDataloader
from src.geometry import PolygonWrapper
import numpy as np


def convert_rdp_folder(src_folder,dst_file_path,mapping_file,factor=3,use_convex_hull=False):
    '''
        src_folder - the folder of csv output of the rdp 
        dst_file_path - the path of the final csv of the pieces
        mapping_file - file that maps betwen name to the num order....
    '''
    fragment_files = glob.glob(src_folder+"/*.csv")
    fragment2num = {}
    xs = []
    ys = []
    ids = []
    fragments_names = []


    for i,file in enumerate(fragment_files):
        fragment_name = file.split("\\")[-1].split(".")[0]
        fragments_names.append(fragment_name)
        rdp_loader = RdpDataloader(file)
        rdp_loader.load()
        polygon_coords = rdp_loader.get_polygon_coords()

        if use_convex_hull:
            polygon = PolygonWrapper(polygon_coords)
            convex_hull = polygon.polygon.convex_hull
            convex_hull_x,convex_hull_y = convex_hull.exterior.xy
            convex_hull_x = convex_hull_x.tolist()
            convex_hull_y = convex_hull_y.tolist()
            x_mean = np.mean(convex_hull_x)
            y_mean = np.mean(convex_hull_y)

            for x,y in zip(convex_hull_x,convex_hull_y):
                xs.append((x-x_mean)*factor)
                ys.append((y-y_mean)*factor)
                ids.append(i)
        else:
            x_sum = 0
            y_sum = 0

            for coord in polygon_coords:
                x_sum+=coord[0]
                y_sum+= coord[1]
            
            x_mean = x_sum/len(polygon_coords)
            y_mean = y_sum/len(polygon_coords)

            for coord in polygon_coords:
                xs.append((coord[0]-x_mean)*factor)
                ys.append((coord[1]-y_mean)*factor)
                # xs.append(float(coord[0])*factor)
                # ys.append(float(coord[1])*factor)
                ids.append(i)
    
    # Ofir convention
    df_result = pd.DataFrame({
        "piece":ids,
        "x":xs,
        "y":ys
    })

    df_mapping = pd.DataFrame(
        {
        "fragment":fragments_names,
        "ids":range(len(fragment_files))
        }
    )

    df_result.to_csv(dst_file_path,index=False)
    df_mapping.to_csv(mapping_file,index=False)



