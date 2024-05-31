import sqlite3
import multiprocessing as mp
from multiprocessing.managers import BaseManager
from loginRequests import Login_Request, Signup_Request

class Worker(mp.Process):
    def __init__(self, message_queue):
        super(Worker, self).__init__()
        self.message_queue = message_queue
        self.server_password = b'your_secret_key'  

    def run(self):
        self.conn = sqlite3.connect('users.db')
        self.cursor = self.conn.cursor()
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT
            )
        ''')
        self.conn.commit()

        while True:
            request = self.message_queue.get()
            if request is None:
                self.message_queue.put("404")
                break
            if isinstance(request, Login_Request):
                print("Case 2: Login")
                self.cursor.execute('''SELECT * FROM users WHERE username = ? AND password = ?''', (request.username, request.password))
                user = self.cursor.fetchone()
                if user:
                    response_message = f"Login successful: {self.server_password}"
                else:
                    response_message = "404"
                self.message_queue.put(response_message)
                
            if isinstance(request, Signup_Request):
                print("Case 3: Signup")
                try:
                    self.cursor.execute('''INSERT INTO users (username, password) VALUES (?, ?)''', (request.username, request.password))
                    self.conn.commit()
                    response_message = f"Signup successful: {self.server_password}"
                except sqlite3.IntegrityError:
                    response_message = "404"
                self.message_queue.put(response_message)

class QueueManager(BaseManager):
    pass

class LoginServer:
    def __init__(self, address=('localhost', 4999), authkey=b'your_secret_key'):
        self.queue = mp.Queue()
        self.worker = Worker(self.queue)
        self.worker.start()

        QueueManager.register('get_queue', callable=lambda: self.queue)
        self.manager = QueueManager(address=address, authkey=authkey)

    def start(self):
        server = self.manager.get_server()
        server.serve_forever()

    def shutdown(self):
        self.worker.terminate()
        self.worker.join()

if __name__ == '__main__':
    server = LoginServer()
    try:
        server.start()
    except KeyboardInterrupt:
        server.shutdown()
