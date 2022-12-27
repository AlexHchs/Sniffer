#!/usr/bin/env python
# -*-coding:utf-8 -*-
import socket
import struct
import json
import os

def main():
    download_directory = __file__
    HOST = '192.168.56.13'
    PORT = 9091
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    while True:
        connection, address = server.accept()
        while True:
            command = input('>>: ').strip()
            if not command : continue
            
            connection.send(command.encode('utf-8'))

            # Open a new file as writing, then write the new file from the server host
            # First step: receive the header size
            object = connection.recv(4)
            print(object)
            header_size = struct.unpack('i', object)[0]

            # Second step: receive the header
            header_bytes = connection.recv(header_size)

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

            # Fourth step: receive the real data
            with open('%s/%s' % (download_directory, file_name), 'wb') as f:
                recv_size = 0
                while recv_size < total_size:
                    line = server.recv(1024)
                    f.write(line)
                    recv_size += len(line)
                    print('Total size: %s, Already downloads: %s' % (total_size, recv_size))
            connection.close()
        server.close()

if __name__ == "__main__":
    main()