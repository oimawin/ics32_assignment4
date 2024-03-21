
# ds_protocol.py

# Emma Huynh
# emmath@uci.edu
# 50385611

"""
A module containing functions needed to send and receive messages
through the DSP protocol.
"""

import json
import time
from collections import namedtuple


# Namedtuple to hold the values retrieved from json messages.
DataTuple = namedtuple('DataTuple', ['cmd', 'msg', 'token'])

def extract_json(json_msg:str) -> DataTuple:
    """Converts a json string into a DataTuple object.

    Args:
        json_msg (str): A json string of the server response message.

    Returns:
        DataTuple: A DataTuple of the message.
    """
    try:
        json_obj = json.loads(json_msg)
        cmd = json_obj['response']['type']
        msg = json_obj['response']['message']
        if "token" in json_obj['response']:
            token = json_obj['response']['token']
            return DataTuple(cmd, msg, token)
        else:
            return DataTuple(cmd, msg, "")

    except json.JSONDecodeError:
        print("Json cannot be decoded.")


def extract_directmsgs(json_msg:str) -> DataTuple:
    """Returns a DataTuple of json string message

    Args:
        json_msg (str): A json string.

    Returns:
        DataTuple: A DataTuple of the message.
    """
    json_obj = json.loads(json_msg)
    cmd = json_obj['response']['type']
    if "messages" in json_obj['response']:
        msgs = json_obj['response']['messages']
        return DataTuple(cmd, msgs, "")
    else:
        msg = json_obj['response']['message']
        return DataTuple(cmd, msg, "")


def to_json(obj:dict) -> str:
    """Serializes a python dictionary object to a json formatted string"""
    return json.dumps(obj)


def package_join(username:str, password:str) -> str:
    """Returns a formatted json string with the information
    required to join the DSP server as required by the DSP Protocol."""
    info = {"join": {"username": username,"password": password,"token":""}}
    return to_json(info)


def package_msg(cmd:str, message:str, token:str) -> str:
    """Organizes the information to be sent to the DSP server
    into a formatted json string as required by the DSP Protocol.

    Args:
        cmd (str): The type of message to send.
        message (str): The message to be sent.
        token (str): The user's token.

    Returns:
        str: A json formatted string of the message to send to the server.
    """
    timestamp = time.time()
    if cmd == "post":
        info = {"token": token, "post": {"entry": message, "timestamp": timestamp}}
        return to_json(info)
    elif cmd == "bio":
        info = {"token": token, "bio": {"entry": message, "timestamp": timestamp}}
        return to_json(info)


def package_directmsg(token:str, message=None, recipient=None, new=False, all=False) -> str:
    """Organizes the direct messaging information to be sent to the DSP server
    into a formatted json string as required by the DSP Protocol.

    Args:
        token (str): The user's token.
        message (str, optional): The message to be sent to the recipient. Defaults to None.
        recipient (str, optional): The recipient's username. Defaults to None.
        new (bool, optional): True if user wants to retrieve new messages. Defaults to False.
        all (bool, optional): True if user wants to retrieve all messages. Defaults to False.

    Returns:
        str: A json formatted string of the message to send to the server.
    """
    if isinstance(message, str):
        timestamp = time.time()
        info = {"token": token, "directmessage": {"entry": message, "recipient": recipient, "timestamp": timestamp}}
        return to_json(info)
    elif new:
        return to_json({"token": token, "directmessage": "new"})
    elif all:
        return to_json({"token": token, "directmessage": "all"})
