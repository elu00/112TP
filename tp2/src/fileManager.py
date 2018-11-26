import os
import shutil
import enum

from PyQt5.QtGui import QIcon, QPixmap
from PIL import Image
import torchvision.transforms as transforms

import alg

IMAGE_PROCESSING_RESOLUTION = 512

# TODO: Implement file processing
#################################
# Folder Processing
##################################

class Algorithms(enum.Enum):
    Conv_NN = 0
    Cycle_GAN = 1

class Style(object):
    def __init__(self, name, descr, styleImage, alg, computed,
                    styleDir, previewImage = None):
        self.name = name
        self.descr = descr
        self.alg = alg
        self.styleImage = styleImage
        self.styleDir = styleDir
        self.icon = QIcon(styleImage)
        self.imgCount = 100
        if previewImage != None and os.path.exists(previewImage):
            self.displayImage = QPixmap(previewImage).scaledToWidth(600)
        else:
            self.displayImage = QPixmap(styleImage).scaledToWidth(600)
        self.computed = computed


    def __repr__(self):
        return \
        '''
        Current Style: %s \n
        Description: %s   \n
        Algorithm: %s     \n
        Images: %s        \n
        Folder: %s        \n
        ''' % (self.name, self.descr, self.alg, self.imgCount, self.styleDir)

    # Move 
    def load(self):
        fileManager.loadFolder(self.styleDir, PATH_TO_TEXTURES)
    def compute(self):
        return
    def styleToFolder(style):
        path = style.styleDir
        contents = [style.name, style.descr, str(style.alg), style.styleDir]
        if not os.path.exists(path):
            os.mkdir(path)
        with open(path + "cfg.txt", "w+") as f:
            # Create folder if necessary, write images, write contents
            f.writelines(contents)
        return    

    @staticmethod
    def styleFromFolder(path):
        print(path)
        assert(os.path.exists(path + "cfg.txt"))
        with open(path + "cfg.txt", "r") as f:
            lines = list(f)
            name = lines[0].strip()
            descr = lines[1].strip()
            if lines[2] == "Algorithms.Conv_NN":
                alg = Algorithms.Conv_NN
            else:
                alg = Algorithms.Cycle_GAN
            styleDir = path + lines[3].strip()
        styleImage = path + "style.jpg"
        if (os.path.exists(path + "preview.jpg")):
            previewImage = path + "preview.jpg"
        else:
            previewImage = None
        return Style(name = name, descr = descr, alg = alg, styleDir = styleDir,
                    styleImage = styleImage, computed = True, previewImage = previewImage)


  
#################################
# Computational Wrapper Functions
##################################

def findDumpedTextures(dumpDir):
    return list(os.path.listdir(dumpDir))

def recursiveGetFullPath(walk):
    stuff = dict()
    for dir in walk:
        for file in dir[2]:
            stuff[file] = dir[0] + '/' + file
    return stuff


def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)
    return None

def loadImage(imgPath, device):
    img = Image.open(imgPath)
    # Storing the alpha channel for future use
    hasAlpha = True
    try:
        alpha_img = img.getchannel('A')
    except:
        hasAlpha = False
    orig_dim = img.size
    size = [IMAGE_PROCESSING_RESOLUTION, IMAGE_PROCESSING_RESOLUTION]
    content_img = img.resize(size, Image.ANTIALIAS).convert("RGB")
    content_img = image_loader(content_img)

    image = transforms.ToTensor()(image).unsqueeze(0)
    return (image.to(alg.device, torch.float))

def processImage(imgPath, styleImg):

    input_img = content_img.clone()
    output = alg.run_style_transfer(content_img, style_img, input_img)
    output = output.cpu().clone().detach().squeeze(0)
    output = transforms.ToPILImage()(output)
    output = output.resize(orig_dim, Image.ANTIALIAS)
    if hasAlpha:
        output.putalpha(alpha_img)
    output.save(texture, optimize = True, quality = 60)
    print("Style transferred!")



#############################
# Computed Dataset functions
#############################
def loadFolder(folder, destination, newName):
    assert(os.path.exists(folder) and os.path.exists(destination)), \
    "Invalid folder/directory"
    shutil.copytree(folder, destination + folder)
    os.rename(destination + folder, newName)



