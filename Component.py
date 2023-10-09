from abc import ABC, abstractmethod
import numpy as np
import cv2

class Component():

    def __init__(self):
        bool : self.__visible = True
        pass

    @property
    def visible(self) -> bool:
        return self.__visible

    @visible.setter
    def visible(self, val : bool) -> None:
        self.__visible = val

    @visible.getter
    def visible(self) -> bool:
        return self.__visible

    def draw(self, img) -> np.array:
        if self.visible:
            return self.draw(img)
        else:
            return img

    @abstractmethod
    def show(self, img) -> np.array:
        pass

class TitleComponent(Component):

    def __init__(self, pos, text):
        self.text = text
        self.pos  = pos

    def show(self, img) -> np.array:
        img = cv2.putText(img, self.text, self.pos, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        return img
    
class HistogramComponent(Component):

    def __init__(self, hist):
        self.hist = hist

    def show(self, img) -> np.array:
        return self.hist
    
class NumberComponent(Component):

    def __init__(self, pos, num, val):
        self.pos = pos
        self.num = num
        self.val = val

    def show(self, img) -> np.array:
        img = cv2.putText(img, self.num + ": " + str(self.val), self.pos, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        return img

