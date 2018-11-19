import os
import shutil

from PIL import Image
import torchvision.transforms as transforms

from app import Style

IMAGE_PROCESSING_RESOLUTION = 512

#################################
# Style/Folder Processing
##################################

def styleFromFolder(path):
    return Style()

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
    content_img = img.resize([512,512], Image.ANTIALIAS).convert("RGB")
    content_img = image_loader(content_img)
    input_img = content_img.clone()



    # fake dimension required to fit network's input dimensions
    image = transforms.ToTensor()(image).unsqueeze(0)
    return (image.to(device, torch.float))

def processImage(imgPath, device):
    output = run_style_transfer(cnn, cnn_normalization_mean, cnn_normalization_std,
                           content_img, style_img, input_img, device = device)
    output = output.cpu().clone().detach().squeeze(0)
    output = transforms.ToPILImage()(output)
    output = output.resize(orig_dim, Image.ANTIALIAS)
    if hasAlpha:
        output.putalpha(alpha_img)
    output.save(texture, optimize = True, quality = 60)
    i += 1
    print("Style transferred!")







#############################
# Computed Dataset functions
#############################
def loadFolder(folder, destination, newName):
    assert(os.path.exists(folder) and os.path.exists(destination)), \
    "Invalid folder/directory"
    shutil.copytree(folder, destination)



