class Cell:
    def __init__(self, val: int):
        self.val = val
        self.prev = ''


class Align:
    def __init__(self, A: str, B: str):
        self.A = A
        self.B = B
        self.map = {'d': (-1, -1), 'u': (-1, 0), 'l': (0, -1)}
        self.DP = None
        self.path = []
        self.alignment_1 = ''
        self.alignment_2 = ''
        self.min_alignment_score = self.align(A, B)
        self.reconstruct_path(len(A), len(B))

    def reconstruct_path(self, row: int, col: int):
        if not row and not col:
            self.path.append((0, 0))
            return
        curr = self.DP[row][col]
        delta = self.map[curr.prev]
        self.reconstruct_path(row + delta[0], col + delta[1])
        self.path.append((row, col))
        if curr.prev == 'd':
            self.alignment_1 += A[row-1]
            self.alignment_2 += B[col-1]
        elif curr.prev == 'u':
            self.alignment_1 += '-'
            self.alignment_2 += B[col-1]
        elif curr.prev == 'l':
            self.alignment_1 += A[row-1]
            self.alignment_2 += '-'

    def align(self, A: str, B: str) -> int:
        rows, cols = len(A), len(B)
        DP = [[Cell(0) for _ in range(cols+1)] for _ in range(rows+1)]
        for i in range(1, rows+1):
            DP[i][0].val = i
            DP[i][0].prev = 'u'
        for j in range(1, cols+1):
            DP[0][j].val = j
            DP[0][j].prev = 'l'

        for row in range(1, rows+1):
            for col in range(1, cols+1):
                d = DP[row-1][col-1].val + 1 * (A[row-1] != B[col-1])
                l = DP[row][col-1].val + 1
                u = DP[row-1][col].val + 1
                small = min(d, l, u)
                if d == small:
                    DP[row][col].prev = 'd'
                elif l == small:
                    DP[row][col].prev = 'l'
                elif u == small:
                    DP[row][col].prev = 'u'
                DP[row][col].val = small
        self.DP = DP
        return DP[-1][-1].val

    def print_DP(self):
        for R in self.DP:
            for C in R:
                print(C.val, end=" ")
            print()

    def print_report(self):
        print("First String:  {}".format(self.A))
        print("Second String: {}".format(self.B))
        #self.print_DP()
        print("Minimum Alignment Score: {}".format(self.min_alignment_score))
        print("Alignment")
        print(self.alignment_1)
        print(self.alignment_2)


def read_in() -> (str, str):
    with open('data.txt', 'r') as data:
        A = data.readline().split()[0]
        B = data.readline().split()[0]
    return A, B

if __name__ == '__main__':
    A, B = read_in()
    solution = Align(A, B)
    solution.print_report()

