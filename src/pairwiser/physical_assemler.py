from shapely import Polygon
from shapely import unary_union
from src.my_http_client import SpringsHTTPClient

def semi_dice_coef_overlapping(polygons:list):
    shapely_polygons = [Polygon(poly) for poly in polygons]
    dice_sum = 0

    for i in range(len(shapely_polygons)):
        other_polygons = [shapely_polygons[j] for j in range(len(shapely_polygons)) if i!=j]    
        other_union = unary_union(other_polygons)
        curr_intersect_with_other = shapely_polygons[i].intersection(other_union)
        dice_sum+= curr_intersect_with_other.area/shapely_polygons[i].area

    return dice_sum


class PhysicalAssembler():

    def __init__(self,http:SpringsHTTPClient) -> None:
        self.http = http
        # self.id2piece = id2piece # no need it (its old)
    
        
    def run(self, body,screenshot_name=""):
        response = self.http.send_reconstruct_request(body,screenshot_name=screenshot_name)
        return response
    
    def score_assembly(self,response,area_weight=0.5):
        '''
            response- a json of the following fields
                piecesBeforeEnableCollision: list of polygons (list of tuples)
                AfterEnableCollision: springs sum + springs lengths
        '''
        polygons_coords = [piece_json["coordinates"] for piece_json in response["piecesBeforeEnableCollision"] ]
        overalap_area = semi_dice_coef_overlapping(polygons_coords)
        sum_springs_length = response["AfterEnableCollision"]["sumSpringsLength"]
        
        # Notice: overalap_area is a small a number, and sum_springs_length is a big number....
        return area_weight*overalap_area +  (1-area_weight)*sum_springs_length