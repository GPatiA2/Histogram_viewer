from Image import Image
from Component import TitleComponent, HistogramComponent
import cv2
import numpy as np
from functools import partial
from Filter import *

class ComponentBuilder:

    def __init__(self):
        pass

    def buildTitleComponent(self, pos, title):
        return TitleComponent(pos, title)
    
    def build2DHistogramComponent(self, hist):
        return HistogramComponent(hist)
    
    def build3DHistogramComponent(self, hist):
        return HistogramComponent(hist)
    
    def buildTempHistogramComponent(self, hist):
        return HistogramComponent(hist)
    
    def buildSingleChannelFilter(self, f: float, c: int):
        return SingleChannelFilter(partial(cv2.threshold, thresh=f, maxval = 255, type = cv2.THRESH_BINARY), c)
    
    def buildAllChannelsFilter(self, f: float, s: float, t: float):
        def multichanfilter(img, f,s,t):
            f = SingleChannelFilter(partial(cv2.threshold, thresh=f, maxval = 255, type = cv2.THRESH_BINARY), 0).filter
            s = SingleChannelFilter(partial(cv2.threshold, thresh=s, maxval = 255, type = cv2.THRESH_BINARY), 1).filter
            t = SingleChannelFilter(partial(cv2.threshold, thresh=t, maxval = 255, type = cv2.THRESH_BINARY), 2).filter
            f_im = f(img[:,:,0])[1]
            s_im = s(img[:,:,1])[1]
            t_im = t(img[:,:,2])[1]
            and_im = np.logical_and(f_im, s_im, t_im) * 255
            return np.stack((and_im,)*3, axis=-1)
        
        return MultiChannelFilter(partial(multichanfilter, f=f,s=s,t=t))
    
    def buildLaplacianFilter(self,f):
        return Filter(partial(cv2.Laplacian, ddepth=cv2.CV_64F, ksize=f))
    
    def buildGaussianBlurFilter(self,f,sx, sy):
        return Filter(partial(cv2.GaussianBlur, ksize=f, sigmaX=sx, sigmaY=sy))
    
    def buildCannyFilter(self, th1:int, th2:int):
        return Filter(partial(cv2.Canny, threshold1=th1, threshold2=th2))
    
    def buildLocalMaxFilter(self, crop, thermalsize:int):

        def localmaxfilter(img, crop, thermalsize):
            
            mcrop = crop.copy()
            mcrop = cv2.dilate(mcrop, np.ones((thermalsize, thermalsize), np.uint8))
            
            highlight = np.zeros(crop.shape, np.uint8)
            highlight[mcrop == crop] = 255

            crop2 = np.stack((highlight,crop,crop), axis=-1)

            crop3c = np.stack((crop,crop,crop), axis=-1)

            ret = np.uint8(np.concatenate((crop3c, crop2), axis=1))

            return ret

        return Filter(partial(localmaxfilter, crop=crop, thermalsize=thermalsize))
    
