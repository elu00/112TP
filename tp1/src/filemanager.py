import os
import shutil

def loadFolder(folder, destination, newName):
    assert(os.path.exists(folder) and os.path.exists(destination)), \
    "Invalid folder/directory"
    shutil.copytree(folder, destination)
