#!/usr/bin/python3

import pyperclip, qbittorrentapi
import argparse
from os import environ
import _thread


tbox_address = 'http://192.168.1.106'

def input_thread(stop_list):
    input()
    stop_list.append(True)


def check_clipboard():
    if new_clip:=pyperclip.paste():
        pyperclip.copy('')
        return new_clip


def get_cl_args():
    parser = argparse.ArgumentParser(description='add these torrents')
    parser.add_argument('torrents', type=str, nargs='*')
    args = parser.parse_args()
    return args.torrents


def start_up():
    tor_list = get_cl_args()
    print("System clipboard to tbox. Press enter when done")
    if (new_clip:=check_clipboard()) and len(new_clip)>10:
        resp = input(f"But first, add current clipboard ({new_clip[:10]}...)? (default yes)")
        if not resp.lower().startswith('n'):
            pyperclip.copy(new_clip)
    return tor_list


def add_torrents(links_list):
    print('attempting to send:\n')
    print(links_list)
    qb = qbittorrentapi.Client(host=tbox_address, port=8080, username=environ['QBIT_NAME'], password=environ['QBIT_PW'])
    qb.auth_log_in() 
    qb.torrents_add(urls=links_list)
    print(f'sent {len(links_list)} torrents to {tbox_address}')


def main():
    mag_list = start_up()
    stop_list = []
    _thread.start_new_thread(input_thread, (stop_list,))
    while not stop_list:
        if new_clip:=check_clipboard():
            mag_list.append(new_clip)
            print(f'added: {new_clip[64:94]}')

    add_torrents(mag_list)

if __name__ == "__main__":
    main()