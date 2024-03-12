
# ui.py

# Emma Huynh
# emmath@uci.edu
# 50385611

"""
The program that runs the user interface for the journaling program.
"""

from pathlib import Path
import time
import a4
import ds_client
from Profile import Profile

PORT = 3021

ADD_POST_MSG = "Please type out what you would like to post:\n"
CURRENT_POSTS_MSG = "Here are your current posts:"
DLT_POST_MSG = "What is the index of the post you want to delete?: "
EDIT_MSG = "What would you like to change it to?: "
FILE_DLT_MSG = "File has been deleted."
FILE_NAME_MSG = "What is the name of the file?: "
FILE_PATH_MSG = "What is the file path?: "
INVALID_INPT_MSG = "Invalid option input."
NO_POSTS_MSG = "You currently have no posts." \
    "Please create at least one before attempting to post to the server."
SVR_MSG = "What is the IP address of the server you'd like to post to?: "
POST_INDX_PROMPT = "Which index would you like to post to the server?: "
POST_SUCCESS = "Post successful!"
POST_BIO_SUCCESS = "Bio has been successfullly updated!"
VIEW_POST_MSG = "What is the ID of the post you'd like to view?: "


def print_main_menu() -> None:
    """
    Prints the main menu message displaying most commands.
    """
    print("[MAIN MENU]")
    print("Hello! What would you like to do?:")
    print("'l' - Lists the contents of a directory")
    print("'c' - Create a new file")
    print("'d' - Delete a file")
    print("'r' - Read the contents of a file")
    print("'o' - Open an existing file")
    print("'q' - Quit the program")
    print()


def print_o_menu() -> None:
    """
    Prints the menu message after a file has been opened
    and displays the options to either edit or print info
    from the opened file.
    """
    time.sleep(1)
    print()
    print("[FILE MENU]")
    print("What would you like to do?")
    print("'e' - Edit info")
    print("'p' - Print info")
    print("'s' - Post to DSP server", end=' ')
    print("(*Note: Please make any desired edits with the e command before posting to the server)")
    print("'m' - Exit to main menu")
    print()


def print_e_menu() -> None:
    """
    Prints the menu message for and displays each option of
    the edit command.
    """
    time.sleep(1)
    print()
    print("[EDIT MENU]")
    print("What info would you like to edit?:")
    print("'-usr' - Username")
    print("'-pwd' - Password")
    print("'-bio' - Bio")
    print("'-addpost' - Create a post")
    print("'-delpost' - Delete a post")
    print("'b' - Go back")
    print()


def print_p_menu() -> None:
    """
    Prints the menu message for and displays each option of
    the print command.
    """
    time.sleep(1)
    print()
    print("[PRINT MENU]")
    print("What info would you like to print?:")
    print("'-usr' - Username")
    print("'-pwd' - Password")
    print("'-bio' - Bio")
    print("'-posts' - All Posts")
    print("'-post' - Post by ID")
    print("'-all' - All Profile Information")
    print("'b' - Go back")
    print()


def print_s_menu() -> None:
    """
    Prints the post menu.
    """
    time.sleep(1)
    print()
    print("[POST MENU]")
    print("What would you like to post?:")
    print("'-post' - A Post")
    print("'-bio' - Bio")
    print("'-both' - Both bio and a post")
    print("'b' - Go back")
    print()


def c_command() -> None:
    """
    Runs the 'c' command to create a file.
    """
    path = input(FILE_PATH_MSG)
    name = input(FILE_NAME_MSG)
    a4.create_file(path, name)


def d_command() -> None:
    """
    Runs the 'd' command to delete a file.
    """
    path = Path(input(FILE_PATH_MSG))
    a4.delete_file(path)
    print(FILE_DLT_MSG)


def r_command() -> None:
    """
    Runs the 'r' command to read a file.
    """
    path = Path(input(FILE_PATH_MSG))
    a4.read_file(path)


def o_command() -> None:
    """
    Runs the 'o' command to open an existing file,
    then displays the options on what to do with the opened file.
    """
    path = Path(input(FILE_PATH_MSG))
    print("Loading...")
    time.sleep(1)
    user = a4.open_file(path)
    if user is False:
        return
    while True:
        print_o_menu()
        user_input = input().lower()
        if user_input == 'e':
            e_command(path, user)
        elif user_input == 'p':
            p_command(user)
        elif user_input == 's':
            s_command(path, user)
        elif user_input == 'm':
            return
        else:
            print(INVALID_INPT_MSG)
            return


def e_command(path: Path, user: Profile) -> None:
    """
    Runs the 'e' command to edit information with an opened file.
    """
    while True:
        print_e_menu()
        option = input()
        if option == '-usr' or option == '-pwd' or option == '-bio':
            opt_input = input(EDIT_MSG)
        elif option == "-addpost":
            opt_input = input(ADD_POST_MSG)
        elif option == "-delpost":
            print(CURRENT_POSTS_MSG)
            a4.print_data([{'option': '-posts', 'opt_input': ''}], user)
            print()
            opt_input = input(DLT_POST_MSG)
        elif option == 'b':
            return
        else:
            print(INVALID_INPT_MSG)
            return
        a4.edit(path, [{'option': option, 'opt_input': opt_input}], user)


def p_command(user: Profile) -> None:
    """
    Runs the 'p' command to print existing information with an opened file.
    """
    options = ('-usr', '-pwd', '-bio', '-posts', '-post', '-all')
    while True:
        print_p_menu()
        option = input()
        if option == '-post':
            opt_input = input(VIEW_POST_MSG)
        elif option == 'b':
            return
        elif option not in options:
            print(INVALID_INPT_MSG)
            return
        else:
            opt_input = ''
        a4.print_data([{'option': option, 'opt_input': opt_input}], user)


def s_command(path:Path, user:Profile) -> None:
    """
    Runs the 's' command to post a post, bio, or both to a server.
    """
    if not isinstance(user.dsuserver, str):
        user.dsuserver = input(SVR_MSG)
        user.save_profile(path)
    print_s_menu()
    opt_input = input()
    if opt_input == '-post':
        send_post(user, user.dsuserver, user.username, user.password)
    elif opt_input == '-bio':
        send_bio(user, user.dsuserver, user.username, user.password)
    elif opt_input == '-both':
        send_post(user, user.dsuserver, user.username, user.password)
        send_bio(user, user.dsuserver, user.username, user.password)
    elif opt_input == 'b':
        return
    else:
        print(INVALID_INPT_MSG)
        return


def send_post(user:Profile, server:str, username:str, password:str):
    """
    Prompts the user to choose a post through its index,
    then posts that to the server.
    """
    if len(user._posts) == 0:
        print(NO_POSTS_MSG)
    else:
        print(CURRENT_POSTS_MSG)
        a4.print_data([{'option': '-posts', 'opt_input': ''}], user)
        opt_input = int(input(POST_INDX_PROMPT))
        if opt_input >= len(user._posts):
            print("Index is out of range.")
            return
        post = user._posts[opt_input]['entry']
        print(f"Sending post to {server}")
        successful = ds_client.send(server, PORT, username, password, post)
        if successful:
            print(POST_SUCCESS)
        else:
            return


def send_bio(user:Profile, server:str, username:str, password:str) -> bool:
    """
    Displays the user's current bio and posts it to the server.
    """
    print("Here is your current bio:")
    a4.print_data([{'option': '-bio', 'opto_input': ''}], user)
    print(f"Sending bio to {server}")
    successful = ds_client.send(server, PORT, username, password, '', user.bio)
    if successful:
        print(POST_BIO_SUCCESS)
    else:
        return


def run_commands(user_input:str) -> None:
    """
    Calls any of the main menu commands when indicated as input.
    """
    if user_input == 'l':
        #l_command()
        pass
    elif user_input == 'c':
        c_command()
    elif user_input == 'd':
        d_command()
    elif user_input == 'r':
        r_command()
    elif user_input == 'o':
        o_command()
    elif user_input == 'admin':
        a4.run_commands()
    else:
        print(INVALID_INPT_MSG)
    return True


def start() -> None:
    """
    Starts and keeps the program running.
    """
    print_main_menu()
    user_input = input().lower()
    while user_input != 'q':
        time.sleep(1)
        run_commands(user_input)
        time.sleep(1)
        print()
        print_main_menu()
        user_input = input().lower()

if __name__ == "__main__":
    start()
