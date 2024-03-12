
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