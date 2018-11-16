from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QGridLayout, QComboBox
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
        self._n = value


    


    def initUI(self):
        self.setGeometry(600,600,600,600)
        layoutGrid = QGridLayout()
        # Basic Button Functionality
        self.button =  QPushButton(str(self.n), self)
        self.button.clicked.connect(self.buttonClicked)
        layoutGrid.addWidget(self.button, 4,4)
        
        # Dropdown 
        self.dropDownMenu = QComboBox(self)
        entries = ["a", "b", "c"]
        for i in range(len(entries)):
            self.dropDownMenu.insertItem(i, entries[i])
        layoutGrid.addWidget(self.dropDownMenu, 3, 4)

        # Progress Bar
        
        self.show()


    def buttonClicked(self, event):
        self.n = self.n + 1

def main():
    app = QApplication([])
    window = MainWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
