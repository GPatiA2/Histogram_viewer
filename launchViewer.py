from ComponentBuilder import ComponentBuilder
from CustomWindow import CustomWindow
from ComandParser import ComandParser
from Frame import Frame

if __name__ == '__main__':
    
    parser = ComandParser()
    builder = ComponentBuilder()
    window = CustomWindow()
    frame = Frame("Frame", (1920, 1080), builder, window, parser)
    frame.setup()
    
    print('Done!')