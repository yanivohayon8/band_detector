from scripts.intact_surface import detect_straight_line_bands
from scripts.write_csv_to_springs import convert_rdp_folder
from scripts.opposite_surface import detect_bamboo_lines
import os
import glob


SCRIPT = "convert_rdp_folder"#"convert_rdp_folder" #"detect_straight_line_bands" #"detect_bamboo_lines"

if  __name__ == "__main__":

    if SCRIPT == "convert_rdp_folder":
        group_name = "group_39"
        wp3_folder = "C:\\Users\\97254\\Desktop\\msc\\RePAIR\\projects\\WP3-PuzzleSolving\\"
        src_folder = wp3_folder+ f"data\\tests\\output\\segments_rdp\\repair-data\\{group_name}\\rdp_10" #"data/rdp_segments/group_45/rdp_10"
        
        data_folder = f"data\\{group_name}\\"
        images_folder = f"{data_folder}/intact_images"
        dst_folder = f"{data_folder}/puzzle"
        dst_images_folder = f"{dst_folder}/images"

        if not os.path.exists(dst_images_folder):
            os.makedirs(dst_images_folder)

        convert_rdp_folder(src_folder,dst_folder,images_folder)

    if SCRIPT == "detect_straight_line_bands":
        #fragment_name = "RPf_00370" #"RPf_00368" #RPf_00370" #"RPf_00371"
        intact_images = None
        csvs_paths = None
        # intact_images = [
        #     # "data/group_39/intact_images\\RPf_00319_intact_mesh.png",
        #     # #"data/group_39/intact_images\\RPf_00317_intact_mesh.png"
        #     # "data/group_39/intact_images\\RPf_00320_intact_mesh.png"
        #     # #"data/group_45/intact_images\\RPf_00370_intact_mesh.png"
        #     "data/group_45/intact_images\\RPf_00368_intact_mesh.png",
        #     "data/group_45/intact_images\\RPf_00370_intact_mesh.png",
        #     "data/group_45/intact_images\\RPf_00371_intact_mesh.png"
        # ]
        # csvs_paths = [
        #     # "data/rdp_segments/group_39\\RPf_00319_intact_mesh.csv",
        #     # #"data/rdp_segments/group_39\\RPf_00317_intact_mesh.csv"
        #     # "data/rdp_segments/group_39\\RPf_00320_intact_mesh.csv"
        #     # #"data/rdp_segments/group_45\\RPf_00370_intact_mesh.csv"
        #     "data/rdp_segments/group_45\\RPf_00368_intact_mesh.csv",
        #     "data/rdp_segments/group_45\\RPf_00370_intact_mesh.csv",
        #     "data/rdp_segments/group_45\\RPf_00371_intact_mesh.csv"
        # ]
        group = 39

        if intact_images is None:
            intact_images =sorted(glob.glob(f"data/group_{group}/intact_images/*_intact_mesh.png"))
            csvs_paths = sorted(glob.glob(f"data/rdp_segments/group_{group}/*_intact_mesh.csv"))
        
        assert len(intact_images)>0 and len(csvs_paths)>0
        assert len(intact_images)==len(csvs_paths)
        output_dir = f"data/group_{group}/bands/"

        for img_path,csv_path in zip(intact_images,csvs_paths):
            detect_straight_line_bands(img_path,csv_path,output_dir,is_debug=True)

    if SCRIPT == "detect_bamboo_lines":
        group=45#39
        frag_name = "RPf_00368"
        img_name = f"{frag_name}_opposite_mesh_normals.png" #"RPf_00368_opposite_mesh_normals.png"
        img_path = f"data/group_{group}/{img_name}"
        csv_path = f"data/rdp_segments/group_{group}\\{frag_name}_intact_mesh.csv"
        output_path = f"data/group_{group}\\rotated_bamboo\\{frag_name}_intact_mesh_rotated.csv"
        #img_path = "data/images/RPf_00333_opposite_mesh_normals.png"
        detect_bamboo_lines(img_path,csv_path,output_path,is_debug=True)

    print("finish")


