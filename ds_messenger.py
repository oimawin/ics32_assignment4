
# ds_messenger.py

# Emma Huynh
# emmath@uci.edu
# 50385611

import socket
import json
import time
import ds_protocol

PORT = 3021


class DirectMessage:
    def __init__(self):
        self.recipient = None
        self.message = None
        self.timestamp = None
    
    def create_dm(self, recipient, message, timestamp):
        self.recipient = recipient
        self.message = message
        self.timestamp = timestamp


class DirectMessenger:
    def __init__(self, dsuserver=None, username=None, password=None):
        self.token = None
        self.dsuserver = dsuserver
        self.username = username
        self.password = password
		
    def send(self, message:str, recipient:str) -> bool:
        # must return true if message successfully sent, false if send failed.

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection:

            if not self.join_server(connection, PORT):
                return False

            # Send message
            timestamp = time.time()
            out_msg = {"token": self.token, 
                       "directmessage": 
                         {"entry": message, 
                          "recipient": recipient, 
                          "timestamp": timestamp}
                         }
            out_msg = json.dumps(out_msg)
            connection.send(out_msg.encode('utf-8'))

            response = json.loads(connection.recv(2048).decode('utf-8'))
            if self.__error_present(response):
                return False
            
            print(response)
            return True
            
    def retrieve_new(self) -> list:
        # must return a list of DirectMessage objects containing all new messages
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection:

            if not self.join_server(connection, PORT):
                return False

            out_msg = json.dumps({"token": self.token, "directmessage": "new"})

            connection.send(out_msg.encode('utf-8'))
            response = json.loads(connection.recv(2048).decode('utf-8'))
            print(response)

            if self.__error_present(response):
                return False

            msgs = response['response']['messages']
            processed_msgs = []
            if len(msgs) > 0:
                for item in msgs:
                    recipient = item['from']
                    message = item['message']
                    timestamp = item['timestamp']
                    dm = DirectMessage()
                    dm.create_dm(recipient, message, timestamp)
                    processed_msgs.append(dm)

            return processed_msgs
    
    def retrieve_all(self) -> list:
        # must return a list of DirectMessage objects containing all messages
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection:

            if not self.join_server(connection, PORT):
                return False

            out_msg = json.dumps({"token": self.token, "directmessage": "all"})

            connection.send(out_msg.encode('utf-8'))
            response = json.loads(connection.recv(2048).decode('utf-8'))
            print(response)

            if self.__error_present(response):
                return False

            msgs = response['response']['messages']
            processed_msgs = []
            if len(msgs) > 0:
                for item in msgs:
                    recipient = item['from']
                    message = item['message']
                    timestamp = item['timestamp']
                    dm = DirectMessage()
                    dm.create_dm(recipient, message, timestamp)
                    processed_msgs.append(dm)

            return processed_msgs
    
    def join_server(self, connection, port: int) -> bool:
        """
        Returns True if user successfully joined the server and False otherwise.
        """
        try:
            connection.connect((self.dsuserver, port))
            out_msg = ds_protocol.package_join(self.username, self.password)
            connection.send(out_msg.encode('utf-8'))

            response = json.loads(connection.recv(2048).decode('utf-8'))

            if self.__error_present(response):
                return False

            self.token = response['response']['token']
            return True

        except socket.error as e:
            print(e)
            return False
    
    
    def __error_present(self, response: dict) -> bool:
        """
        Returns True if the server sends an error response.
        """
        if response['response']['type'] == 'ok':
            return False
        elif response['response']['type'] == 'error':
            print(f"[ERROR] {response['response']['message']}")
            return True