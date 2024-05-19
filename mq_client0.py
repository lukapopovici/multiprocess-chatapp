# client.py

from multiprocessing.managers import BaseManager
from mess import Message, Request

class QueueManager(BaseManager):
    pass

class Client:
    def __init__(self, address: str, port: int, authkey: bytes):
        self.address = address
        self.port = port
        self.authkey = authkey
        self.manager = None
        self.queue = None

    def connect(self):
        QueueManager.register('get_queue')
        self.manager = QueueManager(address=(self.address, self.port),
                                    authkey=self.authkey)
        self.manager.connect()
        self.queue = self.manager.get_queue()
        print("Connected to the queue manager.")

    def send_request(self, sender: str, receiver: str, number: int):
        if self.queue:
            request = Request(sender=sender, receiver=receiver, number=number)
            self.queue.put(request)
            print(f"Sent: {request}")
        else:
            print("Queue not connected.")

    def receive_message(self):
        if self.queue:
            message = self.queue.get()
            if isinstance(message, Message):
                print(f"Received: {message}")
                return message
            else:
                print("Received an unknown type of message.")
                return None
        else:
            print("Queue not connected.")
            return None

if __name__ == '__main__':
    client = Client('localhost', 50000, b'your_secret_key')
    client.connect()
    
    # Example usage:
    client.send_request(sender="Client1", receiver="Server", number=1)
    message = client.receive_message()
