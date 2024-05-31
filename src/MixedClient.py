import sys
import socket
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton, QInputDialog, QMessageBox
from PyQt5.QtCore import Qt
from multiprocessing.managers import BaseManager

from ClientClass import Client
from loginRequests import Login_Request, Signup_Request

class QueueManager(BaseManager):
    pass

class SimpleInterface(QWidget):
    def __init__(self, sender, password):
        super().__init__()
        self.sender = sender
        self.password = password
        try:
            self.client = Client('localhost', 50000, password.encode(), sender=sender)
            self.client.RefreshFriends()
            self.initUI()
        except Exception as e:
            QMessageBox.critical(self, "Connection Error", f"Failed to connect: {e}")
            sys.exit(1)

    def initUI(self):
        mainLayout = QVBoxLayout()
        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)
        self.updateTextEdit()
        
        middleLayout = QHBoxLayout()
        leftButtonLayout = QVBoxLayout()
        self.buttons = []
        for friend in self.client.friends:
            button = QPushButton(friend)
            button.clicked.connect(self.onFriendButtonClick)
            self.buttons.append(button)
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
        self.textEdit.setText("\n".join(self.client.conversations))

    def onReload(self):
        try:
            self.client.Refresh('Sebi')
            self.updateTextEdit()
            self.lineEdit.clear()
        except Exception as e:
            QMessageBox.critical(self, "Reload Error", f"Failed to reload: {e}")

    def onSend(self):
        try:
            self.client.Send_And_Refresh('Sebi', self.lineEdit.text())
            self.updateTextEdit()
        except Exception as e:
            QMessageBox.critical(self, "Send Error", f"Failed to send message: {e}")

    def onFriendButtonClick(self):
        sender = self.sender
        password = self.password
        friend = self.sender
        self.client = Client('localhost', 50000, password.encode(), sender=sender)
        self.client.RefreshFriends()
        self.updateTextEdit()


if __name__ == '__main__':
    QueueManager.register('get_queue')
    manager = QueueManager(address=('localhost',4999), authkey=b'your_secret_key')  
    manager.connect()
    queue = manager.get_queue()
    app = QApplication(sys.argv)
    #ask me if i want to login or signup
    request_or_login=QMessageBox.question(None, "Login or Signup", "Do you want to login?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

    sender, okPressed = QInputDialog.getText(None, "Login", "Enter your username:", QLineEdit.Normal, "")
    password, okPressed = QInputDialog.getText(None, "Login", "Enter your password:", QLineEdit.Normal, "")
  
    if request_or_login == QMessageBox.StandardButton.Yes:
        request = Login_Request(username=sender, password=password)
    else:
        request = Signup_Request(username=sender, password=password)

    queue.put(request)
    response = queue.get()
    if response == "404":
        QMessageBox.critical(None, "Login Error", "Failed to login.")
        sys.exit(1)
    else:
        print("Login successful.")
        ex = SimpleInterface(sender, response)
        ex.show()
        sys.exit(app.exec_())