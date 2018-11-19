from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QGridLayout, QComboBox, QProgressBar
from PyQt5.QtGui import QIcon, QPixmap
import sys
import alg
import filemanager
import os
import subprocess

PATH_TO_DOLPHIN = "Dolphin.exe"
PATH_TO_GAME = ""
WINDOW_DIMENSIONS = (600,600)

class Style(object):
    def __init__(self, name, descr, styleImage, alg, computed,
                    styleDir, previewImage = None):
        self.name = name
        self.descr = descr
        self.alg = alg
        self.styleImage = styleImage
        self.styleDir = styleDir
        self.icon = QIcon(styleImage)
        if previewImage != None and os.path.exists(previewImage):
            self.displayImage = QPixmap(previewImage).scaledToWidth(600)
        else:
            self.displayImage = QPixmap(styleImage)
        self.computed = computed


    def __repr__(self):
        return \
        '''Current Style: %s \n
        Description: %s              \n
        Algorithm: %s                \n
        Images: %s                   \n
        Folder: %s                   \n
        ''' % (self.name, self.descr, self.alg, 100, self.styleDir)

    def oof(self):
        pass

class StyleLoad(QWidget):
    def __init__(self):
        super().__init__()
        return

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.styles = [Style(
            "Starry Night", "Van Gogh's Starry Night", 
            "../styles/starrynight/style.jpg", "nn",
            True, "../styles/starrynight",
            "../styles/starrynight/preview.png"
        )]
        self.initUI()

    def initUI(self):
        self.setGeometry(600,600,600,600)
        layoutGrid = QGridLayout(self)
        self.setLayout(layoutGrid)

        # Initialize UI Elements, then populate them with updateStyle()

        # Main Preview Image
        self.img = QLabel(self)
        layoutGrid.addWidget(self.img, 0, 0, 4, 1)

        # If necessary, progress bar
        self.progressBar = QProgressBar(self)
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100)
        layoutGrid.addWidget(self.progressBar, 5, 0)

        # Style Selection Menu 
        self.styleMenu = QComboBox(self)
        self.populateStyles()
        self.styleMenu.currentIndexChanged.connect(self.updateStyle)
        layoutGrid.addWidget(self.styleMenu, 0, 1)

        # Info Box
        self.info = QLabel(self)
        layoutGrid.addWidget(self.info, 1, 1)        

        # Compute Button
        self.computeButton = QPushButton("Calculate Style")
        layoutGrid.addWidget(self.computeButton, 2, 1)

        # Import New Style
        self.importButton = QPushButton("Import New Style...")
        layoutGrid.addWidget(self.importButton, 3, 1)

        # Launch Button
        self.launchButton = QPushButton("Start Game!", self)
        self.launchButton.clicked.connect(self.startGame)
        layoutGrid.addWidget(self.launchButton, 5, 1)
    

        # Populate the interface
        self.curStyle = self.styles[0]
        self.updateStyle()

        # Show the window 
        self.show()
    def populateStyles(self):
        for style in self.styles:
            self.styleMenu.addItem(style.icon, style.name)
        return


    def updateStyle(self):
        # Update the preview image
        style = self.curStyle
        self.img.setPixmap(style.displayImage)

        self.info.setText(str(style))


    def startGame(self):
        subprocess.run(PATH_TO_DOLPHIN + PATH_TO_GAME)

def main():
    app = QApplication([])
    app.setWindowIcon(QIcon("icon.png"))
    window = MainWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
