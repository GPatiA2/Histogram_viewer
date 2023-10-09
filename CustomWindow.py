import cv2
import numpy as np
from Component import Component
from Image import Image
from ComponentBuilder import ComponentBuilder

class CustomWindow():

    def __init__(self):
        
        np.array         : self.show = None
        list[Component]  : self.elements = []
        Image            : self.image = None

    def add(self, component : Component) -> None:
        self.elements.append(component)

    def draw(self) -> None:
        for element in self.elements:
            self.show = element.draw(self.show)
        return self.show

    def reset(self) -> None:
        for c in self.elements:
            c.visible = False
        self.draw()

    def clear(self):
        self.elements.clear()
        self.show = None
        self.image = None

    def load(self, img : Image) -> None:
        self.image = img
        self.draw()
    