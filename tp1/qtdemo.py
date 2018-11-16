from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QGridLayout, QComboBox, QProgressBar
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
        layoutGrid.addWidget(self.button, 0,0)
        
        # Dropdown 
        self.dropDownMenu = QComboBox(self)
        entries = ["a", "b", "c"]
        for i in range(len(entries)):
            self.dropDownMenu.insertItem(i, entries[i])
        layoutGrid.addWidget(self.dropDownMenu, 0, 1)

        # Progress Bar
        self.progressBar = QProgressBar(self)
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100)
        layoutGrid.addWidget(self.progressBar, 0, 2)

        # Show the window 
        self.show()


    def buttonClicked(self, event):
        self.n = self.n + 1

def main():
    app = QApplication([])
    window = MainWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
