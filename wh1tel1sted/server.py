import socket
import hashlib
import binascii
import pyaes
import yaml
import json
import os

checkpoint = 0

def checku(unm):
    with open("data.json", "r") as fp:
        data = json.load(fp)
    for p in data["persons"]:
        if unm in list(p.keys())[0]:
            try:
                print("Found:",unm)
                return True
            except:
                print("no user")
                return None
        else:
            pass
            #print("False")

def dupdate(dict, xkey, yvalue):
    for key, value in dict.items():
        if key == xkey:
            dict[key] = yvalue
    print(dict)
    return dict

def loadh(unm):
    with open("data.json", "r") as fp:
        data = json.load(fp)
    for p in data["persons"]:
        if unm in list(p.keys())[0]:
            hash = p.get(unm)
            #print("Hash: ", hash)
            return hash
        else:
            pass

def loada(unm):
    with open("data.json", "r") as fp:
        data = json.load(fp)
    for p in data["persons"]:
        if unm in list(p.keys())[0]:
            age = p.get(list(p.keys())[1])
            return age
        else:
            pass

def u_create(con):
    with open("data.json", "r+") as fp:
        data = json.load(fp)
        #print("data:",data)
        #print("data["persons"]:" ,data["persons"])
        for per in data["persons"]:
            pass
            #print("per:",str(per))
        data["persons"].append(con)
        json.dump(data, fp)
    lines = open("data.json", "r").readlines()
    lines[0] = lines[1]
    lines[1] = "\n"
    file = open("data.json", "w")
    for line in lines:
        file.write(line)
    file.close()

def hashp(pwd):
    salt = hashlib.sha512(os.urandom(60)).hexdigest().encode()
    #print("salt: "+str(salt))
    pw = hashlib.pbkdf2_hmac("sha512", pwd.encode(), salt, 100000)
    pw = binascii.hexlify(pw)
    return (salt + pw).decode()


def encrypt(key,packet):
    aes = pyaes.AESModeOfOperationCTR(key)
    data = aes.encrypt(packet)
    #print(data)
    return data

def decrypt(key,packet):
    aes = pyaes.AESModeOfOperationCTR(key)
    decrypted = aes.decrypt(packet).decode("ISO 8859-1")
    return decrypted

def auth(hash, psw):
    salt = hash[:128]
    print("salt: "+salt)
    hash = hash[128:]
    print("hash:"+hash)
    pw = hashlib.pbkdf2_hmac("sha512", psw.encode(), salt.encode(), 100000)
    pw = binascii.hexlify(pw).decode()
    return pw == hash

def main():
    global checkpoint
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 5000))
        s.listen()
        print("Server running:")
        conn, addr = s.accept()
        with conn:
            print("Connected with", addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                data = bytes.decode(data)
                print("actuall:" ,data, type(data))
                if "REQL-" in data:
                    extract = data[5:]
                    ps = decrypt("dontsharethisapplication".encode("utf-8"),extract)
                    dct = yaml.load(ps)
                    name = [k for k in dct.keys()]
                    pw2 = [a for a in dct.values()]
                    print("DICT ",dct)
                    print("checkpoint",checkpoint)
                    if checkpoint == 3:
                        conn.send("REQL11".encode())
                        break
                    if checku(name[0]) == True:
                        if auth(loadh(name[0]),pw2[0]) == True:
                            conn.send(bytes("REQL+"+encrypt("dontsharethisapplication".encode("utf-8"),"Welcome "+str(name[0])+" your age is :"+str(loada(name[0]))).decode("ISO 8859-1"),"utf-8"))
                        else:
                            print("ERROR")
                            checkpoint += 1
                            conn.send("REQL*".encode())
                    else:
                        print("DE123")
                        checkpoint += 1
                        conn.send("REQL*".encode())

                elif "REQPW-" in data: #request for account creation
                    extract = data[6:]
                    print("ext: ",extract)
                    pa = decrypt("dontsharethisapplication".encode("utf-8"),extract)
                    try:
                        con = yaml.load(pa)
                    except:
                        conn.send("YOU CANT DO THAT HAHA IT WILL BREAK MY DATABASE :(".encode())
                    un = list(con.keys())[0]
                    print("un: ", un)
                    newp = [a for a in con.values()]
                    print("newp:  ",type(newp[0]))
                    dc = dupdate(con, un, hashp(newp[0]))
                    print("lastdict: ",str(dc))
                    if len(dc) == 2:
                        u_create(dc)
                        print("decrypted data:", pa)
                        conn.send("REQPW+".encode()) #send if account has succesfuly been created
                    else:
                        conn.send("YOU CANT DO THAT HAHA IT WILL BREAK MY DATABASE :(".encode())
                else:
                    print("DATA: "+ data)
                print("Packet: "+data)



if __name__ == "__main__":
    main()
