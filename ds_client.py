
# ds_client.py

# Emma Huynh
# emmath@uci.edu
# 50385611

"""
A module with functions to handle sending to and receiving messages
from a DSP server as a client.
"""

import socket
import ds_protocol


def send(server:str, port:int, username:str, password:str, message:str, bio:str=None):
    """
    The send function joins a ds server and sends a message, bio, or both.
    Returns True if the message was successfully sent and False otherwise.

    :param server: The ip address for the ICS 32 DS server.
    :param port: The port where the ICS 32 DS server is accepting connections.
    :param username: The user name to be assigned to the message.
    :param password: The password associated with the username.
    :param message: The message to be sent to the server.
    :param bio: Optional, a bio for the user.
    """
    if not check_send_inputs((server, username, password, message), str):
        return False
    if not isinstance(port, int):
        return False
    if not (bio is None or isinstance(bio, str)):
        return False
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection:
        # Connect to the server using username and password
        try:
            connection.connect((server, port))
            out_msg = ds_protocol.package_join(username, password)
            send_msg(connection, out_msg)
        except socket.error as e:
            print(e)
            return False

        # Receive okay message
        response = rcv_msg(connection)
        if error_present(response):
            return False

        token = response.token

        # Post message
        if msg_valid(message):
            out_msg = ds_protocol.package_msg("post", message, token)
            send_msg(connection, out_msg)

            response = rcv_msg(connection)
            if error_present(response):
                return False

        # Post bio
        if isinstance(bio, str) and msg_valid(bio):
            out_msg = ds_protocol.package_msg("bio", bio, token)
            send_msg(connection, out_msg)

            response = rcv_msg(connection)
            return not error_present(response)
        return True


class ErrorException(Exception):
    """Raised when the DSP server sends an error message."""


def join_server(connection: socket, server: str, port: int, username: str, password: str) -> str:
    """Joins a server and returns a token if the user successfully logged in.

    Args:
        connection (socket): The socket connection.
        server (str): IP address of the server.
        port (int): The port where connection is being accepted.
        username (str): The user name to be assigned to the message.
        password (str): The password associated with the username.

    Returns:
        str: The token associated with the username.
    """
    try:
        connection.connect((server, port))
        out_msg = ds_protocol.package_join(username, password)
        send_msg(connection, out_msg)
    except socket.error as e:
        print(e)
        return None

    # Receive okay message
    response = rcv_msg(connection)
    if error_present(response):
        return None

    return response.token


def send_msg(connection: socket, message:str) -> None:
    """Sending a message to the DSP server through a socket.

    Args:
        connection (socket): The socket connection.
        message (str): The message the user wants to send.
    """
    connection.send(message.encode('utf-8'))
    print("Message is being sent...")
    print(message)


def rcv_msg(connection: socket) -> ds_protocol.DataTuple:
    """Receives a message from the DSP server through a socket and
    returns the response.

    Args:
        connection (socket): The socket connection.

    Returns:
        ds_protocol.DataTuple: A DataTuple representing the information received from the server.
    """
    response = connection.recv(2048).decode('utf-8')
    response = ds_protocol.extract_json(response)
    return response


def error_present(response: ds_protocol.DataTuple) -> bool:
    """Extracts a DataTuple of the response and 
    returns True if the server sends an error response.

    Args:
        response (ds_protocol.DataTuple): A DataTuple of the response from the server.

    Raises:
        ErrorException: Raised when an error response is received.

    Returns:
        bool: True if the server sent an error response and False otherwise.
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
    """Returns True if all inputs in a tuple are the correct type.

    Args:
        inputs (tuple): _description_
        input_type (type): The input type to check for.

    Raises:
        TypeError: Raised when an input is not the specified input type.

    Returns:
        bool: True if all inputs are of the specified type and False otherwise.
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
    """Returns True if a msg is neither blank nor purely whitespace."""
    if isinstance(msg, str) and not msg.isspace() and len(msg) != 0:
        return True
    else:
        return False
