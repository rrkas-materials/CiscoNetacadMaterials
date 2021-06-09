from os import strerror

data = bytearray(10)

try:
    bf = open('file.bin', 'rb')
    bf.readinto(data)
    bf.close()

    for b in data:
        print(chr(b), end='')
except IOError as e:
    print("I/O error occurred:", strerror(e.errno))