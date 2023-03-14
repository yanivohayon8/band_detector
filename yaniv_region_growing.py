import cv2
import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib import colors
from mpl_toolkits.mplot3d import Axes3D  # noqa
from matplotlib.colors import hsv_to_rgb

UNVISITED = -1
SKIPPED = 0


#class pour une pile
# class Stack():
#     def __init__(self):
#         self.item = []
#         self.obj=[]
#     def push(self, value):
#         self.item.append(value)

#     def pop(self):
#         return self.item.pop()

#     def size(self):
#         return len(self.item)

#     def isEmpty(self):
#         return self.size() == 0

#     def clear(self):
#         self.item = []


class regionGrow():
  
    def __init__(self,im,th):
        self.im  = im
        self.n_rows, self.n_cols,_ =  self.im.shape
        self.labels = np.full((self.n_rows,self.n_cols), UNVISITED)
        self.n_region = 0
        self.iterations=0
        self.segments=np.zeros((self.n_rows,self.n_cols,3), dtype='uint8')
        self.queue = [] #Stack()
        self.thresh=float(th)
        # self.random_seed = [[self.h/2,self.w/2],
        #     [self.h/3,self.w/3],[2*self.h/3,self.w/3],[self.h/3-10,self.w/3],
        #     [self.h/3,2*self.w/3],[2*self.h/3,2*self.w/3],[self.h/3-10,2*self.w/3],
        #     [self.h/3,self.w-10],[2*self.h/3,self.w-10],[self.h/3-10,self.w-10]
                    # ]

    def show_image(self,output_path):
        segments_colors = np.array(
                            [
                                255 * np.array([random.uniform(0,1),random.uniform(0,1),random.uniform(0,1)])
                                for _ in range(self.n_region+1)])
        self.out_img = segments_colors[self.labels.reshape(-1)]
        self.out_img = self.out_img.reshape(
            self.im.shape[0],
            self.im.shape[1],
            self.im.shape[2]
        )

        cv2.imwrite(output_path,self.out_img)

    def get_neighbours(self,pixel,direction_origin=None):
        neighbours = []
        x0 = pixel[0]
        y0 = pixel[1]
        for i in (-1,0,1):
            for j in (-1,0,1):
    
                if (i,j) == (0,0): 
                    continue
                x = x0+i
                y = y0+j

                if 0<=x<self.n_rows and 0<=y<self.n_cols:
                    neighbours.append((x,y))

        return neighbours

    def plant_seed(self,next_pixel):
        self.n_region+=1
        self.labels[next_pixel[0],next_pixel[1]] = self.n_region

        #neighbors = self.get_neighbours(next_pixel)
        #self.add_to_line(neighbors)

    # def add_to_line(self,pixels):
    #     [self.queue.append(pixel) for pixel in pixels if self.labels[pixel[0],pixel[1]]==0]

    def run(self):
        first_seed = (int(self.n_rows/2),int(self.n_cols/2))
        self.plant_seed(first_seed)
        [self.queue.append(pixel) for pixel in self.get_neighbours(first_seed)]

        while True:
            
            while(len(self.queue) > 0):
                next_pixel = self.queue.pop(0)       
                pixels_to_queued = self.breadth_scan(next_pixel,self.n_region)
                [self.queue.append(p) for p in pixels_to_queued]
            
            pixels_remains = np.argwhere(self.labels<1)
            n_remains = pixels_remains.size/3
            if n_remains == 0:
                break

            #print(f"The number of remaining pixels is {n_remains}")
            next_seed = (pixels_remains[0,0],pixels_remains[0,1])
            self.plant_seed(next_seed)
            self.queue.append(next_seed)

    def breadth_scan(self,origin_pixel,region):
        #curr_region = self.labels[origin_pixel[0],origin_pixel[1]]
        neighbors = self.get_neighbours(origin_pixel)
        to_be_queued = []

        for x_neigh,y_neigh in neighbors:
            
            if self.labels[x_neigh,y_neigh] == UNVISITED:
                origin_val = self.im[origin_pixel[0],origin_pixel[1],:]
                neigh_val = self.im[x_neigh,y_neigh,:]
                
                #if np.linalg.norm(origin_val-neigh_val) > self.thresh:
                measure = np.dot(origin_val,neigh_val)/(np.linalg.norm(origin_val)*np.linalg.norm(neigh_val))
                epsilon = 0.0001
                if  measure > self.thresh - epsilon:
                    self.labels[x_neigh,y_neigh] = region
                    to_be_queued.append((x_neigh,y_neigh))
                else:
                    self.labels[x_neigh,y_neigh] = SKIPPED
        
        return to_be_queued
    
        
if __name__ == "__main__":
    im = cv2.imread("smoothed_RPf_00102.png").astype('float32')
    im = cv2.cvtColor(im,cv2.COLOR_BGR2HSV)


    
    # h, s, v = cv2.split(im)

    # fig = plt.figure()
    # axis = fig.add_subplot(1, 1, 1, projection="3d")
    # pixel_colors = im.reshape((np.shape(im)[0] * np.shape(im)[1], 3))
    # norm = colors.Normalize(vmin=-1.0, vmax=1.0)
    # norm.autoscale(pixel_colors)
    # pixel_colors = norm(pixel_colors).tolist()
    # axis.scatter(
    #     h.flatten(), s.flatten(), v.flatten(), facecolors=pixel_colors, marker="."
    # )
    # axis.set_xlabel("Hue")
    # axis.set_ylabel("Saturation")
    # axis.set_zlabel("Value")
    # plt.show()


    center_x = int(im.shape[0]/2)
    center_y = int(im.shape[1]/2)
    size_crop = 10
    #im = im[center_x:center_x+size_crop, center_y:center_y+size_crop,:]


    algo = regionGrow(im,1)
    algo.run()
    algo.show_image()