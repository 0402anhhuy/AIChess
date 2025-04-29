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
            - Kiểm tra xem vua của người chơi hiện tại có đang bị chiếu không.
            - Trả về True nếu vua bị đe dọa, False nếu an toàn.
        """
        if self.whiteToMove:
            # Đang là lượt của quân trắng: kiểm tra xem vua Trắng có bị tấn công hay không
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            # Đang là lượt của quân đen: kiểm tra xem vua Đen có bị tấn công hay không
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    # Hàm kiểm tra xem đổi thủ có thể tấn công ô vuông có toạ độ (r, c) không
    def squareUnderAttack(self, r, c):
        """
            - Kiểm tra xem ô (r, c) có đang bị đối thủ tấn công hay không.
            - Trả về True nếu có ít nhất 1 quân địch có thể đến ô đó, ngược lại False.
        """
        self.whiteToMove = not self.whiteToMove  # Chuyển lượt tạm thời sang đối thủ

        oppMoves = self.getAllPossibleMoves()    # Sinh tất cả nước đi của đối thủ

        self.whiteToMove = not self.whiteToMove  # Đổi lượt lại như cũ để tránh làm hỏng trạng thái

        for move in oppMoves:
            # Nếu bất kỳ nước đi nào của đối thủ kết thúc tại (r, c), tức là ô đó bị tấn công
            if move.endRow == r and move.endCol == c:
                return True

        # Nếu không quân nào nhắm vào ô (r, c), trả về False
        return False

                

    # Hàm tạo ra các nước đi cho mỗi quân cờ
    def getAllPossibleMoves(self):
        """
            - Sinh ra tất cả các nước đi có thể cho người chơi hiện tại (chưa kiểm tra chiếu).
        """
        moves = []  # Khởi tạo danh sách lưu nước đi

        # Duyệt từng ô trên bàn cờ 8x8
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]  # Lấy màu quân cờ ('w' hoặc 'b')

                # Chỉ xét quân cờ của bên đang đến lượt
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]  # Lấy loại quân cờ ('P', 'N', 'B', 'R', 'Q', 'K')

                    # Gọi hàm sinh nước đi tương ứng với quân cờ
                    self.moveFunctions[piece](r, c, moves)

        return moves  # Trả về danh sách các nước đi

    # Hàm thực hiện nước đi cho quân Tốt
    def getPawnMoves(self, r, c, moves):
        """
            - Sinh tất cả các nước đi hợp lệ cho quân Tốt (Pawn) tại vị trí (r, c).
            - Bao gồm đi thẳng, bắt chéo, đi 2 bước đầu tiên và bắt en passant.
        """
        if self.whiteToMove:
            # ĐI THẲNG: Tốt trắng đi lên phía trên (giảm hàng)
            if self.board[r - 1][c] == "--":  # Ô phía trước trống
                moves.append(Move((r, c), (r - 1, c), self.board))

                # Nếu tốt đang ở hàng 6 (vị trí ban đầu) và ô phía trước 2 ô trống
                if r == 6 and self.board[r - 2][c] == "--":
                    moves.append(Move((r, c), (r - 2, c), self.board))

            # BẮT TRÁI
            if c - 1 >= 0:
                if self.board[r - 1][c - 1][0] == 'b':  # Có quân đen bên trái
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
                elif (r - 1, c - 1) == self.enpassantPossible:  # En passant trái
                    moves.append(Move((r, c), (r - 1, c - 1), self.board, isEnpassantMove=True))

            # BẮT PHẢI
            if c + 1 <= 7:
                if self.board[r - 1][c + 1][0] == 'b':  # Có quân đen bên phải
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))
                elif (r - 1, c + 1) == self.enpassantPossible:  # En passant phải
                    moves.append(Move((r, c), (r - 1, c + 1), self.board, isEnpassantMove=True))

        else:
            # ĐI THẲNG: Tốt đen đi xuống phía dưới (tăng hàng)
            if self.board[r + 1][c] == "--":  # Ô phía trước trống
                moves.append(Move((r, c), (r + 1, c), self.board))

                # Nếu tốt đang ở hàng 1 và ô phía trước 2 ô trống
                if r == 1 and self.board[r + 2][c] == "--":
                    moves.append(Move((r, c), (r + 2, c), self.board))

            # BẮT TRÁI
            if c - 1 >= 0:
                if self.board[r + 1][c - 1][0] == 'w':  # Có quân trắng bên trái
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
                elif (r + 1, c - 1) == self.enpassantPossible:  # En passant trái
                    moves.append(Move((r, c), (r + 1, c - 1), self.board, isEnpassantMove=True))

            # BẮT PHẢI
            if c + 1 <= 7:
                if self.board[r + 1][c + 1][0] == 'w':  # Có quân trắng bên phải
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))
                elif (r + 1, c + 1) == self.enpassantPossible:  # En passant phải
                    moves.append(Move((r, c), (r + 1, c + 1), self.board, isEnpassantMove=True))
    
    # Hàm thực hiện nước đi cho quân Xe
    def getRookMoves(self, r, c, moves):
        """
            - Sinh tất cả các nước đi hợp lệ cho quân Xe (Rook) tại vị trí (r, c).
            - Xe đi theo 4 hướng: lên, xuống, trái, phải cho đến khi gặp vật cản.
        """
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))  # Hướng: lên, trái, xuống, phải
        enemyColor = 'b' if self.whiteToMove else 'w'    # Màu của quân địch (người đối diện)

        for d in directions:
            for i in range(1, 8):  # Rook có thể đi tối đa 7 ô theo mỗi hướng
                endRow = r + d[0] * i
                endCol = c + d[1] * i

                # Kiểm tra xem ô đích có nằm trong bàn cờ không
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]

                    if endPiece == '--':  # Ô trống → có thể đi
                        moves.append(Move((r, c), (endRow, endCol), self.board))

                    elif endPiece[0] == enemyColor:  # Gặp quân địch → có thể bắt, rồi dừng
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break

                    else:  # Gặp quân mình → không được đi, dừng lại
                        break
                else:
                    break  # Ra ngoài bàn cờ → dừng

    # Hàm thực hiện nước đi cho quân Mã
    def getKnightMoves(self, r, c, moves):
        """
            - Sinh tất cả các nước đi hợp lệ cho quân Mã (Knight) tại vị trí (r, c).
            - Mã di chuyển theo hình chữ L: 2 ô theo một hướng và 1 ô theo hướng vuông góc.
        """
        directions = ((-2, -1), (-2, 1), (-1, 2), (1, 2), (2, -1), (2, 1), (-1, -2), (1, -2))  # 8 hướng có thể đi

        allyColor = 'w' if self.whiteToMove else 'b'  # Màu quân mình (không được ăn)

        for d in directions:
            endRow = r + d[0]
            endCol = c + d[1]

            # Kiểm tra nước đi có nằm trong bàn cờ không
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]

                # Nếu ô trống hoặc có quân địch → thêm nước đi
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    # Hàm thực hiện nước đi cho quân Tượng
    def getBishopMoves(self, r, c, moves):
        """
            - Sinh tất cả các nước đi hợp lệ cho quân Tượng (Bishop) tại vị trí (r, c).
            - Tượng đi chéo theo 4 hướng cho đến khi gặp vật cản.
        """
        directions = ((-1, -1), (-1, 1), (1, 1), (1, -1))  # 4 hướng đi chéo: trái trên, phải trên, phải dưới, trái dưới
        enemyColor = 'b' if self.whiteToMove else 'w'      # Xác định màu quân địch

        for d in directions:
            for i in range(1, 8):  # Bishop có thể đi xa tối đa 7 ô theo mỗi hướng
                endRow = r + d[0] * i
                endCol = c + d[1] * i

                # Kiểm tra xem ô đến có nằm trong bàn cờ không
                if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                    endPiece = self.board[endRow][endCol]

                    if endPiece == '--':  # Ô trống → có thể đi tiếp
                        moves.append(Move((r, c), (endRow, endCol), self.board))

                    elif endPiece[0] == enemyColor:  # Gặp quân địch → có thể bắt rồi dừng
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break

                    else:  # Gặp quân ta → không đi tiếp được
                        break
                else:
                    break  # Ra ngoài bàn cờ → dừng

    # Hàm thực nhiện nước đi cho quân Hậu
    def getQueenMoves(self, r, c, moves):
        """
            - Sinh tất cả các nước đi hợp lệ cho quân Hậu (Queen) tại vị trí (r, c).
            - Hậu kết hợp cách đi của cả Xe (Rook) và Tượng (Bishop): đi ngang, dọc và chéo.
        """
        self.getRookMoves(r, c, moves)   # Gọi hàm của Rook để thêm các nước đi theo hàng và cột
        self.getBishopMoves(r, c, moves) # Gọi hàm của Bishop để thêm các nước đi theo đường chéo

    # Hàm thực hiện nước đi cho quân Vua
    def getKingMoves(self, r, c, moves):
        """
            - Sinh tất cả các nước đi hợp lệ cho quân Vua (King) tại vị trí (r, c).
            - Vua đi được 1 ô theo mọi hướng: ngang, dọc, chéo.
        """
        directions = ((-1, -1), (1, 1), (-1, 1), (1, -1),
                    (-1, 0), (1, 0), (0, -1), (0, 1))  # 8 hướng xung quanh vua

        allyColor = 'w' if self.whiteToMove else 'b'  # Xác định màu quân đồng minh

        for i in range(8):
            endRow = r + directions[i][0]
            endCol = c + directions[i][1]

            # Kiểm tra xem ô đến có nằm trong bàn cờ không
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]

                # Nếu ô đích trống hoặc có quân địch → hợp lệ
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))

        # Bỏ qua nhập thành tại đây, sẽ xử lý riêng trong getCastleMove()
        self.getCastleMove(r, c, moves)

    # Tạo tất cả các nước đi nhập thành hợp lệ với (r, c) là vị trí của vua và thêm chúng vào danh sách các nước đi hợp lệ
    def getCastleMove(self, r, c, moves):
        """
            Kiểm tra các điều kiện nhập thành (castling) và thêm nước đi nhập thành hợp lệ nếu có:
                - Vua không bị chiếu
                - Các ô giữa vua và xe trống
                - Các ô vua đi qua không bị tấn công
                - Xe và vua chưa từng di chuyển (được kiểm soát qua quyền nhập thành)
        """
        if self.squareUnderAttack(r, c):  # Nếu vua đang bị chiếu → không được nhập thành
            return

        # Nhập thành cánh vua (bên phải)
        if (self.whiteToMove and self.currentCastlingRight.wks) or \
        (not self.whiteToMove and self.currentCastlingRight.bks):
            self.getKingSideCastleMove(r, c, moves)

        # Nhập thành cánh hậu (bên trái)
        if (self.whiteToMove and self.currentCastlingRight.wqs) or \
        (not self.whiteToMove and self.currentCastlingRight.bqs):
            self.getQueenSideCastleMove(r, c, moves)


    def getKingSideCastleMove(self, r, c, moves):
        """
            Thêm nước đi nhập thành cánh vua (O-O) nếu hợp lệ:
                - 2 ô bên phải vua trống
                - Các ô đó không bị tấn công
                - Quyền nhập thành bên vua vẫn còn
        """
        if self.board[r][c + 1] == '--' and self.board[r][c + 2] == '--':  # Kiểm tra ô trống giữa vua và xe
            if not self.squareUnderAttack(r, c + 1) and not self.squareUnderAttack(r, c + 2):
                moves.append(Move((r, c), (r, c + 2), self.board, isCastleMove=True))


    def getQueenSideCastleMove(self, r, c, moves):
        """
            Thêm nước đi nhập thành cánh hậu (O-O-O) nếu hợp lệ:
                - 3 ô bên trái vua trống
                - 2 ô vua sẽ đi qua không bị tấn công
                - Quyền nhập thành bên hậu vẫn còn
        """
        if self.board[r][c - 1] == '--' and self.board[r][c - 2] == '--' and self.board[r][c - 3] == '--':
            if not self.squareUnderAttack(r, c - 1) and not self.squareUnderAttack(r, c - 2):
                moves.append(Move((r, c), (r, c - 2), self.board, isCastleMove=True))

class CastleRight():
    def __init__(self, wks, bks, wqs, bqs):
        """
            - wks: nhập thành bên trắng ở hướng bên phải vua
            - bks: nhập thành bên đen ở hướng bên phải vua
            - wqs: nhập thành bên trắng ở hướng bên trái vua (quân hậu)
            - bqs: nhập thành bên đen ở hướng bên trái vua (quân hậu)
        """
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs
