import time
import random
import ChessEngine as CE  # Import mô-đun logic cờ vua chứa GameState, Move, v.v.

# Điểm cơ bản cho từng loại quân cờ
pieceScore = {
    "K": 0,  # Vua không cho điểm (chiếu hết mới quan trọng)
    "Q": 10, # Hậu
    "R": 5,  # Xe
    "B": 3,  # Tượng
    "N": 3,  # Mã
    "P": 1   # Tốt
}

# Bảng bố trợ ghi nhớ trạng thái đã được duyệt (dùng cho AI)
transpositionTable = {}

# Điểm vị trí của Mã trên bàn cờ (càng vào trung tâm càng tốt)
knightScores = [[1, 1, 1, 1, 1, 1, 1, 1],
                [1, 2, 2, 2, 2, 2, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 2, 2, 2, 2, 2, 1],
                [1, 1, 1, 1, 1, 1, 1, 1]]

# Điểm vị trí của Tượng (trên 2 đường chéo càng chính càng tốt)
bishopScores = [[4, 3, 2, 1, 1, 2, 3, 4],
                [3, 4, 3, 2, 2, 3, 4, 3],
                [2, 3, 4, 3, 3, 4, 3, 2],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [2, 3, 4, 3, 3, 4, 3, 2],
                [3, 4, 3, 2, 2, 3, 4, 3],
                [4, 3, 2, 1, 1, 2, 3, 4]]

# Điểm vị trí của Hậu
queenScores = [[1, 1, 1, 3, 1, 1, 1, 1],
               [1, 2, 3, 3, 3, 1, 1, 1],
               [1, 4, 3, 3, 3, 4, 2, 1],
               [1, 2, 3, 3, 3, 2, 2, 1],
               [1, 2, 3, 3, 3, 2, 2, 1],
               [1, 4, 3, 3, 3, 4, 2, 1],
               [1, 1, 2, 3, 3, 1, 1, 1],
               [1, 1, 1, 3, 1, 1, 1, 1]]

# Điểm vị trí của Xe
rookScores = [[4, 3, 4, 4, 4, 4, 3, 4],
              [4, 4, 4, 4, 4, 4, 4, 4],
              [1, 1, 2, 3, 3, 2, 1, 1],
              [1, 2, 3, 4, 4, 3, 2, 1],
              [1, 2, 3, 4, 4, 3, 2, 1],
              [1, 1, 2, 3, 3, 2, 1, 1],
              [4, 4, 4, 4, 4, 4, 4, 4],
              [4, 3, 4, 4, 4, 4, 3, 4]]

# Điểm vị trí của Tốt trắng
whitePawnScores = [[8, 8, 8, 8, 8, 8, 8, 8],
                   [8, 8, 8, 8, 8, 8, 8, 8],
                   [5, 6, 6, 7, 7, 6, 6, 5],
                   [2, 3, 3, 5, 5, 3, 3, 2],
                   [1, 2, 3, 4, 4, 3, 2, 1],
                   [1, 1, 2, 3, 3, 2, 1, 1],
                   [1, 1, 1, 0, 0, 1, 1, 1],
                   [0, 0, 0, 0, 0, 0, 0, 0]]

# Điểm vị trí của Tốt đen (ngược lại tốt trắng)
blackPawnScores = [[0, 0, 0, 0, 0, 0, 0, 0],
                   [1, 1, 1, 0, 0, 1, 1, 1],
                   [1, 1, 2, 3, 3, 2, 1, 1],
                   [1, 2, 3, 4, 4, 3, 2, 1],
                   [2, 3, 3, 5, 5, 3, 3, 2],
                   [5, 6, 6, 7, 7, 6, 6, 5],
                   [8, 8, 8, 8, 8, 8, 8, 8],
                   [8, 8, 8, 8, 8, 8, 8, 8]]

# Bảng chỉ số điểm theo vị trí cho từng loại quân cờ (bao gồm tốt trắng/đen)
piecePositionScores = {
    "N": knightScores,
    "Q": queenScores,
    "B": bishopScores,
    "R": rookScores,
    "bP": blackPawnScores,  # Tốt đen
    "wP": whitePawnScores   # Tốt trắng
}

# Hằng số điểm cho chiếu hết và hòa
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 3  # Mặc định, sẽ điều chỉnh linh hoạt khi tìm nước đi

# Hàm thực hiện tìm nước đi ngẫu nhiên trong danh sách validMoves
def findRandomMove(validMoves):
    """
        - Trả về một nước đi ngẫu nhiên trong danh sách validMoves.
        - Dùng khi cần bot chơi ngẫu nhiên hoặc dùng test nhanh.
    """
    return validMoves[random.randint(0, len(validMoves) - 1)]

# Hàm tìm nước đi tốt nhất cho bot chơi cờ vua
def findBestMove(gs, validMoves):
    """
        - Tìm nước đi tốt nhất dựa theo thuật toán NegaMax + AlphaBeta pruning.
        - gs: Đối tượng GameState (bản cờ hiện tại)
        - validMoves: Danh sách các nước đi hợp lệ
    
        - Gợi ra biến nextMove được chọn trong giá trị toàn cục nhất.
    """
    global nextMove  # Biến lưu nước đi tốt nhất tạm thời

    # Lưu lại quyền nhập thành trước khi giả lập nước đi (tránh bị thay đổi khi undo)
    tempCastleRight = CE.CastleRight(
        gs.currentCastlingRight.wks,
        gs.currentCastlingRight.bks,
        gs.currentCastlingRight.wqs,
        gs.currentCastlingRight.bqs
    )

    nextMove = None  # Reset trạng thái nước tốt nhất
    validMoves = moveOrdering(gs, validMoves)  # Sắp xếp nước đi (gợi ý để pruning tốt hơn)

    # Gọi thuật toán NegaMax với Alpha-Beta pruning
    findMoveNegaMaxAlphaBeta(
        gs,
        validMoves,
        DEPTH,               # Chiều sâu tìm kiếm
        -CHECKMATE,          # Alpha khởi đầu
        CHECKMATE,           # Beta khởi đầu
        1 if gs.whiteToMove else -1  # Màu đang đi (trắng: 1, đen: -1)
    )

    gs.currentCastlingRight = tempCastleRight  # Khôi phục lại quyền nhập thành
    return nextMove  # Trả về nước đi tốt nhất tìm được
    
# Hàm tìm nước đi tốt nhất bằng thuật toán NegaMax với Alpha-Beta pruning
def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    # Sử dụng thuật toán NegaMax với cắt tỉa Alpha-Beta để tìm nước đi tốt nhất
    global nextMove

    boardKey = str(gs.board)  # Dùng string biểu diễn bàn cờ làm khóa lưu trong bảng ghi nhớ

    # Dùng bảng ghi nhớ để tránh tính lại nếu đã duyệt trạng thái này với độ sâu lớn hơn hoặc bằng
    if boardKey in transpositionTable and transpositionTable[boardKey][0] >= depth:
        return transpositionTable[boardKey][1]  # Trả lại điểm đã tính trước

    # Trường hợp cơ sở: nếu độ sâu bằng 0 thì đánh giá bàn cờ hiện tại
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)

    maxScore = -CHECKMATE  # Khởi tạo điểm lớn nhất với giá trị âm vô cùng

    for move in validMoves:
        gs.makeMove(move)  # Thực hiện nước đi giả lập
        nextMoves = gs.getValidMoves()  # Lấy các nước đi tiếp theo của đối thủ
        nextMoves = moveOrdering(gs, nextMoves)  # Sắp xếp thứ tự nước đi để tối ưu hóa

        # Gọi đệ quy NegaMax với lượt của đối thủ và chiều sâu giảm 1
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier)

        gs.undoMove()  # Hoàn tác nước đi giả lập

        # Nếu điểm vừa tìm được lớn hơn điểm lớn nhất hiện tại thì cập nhật
        if score > maxScore:
            maxScore = score
            if depth == DEPTH or depth >= 3:
                nextMove = move  # Ghi nhận nước đi tốt nhất ở mức gốc (top-level)

        alpha = max(alpha, maxScore)  # Cập nhật alpha
        if alpha >= beta:  # Cắt tỉa nếu không còn hy vọng tìm điểm tốt hơn
            break

    # Lưu trạng thái vào bảng ghi nhớ để tái sử dụng sau này
    transpositionTable[boardKey] = (depth, maxScore)

    return maxScore  # Trả về điểm đánh giá tốt nhất tại node này

# Hàm đánh giá bàn cờ hiện tại
def scoreBoard(gs):
    """
        Đánh giá trạng thái bàn cờ hiện tại:
            - Dựa vào điểm quân cờ (pieceScore)
            - Dựa vào vị trí quân cờ (piecePositionScores)
            - Nếu chiếu hết thì trả về điểm tuyệt đối (CHECKMATE)
    """
    if gs.checkMate:
        if gs.whiteToMove:
            return -CHECKMATE  # Trắng bị chiếu hết => thua
        else:
            return CHECKMATE   # Đen bị chiếu hết => thua

    score = 0  # Khởi tạo tổng điểm

    # Duyệt toàn bộ bàn cờ
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            if square != '--':
                piecePositionScore = 0  # Điểm vị trí ban đầu

                if square[1] != "K":  # Không tính điểm vị trí cho vua
                    if square[1] == 'P':  # Nếu là tốt thì cần phân biệt trắng / đen
                        piecePositionScore = piecePositionScores[square][row][col]
                    else:
                        piecePositionScore = piecePositionScores[square[1]][row][col]

                # Cộng hoặc trừ điểm tuỳ theo màu quân cờ
                if square[0] == 'w':
                    score += pieceScore[square[1]] + piecePositionScore * 0.1
                elif square[0] == 'b':
                    score -= pieceScore[square[1]] + piecePositionScore * 0.1

    return score  # Trả về điểm đánh giá cuối cùng

# Hàm sắp xếp thứ tự nước đi dựa trên điểm số
def moveOrdering(gs, validMoves):
    """
        - Sắp xếp thứ tự nước đi dựa trên giá trị chiến lược để tối ưu hóa thuật toán alpha-beta.
        - Ưu tiên: bắt quân mạnh, thăng cấp, nước đi trung tâm, nước đi chiếu vua, ép vua vào góc, phòng thủ khỏi chiếu.
    """
    moveScores = []
    
    for move in validMoves:
        score = 0

        # Ưu tiên thăng cấp tốt
        if move.isPawnPromotion:
            score += 90

        # Ưu tiên bắt quân đắt giá hơn (MVV-LVA)
        if move.isCapture:
            score += 10 * pieceScore[move.pieceCaptured[1]] - pieceScore[move.pieceMoved[1]]

        # Ưu tiên đi gần trung tâm
        centerSquares = {(3, 3), (3, 4), (4, 3), (4, 4)}
        if (move.endRow, move.endCol) in centerSquares:
            score += 3

        # Ưu tiên mở quân hàng đầu
        if (move.startRow, move.startCol) in [(1, i) for i in range(8)] + [(6, i) for i in range(8)]:
            score += 1

        # Giả lập nước đi để đánh giá thêm
        wasInCheck = gs.inCheck()  # Kiểm tra trước khi đi có bị chiếu không
        gs.makeMove(move)

        # Nếu sau khi đi, đối phương bị chiếu → tăng điểm
        if gs.inCheck():
            score += 20

        # Nếu trước khi đi bị chiếu và nước đi giúp thoát chiếu → tăng điểm phòng thủ
        if wasInCheck and not gs.inCheck():
            # Nếu không phải chạy vua mà là chặn/bắt thì càng tốt
            if move.pieceMoved[1] != 'K':
                score += 12
            else:
                score += 5  # Nếu là chạy vua, cộng ít hơn

        # Chiến thuật ép vua về góc nếu đối thủ chỉ còn vua
        enemyKingOnly = all(
            piece == '--' or piece[1] == 'K' or (piece[0] == ('w' if gs.whiteToMove else 'b'))
            for row in gs.board for piece in row
        )
        if enemyKingOnly:
            oppKingPos = gs.blackKingLocation if gs.whiteToMove else gs.whiteKingLocation
            if oppKingPos[0] in {0, 7} and oppKingPos[1] in {0, 7}:
                score += 5  # Nếu vua đối thủ ở góc, tăng điểm

        gs.undoMove()

        moveScores.append(score)

    # Sắp xếp nước đi giảm dần theo điểm số
    sortedMoves = [move for _, move in sorted(zip(moveScores, validMoves), key=lambda pair: pair[0], reverse=True)]

    return sortedMoves


# Hàm kiểm tra xem nước đi có an toàn hay không
def isMoveSafe(gs, move):
    """
        - Kiểm tra xem sau khi thực hiện nước đi, quân cờ có an toàn không.
    """
    gs.makeMove(move)  # Thực hiện nước đi
    opponent_moves = gs.getValidMoves()  # Lấy tất cả nước đi hợp lệ của đối thủ
    gs.undoMove()  # Hoàn tác nước đi để không thay đổi trạng thái bàn cờ

    for opp_move in opponent_moves:
        if opp_move.endRow == move.endRow and opp_move.endCol == move.endCol:
            return False  # Nếu có nước đi của đối thủ ăn được quân cờ tại vị trí mới, nước đi không an toàn

    return True  # Nếu không có nước đi nào của đối thủ ăn được quân cờ, nước đi an toàn

# ==== MINIMAX ====
nodeCountMinimax = 0

def minimax(gs, depth, turnMultiplier):
    """
        Thuật toán Minimax cơ bản.
            - gs: Trạng thái bàn cờ hiện tại.
            - depth: Chiều sâu tìm kiếm.
            - turnMultiplier: 1 nếu là lượt của trắng, -1 nếu là lượt của đen.
    """
    global nodeCountMinimax
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    maxScore = -10000
    for move in gs.getValidMoves():
        nodeCountMinimax += 1
        gs.makeMove(move)
        score = -minimax(gs, depth - 1, -turnMultiplier)
        gs.undoMove()
        if score > maxScore:
            maxScore = score
    return maxScore

def runMinimaxComparison(gs, depth=DEPTH):
    """
        Chạy thuật toán Minimax và đo thời gian thực thi.
            - gs: Trạng thái bàn cờ hiện tại.
            - depth: Chiều sâu tìm kiếm.
    """
    global nodeCountMinimax
    nodeCountMinimax = 0  # Reset bộ đếm node
    start_time = time.time()
    minimaxScore = minimax(gs, depth, 1 if gs.whiteToMove else -1)
    elapsed_time = time.time() - start_time
    return minimaxScore, nodeCountMinimax, elapsed_time

# ==== NEGAMAX + ALPHA-BETA ====
nodeCountNegaMax = 0

def negamax_alpha_beta(gs, depth, alpha, beta, turnMultiplier):
    """
        Thuật toán NegaMax với Alpha-Beta pruning.
            - gs: Trạng thái bàn cờ hiện tại.
            - depth: Chiều sâu tìm kiếm.
            - alpha: Giá trị alpha ban đầu.
            - beta: Giá trị beta ban đầu.
            - turnMultiplier: 1 nếu là lượt của trắng, -1 nếu là lượt của đen.
    """
    global nodeCountNegaMax
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    maxScore = -10000
    for move in gs.getValidMoves():
        nodeCountNegaMax += 1
        gs.makeMove(move)
        score = -negamax_alpha_beta(gs, depth - 1, -beta, -alpha, -turnMultiplier)
        gs.undoMove()
        if score > maxScore:
            maxScore = score
        alpha = max(alpha, maxScore)
        if alpha >= beta:
            break
    return maxScore

def runNegaMaxComparison(gs, depth=3):
    """
    Chạy thuật toán NegaMax với Alpha-Beta pruning và đo thời gian thực thi.
    - gs: Trạng thái bàn cờ hiện tại.
    - depth: Chiều sâu tìm kiếm.
    """
    global nodeCountNegaMax
    nodeCountNegaMax = 0  # Reset bộ đếm node
    start_time = time.time()
    negamaxScore = negamax_alpha_beta(gs, depth, -10000, 10000, 1 if gs.whiteToMove else -1)
    elapsed_time = time.time() - start_time
    return negamaxScore, nodeCountNegaMax, elapsed_time

def compareAlgorithms(gs, depth=DEPTH):
    # Chạy Minimax
    minimaxScore, nodeCountMinimax, timeMinimax = runMinimaxComparison(gs, depth)

    # Chạy NegaMax
    negamaxScore, nodeCountNegaMax, timeNega = runNegaMaxComparison(gs, depth)

    # In kết quả
    print(f"Minimax Score: {minimaxScore}, Nodes: {nodeCountMinimax}, Time: {timeMinimax:.4f}s")
    print(f"NegaMax Score: {negamaxScore}, Nodes: {nodeCountNegaMax}, Time: {timeNega:.4f}s")
