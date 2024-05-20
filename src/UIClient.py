import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt
from Client1 import Client

class SimpleInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.client = Client('localhost', 50000, b'your_secret_key', sender='Luka')
        self.client.RefreshFriends()
        print("asdasdasdaas")
        self.initUI()

    def initUI(self):
        mainLayout = QVBoxLayout()
        self.label = QLabel('TEXT')
        middleLayout = QHBoxLayout()

        leftButtonLayout = QVBoxLayout()
        buttons = []
        for friend in self.client.friends:
            button = QPushButton(friend)
            buttons.append(button)
            leftButtonLayout.addWidget(button)

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
