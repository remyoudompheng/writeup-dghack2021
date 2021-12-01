import socket
import hash_based
import sys
#s = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM,protocol=0)


def add_user(login,pk):
    s = socket.socket()         # Create a socket object
    host = socket.gethostname() # Get local machine name
    s.connect((host,port))
    s.send(b'a')
    s.recv(1024)
    s.send(bytes(login,"utf-8"))
    s.recv(1024)
    s.send(bytes(pk,"utf-8"))
    r = s.recv(1024)
    if r == b'r':
        print("User already exists. Operation forbidden.")
    elif r == b'a':
        print("Success")
    s.close()

def connect(login,sk):
    s = socket.socket()         # Create a socket object
    host = socket.gethostname() # Get local machine name
    s.connect((host,port))
    s.send(b'c')
    s.recv(1024)                # should receive byte b'l'
    s.send(bytes(login,"utf-8")) 
    chall_b = s.recv(1024)      #receives the challenge
#    chall = chall_b.hex()
    sign = hash_based.sign(sk,chall_b)
    sign_b = bytes.fromhex(sign)
    s.send(sign_b)
    r = s.recv(1024)
    if r == b'r':
        print("Authentication failed. Connection refused.")
    elif r == b'm':
        print("Connection success.")
    return s

def add_secret(s,sec):
    s.send(b'a')
    s.recv(1024)
    s.send(bytes(sec,"utf-8"))
    r = s.recv(1024)
    if r == b'm' :
        print("Secret added.")
    return ""

def get_secrets(s):
    s.send(b'g')
    r = s.recv(1024).decode("utf-8")
    print(r)

def stops_connection(s):
    s.send(b's')

def close_connection(s):
    s.close()


# Reserve a port for your service
if len(sys.argv) < 3:
    host='localhost'
    port=12345
else:
    host=sys.argv[1]
    port=int(sys.argv[2])

#Usage example:
#(sk,pk) = hash_based.key_gen()
#add_user("username",pk)
#s = connect("username",sk)
#add_secret(s,"Super secret")
#get_secrets(s)
#s.close()
#
