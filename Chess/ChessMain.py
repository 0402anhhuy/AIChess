import sys
import pygame as p
import time

import Menu
import AIEngine
import Config
import ChessEngine

# Khởi tạo các biến toàn cục
IMAGES = {}  # Lưu trữ hình ảnh của các quân cờ
WIDTH = Config.Config.WIDTH  # Chiều rộng bàn cờ
HEIGHT = Config.Config.HEIGHT  # Chiều cao bàn cờ
MOVE_LOG_W = Config.Config.MOVE_LOG_W  # Chiều rộng bảng ghi nước đi
MOVE_LOG_H = Config.Config.MOVE_LOG_H  # Chiều cao bảng ghi nước đi
DIMENSION = Config.Config.DIMENSION  # Số ô trên bàn cờ (8x8)
SQ_SIZE = Config.Config.SQ_SIZE  # Kích thước mỗi ô vuông
MAX_FPS = Config.Config.MAX_FPS  # Số khung hình mỗi giây
SQ_LIGHT_COLOR = Config.Config.SQ_LIGHT_COLOR  # Màu ô sáng
SQ_DARK_COLOR = Config.Config.SQ_DARK_COLOR  # Màu ô tối
TEXT_LIGHT_COLOR = Config.Config.TEXT_LIGHT_COLOR  # Màu chữ sáng
TEXT_DARK_COLOR = Config.Config.TEXT_DARK_COLOR  # Màu chữ tối
FONT = Config.Config.get_font()  # Font chữ
TIME_WHILE_END = 2  # Thời gian chờ khi kết thúc trò chơi

# Tải hình ảnh quân cờ (chỉ chạy một lần)
def loadImages():
    """
        - Tải hình ảnh của các quân cờ và lưu vào biến toàn cục IMAGES.
    """
    pieces = ["wP", "wR", "wN", "wB", "wQ", "wK", "bP", "bR", "bN", "bB", "bQ", "bK"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(
            p.image.load("Chess/assets/images/" + piece + ".png"), (SQ_SIZE - 20, SQ_SIZE - 20)
        )

# Xử lý sự kiện nhấp chuột
def handleMouseClick(e, gs, sqSelected, playerClicks, validMoves, humanTurn):
    """
        - Xử lý sự kiện nhấp chuột để chọn ô vuông và thực hiện nước đi.
    """
    moveMade = False
    animate = False
    if not gs.checkMate and not gs.staleMate and humanTurn:
        location = p.mouse.get_pos()  # Lấy vị trí chuột
        col = location[0] // SQ_SIZE  # Xác định cột
        row = location[1] // SQ_SIZE  # Xác định hàng
        if sqSelected == (row, col) or col >= 8:  # Nếu nhấp lại vào ô đã chọn hoặc ngoài bàn cờ
            sqSelected = ()
            playerClicks = []
        else:
            sqSelected = (row, col)
            playerClicks.append(sqSelected)  # Lưu tọa độ ô đã chọn
        if len(playerClicks) == 2:  # Nếu đã chọn đủ 2 ô (bắt đầu và kết thúc)
            move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
            for validMove in validMoves:
                if move == validMove:  # Kiểm tra nước đi có hợp lệ không
                    gs.makeMove(validMove)  # Thực hiện nước đi
                    moveMade = True
                    animate = True
                    sqSelected = ()
                    playerClicks = []
                    break
            if not moveMade:
                playerClicks = [sqSelected]  # Nếu nước đi không hợp lệ, giữ lại ô đã chọn
    return sqSelected, playerClicks, moveMade, animate

# Xử lý sự kiện nhấn phím
def handleKeyPress(e, gs):
    """
        - Xử lý sự kiện nhấn phím để hoàn tác nước đi, mở menu hoặc tạm dừng trò chơi.
    """
    moveMade = False
    animate = False
    gameOver = False
    action = None
    if e.key == p.K_z:  # Hoàn tác nước đi
        gs.undoMove()
        moveMade = True
    elif e.key == p.K_m:  # Mở menu chính
        action = "MENU"
    elif e.key == p.K_p:  # Tạm dừng trò chơi
        action = "PAUSE"
    return moveMade, animate, gameOver, action

# Xử lý nước đi của AI
def handleAIMove(gs, validMoves):
    """
        - Xử lý nước đi của AI bằng cách tìm nước đi tốt nhất hoặc ngẫu nhiên.
    """
    moveMade = False
    animate = False
    AImove = AIEngine.findBestMove(gs, validMoves)  # Tìm nước đi tốt nhất
    if AImove is None:  # Nếu không tìm được, chọn nước đi ngẫu nhiên
        AImove = AIEngine.findRandomMove(validMoves)
    gs.makeMove(AImove)  # Thực hiện nước đi
    moveMade = True
    animate = True
    return moveMade, animate

# Đặt lại trạng thái trò chơi
def resetGame():
    """
        - Đặt lại trạng thái trò chơi về ban đầu.
    """
    gs = ChessEngine.GameState()  # Tạo trạng thái bàn cờ mới
    validMoves = gs.getValidMoves()  # Lấy danh sách các nước đi hợp lệ
    sqSelected = ()
    playerClicks = []
    moveMade = False
    animate = False
    gameOver = False
    return gs, validMoves, sqSelected, playerClicks, moveMade, animate, gameOver

# Hàm chính để chơi game
def play(AI):
    """
        - Hàm chính để chơi game, hỗ trợ chế độ PvP và PvE.
    """
    p.init()
    p.display.set_caption("Play with Player")  # Tiêu đề cửa sổ
    screen = p.display.set_mode((WIDTH + MOVE_LOG_W, HEIGHT))  # Tạo cửa sổ hiển thị
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    moveLogFont = p.font.SysFont("Arial", 20, False, False)  # Font chữ cho bảng ghi nước đi

    # Đặt lại trạng thái trò chơi
    gs, validMoves, sqSelected, playerClicks, moveMade, animate, gameOver = resetGame()
    loadImages()  # Tải hình ảnh quân cờ
    running = True
    playerOne = True  # Người chơi 1 (trắng)
    playerTwo = AI  # Người chơi 2 (đen hoặc AI)

    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and not playerTwo)

        for e in p.event.get():
            if e.type == p.QUIT:  # Thoát game
                running = False
                p.quit()
                sys.exit()
            elif e.type == p.MOUSEBUTTONDOWN:  # Xử lý nhấp chuột
                if not gameOver and humanTurn:
                    sqSelected, playerClicks, moveMade, animate = handleMouseClick(
                        e, gs, sqSelected, playerClicks, validMoves, humanTurn
                    )
            elif e.type == p.KEYDOWN:  # Xử lý nhấn phím
                moveUndo, anim, gameOver, action = handleKeyPress(e, gs)
                if moveUndo:
                    moveMade = True
                    animate = anim
                if action == "MENU":  # Mở menu chính
                    running = False
                    Menu.main_menu()
                elif action == "PAUSE":  # Tạm dừng trò chơi
                    running = False
                    pause_action = Menu.pause_menu()
                    if pause_action == "RESUME":  # Tiếp tục trò chơi
                        running = True
                    elif pause_action == "RESTART":  # Chơi lại
                        gs, validMoves, sqSelected, playerClicks, moveMade, animate, gameOver = resetGame()
                        running = True
                    elif pause_action == "QUIT":  # Thoát game
                        p.quit()
                        sys.exit()

        if not gameOver and not humanTurn:  # Xử lý nước đi của AI
            moveMade, animate = handleAIMove(gs, validMoves)

        if moveMade:  # Nếu có nước đi được thực hiện
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)  # Hiển thị hoạt ảnh nước đi
            validMoves = gs.getValidMoves()  # Cập nhật danh sách nước đi hợp lệ
            moveMade = False
            animate = False

        drawGameState(screen, gs, validMoves, sqSelected, moveLogFont)  # Vẽ trạng thái bàn cờ

        end_text = None
        if gs.checkMate:  # Kiểm tra chiếu hết
            gameOver = True
            running = False
            end_text = "Black wins!" if gs.whiteToMove else "White wins!"
        elif gs.staleMate:  # Kiểm tra hòa cờ
            gameOver = True
            running = False
            end_text = "Draw!"

        clock.tick(MAX_FPS)  # Giới hạn FPS
        p.display.flip()  # Cập nhật màn hình

        if gameOver:  # Hiển thị menu kết thúc
            start_time = time.time()
            while time.time() - start_time < TIME_WHILE_END:
                pass
            Menu.end_menu(end_text)

# Các hàm vẽ bàn cờ, quân cờ, lịch sử nước đi, và hoạt ảnh
def drawBoard(screen):
    """
        - Vẽ bàn cờ với các ô sáng và tối xen kẽ.
    """
    global colors
    colors = [p.Color(SQ_LIGHT_COLOR), p.Color(SQ_DARK_COLOR)]

    for row in range(DIMENSION):
        for column in range(DIMENSION):
            color = colors[(row + column) % 2]
            p.draw.rect(screen, color, p.Rect(column * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

# Hàm thực hiện vẽ quân cờ trong trò chơi
def drawPiece(screen, board):
    """
        - Vẽ các quân cờ trên bàn cờ.
    """
    NEW_SIZE = SQ_SIZE - 20
    OFFSET = (SQ_SIZE - NEW_SIZE) // 2
    for row in range(DIMENSION):
        for coloumn in range(DIMENSION):
            piece = board[row][coloumn]
            if piece != "--":  # Nếu ô không trống
                x = coloumn * SQ_SIZE + OFFSET
                y = row * SQ_SIZE + OFFSET
                screen.blit(IMAGES[piece], p.Rect(x, y, NEW_SIZE, NEW_SIZE))

# Hàm đánh dấu các nước đi hợp lệ cho mỗi quân cờ
def highlightSquares(screen, gs, validMoves, sqSelected):
    """
        - Đánh dấu các ô vuông mà người chơi đã chọn và các ô vuông mà người chơi có thể di chuyển.
    """
    if sqSelected != ():
        row, column = sqSelected
        if gs.board[row][column][0] == ("w" if gs.whiteToMove else "b"):
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)  # Đặt độ trong suốt
            s.fill(p.Color("blue"))  # Màu ô đã chọn
            screen.blit(s, (column * SQ_SIZE, row * SQ_SIZE))
            s.fill(p.Color("yellow"))  # Màu ô có thể di chuyển
            for move in validMoves:
                if move.startRow == row and move.startCol == column:
                    screen.blit(s, (move.endCol * SQ_SIZE, move.endRow * SQ_SIZE))

# Hàm ghi lại lịch sử các nước đi
def drawMoveLog(screen, gs, font):
    """
        - Vẽ lịch sử các nước đi ở bên phải bàn cờ.
    """
    moveLogRect = p.Rect(WIDTH, 0, MOVE_LOG_W, MOVE_LOG_H)
    p.draw.rect(screen, p.Color("Black"), moveLogRect)
    moveLog = gs.moveLog
    moveTexts = []
    for i in range(0, len(moveLog), 2):
        moveString = str(i // 2 + 1) + ". " + str(moveLog[i]) + " "
        if i + 1 < len(moveLog):
            moveString += str(moveLog[i + 1]) + "  "
        moveTexts.append(moveString)
    movePerRow = 3
    padding = 5
    lineSpacing = 2
    textY = padding
    for i in range(0, len(moveTexts), movePerRow):
        text = ""
        for j in range(movePerRow):
            if i + j < len(moveTexts):
                text += moveTexts[i + j]
        textObject = font.render(text, True, p.Color("White"))
        textLocation = moveLogRect.move(padding, textY)
        screen.blit(textObject, textLocation)
        textY += textObject.get_height() + lineSpacing

# Hàm tạo hoạt ảnh cho quân cờ khi di chuyển trong trò chơi
def animateMove(move, screen, board, clock):
    """
        - Hiển thị hoạt ảnh khi quân cờ di chuyển.
    """
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol

    framesPerSquare = 10
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare

    for frame in range(frameCount + 1):
        r = move.startRow + dR * frame / frameCount
        c = move.startCol + dC * frame / frameCount

        # Vẽ lại bàn cờ và quân cờ
        drawBoard(screen)
        drawPiece(screen, board)

        # Tô lại ô đích trước khi vẽ hoạt ảnh
        color = p.Color(SQ_LIGHT_COLOR) if (move.endRow + move.endCol) % 2 == 0 else p.Color(SQ_DARK_COLOR)
        endSquare = p.Rect(move.endCol * SQ_SIZE, move.endRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)

        # Vẽ lại quân bị bắt (nếu có)
        if move.pieceCaptured != "--":
            if move.isEnpassantMove:
                enPassantRow = move.endRow + 1 if move.pieceCaptured[0] == "b" else move.endRow - 1
                endSquare = p.Rect(move.endCol * SQ_SIZE, enPassantRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            screen.blit(IMAGES[move.pieceCaptured],
                        (move.endCol * SQ_SIZE + 10, move.endRow * SQ_SIZE + 10))

        # Vẽ quân đang di chuyển theo từng frame
        screen.blit(IMAGES[move.pieceMoved],
                    p.Rect(c * SQ_SIZE + 10, r * SQ_SIZE + 10, SQ_SIZE - 20, SQ_SIZE - 20))

        # Cập nhật màn hình và chờ frame kế
        p.display.flip()
        clock.tick(60)

# Hàm thực hiện vẽ văn bản
def drawText(screen, text):
    """
        - Hiển thị văn bản ở giữa màn hình.
    """
    textObject = FONT.render(text, True, p.Color("Black"))
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(
        WIDTH / 2 - textObject.get_width() / 2,
        HEIGHT / 2 - textObject.get_height() / 2
    )
    screen.blit(textObject, textLocation)

# Hàm thực hiện vẽ trạng thái của trò chơi
def drawGameState(screen, gs, validMoves, sqSelected, moveLogFont):
    """
        - Vẽ toàn bộ trạng thái bàn cờ, bao gồm bàn cờ, quân cờ, các ô được đánh dấu, và lịch sử nước đi.
    """
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPiece(screen, gs.board)
    drawMoveLog(screen, gs, moveLogFont)