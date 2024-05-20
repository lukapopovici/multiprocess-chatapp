import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt
from Client1 import Client

class SimpleInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.client = Client('localhost', 50000, b'your_secret_key', sender='Luka')
        self.client.RefreshFriends()
        self.initUI()

    def initUI(self):
        mainLayout = QVBoxLayout()
        self.label = QLabel(
            f"Conversations:\n{self.formatConversations(self.client.conversations)}"
        )
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

    def formatConversations(self, conversations):
        return "\n".join(conversations)

    def updateLabel(self):
        self.label.setText(f"Conversations:\n{self.formatConversations(self.client.conversations)}")

    def onReload(self):
        print("Reload")
        self.client.Refresh('Sebi')
        self.updateLabel()
        self.lineEdit.clear()

    def onSend(self):
        self.client.Send_And_Refresh('Sebi', self.lineEdit.text())
        print("Send")
        print("Text:", self.lineEdit.text())
        self.updateLabel()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SimpleInterface()
    ex.show()
    sys.exit(app.exec_())
