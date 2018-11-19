from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QGridLayout, QComboBox, QProgressBar
from PyQt5.QtGui import QIcon, QPixmap
import sys
import alg
import filemanager

PATH_TO_DOLPHIN = "Dolphin.exe"
PATH_TO_GAME = ""

class Style(object):
    def __init__(self, styleImage, computed, previewImage = None, styleDir = None):
        self.styleImage = styleImage
        if previewImage != None and os.path.exists(previewImage):
            self.displayImage = QPixMap(previewImage)
        else:
            self.displayImage = QPixMap(styleImage)
        self.computed = computed

    def oof(self):
        pass


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.styles = [Style()]
        self.initUI()

    def initUI(self):
        self.setGeometry(600,600,600,600)
        layoutGrid = QGridLayout(self)

        # Initialize UI Elements, then populate them with updateStyle()
        # Style Selection Menu 
        self.dropDownMenu = QComboBox(self)

        # Main Preview Image
        self.img = QLabel(self)
        layoutGrid.addWidget(self.img, 0, 0)

        # Play Game/Compute results button
        self.button =  QPushButton("Button", self)
        layoutGrid.addWidget(self.button, 1, 1)
        

        # If necessary, progress bar
        self.progressBar = QProgressBar(self)
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100)
        layoutGrid.addWidget(self.progressBar, 1, 2)


        self.curStyle = self.styles[0]
        self.updateStyle()

        # Show the window 
        self.show()

    def updateStyle(self):

        pixmap = QPixmap(self.style.displayImage)
        self.img.setPixmap(pixmap)
        self.entries = ["qtdemo/screenshot1.png", "qtdemo/screenshot2.png"]
        for i in range(len(self.entries)):
            self.dropDownMenu.insertItem(i, self.entries[i])
        self.dropDownMenu.currentIndexChanged.connect(self.updateImage)
        layoutGrid.addWidget(self.dropDownMenu, 1, 0)

        self.button.clicked.connect(self.buttonClicked)


    def startGame(self):
        pass
def main():
    app = QApplication([])
    window = MainWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
