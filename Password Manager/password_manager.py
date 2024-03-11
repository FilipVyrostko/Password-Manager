import random, string
from typing import *
from hashlib import sha256
import datetime
import os, sys, time

_PASSWORD_FILE = "passwords.txt"

class PasswordManager():

    _char_pool = string.ascii_letters + string.digits + "#!?*@"

    def _xor(self, _master_password: str, _password: str) -> str:
        return ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(_master_password, _password)).encode("utf-8").hex()

    def check_master_password(_master_password) -> bool:
        _password_hash = sha256(_master_password.encode("utf-8")).hexdigest()
        with open(_PASSWORD_FILE, "r") as f:
            _stored_password: str = f.readline()
            if _stored_password.endswith("\n"):
                _stored_password = _stored_password[:-1]
            if _password_hash == _stored_password:
                return True
            else:
                sys.stderr.write("\n\tFailed to verify master password.\n")
                time.sleep(5)
                return False
    
    def delete_single_password(self, _master_password: str, _password: str, _desc: str, _date: str):
        _password = self._xor(_master_password, _password)
        time.sleep(1)
        with open(_PASSWORD_FILE, "r") as f1:
            with open("temp.txt", "w") as f2:
                f2.write(f1.readline()[:-1]) # Copy the master password hash
                for line in f1.readlines():
                        if line.endswith("\n"):
                            line = line[:-1]
                        line = line.split(" ")
                        if line[0] != _password or line[1] != _desc or line[2] != _date:
                            f2.write(f"\n{line[0]} {line[1]} {line[2]}")
        os.remove(_PASSWORD_FILE)
        os.rename("temp.txt", _PASSWORD_FILE)

    
    def delete_all_passwords(self, _desc: str) -> bool:
        with open(_PASSWORD_FILE, "r") as f1:
            with open("temp.txt", "w") as f2:
                f2.write(f1.readline()[:-1]) # Copy the master password hash
                for line in f1.readlines()[1:]:
                        if line.endswith("\n"):
                            line = line[:-1]
                        line = line.split(" ")
                        if line[1] != _desc:
                            f2.write(
                                f"\n{line[0]} {line[1]} {line[2]}"
                                )
        os.remove(_PASSWORD_FILE)
        os.rename("temp.txt", _PASSWORD_FILE)

    def generate_pasword(self, _max_len: int = 16) -> str | None:
        if _max_len < 1: 
            return None
        
        _password: str = ""

        for _ in range(_max_len):
            _password += random.choice(self._char_pool)

        return _password

    def set_master_password(self, _password: str):
        while len(_password) != 16:
            _password: str = str(input("Master password must have exactly 16 characters, please try again (press 'q' to quit): "))
            if _password == "q":
                return False
        _password_hash = sha256(_password.encode("utf-8")).hexdigest()
        with open(_PASSWORD_FILE, "w") as f:
            f.write(_password_hash)
        return True

    def save_password(self, _master_password: str, _password: str, _desc: str) -> bool:
        with open(_PASSWORD_FILE, "a") as f:
            _secret: str = self._xor(_master_password, _password)
            f.write(
                f"\n{_secret} {_desc} {datetime.date.today()}"
            )
        print("Passowrd saved.")
        time.sleep(3)
        return True

    def get_password(self, _master_password: str, _desc: str) -> Union[List, None]:
        _password_list = []
        with open(_PASSWORD_FILE, "r") as f:
            for line in f.readlines()[1:]:
                if line.endswith("\n"):
                    line = line[:-1]
                data = line.split(" ")  #[password (as bytes), description, date]
                if data[1].lower() == _desc.lower():
                    _password: str = self._xor(_master_password, bytes.fromhex(data[0]).decode("utf-8"))
                    _password = bytes.fromhex(_password).decode("utf-8")
                    _password_list.append((_password, data[2]))
        return _password_list

    def reset_master_password(self):
        _in: str = str(input("Reseting master password will delete all existing password, do you want to proceed? [y/n]: "))
        if _in.lower() == "y":
            os.remove(_PASSWORD_FILE)
            _in = str(input("Passwords deleted, please enter new master passowrd: "))
            if not self.set_master_password(_in):
                return False
            print("Reset successful.")
            return True
        return False
