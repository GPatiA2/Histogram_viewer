from Component  import Component
import numpy as np
from collections.abc import Callable

class Filter(Component):

    def __init__(self, func):
        super().__init__()
        Callable[[np.array], np.array] : self.filter = func

    def apply(self, img) -> np.array:
        return filter(img)
    
class SingleChannelFilter(Filter):

    def __init__(self, func, channel):
        super().__init__(func)
        int : self.channel = channel

    def apply(self, img) -> np.array:
        im = self.filter(img[:,:,self.channel])[1]
        return np.stack((im,)*3, axis=-1)
    
class MultiChannelFilter(Filter):

    def __init__(self, func):
        super().__init__(func)

    def apply(self, img) -> np.array:
        im = self.filter(img)
        return im
    
class EdgeDenoisingComponent(Filter):

    def __init__(self, func, size):
        super().__init__(func)
        self.size = size

    def apply(self, img) -> np.array:
        return self.filter(img, self.size)
    