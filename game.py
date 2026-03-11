import pygame
import random
import sys

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
FPS = 10

# Colors
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GREEN_BODY = (34, 139, 34)
COLOR_GREEN_HEAD = (50, 205, 50)
COLOR_RED_FOOD = (255, 0, 0)
COLOR_RED_HIGHLIGHT = (255, 100, 100)
COLOR_RED_SHADOW = (150, 0, 0)

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Snake Game - Lab 06")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24)
        self.large_font = pygame.font.SysFont("Arial", 72)
        self.reset_game()

    def reset_game(self):
        self.snake = [(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)]
        self.direction = pygame.K_d
        self.score = 0
        self.game_over = False
        self.food_list = []
        for _ in range(3):
            self.spawn_food()

    def spawn_food(self):
        while True:
            x = random.randrange(0, WINDOW_WIDTH, GRID_SIZE)
            y = random.randrange(0, WINDOW_HEIGHT, GRID_SIZE)
            if (x, y) not in self.snake and (x, y) not in self.food_list:
                self.food_list.append((x, y))
                break

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_r:
                        self.reset_game()
                else:
                    if event.key in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]:
                        # Prevent reversing direction
                        if (event.key == pygame.K_w and self.direction != pygame.K_s) or \
                           (event.key == pygame.K_s and self.direction != pygame.K_w) or \
                           (event.key == pygame.K_a and self.direction != pygame.K_d) or \
                           (event.key == pygame.K_d and self.direction != pygame.K_a):
                            self.direction = event.key

    def update(self):
        if self.game_over:
            return

        # Calculate new head position
        head_x, head_y = self.snake[0]
        if self.direction == pygame.K_w:
            head_y -= GRID_SIZE
        elif self.direction == pygame.K_s:
            head_y += GRID_SIZE
        elif self.direction == pygame.K_a:
            head_x -= GRID_SIZE
        elif self.direction == pygame.K_d:
            head_x += GRID_SIZE

        new_head = (head_x, head_y)

        # Check collisions
        if (head_x < 0 or head_x >= WINDOW_WIDTH or
            head_y < 0 or head_y >= WINDOW_HEIGHT or
            new_head in self.snake):
            self.game_over = True
            return

        self.snake.insert(0, new_head)

        # Check food collision
        food_eaten = False
        if new_head in self.food_list:
            self.food_list.remove(new_head)
            self.score += 10
            self.spawn_food()
            food_eaten = True
        
        if not food_eaten:
            self.snake.pop()

    def draw(self):
        self.screen.fill(COLOR_BLACK)

        # Draw Snake
        for i, (x, y) in enumerate(self.snake):
            color = COLOR_GREEN_HEAD if i == 0 else COLOR_GREEN_BODY
            pygame.draw.rect(self.screen, color, (x, y, GRID_SIZE, GRID_SIZE))

        # Draw Food
        for x, y in self.food_list:
            # Simple 3D effect (circle with highlight)
            center = (x + GRID_SIZE // 2, y + GRID_SIZE // 2)
            radius = GRID_SIZE // 2 - 2
            pygame.draw.circle(self.screen, COLOR_RED_SHADOW, center, radius)
            pygame.draw.circle(self.screen, COLOR_RED_FOOD, center, radius - 1)
            pygame.draw.circle(self.screen, COLOR_RED_HIGHLIGHT, (center[0] - 3, center[1] - 3), radius // 3)

        # Draw UI
        score_text = self.font.render(f"Score: {self.score}", True, COLOR_WHITE)
        food_text = self.font.render(f"Food Items: {len(self.food_list)}", True, COLOR_WHITE)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(food_text, (10, 40))

        if self.game_over:
            over_text = self.large_font.render("GAME OVER", True, COLOR_WHITE)
            restart_text = self.font.render("Press 'R' to Restart", True, COLOR_WHITE)
            self.screen.blit(over_text, (WINDOW_WIDTH // 2 - 180, WINDOW_HEIGHT // 2 - 50))
            self.screen.blit(restart_text, (WINDOW_WIDTH // 2 - 90, WINDOW_HEIGHT // 2 + 30))

        pygame.display.flip()

    def run(self):
        while True:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = SnakeGame()
    game.run()
