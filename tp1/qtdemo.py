from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QVBoxLayout

PATH_TO_DOLPHIN = "Dolphin.exe"
PATH_TO_GAME = ""

def main():
    app = QApplication([])
    window = QWidget()
    layout = QVBoxLayout()
    layout.addWidget(QPushButton('Top'))
    layout.addWidget(QPushButton('Bottom'))
    window.setLayout(layout)
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()
