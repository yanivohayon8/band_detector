from shapely.geometry import LineString,MultiPoint,Polygon,MultiLineString,Point
from shapely import affinity

class PolygonWrapper():

    def __init__(self,polygon_coords:list) -> None:
        #self.coordinates = polygon_coords
        # self.polygon_border = LineString(polygon_coords)#Polygon(polygon_coords)#LineString(polygon_coords)
        self.polygon = Polygon(polygon_coords)#Polygon(polygon_coords)#LineString(polygon_coords)

    def get_coords(self):
        return list(self.polygon.exterior.coords)
    
    def get_coords_separated(self):
        x,y = self.polygon.exterior.coords.xy
        x = x.tolist()
        y = y.tolist()
        return x,y


    def find_intersection(self,line:LineString)->MultiPoint:
        # intersection = self.line_string.intersection(polygon.polygon_border)
        
        intersection = self.polygon.exterior.intersection(line)

        if intersection is None or intersection.is_empty:
            return MultiPoint([])
        
        if isinstance(intersection,MultiPoint):
            return intersection
        
        if isinstance(intersection,Point):            
            return MultiPoint([intersection])
    
    def find_edges_touching_points(self,points:MultiPoint,buffer_size=10):
        coordinates = list(self.polygon.exterior.coords)
        edges_touching_points = []
        
        for i in range(len(coordinates) - 1):
            coord1 = coordinates[i]
            coord2 = coordinates[i + 1]
            edge = LineString([coord1, coord2])
            # edge = edge.buffer(buffer_size)

            #if isinstance(points,MultiPoint):
            if any([point.intersects(edge.buffer(buffer_size)) for point in points.geoms]):
                edges_touching_points.append(edge)
        
        return edges_touching_points
    
    def plot(self,ax,**kwargs):
        coordinates = list(self.polygon.exterior.coords)
        poly_x = [coord[0] for coord in coordinates]
        poly_y = [coord[1] for coord in coordinates]
        ax.plot(poly_x + [poly_x[0]], poly_y + [poly_y[0]], **kwargs)

    def rotated(self,angle_degrees):
        poly =  affinity.rotate(self.polygon,angle_degrees,'center')
        return PolygonWrapper(poly)