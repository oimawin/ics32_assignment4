
# ds_client.py

# Emma Huynh
# emmath@uci.edu
# 50385611

import socket
import json
import time
import ds_protocol


def send(server:str, port:int, username:str, password:str, message:str, bio:str=None):
    '''
    The send function joins a ds server and sends a message, bio, or both

    :param server: The ip address for the ICS 32 DS server.
    :param port: The port where the ICS 32 DS server is accepting connections.
    :param username: The user name to be assigned to the message.
    :param password: The password associated with the username.
    :param message: The message to be sent to the server.
    :param bio: Optional, a bio for the user.
    '''
    if not check_send_inputs((server, username, password, message), str):
        return False
    if not isinstance(port, int):
        return False
    if not (bio is None or isinstance(bio, str)):
        return False
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection:
        try:
            connection.connect((server, port))
            out_msg = package_join(username, password)
            send_msg(connection, out_msg)
        except socket.error as e:
            print(e)
            return False

        response = rcv_msg(connection)
        if error_present(response):
            return False

        token = response.token

        if msg_valid(message):
            out_msg = package_msg("post", message, token)
            send_msg(connection, out_msg)

            response = rcv_msg(connection)
            if error_present(response):
                return False

        if isinstance(bio, str) and msg_valid(bio):
            out_msg = package_msg("bio", bio, token)
            send_msg(connection, out_msg)

            response = rcv_msg(connection)
            if error_present(response):
                return False
            else:
                return True
        return True

    # TODO: return either True or False depending on results of required operation


class ErrorException(Exception):
    """
    Raised when the DSP server sends an error message.
    """


def send_msg(connection, message:str) -> None:
    """
    A function to conviently handle sending user information
    to the DSP server.
    """
    connection.send(message.encode('utf-8'))
    # Debugging statements
    print("Message is being sent...")
    print(message)
    # print()


def rcv_msg(connection) -> ds_protocol.DataTuple:
    """
    A function to conveniently handle receiving the DSP server's
    messages and organizing its information into a DataTuple.
    """
    response = connection.recv(2048).decode('utf-8')
    # Debugging statements
    print("Received response from server:")
    response = ds_protocol.extract_json(response)
    print(response.msg)
    # print()
    return response


def package_join(username:str, password:str) -> str:
    """
    Returns a formatted json string with the information
    required to join the DSP server as required by the DSP Protocol.
    """
    info = {"join": {"username": username,"password": password,"token":""}}
    return to_json(info)


def package_msg(cmd:str, message:str, token:str) -> str:
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


def to_json(obj:dict) -> str:
    """
    Serializes a python dictionary object to a json formatted string
    returns None if object cannot be serialized to json
    """
    return json.dumps(obj)


def error_present(response:ds_protocol.DataTuple) -> bool:
    """
    Returns True if the server sends an error response
    """
    try:
        if response.cmd == 'ok':
            return False
        elif response.cmd == 'error':
            raise ErrorException
    except ErrorException:
        print(f"[ERROR] {response.msg}")
        return True


def check_send_inputs(inputs:tuple, input_type) -> bool:
    """
    Returns true if all send function arguments are the
    correct type.
    """
    try:
        for each in inputs:
            if not isinstance(each, input_type):
                print(f"{each} is not a {input_type}")
                raise TypeError
        return True
    except TypeError:
        return False


def msg_valid(msg:str) -> bool:
    """
    Returns true if a msg is validly formatted
    (neither blank nor purely whitespace).
    """
    if isinstance(msg, str) and not msg.isspace() and len(msg) != 0:
        return True
    else:
        return False
