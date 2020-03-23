offset = 0xe5a0

with open("8dot_out.jpg", "rb") as f:
    data = f.read()

with open("out.png", "wb") as f:
    f.write(data[offset:])
