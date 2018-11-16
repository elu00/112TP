import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

from PIL import Image

import torchvision.transforms as transforms
import torchvision.models as models

import copy
import os


def main():
    # Basic image loading using PIL
    PILImage = Image.open('imageDemo/base.png')
    # Manipulating Image Channels
    redChannel = PILImage.getchannel('R')
    redChannel.save('imageDemo/red.png')
    # Scaling images
    smallImage = PILImage.resize([100,100], Image.ANTIALIAS)
    smallImage.save('imageDemo/small.png')


    # Using Pytorch to manipulate the image as a tensor
    imgTensor = transforms.ToTensor()(PILImage)
    # Add another image to the image-tensor
    newImg = Image.open('imageDemo/add.png')
    newImgTensor = transforms.ToTensor()(newImg)
    imgTensor += newImgTensor

    newPILImage = transforms.ToPILImage()(imgTensor.cpu().clone().detach())
    newPILImage.save('imageDemo/pasted.png')

    
    return



if __name__ == "__main__":
    main()
