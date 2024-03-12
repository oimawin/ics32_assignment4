# a4.py

# Emma Huynh
# emmath@uci.edu
# 50385611


from pathlib import Path
from Profile import Profile, Post, DsuProfileError
import errors
import parse
import ui

DIR_ERROR = "[ERROR] Not a valid directory."
PATH_ERROR = "[ERROR]: Path doesn't exist"

PORT = 3021

def run_commands() -> None:
    """
    Runs whatever command is specified.
    """
    argument = input()
    command = argument[0]
    user_info = {'Profile': None, 'directory': None}

    while command != 'Q':
        if not errors.valid_command(command):
            continue
        if len(argument[1:]) == 0:
            print("ERROR")
        elif command == 'L':
            # run_l_command
            pass
        elif command == 'C':
            # run_c_command
            arguments = parse.parse_c_input(argument)
            create_file(arguments['directory'], arguments['name'])
        elif command == 'D':
            # run_d_command
            directory = parse.create_path(argument[2:])
            if directory is None:
                print(PATH_ERROR)
            else:
                delete_file(directory)
        elif command == 'R':
            # run_r_command
            directory = parse.create_path(argument[2:])
            if directory is None:
                print(PATH_ERROR)
            else:
                read_file(directory)
        elif command == 'O':
            # run_o_command
            directory = parse.create_path(argument[2:])
            if directory is None:
                print(PATH_ERROR)
            else:
                user = open_file(directory)
                user_info['directory'] = directory
                user_info['Profile'] = user
        elif command == 'E':
            # run_e_command
            arguments = parse.parse_e_input(argument)
            edit(user_info['directory'], arguments, user_info['Profile'])
        elif command == 'P':
            # run_p_command
            arguments = parse.parse_e_input(argument)
            print_data(arguments, user_info['Profile'])
        argument = input()
        command = argument[0]


# -----------------------------------
# Part 2


# C COMMAND


def create_file_user() -> tuple:
    """
    Prompts the user for information and returns the username, password, and bio
    """
    print("Please enter a username:")
    username = input()
    print("Please enter a password:")
    password = input()
    print("Please enter a bio:")
    bio = input()
    return username, password, bio


def create_file(directory: Path, name: str) -> None:
    """
    Creates a dsu file with the name at the specified directory,
    then creates the user's Profile and stores it in that dsu file.
    """
    directory = parse.create_path(directory)
    if not directory.is_dir():
        print(DIR_ERROR)
        return
    new_file_path = directory.joinpath(name + '.dsu')
    if new_file_path.is_file():
        open_file(new_file_path)
    else:
        new_file_path.touch(exist_ok=True)
    print(new_file_path)

    username, password, bio = create_file_user()
    user = Profile(None, username, password)
    user.bio = bio
    user.save_profile(new_file_path)
    print("Profile saved")


# D COMMAND


def delete_file(directory: Path) -> None:
    """
    Deletes a file at the specified path.
    """
    if directory.suffix != ".dsu":
        print("ERROR")
        return
    directory.unlink()
    print(f"{directory} DELETED")


# R COMMAND


def read_file(directory: Path) -> None:
    """
    Reads a dsu file at the specified path.
    """
    if directory.suffix != '.dsu':
        print("ERROR")
        return
    with directory.open() as f:
        text = f.readlines()
    if text == '':
        print("EMPTY")
    else:
        for i in text:
            print(i[:-1])



# O COMMAND


def open_file(directory: Path) -> Profile:
    """
    Opens a dsu file for usage and creates a Profile object from the information in the file.
    """
    if directory.suffix != '.dsu':
        print("[ERROR] File is not a dsu file.")
        return False
    elif not directory.is_file():
        print("[ERROR] The specified path is not a file.")
        return False

    user = Profile()
    try:
        user.load_profile(directory)

        print('Profile has been loaded! Here is the information stored so far:')
        print(f'| Username: {user.username}')
        print(f'| Password: {user.password}')
        print(f'| Bio: {user.bio}')

        return user

    except DsuProfileError:
        print("[ERROR]: File is not formatted correctly")
        return False


# E COMMAND


def edit(directory: Path, arguments: list, user: Profile) -> None:
    """
    Edits the user's Profile information and creates and deletes posts.
    """
    for each in arguments:
        if each['opt_input'] == '':
            pass
        else:
            if each['option'] == "-usr":
                user.username = each['opt_input']
                print(f"New username: {user.username}")

            elif each['option'] == "-pwd":
                user.password = each['opt_input']
                print(f"New password: {user.password}")

            elif each['option'] == "-bio":
                user.bio = each['opt_input']
                print(f"New bio: {user.bio}")

            elif each['option'] == "-addpost":
                new_post = Post()
                new_post.set_entry(each['opt_input'])
                user.add_post(new_post)

                print(f"New post: {user._posts[-1]['entry']}")

            elif each['option'] == "-delpost":
                keep_posts = []
                for j, post in enumerate(user._posts):
                    if j != int(each['opt_input']):
                        keep_posts.append(post)

                # for j in range(len(user._posts)):
                #     if j != int(each['opt_input']):
                #         keep_posts.append(user._posts[j])
                print(f"Post {int(each['opt_input'])} has been deleted.")
                user._posts = keep_posts

            else:
                print("Invalid option input: Operation cancelled")
                return
        user.save_profile(directory)


# P COMMAND


def print_data(arguments: list, user: Profile):
    """
    Prints the specified stored information in the user's Profile.
    """
    for each in arguments:
        if each['option'] == "-usr":
            print(f"Username: {user.username}")
        elif each['option'] == "-pwd":
            print(f"Password: {user.password}")
        elif each['option'] == "-bio":
            print(f"Bio: {user.bio}")
        elif each['option'] == "-posts":
            if len(user._posts) == 0:
                print("You currently have no posts.")
            else:
                for i in range(len(user._posts)):
                    print(f"Post {i}: {user._posts[i]['entry']}")
        elif each['option'] == "-post":
            i = int(each['opt_input'])
            print(f"Post {i}: {user._posts[i]}")
        elif each['option'] == "-all":
            print(f"Username: {user.username}")
            print(f"Password: {user.password}")
            print(f"Bio: {user.bio}")
            for i in range(len(user._posts)):
                print(f"Post {i}: {user._posts[i]['entry']}")


def main():
    ui.start()

if __name__ == "__main__":
    main()
