import sys
from random import randint

def generate_string(length: int) -> str:
    M = {0: 'A', 1: 'C', 2: 'T', 3: 'G'}
    S = ''

    for _ in range(length):
        S += M[randint(0,3)]

    return S

def write_out(A: str, B: str):
    with open('data.txt', 'w') as data:
        data.write(A)
        data.write('\n')
        data.write(B)
        data.write('\n')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("ERROR")
        print("Correct Usage: python3 maketest.py <integer>")
        exit()
    n = int(sys.argv[1])
    X = generate_string(n)
#    print(X)
    Y = generate_string(n)
    write_out(X, Y)
#    print(Y)

