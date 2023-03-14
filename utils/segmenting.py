def segment_kmeans(img, n_clusters,random_state=0):
    img_normalized = img/255.0
    img_n = img_normalized.reshape(img_normalized.shape[0]*img_normalized.shape[1], img_normalized.shape[2]) # transform to 2d array
    kmeans = KMeans(n_clusters=n_clusters,random_state=random_state).fit(img_n)
    colors_pool = np.array([
        [255,77,0],
        [30,144,255],
        [173,255,47],        
        [255,0,0],
        [0,0,0],
        [255,255,255],
        [255,4,0]
        
    ])
    len_ = colors_pool.shape[0]
    segments_colors = np.array([colors_pool[i%len_] for i in range(len(kmeans.cluster_centers_))])
    img_segmented = segments_colors[kmeans.labels_]
    return img_segmented.reshape(img.shape[0],img.shape[1],img.shape[2])


def pick_color_segment(img_hsv,img_rgb,color="orange"):
    #img_rpf_000102_kmeans_hsv = cv2.cvtColor((kmeans_img*255).astype(np.uint8),cv2.COLOR_RGB2HSV)
    light_orange = (1, 190, 200)
    dark_orange = (18, 255, 255)
    orange_mask = cv2.inRange(img_hsv,light_orange,dark_orange)
    #segment_orange_img = cv2.bitwise_and((kmeans_img*255).astype(np.uint8),(kmeans_img*255).astype(np.uint8),mask=orange_mask)
    segment_orange_img = cv2.bitwise_and(img_rgb,img_rgb,mask=orange_mask)
    return orange_mask,segment_orange_img
    #plot_images([orange_mask,segment_orange_img],["orange_mask","segment_orange_img"],1,2)