
# test_ds_messenger.py

# Emma Huynh
# emmath@uci.edu
# 50385611

import socket
import unittest
from ds_messenger import DirectMessenger

SERVER = '168.235.86.101'
PORT = 3021

user1 = DirectMessenger(SERVER, 'lunavoyager', 'velvetvortexpassword')
user2 = DirectMessenger(SERVER, 'quantumquasar', 'lunarlegendpassword')

class TestJoin(unittest.TestCase):
    def test_join_svr(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection:
            assert user1.join_server(connection, PORT)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection: 
            assert user2.join_server(connection, PORT)