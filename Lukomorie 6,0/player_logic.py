# player_logic.py
import random

class PlayerLogic:
    def __init__(self, name="Игрок"):
        self.name = name
        self.bon = 0
        self.inventory = [None, None, None]
        self.skip_turn = False
        self.in_mini_game = False
        self.needs_extra_roll = False
        self.current_path_index = 0
        self.path_points = []
        self.load_path_points()

    def load_path_points(self):
        """Загружает путь из файла path_points.txt — только x y"""
        try:
            with open("path_points.txt", "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#") or "..." in line:
                        continue  # Пропускаем комментарии и "и так далее"
                    parts = line.split()
                    if len(parts) >= 2:
                        try:
                            x = int(parts[0])
                            y = int(parts[1])
                            self.path_points.append((x, y))
                        except ValueError:
                            continue
        except FileNotFoundError:
            print(" path_points.txt не найден. Создаётся тестовый путь.")
            for i in range(100):
                self.path_points.append((100 + i*10, 150 + i*5))

        # Дополним до 100 точек, если нужно
        while len(self.path_points) < 100:
            last_x, last_y = self.path_points[-1] if self.path_points else (100, 150)
            dx = 10 if len(self.path_points) < 2 else (self.path_points[-1][0] - self.path_points[-2][0])
            dy = 5 if len(self.path_points) < 2 else (self.path_points[-1][1] - self.path_points[-2][1])
            self.path_points.append((last_x + dx, last_y + dy))

        print(f"Загружено {len(self.path_points)} точек.")

    def move_by_steps(self, steps):
        """Переместиться на N шагов ПО СПИСКУ (индекс + steps)"""
        if self.path_points:
            self.current_path_index = min(len(self.path_points) - 1, self.current_path_index + steps)
            print(f"Ход: +{steps}, новая позиция: индекс {self.current_path_index}")

    # Все остальные методы — пустышки
    def handle_cell_after_move(self): pass
    def handle_extra_roll(self, dice_roll): pass
    def _jump_to_cell(self, target_cell): pass
    def get_treasure(self): pass
    def get_big_treasure(self): pass
    def handle_goose(self): pass
    def handle_repkа_question(self, answer="7"): return False
    def handle_baba_yaga(self): return False
    def handle_waystone(self, dice_roll): pass
    def handle_crossroad(self, dice_roll): pass
    def start_mini_game(self, title): pass
    def exit_mini_game(self): pass