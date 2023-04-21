import cv2

def draw_line(img,line,color,thickness=2):
    point1 = line[0]
    point2 = line[1]
    cv2.line(img,point1,point2,color,thickness)

def draw_band(img,band,color,distance_between_points=1000,thickness=2):
    line1_point1,line1_point2 = band.first_line.sample_two_points(distance_between_points)
    line2_point1,line2_point2 = band.second_line.sample_two_points(distance_between_points)
    draw_line(img,(line1_point1,line1_point2),color,thickness=thickness)
    draw_line(img,(line2_point1,line2_point2),color,thickness=thickness)

def draw_lines(img,lines,colors=(255,0,255),thickness=2):

    if isinstance(colors,tuple):
        colors_ = [colors]*len(lines)
        colors = colors_

    for color,line in zip(colors,lines):
        point1 = line[0]
        point2 = line[1]
        cv2.line(img,point1,point2,color,thickness)