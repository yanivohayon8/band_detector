def mean_smooth_rgb(img,kernel_size):
    def mean_smooth_channel(channel,kernel_size):
        mean_kernel = np.ones(kernel_size,np.float32)/(kernel_size[0]*kernel_size[1])
        return cv2.filter2D(channel,-1,mean_kernel)
    r,g,b = cv2.split(img)
    
    r = mean_smooth_channel(r,kernel_size)
    g = mean_smooth_channel(g,kernel_size)
    b = mean_smooth_channel(b,kernel_size)
    
    return cv2.merge((r,g,b))