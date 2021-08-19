import pyperclip
import qbittorrent
from os import environ
from sys import argv

torrent_box_address = 'http://192.168.1.106:8080/'

def add_torrents(links_list):
    print('\n\n', 'sending to torrent box')
    qb = qbittorrent.Client(torrent_box_address)
    qb.login(environ['QBIT_NAME'], environ['QBIT_PW'])
    [qb.download_from_link(ct) for ct in links_list]
    print(f'sent {len(links_list)} torrents to {torrent_box_address}')


separate, current_cb = ' ', ['']

if '-n' in argv[1:]:
    separate = '\n\n'
    print("new line")

if '-c' in argv[1:]:
    separate = ', '
    print("comma separated")

pyperclip.copy(current_cb[0])

try:
    while True:
        if current_cb[-1] != pyperclip.paste():
            print(pyperclip.paste())
            current_cb.append(pyperclip.paste())

except KeyboardInterrupt:
    current_cb.pop(0)
    if '-t' in argv[1:]:
        add_torrents(current_cb)
    #print('\n', separate.join(current_cb))
    pyperclip.copy(separate.join(current_cb))
