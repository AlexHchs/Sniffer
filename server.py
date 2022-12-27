#!/usr/bin/env python
# -*-coding:utf-8 -*-
import socket
import struct
import json
import os

def main():
    download_directory = os.getcwd()
    HOST = '192.168.56.13'
    PORT = 9091
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print("Waiting for connection......")
    while True:
        connection, address = server.accept()
        print("Connection success......")
        try:
            while True:
                # Receive file numbers
                receive = connection.recv(8096)
                if not receive: break

                # Parse the command
                command = receive.decode('utf-8').split()
                file_number = command[0]
                print(file_number)
                
                for i in range(file_number):
                    # Open a new file as writing, then write the new file from the server host
                    # First step: receive the header size
                    print(i)
                    object = connection.recv(4)
                    print(object)
                    header_size = struct.unpack('i', object)[0]
                    print(header_size)

                    # Second step: receive the header
                    header_bytes = connection.recv(header_size)
                    print(header_bytes)

                    # Third step: extract the detail info. of the real data from header
                    header_json = header_bytes.decode('utf-8')
                    header_dic = json.loads(header_json)
                    '''
                    header_dic = {
                        'filename': filename,
                        'file_size': os.path.getsize('%s/%s' % (shared_directory, filename))
                    }
                    '''
                    total_size = header_dic['file_size']
                    file_name = header_dic['filename']
                    print(total_size)
                    print(file_name)

                    # Fourth step: receive the real data
                    with open('%s/%s' % (download_directory, file_name), 'wb') as f:
                        recv_size = 0
                        while recv_size < total_size:
                            line = connection.recv(1024)
                            f.write(line)
                            recv_size += len(line)
                            print('Total size: %s, Already downloads: %s' % (total_size, recv_size))
        except:
            connection.close()
            break
    server.close()

if __name__ == "__main__":
    main()