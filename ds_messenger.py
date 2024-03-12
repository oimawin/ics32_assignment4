
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


class DirectMessenger:
    def __init__(self, dsuserver=None, username=None, password=None):
        self.token = None
        self.dsuserver = dsuserver
        self.username = username
        self.password = password
		
    def send(self, message:str, recipient:str) -> bool:
        # must return true if message successfully sent, false if send failed.
        pass
            
    def retrieve_new(self) -> list:
        # must return a list of DirectMessage objects containing all new messages
        pass
    
    def retrieve_all(self) -> list:
        # must return a list of DirectMessage objects containing all messages
        pass
    
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