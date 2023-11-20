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
    
    def get_thermal(self) -> np.array:

        thermal = Thermal(
            dirp_filename='plugins/dji_thermal_sdk_v1.1_20211029/linux/release_x64/libdirp.so',
            dirp_sub_filename='plugins/dji_thermal_sdk_v1.1_20211029/linux/release_x64/libv_dirp.so',
            iirp_filename='plugins/dji_thermal_sdk_v1.1_20211029/linux/release_x64/libv_iirp.so',
            exif_filename='plugins/exiftool-12.35.exe',
            dtype=np.float32,
        )

        temperature = thermal.parse_dirp2(self.path)

        return temperature
    
    def crop_bbox(self, img : np.array, idx : int) -> np.array:

        rect = cv2.boundingRect(np.array(self.pannels[idx]["bbox"]))
        rect = np.int0(rect)
        img = img[rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2]]

        return img, rect
    
    def getTempHistogram(self, idx) -> np.array:

        im = cv2.cvtColor(deepcopy(self.image), cv2.COLOR_BGR2GRAY)

        temperature = self.get_thermal()

        crop_pannel, rect = self.crop_bbox(temperature, idx)

        dim = max(crop_pannel.shape[0], crop_pannel.shape[1])
        pad_im = np.zeros((crop_pannel.shape[0],crop_pannel.shape[1]))
        pad_im[:crop_pannel.shape[0], :crop_pannel.shape[1]] = crop_pannel
        pad_im[pad_im < 23.5] = None

        mean = np.max(crop_pannel)

        xx, yy = np.mgrid[0:pad_im.shape[0], 0:pad_im.shape[1]]

        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        ax.view_init()
        ax.plot_surface(xx, yy, pad_im, rstride = 1, cstride = 1, cmap = plt.cm.gray, linewidth= 0)

        mean = np.ones_like(pad_im) * mean


        # ax.plot_surface(xx, yy, mean, cmap = plt.cm.Blues_r)
        # ax.plot_surface(xx, yy, mean + 10, cmap = plt.cm.Greens_r)
        # ax.plot_surface(xx, yy, mean - 10, cmap = plt.cm.Reds_r)

        elev = 5
        azim = 45
        roll = 0

        ax.view_init(elev, azim, roll)
        ax.set_facecolor((.3,.3,.3))

        print("MAX IN PANNEL = ", np.max(crop_pannel[crop_pannel > 23.5]))
        print("MIN IN PANNEL = ", np.min(crop_pannel[crop_pannel > 23.5]))

        plt.show()

        io_buf = io.BytesIO()
        fig.savefig(io_buf, format='raw', dpi = 100)
        io_buf.seek(0)
        img_arr = np.reshape(np.frombuffer(io_buf.getvalue(), dtype=np.uint8),
                            newshape=(int(fig.bbox.bounds[3]), int(fig.bbox.bounds[2]), -1))
        io_buf.close()

        im = im[:,:,None]
        pannel = np.zeros_like(img_arr)
        pannel[rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2], :] = im[rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2], :]

        print(pannel.shape)
        print(img_arr.shape)

        # im = im[:,:,None]
        # pannel = np.zeros((rect[3], rect[2], img_arr.shape[2]))
        # pannel[:,:,:] = im[rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2], :]
        # pannel = cv2.resize(pannel, (int((img_arr.shape[0] / pannel.shape[0]) * pannel.shape[1]), img_arr.shape[0]))

        ret = np.concatenate((img_arr, pannel), axis=1) 

        return ret
    
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




    

