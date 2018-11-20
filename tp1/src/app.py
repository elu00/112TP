from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap

import sys
import alg
import filemanager
import os
import enum
import subprocess

PATH_TO_DOLPHIN = "Dolphin.exe"
PATH_TO_GAME = ""
PATH_TO_TEXTURES = ""
WINDOW_DIMENSIONS = (600,600)

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
            self.displayImage = QPixmap(styleImage)
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

    def load(self):
        filemanager.loadFolder(self.styleDir, PATH_TO_TEXTURES)

    def compute(self):
        return

class StyleLoader(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.initUI()


    def initUI(self):
        layout = QVBoxLayout(self)


        # Select Name
        nameWrapper = QHBoxLayout()
        nameLabel = QLabel("Name the Style")
        self.nameEdit = QLineEdit(self)
        self.nameEdit.setText("NewStyle")
        self.nameEdit.editingFinished.connect(self.updateName)
        self.updateName()
        nameWrapper.addWidget(nameLabel)
        nameWrapper.addWidget(self.nameEdit)
        layout.addLayout(nameWrapper)


        # Add Description
        descrWrapper = QHBoxLayout()
        descrLabel = QLabel("Add a short description")
        self.descrEdit = QLineEdit(self)
        self.descrEdit.setText("Description")
        self.descrEdit.editingFinished.connect(self.updateDescr)
        descrWrapper.addWidget(descrLabel)
        descrWrapper.addWidget(self.descrEdit)
        layout.addLayout(descrWrapper)

        # Style Image Selection
        self.imgSelect = QFileDialog(self)        
        layout.addWidget(self.imgSelect)

        # Select Algorithm
        algWrapper = QHBoxLayout()
        algLabel = QLabel("Algorithm to Run:")
        self.algSelect = QComboBox(self)
        self.algSelect.addItems([str(alg) for alg in Algorithms])
        self.algSelect.currentIndexChanged.connect(self.updateAlg)
        self.updateAlg(0)
        algWrapper.addWidget(algLabel)
        algWrapper.addWidget(self.algSelect)
        layout.addLayout(algWrapper)

        # Select the style directory

        # Confirmation Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        buttons.button(QDialogButtonBox.Ok).setEnabled(False)
        layout.addWidget(buttons)
        self.buttons = buttons


    def updateImage(self):
        img = self.imgSelect
        self.checkCompleteness()

    def updateName(self):
        self.name = self.nameEdit.text()

    def updateDescr(self):
        self.descr = self.descrEdit.text()


    def updateAlg(self, value):
        self.alg = Algorithms(value)

    def updateStyleDir(self):
        self.styleDir = "yes"
        self.checkCompleteness()

    def checkCompleteness(self):
        if True:
            self.buttons.button(QDialogButtonBox.Ok).setEnabled(True)    
    
    def getStyle(self):
        return Style(name = self.name, descr = self.descr, styleImage = self.styleImage, 
                        alg = self.alg, computed = False, styleDir = self.styleDir)

    @staticmethod
    def getNewStyle(parent = None):
        dialog = StyleLoader(parent)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            return dialog.getStyle()
        else:
            return None
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        folders = ["../styles/starrynight/", "../styles/sketch/", "../styles/picasso/"]
        self.styles = [filemanager.styleFromFolder(folder) for folder in folders]
        self.initUI()

    def initUI(self):
        self.setGeometry(600,600,600,600)
        layoutGrid = QGridLayout(self)
        self.setLayout(layoutGrid)

        # Initialize UI Elements, then populate them with updateStyle()

        # Main Preview Image
        self.img = QLabel()
        layoutGrid.addWidget(self.img, 0, 0, 4, 1)

        # If necessary, progress bar
        self.progressBar = QProgressBar()
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100)
        layoutGrid.addWidget(self.progressBar, 5, 0)

        # Style Selection Menu 
        self.styleMenu = QComboBox()
        self.populateStyles()
        self.styleMenu.currentIndexChanged.connect(self.updateStyle)
        layoutGrid.addWidget(self.styleMenu, 0, 1)

        # Info Box
        self.info = QLabel()
        layoutGrid.addWidget(self.info, 1, 1)        

        # Compute Button
        self.computeButton = QPushButton("Calculate Style")
        layoutGrid.addWidget(self.computeButton, 2, 1)

        # Import New Style
        self.importButton = QPushButton("Import New Style...")
        self.importButton.clicked.connect(self.importStyle)
        layoutGrid.addWidget(self.importButton, 3, 1)

        # Launch Button
        self.launchButton = QPushButton("Start Game!")
        self.launchButton.clicked.connect(self.startGame)
        layoutGrid.addWidget(self.launchButton, 5, 1)
    

        # Populate the interface
        self.curStyle = self.styles[0]
        self.updateStyle(0)

        # Show the window 
        self.show()

    def populateStyles(self):
        self.styleMenu.clear()
        for style in self.styles:
            self.styleMenu.addItem(style.icon, style.name)
        return


    def updateStyle(self, value):
        # Update the preview image
        style = self.styles[value]
        self.img.setPixmap(style.displayImage)

        self.info.setText(str(style))
        if style.computed:
            self.computeButton.setEnabled(False)
        else:
            self.computeButton.setEnabled(True)
        self.curStyle = style

    def importStyle(self):
        newStyle = StyleLoader.getNewStyle()
        if newStyle != None:
            self.styles += newStyle
            self.populateStyles


    def startGame(self):
        subprocess.run(PATH_TO_DOLPHIN + PATH_TO_GAME)

def main():
    app = QApplication([])
    app.setWindowIcon(QIcon("icon.png"))
    window = MainWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
