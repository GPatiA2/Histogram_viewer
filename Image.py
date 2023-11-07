import cv2
import numpy as np
from copy import deepcopy
from matplotlib import pyplot as plt
import io
from PIL import Image as PILImage
from thermal import Thermal

class Image():

    def __init__(self, path, is_tiff = False):

        self.path     : str        = path

        if is_tiff:
            img = plt.imread(path)
            self.image    : np.array   = np.array(img, np.uint8)
            self.image = self.image[:,:,None]
        else:
            self.image    : np.array   = cv2.imread(path)
        
        print(self.image.shape)
        self.height   : int        = self.image.shape[0]
        self.width    : int        = self.image.shape[1]
        self.channels : int        = self.image.shape[2]
        self.name     : str        = path.split('/')[-1].split('.')[0]

        print("WHEN LOADING NAME = ", self.name)

    def fromPIL(path : str):
        img = PILImage.open(path)
        np_img = np.array(img)
        return np_img
    
    def setPannels(self, p):
        self.pannels = p

    def draw(self) -> np.array:
        return deepcopy(self.image)
    
    def get2DHistogram(self) -> np.array:
        if self.channels != 1:
            im = cv2.cvtColor(deepcopy(self.image), cv2.COLOR_BGR2GRAY)
        else:
            im = deepcopy(self.image)
            
        fig = plt.figure()
        plt.hist(im.ravel(), 256, [0, 256])
        io_buf = io.BytesIO()
        fig.savefig(io_buf, format='raw', dpi = 100)
        io_buf.seek(0)
        img_arr = np.reshape(np.frombuffer(io_buf.getvalue(), dtype=np.uint8),
                            newshape=(int(fig.bbox.bounds[3]), int(fig.bbox.bounds[2]), -1))
        io_buf.close()
        return img_arr
    
    def getTempHistogram(self, idx) -> np.array:

        im = cv2.cvtColor(deepcopy(self.image), cv2.COLOR_BGR2GRAY)

        thermal = Thermal(
            dirp_filename='plugins/dji_thermal_sdk_v1.1_20211029/linux/release_x64/libdirp.so',
            dirp_sub_filename='plugins/dji_thermal_sdk_v1.1_20211029/linux/release_x64/libv_dirp.so',
            iirp_filename='plugins/dji_thermal_sdk_v1.1_20211029/linux/release_x64/libv_iirp.so',
            exif_filename='plugins/exiftool-12.35.exe',
            dtype=np.float32,
        )

        temperature = thermal.parse_dirp2(self.path)

        rect = cv2.boundingRect(np.array(self.pannels[idx]["bbox"]))
        rect = np.int0(rect)
        temperature = temperature[rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2]]

        dim = max(temperature.shape[0], temperature.shape[1])
        pad_im = np.zeros((dim,dim))
        pad_im[:temperature.shape[0], :temperature.shape[1]] = temperature

        mean = np.max(temperature)

        xx, yy = np.mgrid[0:pad_im.shape[0], 0:pad_im.shape[1]]

        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        ax.view_init()
        ax.plot_surface(xx, yy, pad_im, rstride = 1, cstride = 1, cmap = plt.cm.gray, linewidth= 0)

        mean = np.ones_like(pad_im) * mean

        ax.plot_surface(xx, yy, mean, cmap = plt.cm.Blues_r)
        # ax.plot_surface(xx, yy, mean + 10, cmap = plt.cm.Greens_r)
        ax.plot_surface(xx, yy, mean - 10, cmap = plt.cm.Reds_r)

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




    

