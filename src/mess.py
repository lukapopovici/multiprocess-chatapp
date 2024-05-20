#clasa cu ADT-uri pentru mesaje si tupuri de cerei

class Message_Request:
    def __init__(self, sender: str, receiver: str, message: str):
        self.sender = sender
        self.receiver = receiver
        self.message = message

    def __str__(self):
        return f"{self.message}"

    def set_sender(self, sender: str):
        self.sender = sender

    def set_receiver(self, receiver: str):
        self.receiver = receiver

    def set_message(self, message: str):
        self.message = message

    def get_sender(self) -> str:
        return self.sender

    def get_receiver(self) -> str:
        return self.receiver

    def get_message(self) -> str:
        return self.message


class History_Request:
    def __init__(self, sender: str, receiver: str, number: int):
        self.sender = sender
        self.receiver = receiver
        self.number = number

    def __repr__(self):
        return f"Request(sender='{self.sender}', receiver='{self.receiver}', number={self.number})"

    def __str__(self):
        return f"{self.number}"

    
class Friend_Request:
    def __init__(self, sender: str):
        self.sender = sender