import socket
import subprocess
import sys
import hashlib, uuid
import binascii
import os
import time
import pyaes
import json

os.system("cls")

def encrypt(key,packet):
    aes = pyaes.AESModeOfOperationCTR(key)
    data = aes.encrypt(packet)
    #print(data)
    return data

def decrypt(key,packet):
    aes = pyaes.AESModeOfOperationCTR(key)
    decrypted = aes.decrypt(packet).decode("ISO 8859-1")
    return decrypted

def create_dict(key,value,value2):
        keys = []
        values = []
        keys.append(key)
        keys.append("age")
        values.append(value)
        values.append(value2)
        return dict(zip(keys, values))

def send_req(key,value):
        keys = []
        values = []
        keys.append(key)
        values.append(value)
        return dict(zip(keys, values))

def login(s):
    os.system("cls")
    usn = input("Enter your username:\n")
    os.system("cls")
    pw = input("Enter your password:\n")
    s.sendall(bytes("REQL-"+encrypt("dontsharethisapplication".encode("utf-8"),str(send_req(usn, pw))).decode("ISO 8859-1"),"utf-8"))
    data = s.recv(1024)
    data = bytes.decode(data)
    data.strip("\n")
    if "REQL+" in data:
        pk = decrypt("dontsharethisapplication".encode("utf-8"),data[5:])
        print("Logged in:", pk)
        time.sleep(5)
    elif "REQL11" in data:
        print("Brute force checks are server side restart the server :)")
    elif "REQL*" in data:
        print("Invalid credentials try again")
        time.sleep(3)
        os.system("cls")
        login(s)
    else:
        pass

def create_user(s):
    os.system("cls")
    user = input("Please enter your username:")
    os.system("cls")
    pw = input("Please enter your password:")
    os.system("cls")
    pw2 = input("Please confirm your password:")
    os.system("cls")
    if (len(pw)<8 or len(pw)>15):
        print("The password must be between 8 and 15 characters\n")
        time.sleep(3)
        create_user(s)
    else:
        pass
    if pw == pw2:
        age = input("Please confirm your age:")
        s.sendall(bytes("REQPW-"+encrypt("dontsharethisapplication".encode("utf-8"),str(create_dict(user, pw, age))).decode("ISO 8859-1"),"utf-8"))
        re = input("Your account has been created, would you like to login? y/n\n")
        if "y" in re:
            login(s)
        else:
            print("Goodbye")
            exit()
    elif pw != pw2:
        os.system("cls")
        print("The password is invalid please try again:")
        time.sleep(3)
        create_user(s)
    else:
        print("debugging")


def golf():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("127.0.0.1", 5000))
        os.system("cls")
        c = True
        while c:
            x = input("Welcome to the programming golf project would you like to login? y/n\n")
            if "y" == x:
                c = False
                login(s)
            elif "n" == x:
                os.system("cls")
                if "y" == input("Would you like to create an account first? y/n\n"):
                    c = False
                    create_user(s)
                else:
                    c = False
                    print("ok, bye :(")
            else:
                os.system("cls")
                print("Press y for yes and n for no only!")


if __name__ == "__main__":
    golf()
