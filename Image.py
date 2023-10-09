import cv2
import numpy as np
from copy import deepcopy
from matplotlib import pyplot as plt
import io

class Image():

    def __init__(self, path):

        str      : self.path     = path
        np.array : self.image    = cv2.imread(path)
        int      : self.height   = self.image.shape[0]
        int      : self.width    = self.image.shape[1]
        int      : self.channels = self.image.shape[2]
        str      : self.name     = path.split('/')[-1].split('.')[0]

    def get_image(self) -> np.array:
        return deepcopy(self.image)
    
    def get_histogram_img(self) -> np.array:
        fig = plt.figure()
        plt.hist(self.image.ravel(), 256, [0, 256])
        io_buf = io.BytesIO()
        fig.savefig(io_buf, format='raw', dpi = 100)
        io_buf.seek(0)
        img_arr = np.reshape(np.frombuffer(io_buf.getvalue(), dtype=np.uint8),
                            newshape=(int(fig.bbox.bounds[3]), int(fig.bbox.bounds[2]), -1))
        io_buf.close()
        return img_arr



    

