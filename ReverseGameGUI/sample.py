import msvcrt
while 1:
    if msvcrt.kbhit():
        inp=msvcrt.getwch()
        print(inp)
