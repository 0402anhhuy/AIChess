import sys
import pygame as p
import time

import Menu
import AIEngine
import Config
import ChessEngine

WIDTH = Config.Config.WIDTH
HEIGHT = Config.Config.HEIGHT
MOVE_LOG_W = Config.Config.MOVE_LOG_W
MOVE_LOG_H = Config.Config.MOVE_LOG_H
DIMENSION = Config.Config.DIMENSION  
SQ_SIZE = Config.Config.SQ_SIZE
MAX_FPS = Config.Config.MAX_FPS
SQ_LIGHT_COLOR = Config.Config.SQ_LIGHT_COLOR
SQ_DARK_COLOR = Config.Config.SQ_DARK_COLOR
TEXT_LIGHT_COLOR = Config.Config.TEXT_LIGHT_COLOR
TEXT_DARK_COLOR = Config.Config.TEXT_DARK_COLOR
IMAGES = {}
TIME_WHILE_END = 2

# Tải hình ảnh quân cờ (chỉ chạy một lần)
def loadImages():
    pieces = ["wP", "wR", "wN", "wB", "wQ", "wK", "bP", "bR", "bN", "bB", "bQ", "bK"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("Chess/assets/images/" + piece + ".png"), (SQ_SIZE - 20, SQ_SIZE - 20))


"""
phần chính của code. đoạn này sẽ kiểm soát đầu vào của người dùng và cập nhập đồ hoạ
"""


def play(AI):
    p.init()
    p.display.set_caption("Play with Player")
    screen = p.display.set_mode((WIDTH + MOVE_LOG_W, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    moveLogFont = p.font.SysFont("Arial", 20, False, False)
    # khởi tạo một game state ban đầu
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False  # một biến cờ khi mà một nước đi được tạo ra
    animate = False  # một biến để ktra xem khi nào nên tạo hoạt ảnh cho nước đi
    loadImages()
    running = True
    sqSelected = ()  # ko có hình vuông nào được chọn, theo dõi lần click chuột cuối cùng của user ( tuple : (row, col))
    playerClicks = []  # keep track of player clicks (two tuple [(6,4), (4,4)])
    gameOver = False
    playerOne = True  # nếu người chơi đang chơi màu trắng, biến này sẽ là true. Nếu AI đang chơi màu trắng, biến này là False
    playerTwo = AI
    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (
            not gs.whiteToMove and not playerTwo
        )
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
                p.quit()
                sys.exit()
                break
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
                    location = p.mouse.get_pos()  # trả về một cặp toạ độ x y
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if (
                        sqSelected == (row, col) or col >= 8
                    ):  # hành động chọn 2 lần vào một ô vuông
                        # hoàn tác lại các giá trị
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)
                    if len(playerClicks) == 2:  # sau 2 lan click chuot
                        move = ChessEngine.Move(
                            playerClicks[0], playerClicks[1], gs.board
                        )
                        print(move.getChessNotation())
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                animate = True
                                sqSelected = ()
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]
            # key handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # undo
                    gs.undoMove()
                    moveMade = True
                    animate = False
                    gameOver = False
                if e.key == p.K_r:
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
                    gameOver = False
                if e.key == p.K_m:
                    running = False
                    Menu.main_menu()
        # AI move finder
        if not gameOver and not humanTurn:
            AImove = AIEngine.findBestMove(gs, validMoves)
            if AImove is None:
                AImove = AIEngine.findRandomMove(validMoves)
            gs.makeMove(AImove)
            moveMade = True
            animate = True
        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False

        drawGameState(screen, gs, validMoves, sqSelected, moveLogFont)

        end_text = None
        if gs.checkMate:
            gameOver = True
            running = False
            if gs.whiteToMove:
                end_text = "Black wins!"
                # drawText(screen, " Black wins by checkmate")
            else:
                end_text = "White wins!"
                # drawText(screen, " White wins by checkmate")
        elif gs.staleMate:
            gameOver = True
            running = False
            end_text = "Draw!"
            # drawText(screen, "Stalemate")

        clock.tick(MAX_FPS)
        p.display.flip()

        if gameOver:
            start_time = time.time()
            while True:
                if time.time() - start_time > TIME_WHILE_END:
                    break
            Menu.end_menu(end_text)

# Vẽ bàn cờ
def drawBoard(screen):
    global colors
    colors = [p.Color(SQ_LIGHT_COLOR), p.Color(SQ_DARK_COLOR)]
    font = p.font.Font(None, 28)

    for row in range(DIMENSION):
        for column in range(DIMENSION):
            color = colors[(row + column) % 2]
            p.draw.rect(screen, color, p.Rect(column * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

# Vẽ các quân cờ
def drawPiece(screen, board):
    NEW_SIZE = SQ_SIZE - 20
    OFFSET = (SQ_SIZE - NEW_SIZE) // 2
    for row in range(DIMENSION):
        for coloumn in range(DIMENSION):
            piece = board[row][coloumn]
            if piece != "--":
                x = coloumn * SQ_SIZE + OFFSET
                y = row * SQ_SIZE + OFFSET
                screen.blit(IMAGES[piece], p.Rect(x, y, NEW_SIZE, NEW_SIZE))

# Đánh dấu các ô vuông mà người chơi đã chọn và các ô vuông mà người chơi có thể di chuyển
def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        row, column = sqSelected
        if gs.board[row][column][0] == ("w" if gs.whiteToMove else "b"):
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color("blue"))
            screen.blit(s, (column * SQ_SIZE, row * SQ_SIZE))
            s.fill(p.Color("yellow"))
            for move in validMoves:
                if move.startRow == row and move.startCol == column:
                    screen.blit(s, (move.endCol * SQ_SIZE, move.endRow * SQ_SIZE))

# vẽ lịch sử các nước đi
def drawMoveLog(screen, gs, font):
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


def animateMove(move, screen, board, clock):
    global colors
    coords = []  # danh sách các tọa độ mà hoạt ảnh sẽ di chuyển qua
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol

    framesPerSquare = 10
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare

    for frame in range(frameCount + 1):
        r, c = (
            move.startRow + dR * frame / frameCount,
            move.startCol + dC * frame / frameCount,
        )
        
        drawBoard(screen)
        drawPiece(screen, board)

        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol * SQ_SIZE, move.endRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)

        if move.pieceCaptured != "--":
            if move.isEnpassantMove:
                enPassantRow = (
                    move.endRow + 1 if move.pieceCaptured[0] == "b" else move.endRow - 1
                )
                endSquare = p.Rect(
                    move.endCol * SQ_SIZE, enPassantRow * SQ_SIZE, SQ_SIZE, SQ_SIZE
                )
            screen.blit(IMAGES[move.pieceCaptured], (move.endCol * SQ_SIZE + 10, move.endRow * SQ_SIZE + 10))

        screen.blit(
            IMAGES[move.pieceMoved],
            p.Rect(c * SQ_SIZE + 10, r * SQ_SIZE + 10, SQ_SIZE - 20, SQ_SIZE - 20),
        )

        p.display.flip()
        clock.tick(60)



def drawText(screen, text):
    font = p.font.SysFont("Helvitca", 32, True, False)
    textObject = font.render(text, 0, p.Color("Black"))
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(
        WIDTH / 2 - textObject.get_width() / 2, HEIGHT / 2 - textObject.get_height() / 2
    )
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color("Black"))
    screen.blit(textObject, textLocation.move(2, 2))


def drawGameState(screen, gs, validMoves, sqSelected, moveLogFont):
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPiece(screen, gs.board)
    drawMoveLog(screen, gs, moveLogFont)
