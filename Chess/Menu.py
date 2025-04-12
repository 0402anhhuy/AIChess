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
def get_font(size):
    return pygame.font.SysFont("Inter", size)

# Hàm tạo nút
def create_button(text, pos, font_size, base_color, hovering_color):
    return Button.Button(
        image=None,
        pos=pos,
        text_input=text,
        font=get_font(font_size),
        base_color=base_color,
        hovering_color=hovering_color,
    )

# Hàm hiển thị tất cả các nút
def draw_buttons(buttons, mouse_pos):
    for button in buttons:
        button.changeColor(mouse_pos)
        button.update(SCREEN)

# Menu chơi game
def play_menu():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill("BLACK")
        SCREEN.blit(BG, (0, 0))

        BACK_BUTTON = create_button("BACK", (WIDTH * 0.5, HEIGHT * 0.75), 100, "White", "Green")
        PvP_BUTTON = create_button("PvP", (WIDTH * 0.5, HEIGHT * 0.25), 100, "#d7fcd4", "Blue")
        PvE_BUTTON = create_button("PvE", (WIDTH * 0.5, HEIGHT * 0.5), 100, "#d7fcd4", "Yellow")

        buttons = [BACK_BUTTON, PvP_BUTTON, PvE_BUTTON]
        draw_buttons(buttons, PLAY_MOUSE_POS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    main_menu()
                elif PvE_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    ChessMain.play(True)
                elif PvP_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    ChessMain.play(False)

        pygame.display.update()

def draw_guide_text(text, center_y):
    guide_text = get_font(80).render(text, True, "WHITE")
    guide_rect = guide_text.get_rect(center=(WIDTH / 2, HEIGHT * center_y))
    SCREEN.blit(guide_text, guide_rect)

def guide_menu():
    while True:
        mouse_pos = pygame.mouse.get_pos()

        SCREEN.fill("BLACK")
        SCREEN.blit(BG, (0, 0))

        # Hiển thị khung hướng dẫn
        guide_bg = pygame.image.load("Chess/assets/menu/Guide Rect.png")
        guide_bg_rect = guide_bg.get_rect(center=(WIDTH / 2, HEIGHT * 0.39))
        SCREEN.blit(guide_bg, guide_bg_rect)

        # Hiển thị các dòng hướng dẫn
        draw_guide_text("Z: Undo", 0.26)
        draw_guide_text("R: Reset", 0.39)
        draw_guide_text("P: Pause", 0.52)

        # Nút Back
        back_button = create_button("BACK", (WIDTH / 2, HEIGHT * 0.8), 100, "White", "Green")
        draw_buttons([back_button], mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.checkForInput(mouse_pos):
                    main_menu()

        pygame.display.update()


def pause_menu():
    while True:
        mouse_pos = pygame.mouse.get_pos()

        SCREEN.fill("BLACK")
        SCREEN.blit(BG, (0, 0))

        # Tạo các nút sử dụng hàm tái sử dụng
        buttons = [
            create_button("HOME", (WIDTH / 2, HEIGHT * 0.2), 75, "#d7fcd4", "GREEN"),
            create_button("RESUME", (WIDTH / 2, HEIGHT * 0.4), 75, "#d7fcd4", "WHITE"),
            create_button("RESTART", (WIDTH / 2, HEIGHT * 0.6), 75, "#d7fcd4", "WHITE"),
            create_button("QUIT", (WIDTH * 0.5, HEIGHT * 0.8), 75, "WHITE", "RED"),
        ]

        draw_buttons(buttons, mouse_pos)

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
                    main_menu()
                if buttons[3].checkForInput(mouse_pos):  # QUIT
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


def end_menu(end_text):
    while True:
        mouse_pos = pygame.mouse.get_pos()

        SCREEN.fill("BLACK")
        SCREEN.blit(BG, (0, 0))

        # Hiển thị kết quả trận đấu
        end_text_surface = get_font(75).render(end_text, True, "WHITE")
        end_text_rect = end_text_surface.get_rect(center=(WIDTH / 2, HEIGHT * 0.3))
        SCREEN.blit(end_text_surface, end_text_rect)

        # Tạo các nút
        buttons = [
            create_button("HOME", (WIDTH / 2, HEIGHT * 0.45), 80, "#d7fcd4", "GREEN"),
            create_button("RESTART", (WIDTH / 2, HEIGHT * 0.6), 80, "#d7fcd4", "WHITE"),
            create_button("QUIT", (WIDTH * 0.5, HEIGHT * 0.75), 80, "#d7fcd4", "RED"),
        ]

        draw_buttons(buttons, mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttons[0].checkForInput(mouse_pos):  # HOME
                    main_menu()
                if buttons[1].checkForInput(mouse_pos):  # RESTART
                    ChessMain.play(False)
                if buttons[2].checkForInput(mouse_pos):  # QUIT
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))
        mouse_pos = pygame.mouse.get_pos()

        # Hiển thị tiêu đề "CHESS"
        menu_text_surface = get_font(170).render("CHESS", True, "#b68f40")
        menu_text_rect = menu_text_surface.get_rect(center=(WIDTH * 0.5, HEIGHT * 0.15))
        SCREEN.blit(menu_text_surface, menu_text_rect)

        # Tạo các nút
        buttons = [
            create_button("PLAY", (WIDTH * 0.5, HEIGHT * 0.4), 120, "#d7fcd4", "White"),
            create_button("GUIDE", (WIDTH * 0.5, HEIGHT * 0.6), 120, "#d7fcd4", "White"),
            create_button("QUIT", (WIDTH * 0.5, HEIGHT * 0.8), 120, "#d7fcd4", "RED")
        ]

        draw_buttons(buttons, mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttons[0].checkForInput(mouse_pos):  # PLAY
                    play_menu()
                if buttons[1].checkForInput(mouse_pos):  # GUIDE
                    guide_menu()
                if buttons[2].checkForInput(mouse_pos):  # QUIT
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
