import os, platform
from typing import *
from password_manager import PasswordManager
import time

__cls = "cls" if platform.system() == "Windows" else "clear"
__pm = PasswordManager()

def clear_screen(_func: Callable):
    def wrapper(*args, **kwargs):
        os.system(__cls)
        return _func(*args, **kwargs)
    
    return wrapper


def main():
    os.system(__cls)
    _files_exist = os.path.exists("passwords.txt")
    if not _files_exist:
        _in: str = input("Please, create a master password: ")
        if not __pm.set_master_password(_in):
            return


    _master_password = user_login()
    if not _master_password:
        return
    
    show_option_menu(_master_password)


@clear_screen
def user_login() -> bool:
    _in: str = str(input("Please enter the master passowrd (enter 'q' to quit): "))

    while _in.lower() != "q":
        if __pm.check_master_password(_in):
            return _in
        else:
            os.system(__cls)
            _in = str(input("Incorrect master password, please try again (enter 'q' to quit or 'reset' to reset the master passowrd): "))

        if _in.lower() == "reset":
            if __pm.reset_master_password():
                _in = str(input("Please enter the master passowrd (enter 'q' to quit): "))

    return False

@clear_screen
def generate_password_ui(_master_password):
    while True:
        _password = __pm.generate_pasword()
        print(f"Generated password: {_password}")
        _in: str = str(input(f"Would you like to save the password? [y/n]: "))
        if _in.lower() == "y":
            _desc: str = str(input("Add password desription (default PASSWORD): "))
            if not _desc:
                _desc = "PASSWORD"
            __pm.save_password(_master_password, _password, _desc)
            return
        else:
            _in: str = str(input(f"Would you like to generate new password? [y/n]: "))
            if _in.lower() == "y":
                continue
            else:
                return

@clear_screen
def add_password_ui(_master_password):
    while True:
        _in: str = str(input("Enter custom password (16 characters) to save (enter 'q' to quit): "))
        if _in == "q":
            return
        if len(_in) != 16:
            print(f"Password is of wrong lenght: {len(_in)} characters long, need to be 16")
        else:
            _desc: str = str(input("Add password desription (default PASSWORD): "))
            if not _desc:
                _desc = "PASSWORD"
            __pm.save_password(_master_password, _in, _desc)


@clear_screen
def remove_password_ui(_master_password):
    while True:
        _desc: str = str(input("Enter description of the password to be deleted (enter 'q' to quit): "))
        if _desc == "q":
            return

        _password_list = __pm.get_password(_master_password, _desc)
        if _password_list:
            if len(_password_list) > 1:
                print("\nFound multiple passwords, would you like to:")
                print("1. Delete all passwords")
                print("2. Delete specific password")
                print("3. Exit")
                _in: int = int(input("Select choice: "))
                if _in == 3:
                    return
                elif _in == 1:
                    _verify: str = input("Are you sure you want to delete all matching passwords? [y/n]: ")
                    if _verify.lower() == "y":
                        __pm.delete_all_passwords(_desc)
                elif _in == 2:
                    _formated_list = "".join([f"{ix + 1}. {pair[0]} - {_desc} - {pair[1]}\n" 
                                      for ix, pair in enumerate(_password_list)])
                    print("\nPasswords collected:")
                    print(f"{_formated_list}")
                    _in = int(input("Please enter the number of the password to be deleted: "))
                    __pm.delete_single_password(_master_password, _password_list[_in-1][0], _desc, _password_list[_in-1][1])

            else:
                __pm.delete_single_password(_master_password, _password_list[0][0], _desc, _password_list[0][1])
            
            print("Passwords deleted.")
            time.sleep(2)
            os.system(__cls)
        else:
            print("No matching password found.")



@clear_screen
def find_password_ui(_master_password):
    while True:
        _desc: str = str(input("Please enter password description: "))
        _password_list = __pm.get_password(_master_password, _desc)
        if not _password_list:
            _in: str = str(input("No password found, would you like to try again? [y/n]: "))
            if _in.lower() != "y":
                return
        else:
            _formated_list = "".join([f"{ix + 1}. {pair[0]}  -  {pair[1]}\n" 
                                      for ix, pair in enumerate(_password_list)])
            print("\nPasswords collected:")
            print(f"{_formated_list}")
            _in: str = str(input("Search again? [y/n]: "))
            if _in.lower() != "y":
                return


@clear_screen
def reset_master_password_ui(_):
    __pm.reset_master_password()


def show_option_menu(_master_password):
    _func_list = [
        generate_password_ui,
        add_password_ui,
        remove_password_ui,
        find_password_ui,
        reset_master_password_ui
    ]

    while True:
        os.system(__cls)
        print("""
        {_t:^25}

        1. Generate password
        2. Add password
        3. Remove password
        4. Find password
        5. Reset Master Passoword
        7. Exit
        """.format(_t = "MAIN MENU"))
        
        _in: int = int(input("Select option: "))
        if _in == 7: return
        if _in in range(1, 6):
            _func_list[_in - 1](_master_password)
        else:
            print("Invalid option.")
            time.sleep(2)


if __name__ == "__main__":
    main()