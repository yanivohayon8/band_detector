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


def detect_straight_line_bands(group,img_name,rdp_csv_path,is_debug=False):
    img_path = f"{intact_images_path}/group_{group}/{img_name}"
    processor = IntactProcessor(img_path)
    img = processor.load_img()
    img_preprocessed = processor.preprocess()
    edge_map = processor.get_edge_map()
    
    hough_lines = hough.detect_hough_lines(edge_map,minimum_votes=100)
    
    band_detector = StraightBandsDetector(hough_lines)
    bands = band_detector.detect()
    bands_as_lines = [ ]
    
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

    intersections = []
    intersected_edges = []
    for band_line in bands_as_lines:
        intersec = convex_hull_.find_intersection(band_line.line_string)
        intersections.append(intersec)
        intersected_edges.append(convex_hull_.find_edges_touching_points(intersec))

        
    

    if is_debug:
        
        img_ = img.copy()
        
        # for line in two_point_lines:
        #     cv2.line(img_,line.point1,line.point2,(255,0,255),2)

        for i,band in enumerate(bands):
            for line in band.hough_lines:
                points = line.sample_two_points(edge_map.shape)
                cv2.line(img_,points[0],points[1],DEBUG_COLORS[i%len(DEBUG_COLORS)],2)

        fig, axs = plt.subplots(1,3)
        axs[0].imshow(img_preprocessed)
        axs[0].set_axis_off()
        axs[1].imshow(edge_map,cmap="gray")
        axs[1].set_axis_off()
        axs[2].imshow(img_)
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


        fig2, ax = plt.subplots(1,1)
        ax.set_aspect("equal",adjustable='box')
        ax.plot(poly_x + [poly_x[0]], poly_y + [poly_y[0]],color="red",label="polygon")
        #fig2.gca().invert_xaxis()
        fig2.gca().invert_yaxis()

        ax.plot(convex_hull_x+[convex_hull_x[0]],convex_hull_y+[convex_hull_y[0]],color="blue",label="Convex Hull",linestyle="dashed")
        #ax.scatter(intersec_x, intersec_y, color='green', label='Intersection Points')
        ax.scatter(closest_x, closest_y, color='purple', label='Closest Vertices')
        
        for i,line in enumerate(bands_as_lines):
            xs = [line.point1[0],line.point2[0]]
            ys = [line.point1[1],line.point2[1]]
            ax.plot(xs,ys,color="black",linewidth=2)

        ax.legend()
        ax.set_axis_off()
        plt.show()
        plt.waitforbuttonpress()
        plt.close()
    
