from os import strerror

try:
    cnt = 0
    s = open('text.txt', "rt")
    content = s.read()
    print(content)
    cnt = len(content)
    s.close()
    print("\n\nCharacters in file:", cnt)
except IOError as e:
    print("I/O error occurred: ", strerror(e.errno))