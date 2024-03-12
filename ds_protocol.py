
# ds_protocol.py

# Emma Huynh
# emmath@uci.edu
# 50385611

import json
from collections import namedtuple

# Namedtuple to hold the values retrieved from json messages.
DataTuple = namedtuple('DataTuple', ['cmd', 'msg', 'token'])

def extract_json(json_msg:str) -> DataTuple:
    '''
    Call the json.loads function on a json string and convert it to a DataTuple object.
    '''
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

def to_json(obj:dict) -> str:
    """
    Serializes a python dictionary object to a json formatted string
    returns None if object cannot be serialized to json
    """
    return json.dumps(obj)


def package_join(username:str, password:str) -> str:
    """
    Returns a formatted json string with the information
    required to join the DSP server as required by the DSP Protocol.
    """
    info = {"join": {"username": username,"password": password,"token":""}}
    return to_json(info)


def package_msg(cmd:str, message:str, token:str, recipient=None) -> str:
    """
    Organizes the information to be sent to the DSP server
    into a formatted json string as required by the DSP Protocol.
    """
    timestamp = time.time()
    if cmd == "post":
        info = {"token": token, "post": {"entry": message, "timestamp": timestamp}}
        return to_json(info)
    elif cmd == "bio":
        info = {"token": token, "bio": {"entry": message, "timestamp": timestamp}}
        return to_json(info)