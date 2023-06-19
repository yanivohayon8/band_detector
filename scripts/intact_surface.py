intact_images_path = "data/images"
from src.image_processing.processors import IntactProcessor
import matplotlib.pyplot as plt
from src.bands import hough
from src.bands import two_points
import cv2
from src.intact_surface_detectors import StraightBandsDetector
from src import DEBUG_COLORS
from src.loader import RdpDataloader
from src.geometry import PolygonWrapper
import json


def compute_edge_map_and_segmentation(img_path,output_file_seg,output_file_edge_map):
    processor = IntactProcessor(img_path)
    img = processor.load_img()
    img_segmented = processor.preprocess()
    edge_map = processor.get_edge_map()

    cv2.imwrite(output_file_seg,cv2.cvtColor(img_segmented,cv2.COLOR_BGR2RGBA))
    cv2.imwrite(output_file_edge_map,edge_map)


def detect_straight_line_bands(img_path,rdp_csv_path,output_dir,minimum_votes=100,is_debug=False):
    #img_path = f"{intact_images_path}/group_{group}/{img_name}"
    processor = IntactProcessor(img_path)
    img = processor.load_img()
    img_preprocessed = processor.preprocess()
    edge_map = processor.get_edge_map()
    hough_lines = hough.detect_hough_lines(edge_map,minimum_votes=minimum_votes)
    band_detector = StraightBandsDetector(hough_lines)
    bands = band_detector.detect()
    bands_as_lines = []
    
    for band in bands:
        line = band.get_representive_line()
        points = line.sample_two_points(edge_map.shape)
        bands_as_lines.append(two_points.TwoPointsLine(points[0],points[1]))

    rdp_loader = RdpDataloader(rdp_csv_path)
    rdp_loader.load()
    polygon_coords = rdp_loader.get_polygon_coords()
    polygon = PolygonWrapper(polygon_coords)
    convex_hull = polygon.polygon.convex_hull
    con_x,con_y = convex_hull.exterior.xy
    convex_hull_ = PolygonWrapper([(x,y) for x,y in zip (con_x.tolist(),con_y.tolist())])

    # convex_hull_intersections = []
    # convex_hull_intersected_edges = []
    # for band_line in bands_as_lines:
    #     intersec = convex_hull_.find_intersection(band_line.line_string)
    #     convex_hull_intersections.append(intersec)
    #     convex_hull_intersected_edges.append(convex_hull_.find_edges_touching_points(intersec))

    intersections = []
    intersected_edges = []
    for band_line in bands_as_lines:
        intersec = polygon.find_intersection(band_line.line_string)
        intersections.append(intersec)
        intersected_edges.append(polygon.find_edges_touching_points(intersec))

        
    img_with_bands = img.copy()
    bands_json = []

    for i,band in enumerate(bands):
        band_color = DEBUG_COLORS[i%len(DEBUG_COLORS)]
        lines_as_json = []

        for line in band.hough_lines:
            points = line.sample_two_points(edge_map.shape)
            cv2.line(img_with_bands,points[0],points[1],band_color,2)
            lines_as_json.append(line.toJson())

        band_width = band.get_width()

        bands_json.append(
            {
                "debug_color":band_color,
                "lines":lines_as_json,
                "width":int(band_width)
            }
        )


    for i,edge_pair in enumerate(intersected_edges):
        print("###Vertices indexes of intersected edges for the next band:")
        coords_of_closest = []
        index_of_closest = []

        for edge in edge_pair:
            xs,ys = edge.xy
            xs = xs.tolist()
            ys = ys.tolist()
            
            for x,y in zip(xs,ys):
                cord_ = (x,y)
                contour_vertex_index = polygon.get_coords().index(cord_)
                coords_of_closest.append((str(x),str(y)))
                index_of_closest.append(contour_vertex_index)
                #print(f"The index of ({x},{y}) is {vertex_index} ",end=",")
        
        bands_json[i]["closest_vertices"] = {}
        bands_json[i]["closest_vertices"]["coords"] = coords_of_closest
        bands_json[i]["closest_vertices"]["indices"] = index_of_closest

    
    '''Write the results'''
    image_name = img_path.split("\\")[-1].split(".")[0]
    cv2.imwrite(output_dir+f"/{image_name}.png",img_with_bands)

    with open(output_dir+f"{image_name}.json",'w') as fp:
        json.dump(bands_json,fp)

    

    if is_debug:
        fig, axs = plt.subplots(1,3)
        axs[0].imshow(img_preprocessed)
        axs[0].set_axis_off()
        axs[1].imshow(edge_map,cmap="gray")
        axs[1].set_axis_off()
        axs[2].imshow(img_with_bands)
        axs[2].set_axis_off()

        poly_x = [coord[0] for coord in polygon_coords]
        poly_y = [coord[1] for coord in polygon_coords]
        convex_hull_x,convex_hull_y = convex_hull.exterior.xy
        convex_hull_x = convex_hull_x.tolist()
        convex_hull_y = convex_hull_y.tolist()

        intersec_x = []
        intersec_y = []

        for intersec in intersections:
            _ = [vertex for vertex in list(intersec.geoms)]
            intersec_x = intersec_x + [coord.x for coord in _]
            intersec_y = intersec_y + [coord.y for coord in _]
        
        closest_x = []
        closest_y = []

        for edge_pair in intersected_edges:
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
        
        for i,line in enumerate(bands_as_lines):
            xs = [line.point1[0],line.point2[0]]
            ys = [line.point1[1],line.point2[1]]
            ax.plot(xs,ys,color="black",linewidth=2)

        ax.legend()
        ax.set_axis_off()

        fig2.savefig(f"{output_dir}/{image_name}_polygon.png")

        plt.show()
        plt.waitforbuttonpress()
        plt.close()
    
    
