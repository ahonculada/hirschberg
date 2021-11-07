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
        self.forward = [[Cell(0) for _ in range(len(B)+1)] for _ in range(2)]
        self.reverse = [[Cell(0) for _ in range(len(B)+1)] for _ in range(2)]
        self.min_alignment_score = -1
        #self.naive_align(A, B)
        self.hirsch_align(A, B)

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

    def naive_align(self, A: str, B: str):
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
        self.min_alignment_score = DP[-1][-1].val

    def hirsch_align(self, A: str, B: str):
        A1, A2, B1, B2 = 0, len(A), 0, len(B)
        self._hirsch_align(A1, A2, B1, B2)

    def _hirsch_align(self, A1: int, A2: int, B1: int, B2: int):
        # no more characters in A
        if A2 <= A1:
            for j in range(B1, B2):
                self.alignment_1 += '-'
                self.alignment_2 += self.B[j]
            return
        # no more characters in B
        if B2 <= B1:
            for j in range(B1, B2):
                self.alignment_1 += self.B[j]
                self.alignment_2 += '-'
            return
        # A has exactly one character
        if A1+1 == A2:
            c = self.A[A1]
            memo = B1
            for j in range(B1+1, B2):
                if self.B[j] == c:
                    memo = j
            for j in range(B1, B2):
                if j == memo:
                    self.alignment_1 += c
                else:
                    self.alignment_1 += '-'
                self.alignment_2 += self.B[j]
            return

        # Divide and Conquer
        mid = (A1 + A2) // 2
        self.set_forward(A1, mid, B1, B2)
        self.set_reverse(mid, A2, B1, B2)
        k_star = B1
        best = float('inf')
        # find cheapest split
        for j in range(B1, B2+1):
            S = self.forward[mid%2][j].val + self.reverse[mid%2][j].val
            if S < best:
                best, k_star = S, j
        if self.min_alignment_score == -1:
            self.min_alignment_score = best

        # recursive calls to reconstruct alignment
        #self._hirsch_align(A1, mid, B1, k_star)
        #self._hirsch_align(mid, A2, k_star, B2)

    def set_forward(self, A1: int, A2: int, B1: int, B2: int):
        self.forward[A1%2][B1].val = 0
        # set first row
        for j in range(B1+1, B2+1):
            self.forward[A1%2][j].val = self.forward[A1%2][j-1].val + 1
        #print(self.forward[A1%2][B1:B2+1].val)

        for i in range(A1+1, A2+1):
            # set first column
            self.forward[i%2][B1].val = self.forward[(i-1)%2][B1].val + 1
            for j in range(B1+1, B2+1):
                self.forward[i%2][j].val = min(
                    self.forward[(i-1)%2][j].val + 1,
                    self.forward[i%2][j-1].val + 1,
                    self.forward[(i-1)%2][j-1].val + 1 * (self.A[i-1] != self.B[j-1])
                )
            #print(self.forward[i%2][B1:B2+1].val)

    def set_reverse(self, A1: int, A2: int, B1: int, B2: int):
        self.reverse[A2%2][B2].val = 0
        # set first row
        for j in range(B2-1, B1-1, -1):
            self.reverse[A2%2][j].val = self.reverse[A2%2][j+1].val + 1
        #print(self.reverse[A1%2][B1:B2+1].val)

        for i in range(A2-1, A1-1, -1):
            # set first column
            self.reverse[i%2][B2].val = self.reverse[(i+1)%2][B2].val + 1
            for j in range(B2-1, B1-1, -1):
                self.reverse[i%2][j].val = min(
                    self.reverse[(i+1)%2][j].val + 1,
                    self.reverse[i%2][j+1].val + 1,
                    self.reverse[(i+1)%2][j+1].val + 1 * (self.A[i] != self.B[j])
                )
            #print(self.reverse[i%2][B1:B2+1].val)

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
        #print()
        #self.reconstruct_path(len(self.A), len(self.B))
        #print("Alignment:")
        #print(self.alignment_1)
        #print(self.alignment_2)


def read_in() -> (str, str):
    with open('data.txt', 'r') as data:
        A = data.readline().split()[0]
        B = data.readline().split()[0]
    return A, B

if __name__ == '__main__':
    A, B = read_in()
    A = 'GATCGTA'
    B = 'GACGGGA'
    solution = Align(A, B)
    solution.print_report()

