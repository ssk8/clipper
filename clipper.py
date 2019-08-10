import pyperclip
import qbittorrent
from os import environ
from sys import argv

separate, current_cb = ' ', ['']


def add_torrents(links_list):
    print('\n\n', 'sending to torrent box')
    qb = qbittorrent.Client('http://192.168.1.144:8080/')
    qb.login(environ['QBIT_NAME'], environ['QBIT_PW'])
    [qb.download_from_link(ct) for ct in links_list]


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
    if '-t' in argv[1:]:
        add_torrents(current_cb)
    print('\n\n', separate.join(current_cb))
    pyperclip.copy(separate.join(current_cb))

