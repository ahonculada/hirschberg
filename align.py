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
        self.foward = [[0 for _ in range(len(B)+1)] for _ in range(2)]
        self.reverse = [[0 for _ in range(len(B)+1)] for _ in range(2)]
        self.min_alignment_score = self.naive_align(A, B)
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

    def naive_align(self, A: str, B: str) -> int:
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

    def hirsch_align(self, A1: int, A2: int, B1: int, B2: int):
        # no more characters in A
        if A2 <= A1:
            for i in range(B1, B2):
                self.alignment_1 += '-'
                self.alignment_2 += self.B[i]
            return
        # no more characters in B
        if B2 <= B1:
            for i in range(B1, B2):
                self.alignment_1 += self.B[i]
                self.alignment_2 += '-'
            return
        # A has exactly one character
        if A1+1 == A2:
            c = self.A[A1]
            memo = B1
            for i in range(B1+1, B2):
                if self.B[i] == c:
                    memo = i
            for i in range(B1, B2):
                if i == memo:
                    self.alignment_1 += c
                else:
                    self.alignment_1 += '-'
                self.alignment_2 += self.B[i]
            return

        # Divide and Conquer
        mid = (A1 + A2) // 2
        self.set_forward(A1, mid, B1, B2)
        self.set_reverse(mid, A2, B1, B2)
        B_mid = B1
        best = float('inf')
        # find cheapest split
        for i in range(B1, B2):
            S = self.foward[mid%2][i] + self.reverse[mid%2][i]
            if S < best:
                best, B_mid = S, i

        self.hirsch_align(A1, mid, B1, B_mid)
        self.hirsch_align(mid, A2, B_mid, B2)

    def set_forward(self, A1: int, A2: int, B1: int, B2: int):
        self.forward[A1%2][B1] = 0
        # set first row
        for j in range(B1+1, B2+1):
            self.forward[A1%2][j] = self.forward[A1%2][j-1] + 1
        for i in range(A1+1, A2+1):
            self.forward[i%2][B1] = self.forward[(i-1)%2][B1] + 1
            for j in range(B1+1, B2+1):
                self.forward[i%2][j] = min(
                    self.forward[(i-1)%2][j] + 1,
                    self.forward[i%2][j-1] + 1,
                    self.forward[(i-1)%2][j-1] + 1 * (self.A[i-1] == self.B[j-1])
                )

    def set_reverse(self, A1: int, A2: int, B1: int, B2: int):
        self.reverse[A2%2][B2] = 0
        # set first row
        for j in range(B2-1, B1-1, -1):
            self.reverse[A2%2][j] = self.reverse[A2%2][j+1] + 1
        for i in range(A2-1, A1-1, -1):
            self.reverse[i%2][B2] = self.reverse[(i+1)%2][B2] + 1
            for j in range(B2-1, B1-1, -1):
                self.reverse[i%2][j] = min(
                    self.reverse[(i+1)%2][j] + 1,
                    self.reverse[i%2][j+1] + 1,
                    self.reverse[(i+1)%2][j+1] + 1 * (self.A1[i-1] == self.B[j-1])
                )

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

