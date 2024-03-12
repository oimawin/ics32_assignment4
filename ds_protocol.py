
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
