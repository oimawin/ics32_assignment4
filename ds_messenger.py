
# ds_messenger.py

# Emma Huynh
# emmath@uci.edu
# 50385611

"""
Module containing the DirectMessage and DirectMessenger classes
which handle the exchange and storage of message and user information
to and from a DSP server.
"""

import socket
import json
import time
import ds_protocol

PORT = 3021

class DirectMessage:
    """Class which stores the information of a Direct Message."""
    def __init__(self):
        """Constructor to instantiate the DirectMessage class."""
        self.recipient = None
        self.message = None
        self.timestamp = None

    def create_dm(self, recipient, message, timestamp):
        """Assigns information to the attributes of the DirectMessage object."""
        self.recipient = recipient
        self.message = message
        self.timestamp = timestamp


class DirectMessenger:
    """Class which stores the information of a user in a DSP server."""
    def __init__(self, dsuserver=None, username=None, password=None):
        """Constructor to instantiate the DirectMessenger class."""
        self.token = None
        self.dsuserver = dsuserver
        self.username = username
        self.password = password

    def send(self, message:str, recipient:str) -> bool:
        """Returns True if a message was successfully sent to the recipient.

        Args:
            message (str): The message the user wants to send.
            recipient (str): The username of the recipient who is receiving the message.

        Returns:
            bool: True if message was successfully sent.
        """
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
            if self._error_present(response):
                return False

            return True


    def retrieve_new(self) -> list:
        """Returns a list of DirectMessgae objects containing new messages.

        Returns:
            list: A list of the user's new messages as DirectMessage objects.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection:

            if not self.join_server(connection, PORT):
                return False

            out_msg = json.dumps({"token": self.token, "directmessage": "new"})
            connection.send(out_msg.encode('utf-8'))

            rcv = connection.makefile('r')
            response = json.loads(rcv.readline())

            if self._error_present(response):
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
        """Returns a list of DirectMessage objects containing all messages.

        Returns:
            list: A list of all of the user's messages as DirectMessage objects.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection:

            if not self.join_server(connection, PORT):
                return False

            out_msg = json.dumps({"token": self.token, "directmessage": "all"})
            connection.send(out_msg.encode('utf-8'))

            rcv = connection.makefile('r')
            response = json.loads(rcv.readline())
            #print(response)

            if self._error_present(response):
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
        """Returns True if user successfully joined the server and False otherwise.

        Args:
            connection (socket): The socket connection.
            port (int): The port where connection is being accepted.

        Returns:
            bool: True if user successfully joined the server.
        """
        try:
            connection.connect((self.dsuserver, port))
            out_msg = ds_protocol.package_join(self.username, self.password)
            connection.send(out_msg.encode('utf-8'))

            response = json.loads(connection.recv(2048).decode('utf-8'))

            if self._error_present(response):
                return False

            self.token = response['response']['token']
            return True

        except socket.error as e:
            print(e)
            return False


    def _error_present(self, response: dict) -> bool:
        """Returns True if the server sends an error response."""
        if response['response']['type'] == 'ok':
            return False
        elif response['response']['type'] == 'error':
            print(f"[ERROR] {response['response']['message']}")
            return True
