intact_images_path = "data/images"
from src.image_processing.processors import IntactProcessor
from src.image_processing.utils import line_pixels
import matplotlib.pyplot as plt
from src.bands import hough
from src.bands import two_points
import cv2
from src.intact_surface_detectors import StraightBandsDetector
from src import DEBUG_COLORS
from src.loader import RdpDataloader
from src.geometry import PolygonWrapper
import json
import numpy as np

def compute_edge_map_and_segmentation(img_path,output_file_seg,output_file_edge_map):
    processor = IntactProcessor(img_path)
    img = processor.load_img()
    img_segmented = processor.preprocess()
    edge_map = processor.get_edge_map()

    cv2.imwrite(output_file_seg,cv2.cvtColor(img_segmented,cv2.COLOR_BGR2RGBA))
    cv2.imwrite(output_file_edge_map,edge_map)


def detect_straight_line_bands(img_path,rdp_csv_path,output_dir,
                               minimum_votes=100,theta_diff = 1, rho_diff = 200,
                               min_band_width=50,
                               max_band_theta_variance=0.2,
                               max_color_var = 8000,
                               is_debug=False):
    rdp_loader = RdpDataloader(rdp_csv_path)
    rdp_loader.load()
    polygon_coords = rdp_loader.get_polygon_coords()
    polygon = PolygonWrapper(polygon_coords)
    convex_hull = polygon.polygon.convex_hull
    # con_x,con_y = convex_hull.exterior.xy
    # convex_hull_ = PolygonWrapper([(x,y) for x,y in zip (con_x.tolist(),con_y.tolist())])

    processor = IntactProcessor(img_path)
    img = processor.load_img()
    img_preprocessed,labels = processor.preprocess(n_clusters=3)
    img_masked = processor.masked_image(2) # We have 3 clusters and empirically this has the highest variance in color (todo: compute the var?)
    edge_map = processor.get_edge_map(img_masked)

    hough_lines = hough.detect_hough_lines(edge_map,minimum_votes=minimum_votes)
    band_detector = StraightBandsDetector(hough_lines)
    raw_bands = band_detector.detect(theta_diff=theta_diff,rho_diff=rho_diff)
    
    img_with_bands = img.copy()
    bands_json = []
    debug_all_intersections = []
    debug_all_intersected_edges = []
    debug_all_bands_as_lines = []

    for band in raw_bands:
        
        print(f"Detected potential band:")
        width = band.get_width()
        print(f"\t width {width}")

        if  width < min_band_width:
            print(f"\t {width} < {min_band_width}, reject the potential band")
            continue

        theta_variance = band.get_theta_variance()
        print(f"\t theta variance {theta_variance}")

        if theta_variance > max_band_theta_variance:
            print(f"\t {theta_variance} > {max_band_theta_variance}, reject the potential band")
            continue


        representive_line = band.get_representive_line()
        shape_shrink = (edge_map.shape[0]-1,edge_map.shape[1]-1)
        points = representive_line.sample_two_points(shape_shrink)
        band_two_points = two_points.TwoPointsLine(points[0],points[1])

        intersec = polygon.find_intersection(band_two_points.line_string)
        intersected_edges = polygon.find_edges_touching_points(intersec)

        # four is heuristic number since the polygon shape is concave
        if len(intersected_edges) >4:
            print(f"\t {len(intersected_edges)} >4 , reject the potential band (maybe it is a contour edge?)")
            continue

        pixels = line_pixels(img,points[0],points[1])
        pixels = [non_transparent for non_transparent in pixels if np.linalg.norm(non_transparent)>0] 
        
        channels_variance = np.var(pixels,axis=0)
        print(f"\t color variance ({channels_variance[0]},{channels_variance[1]},{channels_variance[2]})")

        #5000
        if channels_variance[0] > max_color_var or channels_variance[1]> max_color_var or channels_variance[2] > max_color_var:
            print(f"\t Each color variance of a channel should be less than {max_color_var}, rejecting potential band.")
            continue
        
        print("Since the band passed all the test, confirm the band")
        debug_all_intersections.append(intersec) # 
        debug_all_intersected_edges.append(intersected_edges)
        debug_all_bands_as_lines.append(band_two_points)


        debug_band_color = DEBUG_COLORS[len(bands_json)%len(DEBUG_COLORS)]
        avg_color = np.mean(pixels,axis=0)
        
        band_hough_lines_as_json = []
        for hg_line in band.hough_lines:
            hg_line_points = hg_line.sample_two_points(edge_map.shape)
            cv2.line(img_with_bands,hg_line_points[0],hg_line_points[1],debug_band_color,2)
            band_hough_lines_as_json.append(hg_line.toJson())

        #cv2.line(img_with_bands,points[0],points[1],debug_band_color,int(width))

        coords_of_closest = []
        index_of_closest = []

        for edge in intersected_edges:#edge_pair:
            xs,ys = edge.xy
            xs = xs.tolist()
            ys = ys.tolist()
            
            for x,y in zip(xs,ys):
                cord_ = (x,y)
                contour_vertex_index = polygon.get_coords().index(cord_)
                coords_of_closest.append((str(x),str(y)))
                index_of_closest.append(contour_vertex_index)

        bands_json.append(
            {
                "representive_line": [band_two_points.point1,band_two_points.point2],
                "lines":band_hough_lines_as_json,
                "width":int(width),
                "theta_variance":str(theta_variance),
                "color_variance":(str(channels_variance[0]),str(channels_variance[1]),str(channels_variance[2])),
                "color_average":(int(avg_color[0]),int(avg_color[1]),int(avg_color[2])),
                "debug_color":debug_band_color,
                "closest_vertices_on_contour":{
                    "coords":coords_of_closest,
                    "indices":index_of_closest
                }
            }
        )
        
    # bands_as_lines = []

    
    # for band in bands:
    #     line = band.get_representive_line()
    #     shape_shrink = (edge_map.shape[0]-1,edge_map.shape[1]-1)
    #     points = line.sample_two_points(shape_shrink)
    #     bands_as_lines.append(two_points.TwoPointsLine(points[0],points[1]))

    

    # intersections = []
    # intersected_edges = []
    # for band_line in bands_as_lines:
    #     intersec = polygon.find_intersection(band_line.line_string)
    #     intersections.append(intersec)
    #     intersected_edges.append(polygon.find_edges_touching_points(intersec))

    # bands_json = []

   

    
    '''Write the results'''
    image_name = img_path.split("\\")[-1].split(".")[0]
    cv2.imwrite(output_dir+f"/{image_name}.png",cv2.cvtColor(img_with_bands,cv2.COLOR_BGR2RGB))

    with open(output_dir+f"{image_name}.json",'w') as fp:
        json.dump(bands_json,fp)

    

    img_with_raw_lines = np.copy(img)

    for ln in hough_lines:
        ln_points = ln.sample_two_points(img.shape)
        cv2.line(img_with_raw_lines,ln_points[0],ln_points[1],(255,0,0),2)

    if not is_debug:
        plt.ioff()

    fig, axs = plt.subplots(2,2)
    #axs[0].imshow(img_preprocessed)
    axs[0,0].imshow(img_masked)
    axs[0,0].set_title("Masking")
    axs[0,0].set_axis_off()
    axs[0,1].imshow(edge_map,cmap="gray")
    axs[0,1].set_title("Edge Map")
    axs[0,1].set_axis_off()
    axs[1,0].imshow(img_with_raw_lines)
    axs[1,0].set_title("All detected lines ")
    axs[1,0].set_axis_off()
    axs[1,1].imshow(img_with_bands)
    axs[1,1].set_title("Detected Bands")
    axs[1,1].set_axis_off()

    poly_x = [coord[0] for coord in polygon_coords]
    poly_y = [coord[1] for coord in polygon_coords]
    convex_hull_x,convex_hull_y = convex_hull.exterior.xy
    convex_hull_x = convex_hull_x.tolist()
    convex_hull_y = convex_hull_y.tolist()

    intersec_x = []
    intersec_y = []

    for intersec in debug_all_intersections:
        _ = [vertex for vertex in list(intersec.geoms)]
        intersec_x = intersec_x + [coord.x for coord in _]
        intersec_y = intersec_y + [coord.y for coord in _]
    
    closest_x = []
    closest_y = []

    for edge_pair in debug_all_intersected_edges:
        print("###Vertices indexes of intersected edges for the next band:")
        for edge in edge_pair:
            xs,ys = edge.xy
            xs = xs.tolist()
            ys = ys.tolist()
            closest_x= closest_x + xs 
            closest_y= closest_y + ys

            
            for x,y in zip(xs,ys):
                vertex_index = polygon_coords.index((x,y))
                print(f"The index of ({x},{y}) is {vertex_index} ",end=",")
        print()

    fig.savefig(f"{output_dir}/{image_name}_pipeline.png")


    # if not is_debug:
    #     plt.ioff()
        
    fig2, ax = plt.subplots(1,1)
    ax.set_aspect("equal",adjustable='box')
    poly_x_plot = poly_x + [poly_x[0]]
    poly_y_plot = poly_y + [poly_y[0]]
    ax.plot(poly_x_plot,poly_y_plot ,color="red",label="polygon")

    for i,coord in enumerate(polygon_coords):
        ax.annotate(i,(coord[0]-1,coord[1]-1))



    #fig2.gca().invert_xaxis()
    fig2.gca().invert_yaxis()

    ax.plot(convex_hull_x+[convex_hull_x[0]],convex_hull_y+[convex_hull_y[0]],color="blue",label="Convex Hull",linestyle="dashed")
    ax.scatter(intersec_x, intersec_y, color='green', label='Intersection Points')
    #ax.scatter(closest_x, closest_y, color='purple', label='Closest Vertices')
    
    for i,line in enumerate(debug_all_bands_as_lines):
        xs = [line.point1[0],line.point2[0]]
        ys = [line.point1[1],line.point2[1]]
        ax.plot(xs,ys,color="black",linewidth=2)

    ax.legend()
    ax.set_axis_off()
    
    fig2.savefig(f"{output_dir}/{image_name}_polygon.png")

    if is_debug:
        plt.waitforbuttonpress()
        plt.close()
    
    
