import sys
import tracemalloc
from align import Align, read_in
from maketest import generate_string, write_out

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Error")
        print("Corrrect Usage: python3 average.py <integer>")
        exit()
    avg = []
    n = int(sys.argv[1])
    for _ in range(10):
        X = generate_string(n)
        Y = generate_string(n)
        write_out(X, Y)
        A, B = read_in()
        tracemalloc.start()
        Solution = Align(A, B)
        mem = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        avg.append(mem[1])
    with open('results.txt', 'a') as data:
        A = sum(avg)/10
        data.write(f'{n}\t{A}\n')

