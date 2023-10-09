import cv2
from Image import Image

class Frame():

    def __init__(self):

        ComponentBuilder : self.builder = ComponentBuilder()
        CustomWindow     : self.window  = CustomWindow()

    def load_image(self):

        path = input("Enter the path to the image: ")
        self.builder.setImage(Image(path))
        self.window.load(self.builder.image)