from scripts.intact_surface import detect_straight_line_bands
from scripts.write_csv_to_springs import convert_rdp_folder
from scripts.opposite_surface import detect_bamboo_lines
import os
import glob


SCRIPT = "detect_straight_line_bands"#"convert_rdp_folder" #"detect_straight_line_bands" #"detect_bamboo_lines"

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
        group = 39
        fragment_name = "RPf_00370" #"RPf_00368" #RPf_00370" #"RPf_00371"

        intact_images =sorted(glob.glob(f"data/group_{group}/*_intact_mesh.png"))
        csvs_paths = sorted(glob.glob(f"data/rdp_segments/group_{group}/*_intact_mesh.csv"))
        
        assert len(intact_images)>0 and len(csvs_paths)>0

        for img_path,csv_path in zip(intact_images,csvs_paths):
            detect_straight_line_bands(img_path,csv_path,is_debug=True)

    if SCRIPT == "detect_bamboo_lines":
        group=45#39
        img_name ="RPf_00370_opposite_mesh_normals.png" #"RPf_00368_opposite_mesh_normals.png"
        img_path = f"data/group_{group}/{img_name}"
        #img_path = "data/images/RPf_00333_opposite_mesh_normals.png"
        detect_bamboo_lines(img_path)

    print("finish")


