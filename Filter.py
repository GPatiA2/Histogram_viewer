from Component  import Component
import numpy as np
from collections.abc import Callable

class Filter(Component):

    def __init__(self, func: Callable[[np.array], np.array] ):
        super().__init__()
        self.filter = func

    def show(self, img) -> np.array:
        return self.filter(img)
    
class SingleChannelFilter(Filter):

    def __init__(self, func, channel):
        super().__init__(func)
        self.channel : int = channel

    def show(self, img) -> np.array:
        im = self.filter(img[:,:,self.channel])[1]
        return np.stack((im,)*3, axis=-1)
    
class MultiChannelFilter(Filter):

    def __init__(self, func):
        super().__init__(func)

    def show(self, img) -> np.array:
        im = self.filter(img)
        return im
    