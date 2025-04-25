import copy

class State:
    def __init__(self, data=None, N=3):
        self.data = data or [0] * (N * N)
        self.N = N

    def close(self):
        return copy.deepcopy(self)
    
    def isFull(self):
        return all(cell != 0 for cell in self.data)

    def Print(self):
        boardSize = self.N
        for row in range(boardSize):
            for col in range(boardSize):
                cellValue = self.data[row * boardSize + col]
                if cellValue == 0:
                    print('_', end=' ')
                elif cellValue == 1:
                    print('o', end=' ')
                else:
                    print('x', end=' ')
            print()
        print("=" * (boardSize * 2))

class Operator:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def Move(self, state):
        boardSize = state.N
        row = self.x
        col = self.y
        if row < 0 or row >= boardSize or col < 0 or col >= boardSize:
            return None
        if state.data[row * boardSize + col] != 0:
            return None
        filledCells = sum(1 for value in state.data if value != 0)
        newState = state.close()
        newState.data[row * boardSize + col] = 1 if filledCells % 2 == 0 else 2
        return newState

    def isEndNode(self, state):
        boardSize = state.N
        boardData = state.data
        for row in range(boardSize):
            if boardData[row * boardSize + 0] != 0 and boardData[row * boardSize + 0] == boardData[row * boardSize + 1] == boardData[row * boardSize + 2]:
                return True
            if boardData[0 * boardSize + row] != 0 and boardData[0 * boardSize + row] == boardData[1 * boardSize + row] == boardData[2 * boardSize + row]:
                return True
        if boardData[0] != 0 and boardData[0] == boardData[4] == boardData[8]:
            return True
        if boardData[2] != 0 and boardData[2] == boardData[4] == boardData[6]:
            return True
        return all(cell != 0 for cell in boardData)

    def Win(self, state):
        if state.data is None:
            return False
        boardSize = state.N
        boardData = state.data
        for row in range(boardSize):
            if boardData[row * boardSize + 0] != 0 and boardData[row * boardSize + 0] == boardData[row * boardSize + 1] == boardData[row * boardSize + 2]:
                return True
            if boardData[0 * boardSize + row] != 0 and boardData[0 * boardSize + row] == boardData[1 * boardSize + row] == boardData[2 * boardSize + row]:
                return True
        if boardData[0] != 0 and boardData[0] == boardData[4] == boardData[8]:
            return True
        if boardData[2] != 0 and boardData[2] == boardData[4] == boardData[6]:
            return True
        return False

    def checkMyTurn(self, s):
        empty = sum(1 for x in s.data if x == 0)
        return empty % 2 == 0

    def Value(self, s):
        if self.Win(s):
            return 1 if self.checkMyTurn(s) else -1
        return 0

    def AlphaBeta(self, state, depth, alpha, beta, maximizingPlayer):
        if self.isEndNode(state) or depth == 0:
            return self.Value(state)

        boardSize = state.N
        if maximizingPlayer:
            for row in range(boardSize):
                for col in range(boardSize):
                    childState = Operator(row, col).Move(state)
                    if childState is None:
                        continue
                    evaluation = self.AlphaBeta(childState, depth - 1, alpha, beta, False)
                    alpha = max(alpha, evaluation)
                    if alpha >= beta:
                        return alpha
            return alpha
        else:
            for row in range(boardSize):
                for col in range(boardSize):
                    childState = Operator(row, col).Move(state)
                    if childState is None:
                        continue
                    evaluation = self.AlphaBeta(childState, depth - 1, alpha, beta, True)
                    beta = min(beta, evaluation)
                    if alpha >= beta:
                        return beta
            return beta

    def Minimax(self, state, depth, maximizingPlayer):
        return self.AlphaBeta(state, depth, -2, 2, maximizingPlayer)

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