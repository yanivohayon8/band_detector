import glob
import pandas as pd
from src.loader import RdpDataloader

def convert_rdp_folder(src_folder,dst_file_path):
    '''
        Reads the csvs in the file and writes it to it to a single csv
    '''
    fragment_files = glob.glob(src_folder+"/*.csv")
    fragment2num = {}
    xs = []
    ys = []
    ids = []
    
    for i,file in enumerate(fragment_files):
        rdp_loader = RdpDataloader(file)
        rdp_loader.load()
        polygon_coords = rdp_loader.get_polygon_coords()

        for coord in polygon_coords:
            xs.append(coord[0])
            ys.append(coord[1])
            ids.append(i)
    
    # Ofir convention
    df_result = pd.DataFrame({
        "piece":ids,
        "x":xs,
        "y":ys
    })

    df_result.to_csv(dst_file_path,index=False)



