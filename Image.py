import cv2
import numpy as np
from copy import deepcopy
from matplotlib import pyplot as plt
import io

class Image():

    def __init__(self, path):

        self.path     : str        = path
        self.image    : np.array   = cv2.imread(path)
        self.height   : int        = self.image.shape[0]
        self.width    : int        = self.image.shape[1]
        self.channels : int        = self.image.shape[2]
        self.name     : str        = path.split('/')[-1].split('.')[0]
        print("WHEN LOADING NAME = ", self.name)

    def draw(self) -> np.array:
        return deepcopy(self.image)
    
    def get2DHistogram(self) -> np.array:
        im = cv2.cvtColor(deepcopy(self.image), cv2.COLOR_BGR2GRAY)
        fig = plt.figure()
        plt.hist(im.ravel(), 256, [0, 256])
        io_buf = io.BytesIO()
        fig.savefig(io_buf, format='raw', dpi = 100)
        io_buf.seek(0)
        img_arr = np.reshape(np.frombuffer(io_buf.getvalue(), dtype=np.uint8),
                            newshape=(int(fig.bbox.bounds[3]), int(fig.bbox.bounds[2]), -1))
        io_buf.close()
        return img_arr
    
    def get3DHistogram(self) -> np.array:
        im = cv2.cvtColor(deepcopy(self.image), cv2.COLOR_BGR2GRAY)
        dim = max(im.shape[0], im.shape[1])
        pad_im = np.zeros((dim,dim))
        pad_im[:im.shape[0], :im.shape[1]] = im

        mean = np.mean(im)
        std  = np.std(im)

        xx, yy = np.mgrid[0:pad_im.shape[0], 0:pad_im.shape[1]]

        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        ax.view_init()
        ax.plot_surface(xx, yy, pad_im, rstride = 1, cstride = 1, cmap = plt.cm.gray, linewidth= 0)

        mean = np.ones_like(pad_im) * mean

        ax.plot_surface(xx, yy, mean, cmap = plt.cm.Blues_r)
        ax.plot_surface(xx, yy, mean + std, cmap = plt.cm.Greens_r)
        ax.plot_surface(xx, yy, mean - std, cmap = plt.cm.Reds_r)

        elev = 5
        azim = 45
        roll = 0

        ax.view_init(elev, azim, roll)
        ax.set_facecolor((.3,.3,.3))

        io_buf = io.BytesIO()
        fig.savefig(io_buf, format='raw', dpi = 100)
        io_buf.seek(0)
        img_arr = np.reshape(np.frombuffer(io_buf.getvalue(), dtype=np.uint8),
                            newshape=(int(fig.bbox.bounds[3]), int(fig.bbox.bounds[2]), -1))
        io_buf.close()
        return img_arr




    

