# Lukomorie.py
import pygame
import sys
import math
from Wheel_Aprons import DiceWheel
from player_logic import PlayerLogic

# Инициализация Pygame
pygame.init()

# Настройки окна
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1030
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Лукоморье 1")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (200, 200, 200)
PURPLE = (100, 0, 200)
light_blue = (0, 153, 125)

# Шрифты
font_small = pygame.font.SysFont('Arial', 24)
font_medium = pygame.font.SysFont('Arial', 36)
font_large = pygame.font.SysFont('Arial', 48)
font_huge = pygame.font.SysFont('Arial', 72)

# Загрузка фона
try:
    board_image = pygame.image.load("lukomorie_board1.jpg")
    board_image = pygame.transform.rotate(board_image, -90)
    board_image = pygame.transform.scale(board_image, (SCREEN_WIDTH - 300, SCREEN_HEIGHT))
except FileNotFoundError:
    print("Файл 'lukomorie_board1.jpg' не найден. Используется заглушка.")
    board_image = pygame.Surface((SCREEN_WIDTH - 300, SCREEN_HEIGHT))
    board_image.fill(GREEN)
    pygame.draw.rect(board_image, BLACK, (0, 0, SCREEN_WIDTH - 300, SCREEN_HEIGHT), 2)
    text = font_medium.render("Фон", True, WHITE)
    board_image.blit(text, (10, 10))

# Создание игрока и колеса
player = PlayerLogic("Игрок 1")
wheel = DiceWheel(SCREEN_WIDTH - 160, SCREEN_HEIGHT // 2, 150, font_large, font_huge)

# Флаги
dice_result_handled = False
extra_roll_handled = False

# UI
INVENTORY_RECT = pygame.Rect(SCREEN_WIDTH - 300, 100, 280, 100)
BON_DISPLAY_RECT = pygame.Rect(SCREEN_WIDTH - 300, 250, 280, 50)

# Основной цикл
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and not player.in_mini_game:
            mouse_x, mouse_y = event.pos
            dist_sq = (mouse_x - wheel.center_x) ** 2 + (mouse_y - wheel.center_y) ** 2
            if dist_sq <= wheel.radius ** 2:
                if not wheel.is_spinning():
                    if not player.skip_turn:
                        wheel.spin()
                        dice_result_handled = False
                        extra_roll_handled = False
                    elif hasattr(player, 'needs_extra_roll') and player.needs_extra_roll:
                        wheel.spin()
                        extra_roll_handled = False

    # Обновление колеса
    wheel.update()

    # Основной бросок → перемещение по списку координат
    if not wheel.is_spinning() and not dice_result_handled and not player.in_mini_game and not player.skip_turn:
        dice_roll = wheel.get_dice_result()
        if dice_roll != 0:
            print(f"[Ход] Выпало: {dice_roll}")
            player.move_by_steps(dice_roll)
            # handle_cell_after_move отключён — ничего не происходит на клетках
            dice_result_handled = True

    # Доп. бросок — тоже отключён логически, но флаги оставлены на будущее
    if not wheel.is_spinning() and not extra_roll_handled and not player.in_mini_game:
        if hasattr(player, 'needs_extra_roll') and player.needs_extra_roll:
            dice_roll = wheel.get_dice_result()
            if dice_roll != 0:
                player.handle_extra_roll(dice_roll)
                extra_roll_handled = True

    # Очистка экрана
    screen.fill(WHITE)
    screen.blit(board_image, (0, 0))

    # Отрисовка фишки — ПО СПИСКУ ИЗ path_points.txt
    if player.path_points and 0 <= player.current_path_index < len(player.path_points):
        x, y = player.path_points[player.current_path_index]
        pygame.draw.circle(screen, RED, (int(x), int(y)), 15)
        # Отображаем порядковый номер точки (1-based)
        point_number = player.current_path_index + 1
        token_label = font_small.render(str(point_number), True, WHITE)
        screen.blit(token_label, (int(x) - 5, int(y) - 10))

    # Отрисовка колеса
    wheel.draw(screen)

    # UI: Инвентарь (пусть остаётся, даже если пустой)
    pygame.draw.rect(screen, GRAY, INVENTORY_RECT)
    inv_text = font_small.render("Инвентарь:", True, BLACK)
    screen.blit(inv_text, (INVENTORY_RECT.x + 5, INVENTORY_RECT.y + 5))
    for i, item in enumerate(player.inventory):
        item_text = font_small.render(item or "Пусто", True, BLACK)
        screen.blit(item_text, (INVENTORY_RECT.x + 5, INVENTORY_RECT.y + 30 + i * 20))

    # UI: Боны
    pygame.draw.rect(screen, YELLOW, BON_DISPLAY_RECT)
    bon_text = font_medium.render(f"Боны: {player.bon}", True, BLACK)
    screen.blit(bon_text, (BON_DISPLAY_RECT.x + 10, BON_DISPLAY_RECT.y + 10))

    # Мини-игра
    '''
    if player.in_mini_game:
        mini_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        mini_screen.fill(BLACK)
        if player.position == 3:
            title = "Кот Учёный"
        elif player.position == 5:
            title = "Царевна Лягушка"
        else:
            title = "Мини-игра"

        text = font_large.render(f"Мини-игра: {title}", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        mini_screen.blit(text, text_rect)
        prompt = font_small.render("Нажмите любую клавишу, чтобы продолжить...", True, WHITE)
        mini_screen.blit(prompt, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 50))
        pygame.display.flip()

        waiting = True
        while waiting:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if ev.type == pygame.KEYDOWN:
                    waiting = False
                    player.exit_mini_game()
                    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    '''

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()