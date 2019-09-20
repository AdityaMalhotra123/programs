while True:
    height = int(input("Height: "))
    if (height > 0 and height <= 23):
        break
spaces = height - 1
hashes = 2
x = 0

while x < height:
    z = 0
    y = 0
    while z < spaces:
        print(" ",end='')
        z = z + 1

    while y < hashes:
        print("#",end='')
        y = y + 1

    print("")
    hashes = hashes + 1
    spaces = spaces - 1
    x = x + 1
