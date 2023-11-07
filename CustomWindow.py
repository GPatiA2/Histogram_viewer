import cv2
import numpy as np
from Component import Component
from Image import Image
from typing import List
import json

class CustomWindow():

    def __init__(self, json_path : str):
        
        self.show = None
        self.elements = list()
        self.image = None
        self.last_visible = -1

        self.json_path = json_path
        with open(json_path) as f:
            self.pannels = json.load(f)

    def add(self, component : Component) -> None:
        self.elements.append(component)
        self.last_visible = len(self.elements) - 1

    def draw(self) -> np.array:
        self.show = self.image.draw()
        for element in self.elements:
            print("DRAWING " + str(element))
            self.show = element.draw(self.show)
            print("ONCE DROWN " + str(self.show.shape))
        return self.show

    def reset(self) -> np.array:
        for c in self.elements:
            c.visible = False
            self.last_visible = -1

        self.draw()

    def get_name(self) -> str:
        return self.image.name

    def get2DHistogram(self) -> np.array:
        return self.image.get2DHistogram()
    
    def get3DHistogram(self) -> np.array:
        return self.image.get3DHistogram()
    
    def getTempHistogram(self, idx) -> np.array:
        return self.image.getTempHistogram(idx)

    def clear(self):
        self.elements.clear()
        self.last_visible = -1
        self.show = None
        self.image = None

    def load(self, img : Image) -> np.array:
        self.image = img
        self.image.setPannels(self.pannels[self.image.name])
        self.draw()

    def pop_visible(self):
        self.elements[self.last_visible].visible = False
        self.last_visible -= 1

    def push_visible(self):
        self.last_visible += 1
        self.elements[self.last_visible].visible = True