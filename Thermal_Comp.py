from Component import Component
import numpy as np
from abc import ABC, abstractmethod

class ThermalComponent(Component):

    def __init__(self, thermal):
        super().__init__()
        self.thermal = thermal

    @abstractmethod
    def show(self, img) -> np.array: ...

class ThermalPannelComponent(Component):

    def __init__(self, thermal):
        super().__init__()
        self.thermal = thermal

    @abstractmethod
    def show(self, img) -> np.array: ...