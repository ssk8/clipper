import pyperclip
from sys import argv

separate, current_cb = ' ', ''

if '-n' in argv[1:]:
    separate = '\n\n'

pyperclip.copy(current_cb)

try:
    while True:
        if current_cb != pyperclip.paste():
            print(pyperclip.paste())
            current_cb += pyperclip.paste() + separate
            pyperclip.copy(current_cb)

except KeyboardInterrupt:
    print('\n\n', current_cb)
    pyperclip.copy(current_cb)

