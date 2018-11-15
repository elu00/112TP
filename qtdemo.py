from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QVBoxLayout
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
