from scripts.intact_surface import detect_straight_line_bands
from scripts.write_csv_to_springs import convert_rdp_folder
import os


SCRIPT = "detect_straight_line_bands"#"convert_rdp_folder" #"detect_straight_line_bands"

if  __name__ == "__main__":

    if SCRIPT == "convert_rdp_folder":
        group_name = "group_45"
        wp3_folder = "C:\\Users\\97254\\Desktop\\msc\\RePAIR\\projects\\WP3-PuzzleSolving\\"
        src_folder = wp3_folder+ f"data\\tests\\output\\segments_rdp\\repair-data\\{group_name}\\rdp_10" #"data/rdp_segments/group_45/rdp_10"
        
        dst_folder = f"data\\{group_name}\\"
        if not os.path.exists(dst_folder):
            os.makedirs(dst_folder)

        dst_file = dst_folder + "pieces.csv"
        mapping_file = dst_folder +"mapping.csv"

        convert_rdp_folder(src_folder,dst_file,mapping_file)

    if SCRIPT == "detect_straight_line_bands":
        fragment_name ="RPf_00370" #"RPf_00368"
        csv_path = f"data/rdp_segments/group_45/{fragment_name}_intact_mesh.csv"

        detect_straight_line_bands(45,f"{fragment_name}_intact_mesh.png",csv_path,is_debug=True)
    print("finish")


