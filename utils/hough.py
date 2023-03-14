def r_theta_to_points(r,theta,point_distance=1000):
    a,b = np.cos(theta), np.sin(theta)
    x0,y0 = a*r, b*r
    x1,y1 = int(x0 + point_distance * (-b)), int(y0 + point_distance*a)
    x2,y2 = int(x0 - point_distance * (-b)), int(y0 - point_distance*a)
    return [(x1,y1),(x2,y2)]

def find_parallel_lines(out_lines,max_theta_thresh = 0.06,min_r_thresh = 100):
    parrallel_lines = [] # will contain indexes from out_lines
    for line_i in range(len(out_lines)):
        for line_j in range(len(out_lines)):
            if line_i == line_j:
                continue
                
            # check for duplicates
            if (line_j,line_i) in parrallel_lines or (line_i,line_j) in parrallel_lines:
                continue
            r_diff = abs(out_lines[line_i][0]-out_lines[line_j][0])
            theta_diff = abs(out_lines[line_i][1]-out_lines[line_j][1])
            if  r_diff > min_r_thresh and theta_diff < max_theta_thresh:
                parrallel_lines.append((line_i,line_j))
    return parrallel_lines

def draw_hough_lines(img,edge_map,
                     theta_res,rho_res=1,min_votes=150,point_distance=1000,
                    lines_color = (255,0,0)):
    '''
        theta_res = np.pi/180
    '''
    
    lines_map = cv2.HoughLines(edge_map,rho_res,theta_res,min_votes,0,0)
    
    #print(lines_map)
    
    
    outlines  = []
    #for r,theta in lines_map:
    for line in lines_map:
        r,theta = line[0]
        a,b = np.cos(theta), np.sin(theta)
        x0,y0 = a*r, b*r
        x1,y1 = int(x0 + point_distance * (-b)), int(y0 + point_distance*a)
        x2,y2 = int(x0 - point_distance * (-b)), int(y0 - point_distance*a)
        outlines.append([r,theta])
        cv2.line(img,(x1,y1),(x2,y2),lines_color,2)
    return img,outlines


import imageio
import math

def hough_line(img, angle_step=1, lines_are_white=True, value_threshold=5):
    """
    Hough transform for lines
    Input:
    img - 2D binary image with nonzeros representing edges
    angle_step - Spacing between angles to use every n-th angle
                 between -90 and 90 degrees. Default step is 1.
    lines_are_white - boolean indicating whether lines to be detected are white
    value_threshold - Pixel values above or below the value_threshold are edges
    Returns:
    accumulator - 2D array of the hough transform accumulator
    theta - array of angles used in computation, in radians.
    rhos - array of rho values. Max size is 2 times the diagonal
           distance of the input image.
    """
    # Rho and Theta ranges
    thetas = np.deg2rad(np.arange(-90.0, 90.0, angle_step))
    width, height = img.shape
    diag_len = int(round(math.sqrt(width * width + height * height)))
    rhos = np.linspace(-diag_len, diag_len, diag_len * 2)

    # Cache some resuable values
    cos_t = np.cos(thetas)
    sin_t = np.sin(thetas)
    num_thetas = len(thetas)

    # Hough accumulator array of theta vs rho
    accumulator = np.zeros((2 * diag_len, num_thetas), dtype=np.uint8)
    # (row, col) indexes to edges
    are_edges = img > value_threshold if lines_are_white else img < value_threshold
    y_idxs, x_idxs = np.nonzero(are_edges)

    # Vote in the hough accumulator
    for i in range(len(x_idxs)):
        x = x_idxs[i]
        y = y_idxs[i]

        for t_idx in range(num_thetas):
            # Calculate rho. diag_len is added for a positive index
            rho = diag_len + int(round(x * cos_t[t_idx] + y * sin_t[t_idx]))
            accumulator[rho, t_idx] += 1

    return accumulator, thetas, rhos


def show_hough_line(img, accumulator, thetas, rhos, save_path=None):
    plt.imshow(accumulator, aspect='auto',cmap='jet', extent=[np.rad2deg(thetas[-1]), np.rad2deg(thetas[0]), rhos[-1], rhos[0]])
    if save_path is not None:
        plt.savefig(save_path, bbox_inches='tight')
    plt.show()