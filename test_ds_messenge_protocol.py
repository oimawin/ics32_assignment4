
# test_ds_message_protocol.py

# Emma Huynh
# emmath@uci.edu
# 50385611

import time
import unittest
import ds_protocol as dsp
from ds_protocol import DataTuple

def error_msg(expected, output):
    return f"Expected output: {expected}. Actual output: {output}."

class TestPckgDirectMsg(unittest.TestCase):
    def test_directmsg(self):
        entry = "I did not hit her! I did noooot."
        recipient = "ohhimark"
        expected = dsp.to_json({"token": "chicken_fries", "directmessage": {"entry": "I did not hit her! I did noooot.","recipient":"ohhimark", "timestamp": time.time()}})
        output = dsp.package_directmsg("chicken_fries", message=entry, recipient=recipient)
        assert expected == output, error_msg(expected, output)

class TestPckgNewMsgs(unittest.TestCase):
    def test_new(self):
        expected = '{"token": "chicken_fries", "directmessage": "new"}'
        output = dsp.package_directmsg("chicken_fries", new=True)
        assert expected == output, error_msg(expected, output)