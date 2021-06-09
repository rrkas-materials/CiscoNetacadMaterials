from os import strerror

try:
    bf = open('file.bin', 'rb')
    data = bytearray(bf.read())
    bf.close()

    for b in data:
        print(chr(b), end='')

except IOError as e:
    print("I/O error occurred:", strerror(e.errno))