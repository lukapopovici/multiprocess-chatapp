import multiprocessing as mp
from multiprocessing.managers import BaseManager
from mess import Message, Request

class Worker(mp.Process):
    def __init__(self, message_queue):
        super(Worker, self).__init__()
        self.message_queue = message_queue

    def run(self):
        request = self.message_queue.get()
        if isinstance(request, Request):
            response_message = f"Processed request number: {request.number}"
            response = Message(sender=request.receiver, receiver=request.sender, message=response_message)
            self.message_queue.put(response)
            print(respose)
            print(request)

        else:
            print(respose)
            print(request)
            print("Received an unknown type of message.")

class QueueManager(BaseManager):
    pass

class Server:
    def __init__(self, address=('localhost', 50000), authkey=b'your_secret_key'):
        self.queue = mp.Queue()
        self.worker = Worker(self.queue)
        self.worker.start()

        QueueManager.register('get_queue', callable=lambda: self.queue)
        self.manager = QueueManager(address=address, authkey=authkey)

    def start(self):
        server = self.manager.get_server()
        server.serve_forever()

if __name__ == '__main__':
    server = Server()
    server.start()
