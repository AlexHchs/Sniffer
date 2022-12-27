#!/usr/bin/env python
# -*-coding:utf-8 -*-
import socket
import subprocess
import struct
import json
import os

def main():
    shared_directory = __file__
    HOST = '192.168.56.13'
    PORT = 9091
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    print("Connect sucess......")

    while True:
        try: 
            # Receive command
            receive = client.recv(8096)
            if not receive: continue # For Linux OS
            print(receive)

            # Parse command and extract the related command parameters
            commands = receive.decode('utf-8').split()
            filename = commands[1]
            print(filename)

            # Open the file as the read, send the content back to the client host
            # First step: make the static size header
            header_dic = {
                'filename': filename,
                'file_size': os.path.getsize('%s/%s' % (shared_directory, filename))
            }
            header_json = json.dumps(header_dic)
            header_bytes = header_json.encode('utf-8')

            # Second step: send the header's size
            client.send(struct.pack('i', len(header_bytes)))

            # Third step: send the header
            client.send(header_bytes)

            # Fourth step: send the real file
            with open('%s/%s' % (shared_directory, filename), 'rb') as f:
                for line in f:
                    client.send(line)
        except:
            break
    client.close()

if __name__ == "__main__":
    main()