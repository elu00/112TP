################################################################################
# bench.py:
# This file handles the user interface and databinding for the benchmarking suite.
################################################################################
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt
import pyqtgraph as pg

import sys
import time
import alg
from fileManager import Algorithms, Style, BenchThread
import os


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("StyleDev Benchmarker")
        self.initUI()

    def initUI(self):
        self.setGeometry(200,200,800,800)
        layoutGrid = QGridLayout(self)
        self.setLayout(layoutGrid)

        # Initialize UI Elements
        # Main Preview Image
        dataGraph = pg.PlotWidget(title = "Benchmark Results")
        self.dataPlot = dataGraph.getPlotItem()
        self.dataPlot.setLabel('left', "Computation Time", units='s')
        self.dataPlot.setLabel('bottom', "Iterations")
        layoutGrid.addWidget(dataGraph, 0, 0, 6, 1)

        # Style Image Selection
        styleWrapper = QHBoxLayout()
        self.styleSelect = QPushButton("Select the style image")
        self.styleSelect.clicked.connect(self.updateStyleImage)
        self.styleLabel = QLabel()
        self.stylePath = ""
        styleWrapper.addWidget(self.styleSelect)
        styleWrapper.addWidget(self.styleLabel)
        layoutGrid.addLayout(styleWrapper, 1, 1)

        # Content Image Selection
        contentWrapper = QHBoxLayout()
        self.contentSelect = QPushButton("Select the content image")
        self.contentSelect.clicked.connect(self.updateContentImage)
        self.contentLabel = QLabel()
        self.contentPath = ""
        contentWrapper.addWidget(self.contentSelect)
        contentWrapper.addWidget(self.contentLabel)
        layoutGrid.addLayout(contentWrapper, 2, 1)

        # Parameter adjustment
        algWrapper = QGridLayout()
        self.iterLabel = QLabel("Iteration Step Size: ")
        self.iterSelect = genSlider(10)
        self.iterSelect.setOrientation(Qt.Horizontal)
        self.iterSelect.sliderMoved.connect(self.updateIter)
        self.updateIter(1)
        algWrapper.addWidget(self.iterLabel, 0, 0)
        algWrapper.addWidget(self.iterSelect, 0, 2)

        self.stepLabel = QLabel("Step Count:")
        self.stepSelect = genSlider(10)
        self.stepSelect.sliderMoved.connect(self.updateSteps)
        self.updateSteps(1)
        algWrapper.addWidget(self.stepLabel, 1, 0)
        algWrapper.addWidget(self.stepSelect, 1, 2)
        layoutGrid.addLayout(algWrapper, 3, 1)


        # Progress bar
        self.progressBar = QProgressBar()
        self.progressBar.setMinimum(0)
        layoutGrid.addWidget(self.progressBar, 7, 0)


        # Compute Button
        self.benchButton = QPushButton("Benchmark!")
        self.benchButton.clicked.connect(self.startBench)
        self.benchButton.setEnabled(False)
        self.computeThread = None
        layoutGrid.addWidget(self.benchButton, 5, 1)
    
        # Show the window 
        self.show()

    
    def startBench(self):
        self.alg = Algorithms(0, 512)
        style = Style("Bench", "Bench", self.stylePath, self.alg, False, "")
        try:
            os.mkdir("temp")
        except:
            pass
        self.disableAll()
        self.curStep = 0
        self.lastTime = None
        self.data = ([], [])
        self.progressBar.setMaximum(self.steps * self.iterations)
        self.computeThread = BenchThread(style, self)
        self.computeThread.finished.connect(self.calcNextStep)
        self.calcNextStep()

    def calcNextStep(self):
        # Process/graph the new data
        if self.lastTime != None:
            timeElapsed = time.time() - self.lastTime
            (x, y) = (self.alg.iterations, timeElapsed)
            self.dataPlot.plot([x], [y], pen=(200,200,200), 
                        symbolBrush=(64,181,246), symbolPen='w')
            self.data[0].append(x)
            self.data[1].append(y)
        self.progressBar.setValue(self.alg.iterations)
        # Recursively run the next step
        if self.alg.iterations < self.steps * self.iterations:
            self.alg.iterations += self.iterations
            self.lastTime = time.time()
            self.computeThread.start()
        else:
            # All the iterations have finished, so we can display all the data.
            self.dataPlot.plot(self.data[0], self.data[1], pen=(200,200,200), 
                        symbolBrush=(64,181,246), symbolPen='w')
            

    def updateStyleImage(self):
        fileTypes = "Images (*.jpg *.png)"
        self.stylePath = QFileDialog.getOpenFileName(self, 
                        "Choose an Image", "../styles", fileTypes)[0]
        self.styleLabel.setText(self.stylePath.split("/")[-1])
        self.checkCompleteness()

    def updateContentImage(self):
        fileTypes = "Images (*.jpg *.png)"
        self.contentPath = QFileDialog.getOpenFileName(self, 
                        "Choose an Image", "../styles", fileTypes)[0]
        self.contentLabel.setText(self.contentPath.split("/")[-1])
        self.checkCompleteness()
    
    def updateIter(self, value):
        self.iterations = value * 100
        self.iterLabel.setText("Iteration Step Size: %d" % self.iterations)

    def updateSteps(self, value):
        self.steps = value
        self.stepLabel.setText("Step Count: %d" % self.steps)

    def disableAll(self):
        self.benchButton.setEnabled(False)
        self.styleSelect.setEnabled(False)
        self.contentSelect.setEnabled(False)

    def checkCompleteness(self):
        if self.stylePath != "" and self.contentPath != "":
            self.benchButton.setEnabled(True)



def genSlider(number):
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
