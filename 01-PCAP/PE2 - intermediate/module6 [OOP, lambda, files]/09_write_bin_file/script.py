from os import strerror

data = bytearray(10)

for i in range(len(data)):
    data[i] = ord('a') + i

try:
    bf = open('file.bin', 'wb')
    print(bf.write(data))
    bf.close()
except IOError as e:
    print("I/O error occurred:", strerror(e.errno))