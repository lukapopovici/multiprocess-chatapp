import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton
from PyQt5.QtCore import Qt
from ClientClass import Client

class SimpleInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.client = Client('localhost', 50000, b'your_secret_key', sender='Luka')
        self.client.RefreshFriends()
        self.initUI()

    def initUI(self):
        mainLayout = QVBoxLayout()
        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)
        self.updateTextEdit()
        
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

        mainLayout.addWidget(self.textEdit)
        mainLayout.addLayout(middleLayout)
        mainLayout.addLayout(bottomButtonLayout)

        self.setLayout(mainLayout)

        self.setWindowTitle('Uestfal EN')
        self.setGeometry(100, 100, 400, 200)
        reloadButton.clicked.connect(self.onReload)
        sendButton.clicked.connect(self.onSend)


    def updateTextEdit(self):
        self.textEdit.setText(
            "\n".join(self.client.conversations)
            )
        


    def onReload(self):
        self.client.Refresh('Sebi')
        self.updateTextEdit()
        self.lineEdit.clear()

    def onSend(self):
        self.client.Send_And_Refresh('Sebi', self.lineEdit.text())
        print("Text:", self.lineEdit.text())
        self.updateTextEdit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SimpleInterface()
    ex.show()
    sys.exit(app.exec_())
