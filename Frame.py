import cv2
from ComponentBuilder import ComponentBuilder
from CustomWindow import CustomWindow
import numpy as np

class Frame():

    def __init__(self, name:str, res:tuple[int], builder : ComponentBuilder,
                 window : CustomWindow, parser):

        self.builder  : ComponentBuilder = builder
        self.window   : CustomWindow     = window
        self.win_name : str              = name
        self.res      : tuple[int]       = res
        self.img_name : str              = None
        self.parser                      = parser
        self.pos      : tuple[int]       = (0,0)
        cv2.namedWindow(self.win_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.win_name, 1920, 1080)
        cv2.setMouseCallback(self.win_name, self.storepos)

    def storepos(self, event, x, y, flags, param) -> None:
        if event == cv2.EVENT_LBUTTONDOWN:
            self.pos = (x, y)
            print(self.pos)

    def get_name(self) -> str:
        return self.window.get_name()

    def draw(self):
        final_img : np.array = self.window.draw()
        cv2.imshow(self.win_name, final_img)

    def get_name(self) -> str:
        return self.img_name
    
    def get_pos(self) -> tuple[int]:
        return self.pos

    def setup(self):

        command : str = ""
        while command != "exit":
            command = input("Enter a command: ")
            comand_obj = self.parser.parseComand(command, self)
            comand_obj.execute(self.window, self.builder)
            self.draw()
            cv2.waitKey(0)
            
            