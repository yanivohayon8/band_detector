from scripts.intact_surface import detect_straight_line_bands

if  __name__ == "__main__":
    csv_path = "data/rdp_segments/group_45/csv/RPf_00368_intact_mesh_rdp_10.csv"

    detect_straight_line_bands(45,"RPf_00368_intact_mesh.png",csv_path,is_debug=True)
    print("finish")


