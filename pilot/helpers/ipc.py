# ipc.py
import socket
import json
import time

from utils.utils import json_serial

class IPCClient:
    def __init__(self, port):
        self.port = port
        self.client = None
        self.connected = False

    def connect(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Connecting to the external process...")
        try:
            self.client.connect(('localhost', self.port))
            self.connected = True
            print("Connected!")
        except ConnectionRefusedError:
            self.client = None
            self.connected = False
            print("Connection refused, make sure you started the external process")

    def handle_request(self, message_content):
        print(f"Received request from the external process: {message_content}")
        return message_content  # For demonstration, we're just echoing back the content

    def listen(self):
        if not self.connected:
            print("Not connected to the external process!")
            return None

        data = b''
        while True:
            try:
                data = data + self.client.recv(512 * 1024)
                message = json.loads(data)
                break
            except json.JSONDecodeError:
                # This means we still got an incomplete message, so
                # we should continue to receive more data.
                continue

        if message.get('type') == 'response':
            # self.client.close()
            return message.get('content')

    def send(self, data):
        if not self.connected:
            print("Not connected to the external process!")
            return

        serialized_data = json.dumps(data, default=json_serial)
        data_length = len(serialized_data).to_bytes(4, byteorder='big')
        self.client.sendall(data_length)
        self.client.sendall(serialized_data.encode('utf-8'))
