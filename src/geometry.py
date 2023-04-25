from shapely.geometry import LineString,MultiPoint,Polygon,MultiLineString

class PolygonWrapper():

    def __init__(self,polygon_coords:list) -> None:
        self.coordinates = polygon_coords
        # self.polygon_border = LineString(polygon_coords)#Polygon(polygon_coords)#LineString(polygon_coords)
        self.polygon = Polygon(polygon_coords)#Polygon(polygon_coords)#LineString(polygon_coords)


    def find_intersection(self,line:LineString)->MultiPoint:
        # intersection = self.line_string.intersection(polygon.polygon_border)
        
        intersection = self.polygon.exterior.intersection(line)

        if intersection is None or intersection.is_empty:
            return MultiPoint([])
        
        return intersection
    
    def find_edges_touching_points(self,points:MultiPoint,buffer_size=10):
        edges_touching_points = []
        
        for i in range(len(self.coordinates) - 1):
            coord1 = self.coordinates[i]
            coord2 = self.coordinates[i + 1]
            edge = LineString([coord1, coord2])
            # edge = edge.buffer(buffer_size)

            #if isinstance(points,MultiPoint):
            if any([point.intersects(edge.buffer(buffer_size)) for point in points.geoms]):
                edges_touching_points.append(edge)
        
        return edges_touching_points
    
    def plot(self,ax,**kwargs):
        poly_x = [coord[0] for coord in self.coordinates]
        poly_y = [coord[1] for coord in self.coordinates]
        ax.plot(poly_x + [poly_x[0]], poly_y + [poly_y[0]], **kwargs)
