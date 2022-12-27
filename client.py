#!/usr/bin/env python
# -*-coding:utf-8 -*-
import numpy
import time
import socket
import subprocess
import struct
import json
import os

def main():
    shared_directory = os.getcwd()
    HOST = '192.168.56.13'
    PORT = 9091
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    print("Connect sucess......")

    while True:
        try: 
            # Checking the files in directory
            directory_path = os.path.dirname(shared_directory)
            all_file_name = os.listdir(directory_path)
            if not all_file_name: continue
            file_number = numpy.size(all_file_name)
            
            # Start to transport the files from all_file_name
            for filename in all_file_name:
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
                
                # Fifth step: remove the file after sending
                os.remove(filename)

            # After all traffics have been send, wait for 1 second to collect the traffic
            time.sleep(1)

        except:
            break
    client.close()

if __name__ == "__main__":
    main()