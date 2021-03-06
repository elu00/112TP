################################################################################
# fileManager.py:
# This file contains the Style and Algorithms classes for use in the other 
# parts of the application.
# A variety of other computational functions are provided as well.
################################################################################
import os
import shutil
import enum

from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QThread
from PIL import Image
import torch
import torchvision.transforms as transforms

import alg

GAME_ID = "G8M"

######################################
# Folder Processing
######################################

# Base class for passing algorithm parameters around
class Algorithms(object):
    def __init__(self, iterations = 500, resolution = 128):
        self.iterations = iterations
        self.resolution = resolution
    def __repr__(self):
        return "CONV_NN; %d iterations; %d processing resolution" \
            % (self.iterations, self.resolution)
    # Derive a new Algorithms object from it's string representation
    @staticmethod
    def fromStr(s):
        iterString = s.split(";")[1]
        resString = s.split(";")[2]
        # Cutting the string to remove the "iterations" and 
        # "processing resolution" bits
        iterations = int(iterString[1:-10])
        resolution = int(resString[1:-23])
        return Algorithms(iterations, resolution)

# The class that specifies a style, complete with computational functions
class Style(object):
    def __init__(self, name, descr, styleImage, alg, computed,
                    styleDir, previewImage = None):
        self.name = name
        self.descr = descr
        self.alg = alg
        self.styleImage = styleImage
        self.styleDir = styleDir
        self.icon = QIcon(styleImage)
        # All the images to process should be in /dump/
        tempList = list(os.listdir("dump"))
        self.imgCount = len(tempList)
        self.imgList = ["dump/" + tempList[i] for i in range(self.imgCount)]
        # Handle the preview image PixMap
        if previewImage != None and os.path.exists(previewImage):
            self.displayImage = QPixmap(previewImage).scaledToWidth(600)
        else:
            self.displayImage = QPixmap(styleImage).scaledToWidth(600)
        self.computed = computed

    # String characterization of the Style
    def __repr__(self):
        return \
        '''
        Current Style: %s \n
        Description: %s   \n
        Algorithm: %s     \n
        Computed: %s      \n
        Images: %s        \n
        Folder: %s        \n
        ''' % (self.name, self.descr, str(self.alg), self.computed,
                                     self.imgCount, self.styleDir)

    #################################
    # Computational Wrapper Functions
    ##################################
    # Compute the entire style
    def compute(self, window):
        window.progressBar.setMinimum(0)
        window.progressBar.setMaximum(self.imgCount)
        # Precompute style tensor
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        styleTensor = self.loadImage(self.styleImage, device)[0]
        # Process each image
        for i in range(self.imgCount):
            imgPath = self.imgList[i]
            # Manipulations to make the path correct
            outputPath = self.styleDir + "/" + imgPath[5:-3] + "png"
            self.processImage(imgPath, styleTensor, outputPath, device)
            window.progressBar.setValue(i + 1)
        self.writeCFG()
        self.computed = True
        window.updateStatus()
        return

    # Compute a single image for benchmarking purposes
    def bench(self, imgPath):
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        styleTensor = self.loadImage(self.styleImage, device)[0]
        # Manipulations to make the path correct
        outputPath = imgPath[:-3] + "transfer" + str(self.alg.iterations) + ".png"
        self.processImage(imgPath, styleTensor, outputPath, device)
        return

    # Loads an image into the PyTorch library
    def loadImage(self, imgPath, device):
        img = Image.open(imgPath)
        # Storing the alpha channel and original resolution of the image
        # to be able to restore it later
        try:
            alphaIMG = img.getchannel('A')
        except:
            alphaIMG = None
        origDim = img.size
        # resize it for processing
        size = [self.alg.resolution, self.alg.resolution]
        img = img.resize(size).convert("RGB")
        img = transforms.ToTensor()(img).unsqueeze(0)
        return (img.to(alg.device, torch.float), origDim, alphaIMG)

    # Process/style transfer a single image against a style tensor
    def processImage(self, imgPath, styleTensor, outputPath, device):
        contentImg, origDim, alphaIMG = self.loadImage(imgPath, device)
        inputImg = contentImg.clone()
        output = alg.run_style_transfer(contentImg, styleTensor, inputImg, self.alg.iterations)
        # Process the output image
        output = output.cpu().clone().detach().squeeze(0)
        output = transforms.ToPILImage()(output)
        output = output.resize(origDim)
        if alphaIMG != None:
            output.putalpha(alphaIMG)
        output.save(outputPath, optimize = True, quality = 60)
        print("Style transferred!")

    # Write the configuration of a style to disk, and copy over the style image
    def writeCFG(self):
        path = self.styleDir
        contents = "\n".join([self.name, self.descr, str(self.alg), path])
        if not os.path.exists(path):
            os.mkdir(path)
        with open(path + "/cfg.txt", "w+") as f:
            # Create folder if necessary, write images, write contents
            f.writelines(contents)
        shutil.copyfile(self.styleImage, path + "/style.jpg")
        return    
    
    # Read in a folder to a style using the configuration text file 
    @staticmethod
    def styleFromFolder(path):
        print("Loading Style from:" + path)
        assert(os.path.exists(path + "/cfg.txt"))
        with open(path + "/cfg.txt", "r") as f:
            lines = list(f)
            name = lines[0].strip()
            descr = lines[1].strip()
            alg = Algorithms.fromStr(lines[2])
            styleDir = lines[3].strip()
        styleImage = path + "/style.jpg"
        if (os.path.exists(path + "/preview.jpg")):
            previewImage = path + "/preview.jpg"
        else:
            previewImage = None
        return Style(name = name, descr = descr, alg = alg, styleDir = styleDir,
                    styleImage = styleImage, computed = True, previewImage = previewImage)

    # Load in modified textures into the Dolphin Path 
    def load(self, window):
        texturePath = window.dolphinPath + "/User/Load/Textures/" + GAME_ID + "/"
        print("Removing", texturePath)
        try:
            shutil.rmtree(texturePath)
        except:
            print("Dir doesn't exist")
        shutil.copytree(self.styleDir, texturePath)

# Separate thread for Image Processing
class ImageThread(QThread):
    def __init__(self, style, window):
        super().__init__()
        self.style = style
        self.window = window

    def run(self):
        self.style.compute(self.window)
        return

# Separate thread for Image Processing
class BenchThread(QThread):
    def __init__(self, style, window):
        super().__init__()
        self.style = style
        self.window = window

    def run(self):
        self.style.bench(self.window.contentPath)
        return


