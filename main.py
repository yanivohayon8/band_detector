from scripts.intact_surface import detect_straight_line_bands
from scripts.write_csv_to_springs import convert_rdp_folder
import os


SCRIPT = "convert_rdp_folder" #"detect_straight_line_bands"

if  __name__ == "__main__":

    if SCRIPT == "convert_rdp_folder":
        group_name = "group_45"
        wp3_folder = "C:\\Users\\97254\\Desktop\\msc\\RePAIR\\projects\\WP3-PuzzleSolving\\"
        src_folder = wp3_folder+ f"data\\tests\\output\\segments_rdp\\repair-data\\{group_name}\\rdp_10" #"data/rdp_segments/group_45/rdp_10"
        
        dst_folder = f"data/{group_name}/"
        if not os.path.exists(dst_folder):
            os.makedirs(dst_folder)

        dst_file = dst_folder + "pieces.csv"

        convert_rdp_folder(src_folder,dst_file)

    if SCRIPT == "detect_straight_line_bands":
        csv_path = "data/rdp_segments/group_45/csv/RPf_00368_intact_mesh_rdp_10.csv"

        detect_straight_line_bands(45,"RPf_00368_intact_mesh.png",csv_path,is_debug=True)
    print("finish")


