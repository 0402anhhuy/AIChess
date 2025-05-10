import pygame
import time
from ChessEngine import GameState, Move

# ==== AI SCORING ====
def scoreBoard(gs):
    pieceScore = {"K": 0, "Q": 10, "R": 5, "B": 3, "N": 3, "P": 1}
    score = 0
    for row in gs.board:
        for square in row:
            if square != "--":
                if square[0] == "w":
                    score += pieceScore.get(square[1], 0)
                else:
                    score -= pieceScore.get(square[1], 0)
    return score

# ==== MINIMAX ====
nodeCountMinimax = 0

def minimax(gs, depth, turnMultiplier):
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

# ==== NEGAMAX + ALPHA-BETA ====
nodeCountNegaMax = 0

def negamax_alpha_beta(gs, depth, alpha, beta, turnMultiplier):
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

# ==== TEST BOARD SETUP ====
gs = GameState()
gs.board = [
    ['bR', '--', '--', '--', 'bK', '--', '--', 'bR'],
    ['bP', 'bP', 'bN', '--', '--', '--', 'bP', 'bP'],
    ['--', '--', '--', '--', '--', '--', '--', '--'],
    ['--', '--', '--', 'wQ', '--', '--', '--', '--'],
    ['--', '--', 'wP', '--', '--', '--', '--', '--'],
    ['--', '--', '--', '--', '--', '--', '--', '--'],
    ['wP', 'wP', '--', '--', 'wP', 'wP', 'wP', 'wP'],
    ['wR', 'wN', '--', '--', 'wK', '--', '--', 'wR'],
]
gs.whiteToMove = True

# ==== THUẬT TOÁN ====
DEPTH = 3
start = time.time()
minimaxScore = minimax(gs, DEPTH, 1)
timeMinimax = time.time() - start

start = time.time()
negamaxScore = negamax_alpha_beta(gs, DEPTH, -10000, 10000, 1)
timeNega = time.time() - start

# ==== GUI VỚI BÀN CỜ + SO SÁNH ====
pygame.init()
square_size = 60
screen = pygame.display.set_mode((square_size * 8 + 400, square_size * 8))
pygame.display.set_caption("Minimax và NegaMax + Alpha-Beta")
font = pygame.font.SysFont("Arial", 20)
colors = [(240, 217, 181), (181, 136, 99)]

# Tải ảnh quân cờ
IMAGES = {}
def loadImages():
    pieces = ["wP", "wR", "wN", "wB", "wQ", "wK", "bP", "bR", "bN", "bB", "bQ", "bK"]
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(
            pygame.image.load("Chess/assets/images/" + piece + ".png"), (square_size - 10, square_size - 10)
        )

loadImages()

def draw_board(screen, board):
    for r in range(8):
        for c in range(8):
            color = colors[(r + c) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(c * square_size, r * square_size, square_size, square_size))
            piece = board[r][c]
            if piece != "--":
                if piece in IMAGES:
                    screen.blit(IMAGES[piece], (c * square_size + 5, r * square_size + 5))
                else:
                    text = font.render(piece, True, (0, 0, 0))
                    screen.blit(text, (c * square_size + 5, r * square_size + 5))

running = True
while running:
    screen.fill((255, 255, 255))
    draw_board(screen, gs.board)

    offset = square_size * 8 + 20
    pygame.draw.rect(screen, (200, 200, 255), (offset - 10, 60, 360, 100))
    mm_title = font.render("Minimax:", True, (0, 0, 0))
    mm_nodes = font.render(f"Node: {nodeCountMinimax}", True, (0, 0, 0))
    mm_time = font.render(f"Time: {timeMinimax:.4f}s", True, (0, 0, 0))
    mm_score = font.render(f"Score: {minimaxScore}", True, (0, 0, 0))
    screen.blit(mm_title, (offset, 70))
    screen.blit(mm_nodes, (offset, 100))
    screen.blit(mm_time, (offset, 130))
    screen.blit(mm_score, (offset, 160))

    pygame.draw.rect(screen, (200, 255, 200), (offset - 10, 200, 360, 100))
    ng_title = font.render("NegaMax + Alpha-Beta:", True, (0, 0, 0))
    ng_nodes = font.render(f"Node: {nodeCountNegaMax}", True, (0, 0, 0))
    ng_time = font.render(f"Time: {timeNega:.4f}s", True, (0, 0, 0))
    ng_score = font.render(f"Score: {negamaxScore}", True, (0, 0, 0))
    screen.blit(ng_title, (offset, 210))
    screen.blit(ng_nodes, (offset, 240))
    screen.blit(ng_time, (offset, 270))
    screen.blit(ng_score, (offset, 300))

    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
