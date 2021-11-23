import sys
import timeit
import tracemalloc
from align import Align, read_in
from maketest import generate_string, write_out

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Error")
        print("Corrrect Usage: python3 average.py <integer>")
        exit()
    avgm = []
    avgt = []
    n = int(sys.argv[1])
    for _ in range(10):
        X = generate_string(n)
        Y = generate_string(n)
        write_out(X, Y)
        A, B = read_in()
        start = timeit.default_timer()
        tracemalloc.start()
        Solution = Align(A, B)
        mem = tracemalloc.get_traced_memory()
        end = timeit.default_timer()
        tracemalloc.stop()
        avgm.append(mem[1])
        avgt.append(end-start)
    with open('results.txt', 'a') as data:
        Am = sum(avgm)/10
        At = sum(avgt)/10
        data.write(f'{n}\t{Am}\t{At}\n')

