from multiprocessing.managers import BaseManager
from mess import Message_Request as Message, History_Request as Request, Friend_Request

class QueueManager(BaseManager):
    pass

class Client:
    def __init__(self, address: str, port: int, authkey: bytes, sender: str):
        self.address = address
        self.port = port
        self.authkey = authkey
        self.sender = sender
        self.manager = None
        self.queue = None
        self.friends = []
        self.conversations = []

    def connect(self):
        QueueManager.register('get_queue')
        self.manager = QueueManager(address=(self.address, self.port), authkey=self.authkey)
        self.manager.connect()
        self.queue = self.manager.get_queue()
        print("Connected to the queue manager.")

    def send_friend_request(self):
        if self.queue:
            request = Friend_Request(sender=self.sender)
            self.queue.put(request)
            response = self.queue.get()
            response = response.split("\n")
            self.friends = response

        else:
            print("Queue not connected.")

    def send_request(self, receiver: str, number: int):
        if self.queue:
            request = Request(sender=self.sender, receiver=receiver, number=number)
            self.queue.put(request)
        else:
            print("Queue not connected.")

    def send_message(self, receiver: str, message: str):
        if self.queue:
            message = Message(sender=self.sender, receiver=receiver, message=message)
            self.queue.put(message)
        else:
            print("Queue not connected.")

    def receive_message(self):
        if self.queue:
            message = self.queue.get()
            message = message.split("\n")
            self.conversations = message

        else:
            print("Queue not connected.")
            return None



    def Send_And_Refresh(self, receiver, my_message):
        self.connect()
        self.send_request(receiver, number=10)
        self.receive_message()
        print("[*]")
        self.send_message(receiver, message=my_message)

    def Refresh(self, receiver):
        self.connect()

        self.send_friend_request()
        

        self.send_request(receiver, number=10)
        self.receive_message()

    def RefreshFriends(self):
        self.connect()
        self.send_friend_request()


