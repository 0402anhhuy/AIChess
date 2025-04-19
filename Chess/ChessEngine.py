class Move():
    """
           a b  c d  e f  g h
        8 ⬜⬛⬜⬛⬜⬛⬜⬛  (row 0)
        7 ⬛⬜⬛⬜⬛⬜⬛⬜  (row 1)
        6 ⬜⬛⬜⬛⬜⬛⬜⬛  (row 2)
        5 ⬛⬜⬛⬜⬛⬜⬛⬜  (row 3)
        4 ⬜⬛⬜⬛⬜⬛⬜⬛  (row 4)
        3 ⬛⬜⬛⬜⬛⬜⬛⬜  (row 5)
        2 ⬜⬛⬜⬛⬜⬛⬜⬛  (row 6)
        1 ⬛⬜⬛⬜⬛⬜⬛⬜  (row 7)
    """

    # Ánh xạ từ vị trí hàng và cột sang vị trí hàng và cột (1 - 8)
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {}
    for k, v in ranksToRows.items():
        rowsToRanks[v] = k

    # Ánh xạ từ vị trí cột và hàng sang vị trí hàng và cột (a - h)
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {}
    for k, v in filesToCols.items():
        colsToFiles[v] = k

    def __init__(self, startSq, endSq, board, isEnpassantMove = False, isCastleMove = False):
        # Xác định hàng và cột của ô bắt đầu và ô kết thúc
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]

        # Xác định quân cờ di chuyển và quân cờ bị bắt
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]

        # Xác định quân tốt di chuyển đến cuối bàn cờ (để thực hiện thăng tốt)
        self.isPawnPromotion = (self.pieceMoved == 'wP' and self.endRow == 0) or (self.pieceMoved == 'bP' and self.endRow == 7)
            
        # Xác định nước đi bắt tốt qua đường
        self.isEnpassantMove = isEnpassantMove
        if self.isEnpassantMove:
            self.pieceCaptured = 'wP' if self.pieceMoved =='bP' else 'bP'

        # Xác định nước đi nhập thành
        self.isCastleMove = isCastleMove    

        self.isCapture = self.pieceCaptured != '--'
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):    
        return self.colsToFiles[c] + self.rowsToRanks[r]

    def __str__(self):
        if self.isCastleMove:
            return "O-O" if self.endCol == 6 else "O-O-O"
        
        endSquare = self.getRankFile(self.endRow, self.endCol)

        if self.pieceMoved[1] == 'P':
            if self.isCapture:
                return self.colsToFiles[self.startCol] + "x" + endSquare 
       
        moveString = self.pieceMoved[1]
        if self.isCapture:
            moveString += 'x'
        return moveString + endSquare

class GameState():
    def __init__(self):
        """
            Khởi tạo bàn cờ
                - Là bảng 8x8
                - Các quân cờ được đặt ở vị trí ban đầu
                - "--" là ô trống
                - "w" là quân trắng
                - "b" là quân đen
        """
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]

        self.moveFunctions = {
            'P': self.getPawnMoves, 
            'R': self.getRookMoves, 
            'N': self.getKnightMoves, 
            'B': self.getBishopMoves,
            'Q': self.getQueenMoves, 
            'K': self.getKingMoves
        }

        self.whiteToMove = True
        self.moveLog = []

        """
            Vị trí của vua
                - whiteKingLocation: Vị trí của vua trắng
                - blackKingLocation: Vị trí của vua đen
                - Kiểm tra vua có an toàn sau mỗi nước đi
                - Lấy tọa độ cho việc nhập thành
        """
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)

        # Kiểm tra chiếu hết
        self.checkMate = False

        # Kiểm tra hết cờ
        self.staleMate = False

        # Toạ độ của ô có thể thực hiện bắt tốt qua đường
        self.enpassantPossible = ()
        self.enpassantPossibleLog = [self.enpassantPossible]

        # Khởi tạo 1 trạng thái có thể nhập thành không của bàn cơ hiện tại
        self.currentCastlingRight = CastleRight(True, True, True, True)

        # Ghi lại lịch sử các trạng thái có thể nhập thành để phục vụ việc undo
        self.castleRightLog = [CastleRight(
            self.currentCastlingRight.wks, 
            self.currentCastlingRight.bks, 
            self.currentCastlingRight.wqs, 
            self.currentCastlingRight.bqs
        )]

    def makeMove(self, move):
        """
            Thực hiện nước đi
                - Di chuyển quân cờ từ ô bắt đầu đến ô kết thúc (Xóa quân cờ ở ô bắt đầu và thêm quân cờ ở ô kết thúc)
                - Thêm nước đi vào lịch sử
                - Đổi lượt đi
        """
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove

        # Cập nhập lại toạ độ của vua nếu vua di chuyển
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol) 

        # Nếu nước đi đó là nước thăng tốt
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'
        
        # Nếu nước đi đó là một nước đi qua đường
        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = '--'

        # Update biến enpassantPossible()
        if move.pieceMoved[1] == 'P' and abs(move.startRow - move.endRow) == 2:
            self.enpassantPossible = ((move.startRow + move.endRow) // 2, move.startCol)
        else:
            self.enpassantPossible = ()
        self.enpassantPossibleLog.append(self.enpassantPossible)

        # Nếu nước đi đó là nước nhập thành
        if move.isCastleMove:
            """
                Nhập thành ở hướng bên phải vua
                    - Di chuyển quân xe
                    - Xoá quân xe cũ
                    - Vị trí của quân xe mới là (endRow, endCol - 1)
                    - Vị trí của quân xe cũ là (endRow, endCol + 1)
                Nhập thành ở hướng bên trái vua
                    - Di chuyển quân xe
                    - Xoá quân xe cũ
                    - Vị trí của quân xe mới là (endRow, endCol + 1)
                    - Vị trí của quân xe cũ là (endRow, endCol - 2)
            """
            if move.isCastleMove:
                if move.endCol - move.startCol == 2:  # Nhập thành cánh vua (bên phải)
                    self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][move.endCol + 1]
                    self.board[move.endRow][move.endCol + 1] = '--'  # Xoá quân xe cũ
                elif move.endCol - move.startCol == -2:  # Nhập thành cánh hậu (bên trái)
                    self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.startCol - 4]  # Di chuyển xe
                    self.board[move.endRow][move.startCol - 4] = '--'  # Xoá vị trí cũ của xe


        # Cập nhập quyền nhập thành - khi nước đi là nước đi của xe hoặc của vua
        self.updateCastleRight(move)
        self.castleRightLog.append(CastleRight(
            self.currentCastlingRight.wks,
            self.currentCastlingRight.bks,
            self.currentCastlingRight.wqs,
            self.currentCastlingRight.bqs
        ))

    def undoMove(self):
        # Kiểm tra xem có nước đi để undo hay không
        if len(self.moveLog) == 0:
            return

        move = self.moveLog.pop()
        self.board[move.startRow][move.startCol] = move.pieceMoved
        self.board[move.endRow][move.endCol] = move.pieceCaptured
        self.whiteToMove = not self.whiteToMove

        # Cập nhật lại vị trí vua
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.startRow, move.startCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.startRow, move.startCol)

        # Cập nhật lại trạng thái đi qua đường
        if move.isEnpassantMove:
            self.board[move.endRow][move.endCol] = '--'
            self.board[move.startRow][move.endCol] = move.pieceCaptured

        # Kiểm tra trước khi pop để tránh lỗi rỗng danh sách
        if len(self.enpassantPossibleLog) > 1:
            self.enpassantPossibleLog.pop()
            self.enpassantPossible = self.enpassantPossibleLog[-1]
        else:
            self.enpassantPossible = None

        # Khôi phục lại trạng thái nhập thành đúng cách
        if len(self.castleRightLog) > 1:
            self.castleRightLog.pop()
        self.currentCastlingRight = self.castleRightLog[-1]  # Phải cập nhật ngay cả khi không pop

        # Hoàn tác nhập thành
        if move.isCastleMove:
            if move.endCol - move.startCol == 2:  
                # Nhập thành cánh vua (O-O)
                self.board[move.endRow][move.startCol + 3] = self.board[move.endRow][move.startCol + 1]  # Đưa quân xe về vị trí cũ
                self.board[move.endRow][move.startCol + 1] = '--'  # Xóa quân xe khỏi vị trí mới
            else:  
                # Nhập thành cánh hậu (O-O-O)
                self.board[move.endRow][move.startCol - 4] = self.board[move.endRow][move.startCol - 1]  # Đưa quân xe về vị trí cũ
                self.board[move.endRow][move.startCol - 1] = '--'  # Xóa quân xe khỏi vị trí mới
            if len(self.castleRightLog) > 1:
                self.castleRightLog.pop()
            self.currentCastlingRight = self.castleRightLog[-1] 

        self.checkMate = False
        self.staleMate = False

     # Cập nhập quyền nhập thành - khi nước đi là nước đi của xe hoặc của vua        
    def updateCastleRight(self, move):
        # Kiểm tra xem quân cờ di chuyển có phải là quân xe hay quân vua hay không
        if move.pieceMoved == 'wK':
            self.currentCastlingRight.wks = False
            self.currentCastlingRight.wqs = False
        elif move.pieceMoved == 'bK':
            self.currentCastlingRight.bks = False
            self.currentCastlingRight.bqs = False
        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 0:
                    self.currentCastlingRight.wqs = False
                elif move.startCol == 7:
                    self.currentCastlingRight.wks = False
        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 0:
                    self.currentCastlingRight.bqs = False
                elif move.startCol == 7:
                    self.currentCastlingRight.bks = False

        # Nếu quân bị bắt là quân xe
        if move.pieceCaptured == 'wR':
            if move.endRow == 7:
                if move.endCol == 0:
                    self.currentCastlingRight.wqs = False
                elif move.endCol == 7:
                    self.currentCastlingRight.wks = False
        elif move.pieceCaptured == 'bR':
            if move.endRow == 0:
                if move.endCol == 0:
                    self.currentCastlingRight.bqs = False
                elif move.endCol == 7:
                    self.currentCastlingRight.bks = False


    """
    các nước đi cần phải xem xét có ảnh hưởng đến vua không
    """
    def getValidMoves(self):
        tempEnpassant = self.enpassantPossible
        tempCastleRight = CastleRight(self.currentCastlingRight.wks, self.currentCastlingRight.bks, self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)
        # thuật toán để tìm các nước đi hợp lệ
        # 1) tạo ra tất cả các nước đi hợp lệ bất kể có ảnh hưởng đến vua hay không
        moves = self.getAllPossibleMoves()

        # tạo riêng các nước nhập thành để tránh bị đệ quy vô hạn
        if self.whiteToMove:
            self.getCastleMove(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
        else:
            self.getCastleMove(self.blackKingLocation[0], self.blackKingLocation[1], moves)

        # 2) với mỗi nước đi, thực hiện chúng
        for i in range(len(moves) - 1, -1, -1): # thực hiện một vòng for duyệt từ phần tử cuối đến phần tử đầu 
            self.makeMove(moves[i])
        # 3) với mỗi nước đi được thực hiện, tạo ra tất cả các nước đi của đối thủ
        # 4) với mỗi nước đi của đối thủ, kiểm tra xem họ có thể tấn công được vua của mình không
            # sau khi gọi đến phương thức makeMove, lượt đi sẽ được đổi cho đối thủ
            # vậy nên để có thể kiểm tra được các nước đi của đối thủ, ta cần đổi lại lượt chơi 1 lần nữa
            self.whiteToMove = not self.whiteToMove 
            if self.inCheck():
                # 5) nếu có, nước đi trc đó là nước đi không hợp lệ
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()

        if len(moves) == 0:
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        

        self.enpassantPossible = tempEnpassant
        self.currentCastlingRight = tempCastleRight
        return moves
    
    # hàm này kiểm tra xem vua của người chơi có đang bị chiếu không
    def inCheck(self):
        if self.whiteToMove:
            # nếu đang là lượt của quân trắng, kiểm tra xem sau lượt đi dó quân vua có thể bị tấn công không
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    # hàm này để kiểm tra  xem đổi thủ có thể tấn công ô vuông có toạ độ (r, c) không
    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove # chuyển sang lượt đi của đối thủ 
        oppMoves = self.getAllPossibleMoves() # lấy các lượt đi được của dối thủ
        self.whiteToMove = not self.whiteToMove # chuyển lại về lượt đi của bản thân để không gặp lỗi
        for move in oppMoves:
            if move.endRow == r and move.endCol == c: # có nghĩa là ô vuông đó có thể bị tấn công
                return True
        return False
                

    """
    các nước đi không cần xem xét
    """
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)
        return moves

    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:
            if self.board[r - 1][c] == "--":
                moves.append(Move((r, c), (r - 1, c), self.board))
                if r == 6 and self.board[r - 2][c] == "--":
                    moves.append(Move((r, c), (r - 2, c), self.board))
            if c - 1 >= 0:
                if self.board[r - 1][c - 1][0] == 'b': # có quân của kẻ thù để bắt ở bên trái
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
                elif (r - 1, c - 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r - 1, c - 1), self.board, isEnpassantMove=True))
            
            if c + 1 <= 7:
                if self.board[r - 1][c + 1][0] =='b': # có quân của kẻ thủ để bắt ở bên phải
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))
                elif (r - 1, c + 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r - 1, c + 1), self.board, isEnpassantMove=True)) 

        else:
            if self.board[r + 1][c] == "--":
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == "--":
                    moves.append(Move((r, c), (r + 2, c), self.board))
            if c - 1 >= 0:
                if self.board[r + 1][c - 1][0] == 'w': # có quân của kẻ thù để bắt ở bên trái
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
                elif (r + 1, c - 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r + 1, c - 1), self.board, isEnpassantMove=True))
            
            if c + 1 <= 7:
                if self.board[r + 1][c + 1][0] =='w': # có quân của kẻ thủ để bắt ở bên phải
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))
                elif (r + 1, c + 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r + 1, c + 1), self.board, isEnpassantMove=True))

    def getRookMoves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1)) #up, left, down, right
        enemyColor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1, 8): 
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--':
                        moves.append(Move((r, c), (endRow,endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow,endCol), self.board))
                        break
                    else:
                        break
                else:
                    break


    def getKnightMoves(self, r,c, moves):
        directions = ((-2, -1), (-2, 1), (-1, 2), (1, 2), (2, -1), (2, 1), (-1, -2), (1, -2))
        allyColor = 'w' if self.whiteToMove else 'b'
        for i in directions:
            endRow = r + i[0]
            endCol = c + i[1]
            if 0<= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, 1), (1, -1))
        enemyColor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--':
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break


    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    def getKingMoves(self,r,c,moves):
        directions = ((-1, -1), (1, 1), (-1, 1), (1, -1), (-1, 0), (1, 0), (0, -1), (0, 1))
        allyColor = 'w' if self.whiteToMove else 'b'
        for i in range(8):
            endRow = r + directions[i][0]
            endCol = c + directions[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow,endCol), self.board))
        
        #self.getCastleMove(r,c,moves)

    # tạo tất cả các nước đi nhập thành hợp lệ với (r,c) là vị trí của vua và thêm chúng vào danh sách các nước đi hợp lệ
    def getCastleMove(self, r, c, moves):
        if self.squareUnderAttack(r, c): # nếu vua đang bị chiếu
            return
        if (self.whiteToMove and self.currentCastlingRight.wks) or (not self.whiteToMove and self.currentCastlingRight.bks):
            self.getKingSideCastleMove(r, c, moves)
        if (self.whiteToMove and self.currentCastlingRight.wqs) or (not self.whiteToMove and self.currentCastlingRight.bqs):
            self.getQueenSideCastleMove(r, c, moves)
        
    # Thực hiện nước đi nhập thành ở hướng bên phải vua
    def getKingSideCastleMove(self, r, c, moves):
        if self.board[r][c + 1] == '--' and self.board[r][c + 2] == '--':
            if not self.squareUnderAttack(r, c + 1) and not self.squareUnderAttack(r, c + 2): # nếu 2 ô bên phải vua không trong trạng thái có thể bị tấn công
                moves.append(Move((r, c), (r, c + 2), self.board, isCastleMove = True))

    # Thực hiện nước đi nhập thành ở phía bên quân hậu (bên trái của vua)
    def getQueenSideCastleMove(self, r, c, moves):
        if self.board[r][c - 1] == '--' and self.board[r][c - 2] == '--' and self.board[r][c - 3] == '--':
            if not self.squareUnderAttack(r, c - 1) and not self.squareUnderAttack(r, c-2): # nếu 2 ô bên trái vua không trong trạng thái có thể bị tấn công
                moves.append(Move((r, c), (r, c - 2), self.board, isCastleMove = True))

class CastleRight():
    def __init__(self, wks, bks, wqs, bqs):
        """
            wks: nhập thành bên trắng ở hướng bên phải vua
            bks: nhập thành bên đen ở hướng bên phải vua
            wqs: nhập thành bên trắng ở hướng bên trái vua (quân hậu)
            bqs: nhập thành bên đen ở hướng bên trái vua (quân hậu)
        """
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs
