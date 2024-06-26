
# test_ds_message_protocol.py

# Emma Huynh
# emmath@uci.edu
# 50385611

"""
Module to test the ds_protocol functions.
"""

import time
import ds_protocol as dsp
from ds_protocol import DataTuple

def error_msg(expected, output):
    return f"Expected output: {expected}. Actual output: {output}."

def test_directmsg():
    entry = "I did not hit her! I did noooot."
    recipient = "ohhimark"
    expected = dsp.to_json({"token": "chicken_fries", "directmessage": {"entry": "I did not hit her! I did noooot.","recipient":"ohhimark", "timestamp": time.time()}})
    output = dsp.package_directmsg("chicken_fries", message=entry, recipient=recipient)
    assert expected == output, error_msg(expected, output)

def test_new():
    expected = '{"token": "chicken_fries", "directmessage": "new"}'
    output = dsp.package_directmsg("chicken_fries", new=True)
    assert expected == output, error_msg(expected, output)

def test_all():
    expected = '{"token": "chicken_fries", "directmessage": "all"}'
    output = dsp.package_directmsg("chicken_fries", all=True)
    assert expected == output, error_msg(expected, output)

def test_extract_send():
    expected = DataTuple("ok", "Direct message sent", "")
    output = dsp.extract_directmsgs('{"response": {"type": "ok", "message": "Direct message sent"}}')
    assert expected == output, error_msg(expected, output)

def test_extract_msgs():
    example_response = {"response": 
            {
                "type": "ok", 
                "messages": [{"message": "Hello User 1!", "from": "markb", "timestamp": "1603167689.3928561"}, 
                                {"message": "Bzzzzz", "from": "thebeemoviescript", "timestamp": "1603167689.3928561"}]
                }
            }
    example_response_str = '{"response": \
        {"type": "ok", \
        "messages": \
            [{"message": "Hello User 1!", "from": "markb", "timestamp": "1603167689.3928561"}, \
            {"message": "Bzzzzz", "from": "thebeemoviescript", "timestamp": "1603167689.3928561"}]}}'

    expected = DataTuple("ok", example_response['response']['messages'], "")
    output = dsp.extract_directmsgs(example_response_str)
    assert expected == output, error_msg(expected, output)