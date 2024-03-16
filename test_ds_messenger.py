
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

class Communication(unittest.TestCase):
    def test_send_msg(self):
        assert user1.send("Honey! Where's my paaaanntttsss??", user2.username)
        assert user1.send("Always root for the local sports team.", user1.username)
        assert user1.send("Go, sports team!", user1.username)
        
    def test_new_msgs(self):
        new_msgs = user1.retrieve_new()
        for each in new_msgs:
            print(each.__dict__)
    
    def test_all_msgs(self):
        all_msgs = user1.retrieve_all()
        for each in all_msgs:
            print(each.__dict__)

if __name__ == "__main__":
    #unittest.main()
    newtest = Communication()
    newtest.test_new_msgs()