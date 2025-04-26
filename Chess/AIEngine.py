import random
import ChessEngine as CE

pieceScore ={"K": 0, "Q": 10, "R": 5, "B": 3, "N": 3, "P": 1}
transpositionTable = {}

knightScores = [[1, 1, 1, 1, 1, 1, 1, 1],
                [1, 2, 2, 2, 2, 2, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 2, 2, 2, 2, 2, 1],
                [1, 1, 1, 1, 1, 1, 1, 1]]

bishopScores = [[4, 3, 2, 1, 1, 2, 3, 4],
                [3, 4, 3, 2, 2, 3, 4, 3],
                [2, 3, 4, 3, 3, 4, 3, 2],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [2, 3, 4, 3, 3, 4, 3, 2],
                [3, 4, 3, 2, 2, 3, 4, 3],
                [4, 3, 2, 1, 1, 2, 3, 4]]

queenScores =  [[1, 1, 1, 3, 1, 1, 1, 1],
                [1, 2, 3, 3, 3, 1, 1, 1],
                [1, 4, 3, 3, 3, 4, 2, 1],
                [1, 2, 3, 3, 3, 2, 2, 1],
                [1, 2, 3, 3, 3, 2, 2, 1],
                [1, 4, 3, 3, 3, 4, 2, 1],
                [1, 1, 2, 3, 3, 1, 1, 1],
                [1, 1, 1, 3, 1, 1, 1, 1]]

rookScores =   [[4, 3, 4, 4, 4, 4, 3, 4],
                [4, 4, 4, 4, 4, 4, 4, 4],
                [1, 1, 2, 3, 3, 2, 1, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 1, 2, 3, 3, 2, 1, 1],
                [4, 4, 4, 4, 4, 4, 4, 4],
                [4, 3, 4, 4, 4, 4, 3, 4]]

whitePawnScores = [ [8, 8, 8, 8, 8, 8, 8, 8],
                    [8, 8, 8, 8, 8, 8, 8, 8],
                    [5, 6, 6, 7, 7, 6, 6, 5],
                    [2, 3, 3, 5, 5, 3, 3, 2],
                    [1, 2, 3, 4, 4, 3, 2, 1],
                    [1, 1, 2, 3, 3, 2, 1, 1],
                    [1, 1, 1, 0, 0, 1, 1, 1],
                    [0, 0, 0, 0, 0, 0, 0, 0]]

blackPawnScores = [ [0, 0, 0, 0, 0, 0, 0, 0],
                    [1, 1, 1, 0, 0, 1, 1, 1],
                    [1, 1, 2, 3, 3, 2, 1, 1],
                    [1, 2, 3, 4, 4, 3, 2, 1],
                    [2, 3, 3, 5, 5, 3, 3, 2],
                    [5, 6, 6, 7, 7, 6, 6, 5],
                    [8, 8, 8, 8, 8, 8, 8, 8],
                    [8, 8, 8, 8, 8, 8, 8, 8]]

piecePositionScores = {"N": knightScores, "Q": queenScores, "B": bishopScores, "R": rookScores, "bP": blackPawnScores, "wP": whitePawnScores}

CHECKMATE = 1000
STALEMATE = 0
DEPTH = 2

def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]

def findBestMove(gs, validMoves):
    global nextMove
    tempCastleRight = CE.CastleRight(gs.currentCastlingRight.wks, gs.currentCastlingRight.bks, gs.currentCastlingRight.wqs, gs.currentCastlingRight.bqs)
    nextMove = None
    validMoves = moveOrdering(gs, validMoves)
    findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE,  CHECKMATE, 1 if gs.whiteToMove else -1)
    gs.currentCastlingRight = tempCastleRight
    return nextMove      

def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove

    boardKey = str(gs.board)
    if boardKey in transpositionTable and transpositionTable[boardKey][0] >= depth:
        return transpositionTable[boardKey][1]

    if depth == 0:
        return turnMultiplier * scoreBoard(gs)

    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        nextMoves = moveOrdering(gs, nextMoves)
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier)
        gs.undoMove()

        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move

        alpha = max(alpha, maxScore)
        if alpha >= beta:
            break

    transpositionTable[boardKey] = (depth, maxScore)

    return maxScore


def scoreBoard(gs):
    if gs.checkMate:
        if gs.whiteToMove:
            return -CHECKMATE
        else:
            return CHECKMATE
    score = 0
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            if square != '--':
                piecePositionScore = 0
                if square[1] != "K":
                    if square[1] == 'P':
                        piecePositionScore = piecePositionScores[square][row][col]
                    else:    
                        piecePositionScore = piecePositionScores[square[1]][row][col]
                if square[0] == 'w':
                    score += pieceScore[square[1]] + piecePositionScore * 0.1
                elif square[0] == 'b':
                    score -= (pieceScore[square[1]] + piecePositionScore * 0.1)
    return score

def moveOrdering(gs, validMoves):
    # Tạo một danh sách để lưu trữ điểm số cho mỗi nước đi
    moveScores = []
    winningCapture = 0.8
    losingCapture = 0.2

    # Tính toán điểm số cho mỗi nước đi
    for move in validMoves:
        gs.makeMove(move)
        # Điểm số cơ bản dựa trên bảng điểm hiện tại
        score = scoreBoard(gs)
        gs.undoMove()

        # Thêm điểm thưởng hoặc phạt dựa trên các yếu tố khác
        if move.isCapture:
        
            score += pieceScore[move.pieceCaptured[1]]
        if move.isPawnPromotion:
            # Thêm điểm nếu là nước thăng cấp
            score += 1  # Giả sử thăng cấp được 1 điểm thưởng

        moveScores.append(score)

    # Sắp xếp các nước đi dựa trên điểm số, từ cao xuống thấp
    sortedMoves = [move for _, move in sorted(zip(moveScores, validMoves), key=lambda pair: pair[0], reverse=True)]

    return sortedMoves

def isMoveSafe(gs, move):
    """
    Kiểm tra xem sau khi thực hiện nước đi, quân cờ có an toàn không.
    """
    gs.makeMove(move)  # Thực hiện nước đi
    opponent_moves = gs.getValidMoves()  # Lấy tất cả nước đi hợp lệ của đối thủ
    gs.undoMove()  # Hoàn tác nước đi để không thay đổi trạng thái bàn cờ

    for opp_move in opponent_moves:
        if opp_move.endRow == move.endRow and opp_move.endCol == move.endCol:
            return False  # Nếu có nước đi của đối thủ ăn được quân cờ tại vị trí mới, nước đi không an toàn

    return True  # Nếu không có nước đi nào của đối thủ ăn được quân cờ, nước đi an toàn