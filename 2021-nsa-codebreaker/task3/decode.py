key = b"D"  # 0x68 in ASCII
out = b""

# Open in Read Bytes mode
with open("pressure", "rb") as f:
    c = f.read()

    # Chained XOR
    for x in c:
        key = bytes([x ^ int.from_bytes(key, "little")])
        out += key

# Write output file
with open("pressure_decrypted", "wb") as f:
    f.write(out)
