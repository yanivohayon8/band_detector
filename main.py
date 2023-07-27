from scripts.intact_surface import detect_straight_line_bands,compute_edge_map_and_segmentation
from scripts.write_csv_to_springs import convert_rdp_folder,rdp_to_csv
from scripts.opposite_surface import detect_bamboo_lines
from scripts.visual_postprocessing import draw_line_on_image
import os
import glob
import argparse
import re


SCRIPT = "detect_straight_line_bands"#"convert_rdp_folder" #"detect_straight_line_bands" #"detect_bamboo_lines"

if  __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--script", help="Name of the script to run.",default="detect_straight_line_bands") # I use
    parser.add_argument("--group", help="",default="-1") # I use
    parser.add_argument("--fragment_id", help="",default="all") # I use
    parser.add_argument("--img_path", help="Image path.") # I use in detect , bamboo
    parser.add_argument("--csv_path", help="CSV path.") # I use in detect, bamboo
    parser.add_argument("--output_path", help="Output path.") # bamboo
    parser.add_argument("--src_folder", help="Source folder.")# I use in convert
    parser.add_argument("--dst_folder", help="Destination folder.") # I use in convert  and detect
    parser.add_argument("--images_folder", help="Images folder.") # I use in convert 
    parser.add_argument("--is_debug", action="store_true", help="Debug mode.")
    parser.add_argument("--minimum_votes", help="minimum_votes.",default=100) # I use in detect , bamboo
    parser.add_argument("--theta_diff", help="theta_diff.",default=0.05) # I use in detect , bamboo
    parser.add_argument("--rho_diff", help="rho_diff.",default=100) # I use in detect , bamboo
    parser.add_argument("--min_band_width", help="min_band_width.",default=10) # I use in detect , bamboo
    parser.add_argument("--max_band_theta_variance", help="max_band_theta_variance.",default=0.005) # I use in detect , bamboo

    args = parser.parse_args()


    if args.script == "seg_and_edge_map":

        root_path = args.src_folder #f"data/intact_imgs" #
        images = glob.glob(f"{root_path}/**/*.png",recursive=True)

        for i,img_path in enumerate(images):
            splitted = img_path.split("\\") 
            frag_name = splitted[-1].split(".")[0]
            group_name = splitted[-2]
            directory_path = '/'.join(splitted[:-2])
            kmeans_path = f"data/segmentation_kmeans/{group_name}"#directory_path + "/segmentation_kmeans"
            edge_map_path = f"data/edge_map_canny/{group_name}" #directory_path + "/edge_map_canny"

            if not os.path.exists(kmeans_path):
                os.makedirs(kmeans_path)
            
            if not os.path.exists(edge_map_path):
                os.makedirs(edge_map_path)
            
            edge_file = edge_map_path+f"/{frag_name}.png"
            seg_file = kmeans_path+f"/{frag_name}.png"
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

    elif args.script == "rdp_to_csv_per_piece":
        
        def single_piece(group,fragment):
            rdp_csv_path = f"data/rdp_segments/group_{group}\\{fragment}_intact_mesh.csv"
            img_path =f"../../RGBA/group_{group}\\{fragment}_intact_mesh.png" #f"data/group_{group}/intact_images\\{fragment_id}_intact_mesh.png"
            dst_working_dir = "C:\\Users\\97254\\Desktop\\msc\\RePAIR\\projects\\springs_assembler_sfml\\2D_puzzle_springs_assembler\\data\\RePAIR"
            dst_csv_folder = dst_working_dir+f"\\csv" #dst_working_dir+f"\\group_{group}\\csv"
            dst_img_folder = dst_working_dir+f"\\images"#dst_working_dir+f"\\group_{group}\\images"

            if not os.path.exists(dst_csv_folder):
                os.makedirs(dst_csv_folder)
            
            if not os.path.exists(dst_img_folder):
                os.makedirs(dst_img_folder)
            
            dst_csv_file = dst_csv_folder+f"\\{fragment}_intact_mesh.csv"
            dst_img_file = dst_img_folder+f"\\{fragment}_intact_mesh.png"

            rdp_to_csv(rdp_csv_path,img_path,dst_csv_file,dst_img_file)
        
        if args.group != "-1":
            
            if args.fragment_id == "all":
                # RPf_00344_intact_mesh.png.csv an example of csv
                fragments_ids = [re.search("RPf_\d{5}",csv_name).group() for csv_name in glob.glob(f"data/rdp_segments/group_{args.group}/*.csv")] 
                [single_piece(args.group,fragment_id) for fragment_id in fragments_ids]
            else:
                single_piece(args.group,args.fragment_id)
        

    elif args.script == "detect_straight_line_bands":
        
        def run_on_single_piece(group,fragment_id):
            dst_folder = f"data/bands/group_{group}/{fragment_id}/"
            csv_path = f"data/rdp_segments/group_{group}\\{fragment_id}_intact_mesh.csv"
            img_path =f"../../RGBA/group_{group}\\{fragment_id}_intact_mesh.png" #f"data/group_{group}/intact_images\\{fragment_id}_intact_mesh.png"

            if not os.path.exists(dst_folder):
                os.makedirs(dst_folder)

            print(f"***** Running on fragment {fragment_id} in group {group} ****")
            detect_straight_line_bands(img_path,csv_path,dst_folder,
                                    minimum_votes=int(args.minimum_votes),
                                    rho_diff=int(args.rho_diff),theta_diff=float(args.theta_diff),
                                    min_band_width=int(args.min_band_width),
                                    max_band_theta_variance=float(args.max_band_theta_variance),
                                        is_debug=args.__dict__["is_debug"])
        
        if args.group != "-1":
            
            if args.fragment_id == "all":
                # RPf_00344_intact_mesh.png.csv an example of csv
                fragments_ids = [re.search("RPf_\d{5}",csv_name).group() for csv_name in glob.glob(f"data/rdp_segments/group_{args.group}/*.csv")] 
                [run_on_single_piece(args.group,fragment_id) for fragment_id in fragments_ids]
            else:
                run_on_single_piece(args.group,args.fragment_id)
        else:
            detect_straight_line_bands(args.img_path,args.csv_path,args.dst_folder,
                                    minimum_votes=int(args.minimum_votes),
                                    rho_diff=int(args.rho_diff),theta_diff=float(args.theta_diff),
                                    min_band_width=int(args.min_band_width),
                                    max_band_theta_variance=float(args.max_band_theta_variance),
                                        is_debug=args.__dict__["is_debug"])

        
    elif args.script == "draw_representive_line":
        def single_piece(group,fragment_id):
            # group = args.group
            # fragment_id = args.fragment_id
            base_folder= f"data/bands/group_{group}/{fragment_id}"
            json_file = f"{base_folder}/{fragment_id}_intact_mesh.json"
            input_image = f"../../RGBA/group_{group}\\{fragment_id}_intact_mesh.png"
            output_image = f"{base_folder}/{fragment_id}_intact_mesh.png"
            draw_line_on_image(json_file,input_image,output_image)
        
        if args.group != "-1":
            if args.fragment_id == "all":
                # RPf_00344_intact_mesh.png.csv an example of csv
                fragments_ids = [re.search("RPf_\d{5}",csv_name).group() for csv_name in glob.glob(f"data/rdp_segments/group_{args.group}/*.csv")] 
                [single_piece(args.group,fragment_id) for fragment_id in fragments_ids]
            else:
                single_piece(args.group,args.fragment_id)

    if SCRIPT == "detect_bamboo_lines":
        raise("Under Construction")
        detect_bamboo_lines(args.img_path,args.csv_path,args.output_path,is_debug=True)

    print("finish")


