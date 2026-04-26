from random import randint
import pygame


# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона — чёрный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)
# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)
# Цвет яблока
APPLE_COLOR = (255, 0, 0)
# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')
# Настройка времени:
clock = pygame.time.Clock()



class GameObject:
    """Базовый класс, от которого наследуются все объекты.
    Содержит общие атрибуты: позиция и цвет.
    """

    def __init__(self, position=None, body_color=None):
        """Конструктор базового игрового объекта.

        Аргументы:
            position (tuple): координаты.
            body_color (tuple): цвет.
        """
        if position is None:
            self.position = (320, 240)
        else:
            self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """Абстрактный метод: для отрисовки объекта на экране.

        Аргумент:
            surface (pygame.Surface): поверхность, на которой рисуем.
        """
        pass



class Apple(GameObject):
    """Класс Apple. Наследуется от GameObject.
    Появляется в случайном месте поля.
    """

    def __init__(self):
        super().__init__(position=None, body_color=APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайные координаты для яблока."""
        max_x = SCREEN_WIDTH - GRID_SIZE
        max_y = SCREEN_HEIGHT - GRID_SIZE
        x = randint(0, max_x // GRID_SIZE - 1) * GRID_SIZE
        y = randint(0, max_y // GRID_SIZE - 1) * GRID_SIZE
        self.position = (x, y)

    def draw(self, surface):
        """Отрисовка яблока на игровом поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)



class Snake(GameObject):
    """Класс Snake. Наследуется от GameObject.
    Представляет змейку в игре.
    """

    def __init__(self):
        super().__init__(position=(320, 240), body_color=SNAKE_COLOR)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Движение змейки по игровому полю."""
        head_x, head_y = self.positions[0]
        dx, dy = self.direction
        new_position = (
            (head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_position)
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self, surface):
        """Отрисовка змейки на игровом поле."""
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сброс змейки к начальному состоянию."""
        self.length = 1
        self.positions = [(320, 240)]
        self.direction = RIGHT
        self.next_direction = None



def handle_keys(snake):
    """Обработка нажатий клавиш для управления змейкой.

    Аргумент:
        snake (Snake): объект змейки.

    Возвращает:
        bool: True, если игра продолжается, False — если нужно выйти.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT
    return True



def main():
    """Основная функция игры."""
    snake = Snake()
    apple = Apple()

    while True:
        if not handle_keys(snake):
            break

        snake.update_direction()
        snake.move()

        # Проверка столкновения головы змейки с яблоком
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
            # Убедимся, что яблоко не появляется на змейке
            while apple.position in snake.positions:
                apple.randomize_position()

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)

        pygame.display.update()
        clock.tick(SPEED)



if __name__ == '__main__':
    main()
