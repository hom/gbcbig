import binascii

with open("gbcbig.shx", "rb") as f:
    content = f.read()
    # print(binascii.hexlify(content, " "))

with open("gbcbig.txt", "wb") as f:
    f.write(binascii.hexlify(content, " "))
