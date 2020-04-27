import itertools
import sys

def superstring(x):
    # turn subsets into strings
    x = [''.join(y) for y in x]
    
    ss = ''
    ss += x[0]
    ss += x[1]

    x.remove(x[0])
    x.remove(x[1])

    # superstring that 
    for y in x:
        c = 0
        for c in range(0, (len(ss) - len(y))):
            if ss[c:c+len(y)] == y:
                c = 1
                break
        if not c == 1:
            ss += y
        x.remove(y)

    return ss




charset = [char for char in sys.argv[1]]
length = int(sys.argv[2])

passcode_list = list(itertools.product(charset, repeat=length))
# print(''.join([''.join(y) for y in passcode_list]))
print(superstring(passcode_list))