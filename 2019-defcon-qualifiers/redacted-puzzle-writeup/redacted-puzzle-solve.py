verticies = ['10001100', '01100011', '11100100', '01000110', '10000101', '00111101', '01000010', '10011000', '11100000',
                 '11110100', '10000000', '00101101', '01110010', '00011100', '00001000', '10100101', '11010111', '01101110',
                 '10100110', '10010001', '10111100', '10000100', '10000001', '10111001', '11010100', '00111011', '11001110',
                 '11110010', '00011110', '10011101', '11001001', '11000111', '01100101', '00011110', '10011111']
    

alphabet = '+-=ABCDEFGHIJKLMNOPQRSTUVWXYZ_{}'

def solve(verticies):

    combined = ''

    for v in verticies:

        combined += v


    indicies = []

    for x in range (0, len(combined)//5):

        indicies.append(combined[x * 5:x * 5 + 5])

    answer = ''

    for x in indicies:

        answer += alphabet[int(x, 2)]

    print (answer)

    

def twist(verticies):

    newverticies = []

    for v in verticies:

        # v = abcdefgh -> habcdefg

        newv = ''
        newv+=v[7]
        newv+=v[0:7]        
        newverticies.append(newv)

    return newverticies

for x in range (0,8):

    solve(verticies)
    verticies = twist(verticies)
    

print("Finished Program")
