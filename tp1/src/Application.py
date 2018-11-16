from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QGridLayout, QComboBox, QProgressBar
from PyQt5.QtGui import QIcon, QPixmap
import sys

PATH_TO_DOLPHIN = "Dolphin.exe"
PATH_TO_GAME = ""

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        # We need to instantiate a "private" variable and define getters 
        # and setters on it for QT databinding to work properly.
        self._n = 0
        self.initUI()

    @property
    def n(self):
        return self._n

    @n.setter
    def n(self, value):
        self.button.setText(str(value))
        self.progressBar.setValue(value)
        self._n = value


    


    def initUI(self):
        self.setGeometry(600,600,600,600)
        layoutGrid = QGridLayout(self)


        # Basic Button Functionality
        self.button =  QPushButton(str(self.n), self)
        self.button.clicked.connect(self.buttonClicked)
        layoutGrid.addWidget(self.button, 1, 1)
        
        # Progress Bar
        self.progressBar = QProgressBar(self)
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100)
        layoutGrid.addWidget(self.progressBar, 1, 2)

        # Dropdown 
        self.dropDownMenu = QComboBox(self)
        self.entries = ["qtdemo/screenshot1.png", "qtdemo/screenshot2.png"]
        for i in range(len(self.entries)):
            self.dropDownMenu.insertItem(i, self.entries[i])
        self.dropDownMenu.currentIndexChanged.connect(self.updateImage)
        layoutGrid.addWidget(self.dropDownMenu, 1, 0)

        # Images
        self.img = QLabel(self)
        pixmap = QPixmap(self.entries[0])
        self.img.setPixmap(pixmap)
        layoutGrid.addWidget(self.img, 0, 0)



        # Show the window 
        self.show()

    def buttonClicked(self, event):
        self.n = self.n + 1

    def updateImage(self, newIndex):
        pixmap = QPixmap(self.entries[newIndex])
        self.img.setPixmap(pixmap)

def main():
    app = QApplication([])
    window = MainWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
