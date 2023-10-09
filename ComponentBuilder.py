from Image import Image
from Component import TitleComponent, HistogramComponent
import cv2
import numpy as np
from functools import partial
from Filter import *

class ComponentBuilder:

    CHANNEL_FILTERS = ["single", "all"]
    COMPONENT_FILTERS = ["histogram", "title"]
    EDGE_DENOIS_FILTERS = ["laplacian", "gauss_blur"]

    def __init__(self):
        Image : self.image = None

    def setImage(self, image : Image):
        self.image = image

    def buildComponent(self, comp_type : str):
        if comp_type in self.CHANNEL_FILTERS:
            return self.buildFilterComponent(comp_type)
        
        elif comp_type in self.COMPONENT_FILTERS:
            return self.buildGraphicalComponent(comp_type)
        
        elif comp_type in self.EDGE_DENOIS_FILTERS:
            return self.buildEdgeDenoisComponent(comp_type)

    def buildGraphicalComponent(self, comp_type, pos):
        if comp_type == "title":
            return self.buildTitleComponent(pos)
        elif comp_type == "histogram":
            return self.buildHistogramComponent(pos)

    def buildFilterComponent(self, comp_type:str):
        if comp_type == "single":
            f = input("Enter the threshold value: ")
            c = input("Enter the channel number: ")
            return self.buildSingleChannelFilter(f, c)
        elif comp_type == "all":
            f = input("Enter the first threshold value: ")
            s = input("Enter the second threshold value: ")
            t = input("Enter the third threshold value: ")
            return self.buildAllChannelsFilter(f, s, t)
        
    def buildEdgeDenoisingComponent(self, comp_type:str):
        f = input("Enter the kernel size: ")
        if comp_type == "laplacian":
            return self.buildLaplacianFilter(f)
        elif comp_type == "gauss_blur":
            return self.buildGaussianBlurFilter(f)

    def buildTitleComponent(self, pos):
        return TitleComponent(pos, self.image.name)
    
    def buildHistogramComponent(self, pos):
        return HistogramComponent(self.image.get_histogram_img())
    
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
        return EdgeDenoisingComponent(partial(cv2.Laplacian, ddepth=cv2.CV_64F, ksize=f))
    
    def buildGaussianBlurFilter(self,f):
        return EdgeDenoisingComponent(partial(cv2.GaussianBlur, ksize=f))
    
