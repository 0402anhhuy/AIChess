import pygame, sys
import Button
import ChessMain
import ChessEngine
import Config

pygame.init()

# Kích thước màn hình
WIDTH = Config.Config.WIDTH + Config.Config.MOVE_LOG_W  # Chiều rộng màn hình (bao gồm bảng ghi nước đi)
HEIGHT = Config.Config.HEIGHT  # Chiều cao màn hình
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))  # Tạo cửa sổ hiển thị
pygame.display.set_caption("Menu")  # Tiêu đề cửa sổ

# Hình nền menu
BG = pygame.transform.scale(pygame.image.load("Chess/assets/menu/Background_2.png"), (WIDTH, HEIGHT))

# Hàm tạo font chữ
def getFont(size):
    return pygame.font.SysFont("Inter", size)

# Hàm tạo nút
def createButton(text, pos, font_size, base_color, hovering_color):
    """
        - Tạo một nút với văn bản, vị trí, màu sắc cơ bản và màu khi di chuột.
    """
    return Button.Button(
        image=None,
        pos=pos,
        text_input=text,
        font=getFont(font_size),
        base_color=base_color,
        hovering_color=hovering_color,
    )

# Hàm hiển thị tất cả các nút
def drawButtons(buttons, mouse_pos):
    """
        - Hiển thị danh sách các nút trên màn hình và thay đổi màu khi di chuột.
    """
    for button in buttons:
        button.changeColor(mouse_pos)  # Thay đổi màu nếu chuột di qua nút
        button.update(SCREEN)  # Cập nhật hiển thị nút

# Hàm tạo menu chính cho game
def playMenu():
    """
        - Menu chọn chế độ chơi: PvP (Player vs Player) hoặc PvE (Player vs AI).
    """
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()  # Lấy vị trí chuột
        SCREEN.fill("BLACK")  # Xóa màn hình
        SCREEN.blit(BG, (0, 0))  # Hiển thị hình nền

        # Tạo các nút
        BACK_BUTTON = createButton("BACK", (WIDTH * 0.5, HEIGHT * 0.75), 100, "White", "Green")
        PvP_BUTTON = createButton("PvP", (WIDTH * 0.5, HEIGHT * 0.25), 100, "#d7fcd4", "Blue")
        PvE_BUTTON = createButton("PvE", (WIDTH * 0.5, HEIGHT * 0.5), 100, "#d7fcd4", "Yellow")

        buttons = [BACK_BUTTON, PvP_BUTTON, PvE_BUTTON]
        drawButtons(buttons, PLAY_MOUSE_POS)  # Hiển thị các nút

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Thoát game nếu người dùng đóng cửa sổ
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # Xử lý khi người dùng nhấn chuột
                if BACK_BUTTON.checkForInput(PLAY_MOUSE_POS):  # Quay lại menu chính
                    mainMenu()
                elif PvE_BUTTON.checkForInput(PLAY_MOUSE_POS):  # Chơi với AI
                    ChessMain.play(True, "PvE")  # Chơi với AI
                elif PvP_BUTTON.checkForInput(PLAY_MOUSE_POS):  # Chơi với người
                    ChessMain.play(False, "PvP")

        pygame.display.update()  # Cập nhật màn hình

# Hàm hiển thị văn bản hướng dẫn
def drawGuideText(text, center_y):
    """
        - Hiển thị một dòng văn bản hướng dẫn tại vị trí `center_y`.
    """
    guide_text = getFont(80).render(text, True, "WHITE")  # Tạo văn bản
    guide_rect = guide_text.get_rect(center=(WIDTH / 2, HEIGHT * center_y))  # Đặt vị trí
    SCREEN.blit(guide_text, guide_rect)  # Hiển thị văn bản

# Hàm menu hướng dẫn cho trò chơi
def guideMenu():
    """
        - Menu hiển thị hướng dẫn chơi game.
    """
    while True:
        mouse_pos = pygame.mouse.get_pos()  # Lấy vị trí chuột

        SCREEN.fill("BLACK")  # Xóa màn hình
        SCREEN.blit(BG, (0, 0))  # Hiển thị hình nền

        # Hiển thị khung hướng dẫn
        guide_bg = pygame.image.load("Chess/assets/menu/Guide Rect.png")
        guide_bg_rect = guide_bg.get_rect(center=(WIDTH / 2, HEIGHT * 0.39))
        SCREEN.blit(guide_bg, guide_bg_rect)

        # Hiển thị các dòng hướng dẫn
        drawGuideText("Z: Undo", 0.26)
        drawGuideText("M: Menu", 0.39)
        drawGuideText("P: Pause", 0.52)

        # Nút Back
        back_button = createButton("BACK", (WIDTH / 2, HEIGHT * 0.8), 100, "White", "Green")
        drawButtons([back_button], mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Thoát game nếu người dùng đóng cửa sổ
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # Xử lý khi người dùng nhấn chuột
                if back_button.checkForInput(mouse_pos):  # Quay lại menu chính
                    mainMenu()

        pygame.display.update()  # Cập nhật màn hình

# Hàm tạo menu khi tạm dừng trò chơi
def pauseMenu():
    """
        - Menu hiển thị khi trò chơi bị tạm dừng.
    """
    while True:
        mouse_pos = pygame.mouse.get_pos()  # Lấy vị trí chuột

        SCREEN.fill("BLACK")  # Xóa màn hình
        SCREEN.blit(BG, (0, 0))  # Hiển thị hình nền

        # Tạo các nút
        buttons = [
            createButton("HOME", (WIDTH / 2, HEIGHT * 0.2), 75, "#d7fcd4", "GREEN"),
            createButton("RESUME", (WIDTH / 2, HEIGHT * 0.4), 75, "#d7fcd4", "WHITE"),
            createButton("RESTART", (WIDTH / 2, HEIGHT * 0.6), 75, "#d7fcd4", "WHITE"),
            createButton("QUIT", (WIDTH * 0.5, HEIGHT * 0.8), 75, "WHITE", "RED"),
        ]

        drawButtons(buttons, mouse_pos)  # Hiển thị các nút

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Thoát game nếu người dùng đóng cửa sổ
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:  # Xử lý khi người dùng nhấn chuột
                if buttons[0].checkForInput(mouse_pos):  # Quay lại menu chính
                    mainMenu()
                if buttons[1].checkForInput(mouse_pos):  # Tiếp tục trò chơi
                    return "RESUME"
                if buttons[2].checkForInput(mouse_pos):  # Chơi lại
                    return "RESTART"
                if buttons[3].checkForInput(mouse_pos):  # Thoát game
                    pygame.quit()
                    sys.exit()

        pygame.display.update()  # Cập nhật màn hình

# Hàm tạo menu khi kết thúc trò chơi
def endMenu(end_text):
    """
        - Menu hiển thị khi trò chơi kết thúc.
    """
    while True:
        mouse_pos = pygame.mouse.get_pos()  # Lấy vị trí chuột

        SCREEN.fill("BLACK")  # Xóa màn hình
        SCREEN.blit(BG, (0, 0))  # Hiển thị hình nền

        # Hiển thị kết quả trận đấu
        end_text_surface = getFont(75).render(end_text, True, "WHITE")
        end_text_rect = end_text_surface.get_rect(center=(WIDTH / 2, HEIGHT * 0.3))
        SCREEN.blit(end_text_surface, end_text_rect)

        # Tạo các nút
        buttons = [
            createButton("HOME", (WIDTH / 2, HEIGHT * 0.45), 80, "#d7fcd4", "GREEN"),
            createButton("RESTART", (WIDTH / 2, HEIGHT * 0.6), 80, "#d7fcd4", "WHITE"),
            createButton("QUIT", (WIDTH * 0.5, HEIGHT * 0.75), 80, "#d7fcd4", "RED"),
        ]

        drawButtons(buttons, mouse_pos)  # Hiển thị các nút

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Thoát game nếu người dùng đóng cửa sổ
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # Xử lý khi người dùng nhấn chuột
                if buttons[0].checkForInput(mouse_pos):  # Quay lại menu chính
                    mainMenu()
                if buttons[1].checkForInput(mouse_pos):  # Chơi lại
                    return "RESTART"
                if buttons[2].checkForInput(mouse_pos):  # Thoát game
                    pygame.quit()
                    sys.exit()

        pygame.display.update()  # Cập nhật màn hình

def drawComparisonResult(screen, font, minimaxResult, negamaxResult, x, y, width, height):
    """
        Hiển thị kết quả so sánh giữa Minimax và NegaMax trên giao diện.
            - screen: Màn hình Pygame.
            - font: Font chữ để hiển thị.
            - minimaxResult: Kết quả của Minimax (score, nodes, time).
            - negamaxResult: Kết quả của NegaMax (score, nodes, time).
            - x, y: Tọa độ góc trên bên trái của vùng hiển thị.
            - width, height: Kích thước vùng hiển thị.
    """
    # Vẽ khung nền cho phần so sánh
    pygame.draw.rect(screen, (200, 200, 200), (x, y, width, height))
    pygame.draw.rect(screen, (0, 0, 0), (x, y, width, height), 2)  # Viền đen

    # Hiển thị kết quả Minimax
    minimaxTitle = font.render("Minimax:", True, (0, 0, 0))
    minimaxScore = font.render(f"Score: {minimaxResult['score']}", True, (0, 0, 0))
    minimaxNodes = font.render(f"Nodes: {minimaxResult['nodes']}", True, (0, 0, 0))
    minimaxTime = font.render(f"Time: {minimaxResult['time']:.4f}s", True, (0, 0, 0))

    screen.blit(minimaxTitle, (x + 10, y + 10))
    screen.blit(minimaxScore, (x + 10, y + 40))
    screen.blit(minimaxNodes, (x + 10, y + 70))
    screen.blit(minimaxTime, (x + 10, y + 100))

    # Hiển thị kết quả NegaMax
    negamaxTitle = font.render("NegaMax + Alpha-Beta:", True, (0, 0, 0))
    negamaxScore = font.render(f"Score: {negamaxResult['score']}", True, (0, 0, 0))
    negamaxNodes = font.render(f"Nodes: {negamaxResult['nodes']}", True, (0, 0, 0))
    negamaxTime = font.render(f"Time: {negamaxResult['time']:.4f}s", True, (0, 0, 0))

    screen.blit(negamaxTitle, (x + 10, y + 140))
    screen.blit(negamaxScore, (x + 10, y + 170))
    screen.blit(negamaxNodes, (x + 10, y + 200))
    screen.blit(negamaxTime, (x + 10, y + 230))

# Hàm tạo menu chính cho trò chơi
def mainMenu():
    """
        - Menu chính của trò chơi.
    """
    while True:
        SCREEN.blit(BG, (0, 0))  # Hiển thị hình nền
        mouse_pos = pygame.mouse.get_pos()  # Lấy vị trí chuột

        # Hiển thị tiêu đề "CHESS"
        menu_text_surface = getFont(170).render("CHESS", True, "White")
        menu_text_rect = menu_text_surface.get_rect(center=(WIDTH * 0.5, HEIGHT * 0.15))
        SCREEN.blit(menu_text_surface, menu_text_rect)

        # Tạo các nút
        buttons = [
            createButton("PLAY", (WIDTH * 0.5, HEIGHT * 0.4), 120, "Gold", "White"),
            createButton("GUIDE", (WIDTH * 0.5, HEIGHT * 0.6), 120, "Gold", "White"),
            createButton("QUIT", (WIDTH * 0.5, HEIGHT * 0.8), 120, "Gold", "Red")
        ]

        drawButtons(buttons, mouse_pos)  # Hiển thị các nút

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Thoát game nếu người dùng đóng cửa sổ
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # Xử lý khi người dùng nhấn chuột
                if buttons[0].checkForInput(mouse_pos):  # Chơi game
                    playMenu()
                if buttons[1].checkForInput(mouse_pos):  # Hướng dẫn
                    guideMenu()
                if buttons[2].checkForInput(mouse_pos):  # Thoát game
                    pygame.quit()
                    sys.exit()

        pygame.display.update()  # Cập nhật màn hình