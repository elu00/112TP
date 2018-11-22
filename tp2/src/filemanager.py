import os
import shutil

from PIL import Image
import torchvision.transforms as transforms

from app import Style, Algorithms
import alg

IMAGE_PROCESSING_RESOLUTION = 512

#################################
# Folder Processing
##################################

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


def styleToFolder(style):
    path = style.styleDir
    contents = [style.name, style.descr, str(style.alg). style.styleDir]
    with open(path + "cfg.txt", "w+") as f:
        f.writelines(contents)
    return    
#################################
# Computational Wrapper Functions
##################################

def computeStyle(style):

    styleToFolder(style)
    return

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
    shutil.copytree(folder, destination)
    os.rename(destination, newName)



