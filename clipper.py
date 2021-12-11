#!/usr/bin/python3

import pyperclip, qbittorrentapi
from os import environ
import _thread


tbox_address = 'http://192.168.1.106'

def input_thread(stop_list):
    input()
    stop_list.append(True)


def add_torrents(links_list):
    print('attempting to send')
    qb = qbittorrentapi.Client(host=tbox_address, port=8080, username=environ['QBIT_NAME'], password=environ['QBIT_PW'])
    qb.auth_log_in() 
    qb.torrents_add(urls=links_list)
    print(f'sent {len(links_list)} torrents to {tbox_address}')


def main():
    print("press enter to send new clipboard coppies to tbox")
    current_cb = ['']
    pyperclip.copy(current_cb[0])
    stop_list = []
    _thread.start_new_thread(input_thread, (stop_list,))
    while not stop_list:
        if current_cb[-1] != pyperclip.paste():
            print(pyperclip.paste())
            current_cb.append(pyperclip.paste())

    add_torrents(current_cb[1:])

if __name__ == "__main__":
    main()