import os
import shutil
import enum

from PyQt5.QtGui import QIcon, QPixmap
from PIL import Image
import torchvision.transforms as transforms

import alg

IMAGE_PROCESSING_RESOLUTION = 128
GAME_ID = "G8M"

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
        tempList = list(os.listdir("dump"))
        self.imgCount = len(tempList)
        self.imgList = ["dump/" + tempList[i] for i in range(self.imgCount)]
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
        Computed: %s      \n
        Images: %s        \n
        Folder: %s        \n
        ''' % (self.name, self.descr, self.alg, self.computed,
                                     self.imgCount, self.styleDir)

    def compute(self, window):
        window.progressBar.setMinimum(0)
        window.progressBar.setMaximum(self.imgCount - 1)
        # Precompute style tensor
        styleTensor = loadImage(self.styleImage)
        # Process each image
        for i in range(self.imgCount):
            imgPath = self.imgList[i]
            # Manipulations to make the path correct
            outputPath = self.styleDir + "/" + imgPath[5:-3] + "jpg"
            processImage(imgPath, styleTensor, outputPath)
            window.progressBar.setValue(i)
        self.writeCFG()
        self.computed = True
        window.updateStatus()
        return

    def load(self, window):
        texturePath = window.dolphinPath + "/User/Load/Textures/" + GAME_ID
        try:
            os.rmdir(texturePath)
        except:
            pass
        shutil.copytree(self.styleDir, texturePath)

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

    @staticmethod
    def styleFromFolder(path):
        print("Loading Style from:" + path)
        assert(os.path.exists(path + "/cfg.txt"))
        with open(path + "/cfg.txt", "r") as f:
            lines = list(f)
            name = lines[0].strip()
            descr = lines[1].strip()
            if lines[2] == "Algorithms.Conv_NN":
                alg = Algorithms.Conv_NN
            else:
                alg = Algorithms.Cycle_GAN
            styleDir = path + "/" + lines[3].strip()
        styleImage = path + "/style.jpg"
        if (os.path.exists(path + "/preview.jpg")):
            previewImage = path + "/preview.jpg"
        else:
            previewImage = None
        return Style(name = name, descr = descr, alg = alg, styleDir = styleDir,
                    styleImage = styleImage, computed = True, previewImage = previewImage)


  
#################################
# Computational Wrapper Functions
##################################
def loadImage(imgPath, device):
    img = Image.open(imgPath)
    # Storing the alpha channel for future use
    try:
        alpha_img = img.getchannel('A')
    except:
        alpha_img = None
    orig_dim = img.size
    size = [IMAGE_PROCESSING_RESOLUTION, IMAGE_PROCESSING_RESOLUTION]
    content_img = img.resize(size, Image.ANTIALIAS).convert("RGB")
    content_img = image_loader(content_img)

    image = transforms.ToTensor()(image).unsqueeze(0)
    return (image.to(alg.device, torch.float), orig_dim, alpha_img)

def processImage(imgPath, styleImg, outputPath):
    content_img, orig_dim, alpha_img = loadImage(imgPath)
    input_img = content_img.clone()
    output = alg.run_style_transfer(content_img, style_img, input_img)
    # Process the output image
    output = output.cpu().clone().detach().squeeze(0)
    output = transforms.ToPILImage()(output)
    output = output.resize(orig_dim)
    if alpha_img != None:
        output.putalpha(alpha_img)
    output.save(outputPath, optimize = True, quality = 60)
    print("Style transferred!")


#############################
# Computed Dataset functions
#############################
def loadFolder(folder, destination, newName):
    assert(os.path.exists(folder) and os.path.exists(destination)), \
    "Invalid folder/directory"
    shutil.copytree(folder, destination + folder)
    os.rename(destination + folder, newName)



