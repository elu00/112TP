from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt

import sys
import alg
import fileManager
from fileManager import Algorithms, Style, ImageThread
import os


# A QT Dialog for importing in new styles
class StyleLoader(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.initUI()


    def initUI(self):
        layout = QVBoxLayout(self)

        



        # Select the style directory
        dirWrapper = QHBoxLayout()
        self.dirSelect = QPushButton("Select the output/style directory")
        self.dirSelect.clicked.connect(self.updateStyleDir)
        self.dirPath = QLabel()
        self.styleDir = ""
        dirWrapper.addWidget(self.dirSelect)
        dirWrapper.addWidget(self.dirPath)
        layout.addLayout(dirWrapper)


        # Confirmation Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        buttons.button(QDialogButtonBox.Ok).setEnabled(False)
        layout.addWidget(buttons)
        self.buttons = buttons




    def updateIter(self, value):
        self.iterations = value * 100
        self.iterLabel.setText("Iterations: %d" % self.iterations)

    def updateRes(self, value):
        self.resolution = value * 128
        self.resLabel.setText("Resolution: %d" % self.resolution)

    def updateStyleDir(self):
        self.styleDir = QFileDialog.getExistingDirectory(self, 
                        "Choose a folder", "../styles")
        self.dirPath.setText(self.styleDir)
        self.checkCompleteness()

    def checkCompleteness(self):
        if self.styleImage != "" and self.styleDir != "":
            self.buttons.button(QDialogButtonBox.Ok).setEnabled(True)
        else:
            self.buttons.button(QDialogButtonBox.Ok).setEnabled(False)
    
    def getStyle(self):
        return Style(name = self.name, descr = self.descr, 
                        styleImage = self.styleImage, 
                        alg = Algorithms(self.iterations, self.resolution),
                        computed = False, styleDir = self.styleDir)
    
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
        self.setWindowTitle("StyleDev Benchmarker")
        self.initUI()

    def initUI(self):
        self.setGeometry(200,200,800,800)
        layoutGrid = QGridLayout(self)
        self.setLayout(layoutGrid)

        # Initialize UI Elements, then populate them with updateStyle()
        # Main Preview Image
        self.img = QLabel()
        layoutGrid.addWidget(self.img, 0, 0, 5, 1)
        # Select algorithm parameters
        algWrapper = QGridLayout()
        self.iterLabel = QLabel("Iterations: ")
        self.iterSelect = genSlider(100, 5)
        self.iterSelect.setOrientation(Qt.Horizontal)
        self.iterSelect.sliderMoved.connect(self.updateIter)
        self.updateIter(1)
        algWrapper.addWidget(self.iterLabel, 0, 0)
        algWrapper.addWidget(self.iterSelect, 0, 2)

        self.resLabel = QLabel("Resolution: ")
        self.resSelect = genSlider(128, 6)
        self.resSelect.sliderMoved.connect(self.updateRes)
        self.updateRes(1)
        algWrapper.addWidget(self.resLabel, 1, 0)
        algWrapper.addWidget(self.resSelect, 1, 2)
        layout.addLayout(algWrapper)

        # Style Image Selection
        imgWrapper = QHBoxLayout()
        self.imgSelect = QPushButton("Select the style image")
        self.imgSelect.clicked.connect(self.updateImage)
        self.imgPath = QLabel()
        self.styleImage = ""
        imgWrapper.addWidget(self.imgSelect)
        imgWrapper.addWidget(self.imgPath)
        layout.addLayout(imgWrapper)

        # If necessary, progress bar
        self.progressBar = QProgressBar()
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100)
        layoutGrid.addWidget(self.progressBar, 6, 0)

        # Style Selection Menu 
        self.styleMenu = QComboBox()
        self.populateStyles()
        self.styleMenu.currentIndexChanged.connect(self.updateStyle)
        layoutGrid.addWidget(self.styleMenu, 0, 1)

        # Info Box
        self.info = QLabel()
        layoutGrid.addWidget(self.info, 0, 1)   


        # Import New Style
        self.importButton = QPushButton("Import New Style...")
        self.importButton.clicked.connect(self.importStyle)
        layoutGrid.addWidget(self.importButton, 4, 1)

        # Compute Button
        self.computeButton = QPushButton("Calculate Style")
        self.computeButton.clicked.connect(self.computeActiveStyle)
        self.computeThread = None
        layoutGrid.addWidget(self.computeButton, 5, 1)

        # Launch Button
        self.launchButton = QPushButton("Start Game!")
        self.launchButton.clicked.connect(self.startGame)
        layoutGrid.addWidget(self.launchButton, 6, 1)
    

        # Populate the interface
        self.curStyle = self.styles[0]
        self.updateStatus()
        self.updateStyle(0)
    
        # Show the window 
        self.show()

    
    def startBench(self):
        if self.computeThread == None:
            style = self.curStyle
            self.computeButton.setText("Cancel Calculation")
            self.computeThread = ImageThread(style, self)
            self.computeThread.finished.connect(self.done)
            self.computeThread.start()
        else:
            self.updateStatus()
            self.progressBar.setValue(0)
            self.computeThread.terminate()
            self.computeThread = None

    def done(self):
        self.thread = None
        self.updateStatus()
        return
    def updateImage(self):
        fileTypes = "Images (*.jpg *.png)"
        self.styleImage = QFileDialog.getOpenFileName(self, 
                        "Choose an Image", "../styles", fileTypes)[0]
        self.imgPath.setText(self.styleImage)
        self.checkCompleteness()

    def updateStatus(self):
        computed = self.curStyle.computed
        if computed and self.isoPath != "" and self.dolphinPath != "":
            self.launchButton.setText("Start Game!")
            self.launchButton.setEnabled(True)
        else:
            self.launchButton.setText("Need paths set or style to be computed")
            self.launchButton.setEnabled(False)
        # Compute Button Stuff
        if computed:
            self.progressBar.hide()
            self.computeButton.setEnabled(False)
            self.computeButton.setText("Style Already Computed!")
        else:
            self.progressBar.show()
            self.progressBar.setValue(0)
            self.computeButton.setEnabled(True)
            self.computeButton.setText("Calculate Style")

def genSlider(step, number):
    slider = QSlider()
    slider.setOrientation(Qt.Horizontal)
    slider.setRange(1, number)
    slider.setSingleStep(1)
    slider.setPageStep(1)
    return slider

def main():
    app = QApplication([])
    app.setWindowIcon(QIcon("icon.png"))
    window = MainWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()