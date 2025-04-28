import pygame, sys
import Button
import ChessMain
import ChessEngine
import Config

import pygame
import sys
import Config
import ChessMain
import Button

pygame.init()

WIDTH = Config.Config.WIDTH + Config.Config.MOVE_LOG_W
HEIGHT = Config.Config.HEIGHT
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu")

BG = pygame.transform.scale(pygame.image.load("Chess/assets/menu/Background.png"), (WIDTH, HEIGHT))

# Hàm tạo font
def getFont(size):
    return pygame.font.SysFont("Inter", size)

# Hàm tạo nút
def createButton(text, pos, font_size, base_color, hovering_color):
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
    for button in buttons:
        button.changeColor(mouse_pos)
        button.update(SCREEN)

# Hàm tạo menu chính cho game
def playMenu():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill("BLACK")
        SCREEN.blit(BG, (0, 0))

        BACK_BUTTON = createButton("BACK", (WIDTH * 0.5, HEIGHT * 0.75), 100, "White", "Green")
        PvP_BUTTON = createButton("PvP", (WIDTH * 0.5, HEIGHT * 0.25), 100, "#d7fcd4", "Blue")
        PvE_BUTTON = createButton("PvE", (WIDTH * 0.5, HEIGHT * 0.5), 100, "#d7fcd4", "Yellow")

        buttons = [BACK_BUTTON, PvP_BUTTON, PvE_BUTTON]
        drawButtons(buttons, PLAY_MOUSE_POS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    mainMenu()
                elif PvE_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    ChessMain.play(True)
                elif PvP_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    ChessMain.play(False)

        pygame.display.update()

# Hàm tạo bảng hướng dẫn cho trò chơi
def drawGuideText(text, center_y):
    guide_text = getFont(80).render(text, True, "WHITE")
    guide_rect = guide_text.get_rect(center=(WIDTH / 2, HEIGHT * center_y))
    SCREEN.blit(guide_text, guide_rect)

# Hàm menu hướng dẫn cho trò chơi
def guideMenu():
    while True:
        mouse_pos = pygame.mouse.get_pos()

        SCREEN.fill("BLACK")
        SCREEN.blit(BG, (0, 0))

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
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.checkForInput(mouse_pos):
                    mainMenu()

        pygame.display.update()

# Hàm tạo menu khi tạm dừng trò chơi
def pauseMenu():
    while True:
        mouse_pos = pygame.mouse.get_pos()

        SCREEN.fill("BLACK")
        SCREEN.blit(BG, (0, 0))

        # Tạo các nút sử dụng hàm tái sử dụng
        buttons = [
            createButton("HOME", (WIDTH / 2, HEIGHT * 0.2), 75, "#d7fcd4", "GREEN"),
            createButton("RESUME", (WIDTH / 2, HEIGHT * 0.4), 75, "#d7fcd4", "WHITE"),
            createButton("RESTART", (WIDTH / 2, HEIGHT * 0.6), 75, "#d7fcd4", "WHITE"),
            createButton("QUIT", (WIDTH * 0.5, HEIGHT * 0.8), 75, "WHITE", "RED"),
        ]

        drawButtons(buttons, mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttons[1].checkForInput(mouse_pos):  # RESUME
                    return "RESUME"
                if buttons[2].checkForInput(mouse_pos):  # RESTART
                    return "RESTART"
                if buttons[0].checkForInput(mouse_pos):  # HOME
                    mainMenu()
                if buttons[3].checkForInput(mouse_pos):  # QUIT
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


# Hàm tạo menu khi kết thúc trò chơi
def endMenu(end_text):
    while True:
        mouse_pos = pygame.mouse.get_pos()

        SCREEN.fill("BLACK")
        SCREEN.blit(BG, (0, 0))

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

        drawButtons(buttons, mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttons[0].checkForInput(mouse_pos):  # HOME
                    mainMenu()
                if buttons[1].checkForInput(mouse_pos):  # RESTART
                    ChessMain.play(False)
                if buttons[2].checkForInput(mouse_pos):  # QUIT
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

# Hàm tạo menu chính choi trò chơi
def mainMenu():
    while True:
        SCREEN.blit(BG, (0, 0))
        mouse_pos = pygame.mouse.get_pos()

        # Hiển thị tiêu đề "CHESS"
        menu_text_surface = getFont(170).render("CHESS", True, "#b68f40")
        menu_text_rect = menu_text_surface.get_rect(center=(WIDTH * 0.5, HEIGHT * 0.15))
        SCREEN.blit(menu_text_surface, menu_text_rect)

        # Tạo các nút
        buttons = [
            createButton("PLAY", (WIDTH * 0.5, HEIGHT * 0.4), 120, "#d7fcd4", "White"),
            createButton("GUIDE", (WIDTH * 0.5, HEIGHT * 0.6), 120, "#d7fcd4", "White"),
            createButton("QUIT", (WIDTH * 0.5, HEIGHT * 0.8), 120, "#d7fcd4", "RED")
        ]

        drawButtons(buttons, mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttons[0].checkForInput(mouse_pos):  # PLAY
                    playMenu()
                if buttons[1].checkForInput(mouse_pos):  # GUIDE
                    guideMenu()
                if buttons[2].checkForInput(mouse_pos):  # QUIT
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
