from shapely.geometry import LineString,MultiPoint

class TwoPointsLine():
    def __init__(self,point1,point2) -> None:
        self.point1 = point1
        self.point2 = point2
        self.line_string = LineString([point1,point2])
    
    def plot(self,ax,**kwargs):
        line_x = [self.point1[0],self.point2[0]]
        line_y = [self.point1[1],self.point2[1]]
        ax.plot(line_x, line_y, **kwargs)


class TwoPointsBand():

    def __init__(self,line1:TwoPointsLine,line2:TwoPointsLine) -> None:
        self.line1 = line1
        self.line2 = line2

