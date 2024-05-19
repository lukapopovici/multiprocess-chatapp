from multiprocessing.managers import BaseManager
from mess import Message, Request

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

    def connect(self):
        QueueManager.register('get_queue')
        self.manager = QueueManager(address=(self.address, self.port),authkey=self.authkey)
        self.manager.connect()
        self.queue = self.manager.get_queue()
        print("Connected to the queue manager.")

    def send_request(self, receiver: str, number: int):
        if self.queue:
            request = Request(sender=self.sender, receiver=receiver, number=number)
            self.queue.put(request)
            print(f"Sent: {request}")
        else:
            print("Queue not connected.")
    
    def send_message(self, receiver: str, message: str):
        if self.queue:
            message = Message(sender=self.sender, receiver=receiver, message=message)
            self.queue.put(message)
            print(f"Sent: {message}")
        else:
            print("Queue not connected.")

    def receive_message(self):
        if self.queue:
            message = self.queue.get()
            if isinstance(message, Message):
                message_lines = message.message.split('\n')
                print("Received:")
                for line in message_lines[:10]:
                    print(line)
            else:
                print(message)
        else:
            print("Queue not connected.")
            return None
        
    def Send_And_Refresh(self, receiver): 
        self.connect()
        self.send_request(receiver, number=10)
        self.receive_message()        
        print("[*]")
        my_message = input("Enter your message: ")
        self.send_message(receiver, message=my_message)

    def Refresh(self, receiver):
        input("Press Enter to refresh")
        self.connect()
        self.send_request(receiver, number=10)
        self.receive_message()

if __name__ == '__main__':
    client = Client('localhost', 50000, b'your_secret_key', sender='Luka')
    while True:
            client.Refresh("Sebi")   
            