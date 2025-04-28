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

        # Xác định quân có bị bắt hay không
        self.isCapture = self.pieceCaptured != '--'
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    # Trả về ký hiệu cờ vua cho nước đi (VD: e2e4,...)
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):    
        return self.colsToFiles[c] + self.rowsToRanks[r]

    # Hàm trả về ký hiệu cờ vua cho nước đi
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

        # Kiểm tra hết cờ (hòa cờ)
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

    # Hàm để thực hiện nước đi
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

        # Cập nhật biến enpassantPossible()
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


        # Cập nhật quyền nhập thành - khi nước đi là nước đi của xe hoặc của vua
        self.updateCastleRight(move)
        self.castleRightLog.append(CastleRight(
            self.currentCastlingRight.wks,
            self.currentCastlingRight.bks,
            self.currentCastlingRight.wqs,
            self.currentCastlingRight.bqs
        ))

    # Hàm hoàn tác lại nước đi
    def undoMove(self):
        """
            Hoàn tác nước đi gần nhất:
                - Phục hồi bàn cờ
                - Phục hồi lượt đi
                - Phục hồi vị trí vua (nếu vua đã di chuyển)
                - Phục hồi trạng thái en passant
                - Phục hồi quyền nhập thành
                - Phục hồi nước đi nhập thành (nếu có)
                - Reset trạng thái chiếu hết/hòa
        """

        # Không có nước đi nào để undo
        if len(self.moveLog) == 0:
            return  

        # Lấy nước đi cuối cùng ra
        move = self.moveLog.pop()  

        # Phục hồi quân cờ
        self.board[move.startRow][move.startCol] = move.pieceMoved
        self.board[move.endRow][move.endCol] = move.pieceCaptured

        # Đổi lại lượt đi
        self.whiteToMove = not self.whiteToMove

        # Phục hồi vị trí vua (nếu vua di chuyển)
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.startRow, move.startCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.startRow, move.startCol)

        # Hoàn tác en passant
        if move.isEnpassantMove:
            self.board[move.endRow][move.endCol] = '--'  # Xóa quân tốt "ảo" do en passant
            self.board[move.startRow][move.endCol] = move.pieceCaptured  # Đặt lại quân tốt bị bắt

        # Phục hồi trạng thái en passant có thể
        if len(self.enpassantPossibleLog) > 0:
            self.enpassantPossible = self.enpassantPossibleLog.pop()
        else:
            self.enpassantPossible = None

        # Phục hồi quyền nhập thành
        if len(self.castleRightLog) > 0:
            self.currentCastlingRight = self.castleRightLog.pop()

        # Hoàn tác nước nhập thành nếu có
        if move.isCastleMove:
            if move.endCol - move.startCol == 2:  # Nhập thành cánh vua
                self.board[move.endRow][move.startCol + 3] = self.board[move.endRow][move.startCol + 1]  # Xe quay về
                self.board[move.endRow][move.startCol + 1] = '--'  # Xóa vị trí mới
            elif move.endCol - move.startCol == -2:  # Nhập thành cánh hậu
                self.board[move.endRow][move.startCol - 4] = self.board[move.endRow][move.startCol - 1]
                self.board[move.endRow][move.startCol - 1] = '--'

        # Reset cờ chiếu hết/hòa về False (vì undo về trước đó)
        self.checkMate = False
        self.staleMate = False


    # Cập nhập quyền nhập thành - khi nước đi là nước đi của xe hoặc của vua        
    def updateCastleRight(self, move):
        """
        Cập nhật quyền nhập thành (castle rights) sau khi thực hiện nước đi.
        - Nếu vua di chuyển: mất cả 2 quyền nhập thành.
        - Nếu xe di chuyển: mất quyền nhập thành tương ứng.
        - Nếu xe bị bắt: mất quyền nhập thành tương ứng.
        """

        # Kiểm tra xem quân di chuyển có phải và vua hay không
        if move.pieceMoved == 'wK':
            self.currentCastlingRight.wks = False  # Mất quyền nhập thành cánh vua trắng
            self.currentCastlingRight.wqs = False  # Mất quyền nhập thành cánh hậu trắng
        elif move.pieceMoved == 'bK':
            self.currentCastlingRight.bks = False  # Mất quyền nhập thành cánh vua đen
            self.currentCastlingRight.bqs = False  # Mất quyền nhập thành cánh hậu đen

        # Kiểm tra xem quân di chuyển có phải là xe hay không
        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 0:
                    self.currentCastlingRight.wqs = False  # Xe cánh hậu trắng di chuyển -> mất quyền
                elif move.startCol == 7:
                    self.currentCastlingRight.wks = False  # Xe cánh vua trắng di chuyển -> mất quyền
        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 0:
                    self.currentCastlingRight.bqs = False  # Xe cánh hậu đen di chuyển -> mất quyền
                elif move.startCol == 7:
                    self.currentCastlingRight.bks = False  # Xe cánh vua đen di chuyển -> mất quyền

        # Kiểm tra xem quân bị bắt có phải là xe hay không
        if move.pieceCaptured == 'wR':
            if move.endRow == 7:
                if move.endCol == 0:
                    self.currentCastlingRight.wqs = False  # Xe cánh hậu trắng bị bắt -> mất quyền
                elif move.endCol == 7:
                    self.currentCastlingRight.wks = False  # Xe cánh vua trắng bị bắt -> mất quyền
        elif move.pieceCaptured == 'bR':
            if move.endRow == 0:
                if move.endCol == 0:
                    self.currentCastlingRight.bqs = False  # Xe cánh hậu đen bị bắt -> mất quyền
                elif move.endCol == 7:
                    self.currentCastlingRight.bks = False  # Xe cánh vua đen bị bắt -> mất quyền



    # Các nước đi cần phải xem xét có ảnh hưởng đến vua không
    def getValidMoves(self):
        """
            - Trả về danh sách tất cả các nước đi hợp lệ cho người chơi hiện tại (hoặc AI).
            - Không thay đổi giao diện gọi hàm, trả danh sách nước đi của toàn bộ bàn cờ.
        """

        # 1. Lưu trạng thái ban đầu
        tempEnpassant = self.enpassantPossible
        tempCastleRight = CastleRight(
            self.currentCastlingRight.wks,
            self.currentCastlingRight.bks,
            self.currentCastlingRight.wqs,
            self.currentCastlingRight.bqs
        )

        # 2. Sinh ra tất cả các nước đi không quan tâm vua bị chiếu hay không
        moves = self.getAllPossibleMoves()

        # 3. Thêm các nước nhập thành (nếu có)
        if self.whiteToMove:
            self.getCastleMove(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
        else:
            self.getCastleMove(self.blackKingLocation[0], self.blackKingLocation[1], moves)

        # 4. Lọc các nước đi khiến vua bị chiếu
        for i in range(len(moves) - 1, -1, -1):
            self.makeMove(moves[i])
            self.whiteToMove = not self.whiteToMove

            if self.inCheck():
                moves.remove(moves[i])

            self.whiteToMove = not self.whiteToMove
            self.undoMove()

        # 5. Kiểm tra chiếu hết hoặc hòa
        if len(moves) == 0:
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True

        # 6. Phục hồi trạng thái
        self.enpassantPossible = tempEnpassant
        self.currentCastlingRight = tempCastleRight

        return moves
    
    # Hàm kiểm tra xem vua có đang bị chiếu hay không
    def inCheck(self):
        """
        Kiểm tra xem vua của người chơi hiện tại có đang bị chiếu không.
        Trả về True nếu vua bị đe dọa, False nếu an toàn.
        """
        if self.whiteToMove:
            # Đang là lượt của Trắng: kiểm tra xem vua Trắng có bị tấn công hay không
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            # Đang là lượt của Đen: kiểm tra xem vua Đen có bị tấn công hay không
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
