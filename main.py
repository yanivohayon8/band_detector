from scripts.intact_surface import detect_straight_line_bands,compute_edge_map_and_segmentation
from scripts.write_csv_to_springs import convert_rdp_folder
from scripts.opposite_surface import detect_bamboo_lines
import os
import glob
import argparse


SCRIPT = "detect_straight_line_bands"#"convert_rdp_folder" #"detect_straight_line_bands" #"detect_bamboo_lines"

if  __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--script", help="Name of the script to run.") # I use
    parser.add_argument("--img_path", help="Image path.") # I use in detect , bamboo
    parser.add_argument("--csv_path", help="CSV path.") # I use in detect, bamboo
    parser.add_argument("--output_path", help="Output path.") # bamboo
    parser.add_argument("--src_folder", help="Source folder.")# I use in convert
    parser.add_argument("--dst_folder", help="Destination folder.") # I use in convert  and detect
    parser.add_argument("--images_folder", help="Images folder.") # I use in convert 
    parser.add_argument("--is_debug", action="store_true", help="Debug mode.")
    args = parser.parse_args()


    if args.script == "seg_and_edge_map":

        root_path = args.src_folder #f"data/intact_imgs"
        images = glob.glob(f"{root_path}/**/RGBA/*.png",recursive=True)

        for i,img_path in enumerate(images):
            splitted = img_path.split("\\") 
            frag_name = splitted[-1].split(".")[0]
            group_name = splitted[-3]
            directory_path = '/'.join(splitted[:-2])
            kmeans_path = directory_path + "/segmentation_kmeans"
            edge_map_path = directory_path + "/edge_map_canny"

            if not os.path.exists(kmeans_path):
                os.makedirs(kmeans_path)
            
            if not os.path.exists(edge_map_path):
                os.makedirs(edge_map_path)
            
            seg_file = kmeans_path+f"/{frag_name}.png"
            edge_file = edge_map_path+f"/{frag_name}.png"
            print(f"Compute the edge map and segmentation of {group_name}/{frag_name} ({i+1}/{len(images)})")
            compute_edge_map_and_segmentation(img_path,seg_file,edge_file)


    elif args.script == "convert_rdp_folder":
        # group_name = "group_39"
        # wp3_folder = "C:\\Users\\97254\\Desktop\\msc\\RePAIR\\projects\\WP3-PuzzleSolving\\"
        # src_folder = wp3_folder+ f"data\\tests\\output\\segments_rdp\\repair-data\\{group_name}\\rdp_10" #"data/rdp_segments/group_45/rdp_10"
        
        # data_folder = f"data\\{group_name}/"
        # images_folder = f"{data_folder}/intact_images"
        # dst_folder = f"{data_folder}/puzzle"
        dst_images_folder = f"{args.dst_folder}/images"

        if not os.path.exists(dst_images_folder):
            os.makedirs(dst_images_folder)

        convert_rdp_folder(args.src_folder,args.dst_folder,args.images_folder)

    elif args.script == "detect_straight_line_bands":
        detect_straight_line_bands(args.img_path,args.csv_path,args.dst_folder,is_debug=True)

    if SCRIPT == "detect_bamboo_lines":
        raise("Under Construction")
        detect_bamboo_lines(args.img_path,args.csv_path,args.output_path,is_debug=True)

    print("finish")


