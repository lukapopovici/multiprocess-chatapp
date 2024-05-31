#SCHELET PENTRU INTEGRAT LOGICA CLIENT
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton

class SimpleInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        mainLayout = QVBoxLayout()
        self.label = QLabel('TEXT')
        middleLayout = QHBoxLayout()

        leftButtonLayout = QVBoxLayout()

        button1 = QPushButton('Buton 1')
        button2 = QPushButton('Buton 2')

        leftButtonLayout.addWidget(button1)
        leftButtonLayout.addWidget(button2)

        self.lineEdit = QLineEdit()
        middleLayout.addLayout(leftButtonLayout)
        middleLayout.addWidget(self.lineEdit)
        bottomButtonLayout = QHBoxLayout()
        reloadButton = QPushButton('Reload')
        sendButton = QPushButton('Send')
        bottomButtonLayout.addWidget(reloadButton)
        bottomButtonLayout.addWidget(sendButton)
        mainLayout.addWidget(self.label)
        mainLayout.addLayout(middleLayout)
        mainLayout.addLayout(bottomButtonLayout)
        self.setLayout(mainLayout)
        self.setWindowTitle('UI Proof of Concept')
        self.setGeometry(100, 100, 400, 200)
        reloadButton.clicked.connect(self.onReload)
        sendButton.clicked.connect(self.onSend)

    def onReload(self):
        print("Reload")
        self.lineEdit.clear()

    def onSend(self):
        print("Send")
        print("Text:", self.lineEdit.text())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SimpleInterface()
    ex.show()
    sys.exit(app.exec_())
