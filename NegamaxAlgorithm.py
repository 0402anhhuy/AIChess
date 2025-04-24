import copy

class State:
    def __init__(self, data=None, N=3):
        self.data = data or [0] * (N * N)
        self.N = N

    def close(self):
        return copy.deepcopy(self)

    def Print(self):
        sz = self.N
        for i in range(sz):
            for j in range(sz):
                tmp = self.data[i * sz + j]
                if tmp == 0:
                    print('_', end='')
                elif tmp == 1:
                    print('o', end='')
                else:
                    print('x', end='')
            print()
        print("==========")

class Operator:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def Move(self, s):
        sz = s.N
        x = self.x
        y = self.y
        if x < 0 or x >= sz or y < 0 or y >= sz:
            return None
        if s.data[x * sz + y] != 0:
            return None
        res = sum(1 for value in s.data if value != 0)
        sn = s.close()
        sn.data[x * sz + y] = 1 if res % 2 == 0 else 2
        return sn

    def isEndNode(self, s):
        sz = s.N
        data = s.data
        for i in range(sz):
            if data[i * sz + 0] != 0 and data[i * sz + 0] == data[i * sz + 1] == data[i * sz + 2]:
                return True
            if data[0 * sz + i] != 0 and data[0 * sz + i] == data[1 * sz + i] == data[2 * sz + i]:
                return True
        if data[0] != 0 and data[0] == data[4] == data[8]:
            return True
        if data[2] != 0 and data[2] == data[4] == data[6]:
            return True
        return all(v != 0 for v in data)

    def Win(self, s):
        if s.data is None:
            return False
        sz = s.N
        data = s.data
        for i in range(sz):
            if data[i * sz + 0] != 0 and data[i * sz + 0] == data[i * sz + 1] == data[i * sz + 2]:
                return True
            if data[0 * sz + i] != 0 and data[0 * sz + i] == data[1 * sz + i] == data[2 * sz + i]:
                return True
        if data[0] != 0 and data[0] == data[4] == data[8]:
            return True
        if data[2] != 0 and data[2] == data[4] == data[6]:
            return True
        return False

    def checkMyTurn(self, s):
        empty = sum(1 for x in s.data if x == 0)
        return empty % 2 == 0

    def Value(self, s):
        if self.Win(s):
            return 1 if self.checkMyTurn(s) else -1
        return 0

    def AlphaBeta(self, s, d, a, b, mp):
        if self.isEndNode(s) or d == 0:
            return self.Value(s)

        sz = s.N
        if mp:
            for i in range(sz):
                for j in range(sz):
                    child = Operator(i, j).Move(s)
                    if child is None:
                        continue
                    tmp = self.AlphaBeta(child, d - 1, a, b, False)
                    a = max(a, tmp)
                    if a >= b:
                        return a
            return a
        else:
            for i in range(sz):
                for j in range(sz):
                    child = Operator(i, j).Move(s)
                    if child is None:
                        continue
                    tmp = self.AlphaBeta(child, d - 1, a, b, True)
                    b = min(b, tmp)
                    if a >= b:
                        return b
            return b

    def Minimax(self, s, d, mp):
        return self.AlphaBeta(s, d, -2, 2, mp)

    def Run(self):
        player = 1
        turn = 0
        s = State([0] * 9)
        s.Print()
        while True:
            if (turn % 2) + 1 == player:
                print("Player's turn:")
                moved = False
                while not moved:
                    try:
                        x = int(input("Enter row (0-2): "))
                        y = int(input("Enter col (0-2): "))
                        child = Operator(x, y).Move(s)
                        if child:
                            s = child
                            moved = True
                        else:
                            print("Invalid move. Try again.")
                    except ValueError:
                        print("Invalid input. Use integers 0, 1, or 2.")
                if self.Win(s):
                    s.Print()
                    print("Player wins!")
                    break
            else:
                print("AI is thinking...")
                best_score = 2
                best_move = None
                for i in range(3):
                    for j in range(3):
                        child = Operator(i, j).Move(s)
                        if child is None:
                            continue
                        score = self.Minimax(child, 5, True)
                        print(f"AI considers move ({i}, {j}) with score {score}")
                        if score < best_score:
                            best_score = score
                            best_move = child
                s = best_move
                if self.Win(s):
                    s.Print()
                    print("AI wins!")
                    break

            s.Print()
            if self.isEndNode(s):
                print("It's a draw!")
                break
            turn += 1

if __name__ == "__main__":
    operator = Operator()
    operator.Run()