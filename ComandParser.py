from Comand import *
from Frame import *

class ComandParser:

    def __init__(self):
        pass

    def parseComand(self, comand : str, frame : Frame) -> Comand:
        args = comand.split(' ')
        comand.lower()

        if args[0] == "single":
            th1 = int(args[1])
            ch = int(args[2])
            return AddSingleChannelFilterCommand(th1, ch)
        
        elif args[0] == "all":
            th1 = int(args[1])
            th2 = int(args[2])
            th3 = int(args[3])
            return AddAllChannelsFilterCommand(th1, th2, th3)
        
        elif args[0] == "laplacian":
            size = int(args[1])
            return AddLaplacianFilterCommand(size)
        
        elif args[0] == "gaussian":
            size = int(args[1])
            sigmaX = int(args[2])
            sigmaY = int(args[3])
            return AddGaussianBlurFilterCommand(size, sigmaX, sigmaY)
        
        elif args[0] == "canny":
            th1 = int(args[1])
            th2 = int(args[2])
            return AddCannyFilterCommand(th1, th2)
        
        elif args[0] == "3dhist":
            return Add3DHistogramCommand()

        elif args[0] == "2dhist":
            return Add2DHistogramCommand()
        
        elif args[0] == "title":
            title = frame.get_name()
            pos   = frame.get_pos()
            return AddTitleCommand(title, pos)
        
        elif args[0] == "load":
            path = args[1]
            return LoadImageCommand(path)
        
        elif args[0] == "clear":
            return ClearWindowCommand()
        
        elif args[0] == "reset":
            return ResetWindowCommand()
        
        elif args[0] == "pushvisible":
            return PushVisibleCommand()
        
        elif args[0] == "popvisible":
            return PopVisibleCommand()
        
        elif args[0] == "erosion":
            size = (args[1])
            return ErosionCommand(size)
        
        elif args[0] == "dilation":
            size = (args[1])
            return DilationCommand(size)
        
        elif args[0] == "closing":
            size = (args[1])
            return ClosingCommand(size)
        
        elif args[0] == "opening":
            size = (args[1])
            return OpeningCommand(size)

        elif args[0] == "load_tiff":
            path = (args[1])
            return LoadTiffCommand(path)
        
        elif args[0] == "temp_hist":
            idx = int(args[1])
            return AddTempHistogramCommand(idx)
        
        elif args[0] == "local_max":
            pannel = int(args[1])
            size   = int(args[2])
            return LocalMaxFilterCommand(size, pannel)

        else:
            print("Got invalid comand: " + comand)

        