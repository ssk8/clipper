import pyperclip
from sys import argv

cli_args = argv[1:]

links = ['start']
pyperclip.copy('start')

print('copy ---> end <--- to quit')


while links[-1] != 'end':
    if links[-1] != pyperclip.paste():
        links.append(pyperclip.paste())
        print(links[-1])

links = [link.strip() for link in links[1:-1]]

if '-q' in cli_args:
    links = [f'"{lnk}"' for lnk in links]

pyperclip.copy(' '.join(links))

print(' '.join(links))

