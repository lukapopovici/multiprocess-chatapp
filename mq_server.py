import multiprocessing as mp
from multiprocessing.managers import BaseManager
import sqlite3
from mess import Message, Request

class Worker(mp.Process):
    def __init__(self, message_queue):
        super(Worker, self).__init__()
        self.message_queue = message_queue

    def run(self):
        self.conn = sqlite3.connect('messages.db')
        self.cursor = self.conn.cursor()
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender TEXT,
                receiver TEXT,
                message TEXT
            )
        ''')
        self.conn.commit()

        while True:
            request = self.message_queue.get()
            if request is None:
                break
            if isinstance(request, Request):
                self.cursor.execute('''
                    SELECT sender, receiver, message FROM messages 
                    WHERE (sender = ? AND receiver = ?) OR (sender = ? AND receiver = ?)
                    ORDER BY id
                ''', (request.sender, request.receiver, request.receiver, request.sender))
                
                messages = self.cursor.fetchall()
                messages_text = "\n".join([f"{msg[0]} to {msg[1]}: {msg[2]}" for msg in messages])
                
                response_message = f"{messages_text}"
                response = Message(sender=request.receiver, receiver=request.sender, message=response_message)

                #check if response is not null
                if response:
                    self.message_queue.put(response_message)
                else:
                    self.message_queue.put("No messages found")

            if isinstance(request, Message):
                    self.cursor.execute('''
                        INSERT INTO messages (sender, receiver, message) VALUES (?, ?, ?)
                    ''', (request.sender, request.receiver, request.message))
                    self.conn.commit()
                    print(request)

    def delete_db(self):
        self.conn = sqlite3.connect('messages.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('DROP TABLE IF EXISTS messages')
        self.conn.commit()
        self.conn.close()

    def close(self):
        self.conn.close()

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

    def delete_db(self):
        self.worker.delete_db()

    def shutdown(self):
        self.worker.terminate()
        self.worker.join()
        self.worker.close()

if __name__ == '__main__':
    server = Server()
    server.delete_db()
    try:
        server.start()
    except KeyboardInterrupt:
        server.shutdown()
