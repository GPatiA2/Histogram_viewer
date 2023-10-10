from CustomWindow import CustomWindow
from ComponentBuilder import ComponentBuilder
from abc import ABC, abstractmethod
from Image import Image

class Comand():

    def __init__(self):
        pass

    @abstractmethod
    def execute(self, window : CustomWindow, builder : ComponentBuilder):
        pass

class LoadImageCommand(Comand):

    def __init__(self, path):
        super().__init__()
        self.path = path
        self.name = None

    def execute(self, window : CustomWindow, builder : ComponentBuilder):
        img = Image(self.path)
        window.load(img)
        self.name = img.name

class DrawCommand(Comand):

    def __init__(self):
        super().__init__()

    def execute(self, window : CustomWindow, builder : ComponentBuilder):
        window.draw()

class AddTitleCommand(Comand):

    def __init__(self, pos, text):
        super().__init__()
        self.pos  = pos
        self.text = text
        

    def execute(self, window : CustomWindow, builder : ComponentBuilder):
        comp = builder.buildTitleComponent(self.pos, self.text)
        window.add(comp)


class Add2DHistogramCommand(Comand):

    def __init__(self):
        super().__init__()

    def execute(self, window : CustomWindow, builder : ComponentBuilder):
        hist = window.get2DHistogram()
        comp = builder.build2DHistogramComponent(hist)
        window.add(comp)

class Add3DHistogramCommand(Comand):

    def __init__(self):
        super().__init__()

    def execute(self, window : CustomWindow, builder : ComponentBuilder):
        hist = window.get3DHistogram()
        comp = builder.build3DHistogramComponent(hist)
        window.add(comp)

class AddSingleChannelFilterCommand(Comand):

    def __init__(self, thresh: float, channel: int):
        super().__init__()
        self.f = thresh
        self.c = channel

    def execute(self, window : CustomWindow, builder : ComponentBuilder):
        comp = builder.buildSingleChannelFilter(self.f, self.c)
        window.add(comp)

class AddAllChannelsFilterCommand(Comand):

    def __init__(self, f: float, s: float, t: float):
        super().__init__()
        self.f = f
        self.s = s
        self.t = t

    def execute(self, window : CustomWindow, builder : ComponentBuilder):
        comp = builder.buildAllChannelsFilter(self.f, self.s, self.t)
        window.add(comp)

class AddLaplacianFilterCommand(Comand):

    def __init__(self, f: int):
        super().__init__()
        self.f = f

    def execute(self, window : CustomWindow, builder : ComponentBuilder):
        comp = builder.buildLaplacianFilter(self.f)
        window.add(comp)

class AddGaussianBlurFilterCommand(Comand):

    def __init__(self, f: int, sigmaX:int, sigmaY:int):
        super().__init__()
        self.f = f
        self.sigmaX = sigmaX
        self.sigmaY = sigmaY

    def execute(self, window : CustomWindow, builder : ComponentBuilder):
        comp = builder.buildGaussianBlurFilter((self.f, self.f), self.sigmaX, self.sigmaY)
        window.add(comp)

class AddCannyFilterCommand(Comand):

    def __init__(self, th1: int, th2:int):
        super().__init__()
        self.th1 = th1
        self.th2 = th2

    def execute(self, window : CustomWindow, builder : ComponentBuilder):
        comp = builder.buildCannyFilter(self.th1, self.th2)
        window.add(comp)

class ErosionCommand(Comand):

    def __init__(self, f: int):
        super().__init__()
        self.f = f

    def execute(self, window : CustomWindow, builder : ComponentBuilder):
        comp = builder.buildErosionFilter(self.f)
        window.add(comp)

class DilationCommand(Comand):
    
    def __init__(self, f: int):
        super().__init__()
        self.f = f

    def execute(self, window : CustomWindow, builder : ComponentBuilder):
        comp = builder.buildDilationFilter(self.f)
        window.add(comp)

class OpeningCommand(Comand):

    def __init__(self, f: int):
        super().__init__()
        self.f = f

    def execute(self, window : CustomWindow, builder : ComponentBuilder):
        comp = builder.buildOpeningFilter(self.f)
        window.add(comp)

class ClosingCommand(Comand):
    
    def __init__(self, f: int):
        super().__init__()
        self.f = f

    def execute(self, window : CustomWindow, builder : ComponentBuilder):
        comp = builder.buildClosingFilter(self.f)
        window.add(comp)

class ResetCommand(Comand):

    def __init__(self):
        super().__init__()

    def execute(self, window : CustomWindow, builder : ComponentBuilder):
        window.reset()

class ClearCommand(Comand):

    def __init__(self):
        super().__init__()

    def execute(self, window : CustomWindow, builder : ComponentBuilder):
        window.clear()

class ResetWindowCommand(Comand):
    
    def __init__(self):
        super().__init__()

    def execute(self, window : CustomWindow, builder : ComponentBuilder):
        window.reset()

class ClearWindowCommand(Comand):
    
    def __init__(self):
        super().__init__()

    def execute(self, window : CustomWindow, builder : ComponentBuilder):
        window.clear()

class PopVisibleCommand(Comand):

    def __init__(self):
        super().__init__()

    def execute(self, window : CustomWindow, builder : ComponentBuilder):
        window.pop_visible()

class PushVisibleCommand(Comand):

    def __init__(self):
        super().__init__()

    def execute(self, window : CustomWindow, builder : ComponentBuilder):
        window.push_visible()

