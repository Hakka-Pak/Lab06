import pygame
import random
import sys

# Constants
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100
BALL_SIZE = 15
FPS = 60

# Colors
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_NEON_GREEN = (57, 255, 20)
COLOR_YELLOW = (255, 255, 0)

class PongGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Ping Pong - Lab 06")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 36)
        self.large_font = pygame.font.SysFont("Arial", 72)
        self.reset_game()

    def reset_game(self):
        # Paddles
        self.paddle1_y = (WINDOW_HEIGHT - PADDLE_HEIGHT) // 2
        self.paddle2_y = (WINDOW_HEIGHT - PADDLE_HEIGHT) // 2
        self.paddle_speed = 9 # Increased speed

        # Ball
        self.ball_x = WINDOW_WIDTH // 2
        self.ball_y = WINDOW_HEIGHT // 2
        self.initial_ball_speed = 6
        self.ball_speed_x = self.initial_ball_speed * random.choice([1, -1])
        self.ball_speed_y = self.initial_ball_speed * random.choice([1, -1])

        # Scores
        self.score1 = 0
        self.score2 = 0
        self.game_over = False
        self.winner = None

    def reset_ball(self, scorer):
        self.ball_x = WINDOW_WIDTH // 2
        self.ball_y = WINDOW_HEIGHT // 2
        self.ball_speed_x = self.initial_ball_speed if scorer == 2 else -self.initial_ball_speed
        self.ball_speed_y = self.initial_ball_speed * random.choice([1, -1])

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if self.game_over and event.key == pygame.K_r:
                    self.reset_game()

        keys = pygame.key.get_pressed()
        if not self.game_over:
            # Player 1 (W/S)
            if keys[pygame.K_w] and self.paddle1_y > 0:
                self.paddle1_y -= self.paddle_speed
            if keys[pygame.K_s] and self.paddle1_y < WINDOW_HEIGHT - PADDLE_HEIGHT:
                self.paddle1_y += self.paddle_speed
            
            # Player 2 (Arrows)
            if keys[pygame.K_UP] and self.paddle2_y > 0:
                self.paddle2_y -= self.paddle_speed
            if keys[pygame.K_DOWN] and self.paddle2_y < WINDOW_HEIGHT - PADDLE_HEIGHT:
                self.paddle2_y += self.paddle_speed

    def update(self):
        if self.game_over:
            return

        # Move ball
        self.ball_x += self.ball_speed_x
        self.ball_y += self.ball_speed_y

        # Ball collision with top/bottom walls
        if self.ball_y <= 0 or self.ball_y >= WINDOW_HEIGHT - BALL_SIZE:
            self.ball_speed_y *= -1

        # Ball collision with paddles
        ball_rect = pygame.Rect(self.ball_x, self.ball_y, BALL_SIZE, BALL_SIZE)
        paddle1_rect = pygame.Rect(30, self.paddle1_y, PADDLE_WIDTH, PADDLE_HEIGHT)
        paddle2_rect = pygame.Rect(WINDOW_WIDTH - 30 - PADDLE_WIDTH, self.paddle2_y, PADDLE_WIDTH, PADDLE_HEIGHT)

        if ball_rect.colliderect(paddle1_rect):
            self.ball_speed_x = abs(self.ball_speed_x)
            self.ball_speed_x *= 1.1 # Bonus: Speed Up
            self.ball_speed_y *= 1.1
            self.ball_speed_y += (self.ball_y + BALL_SIZE/2 - (self.paddle1_y + PADDLE_HEIGHT/2)) * 0.1
        
        if ball_rect.colliderect(paddle2_rect):
            self.ball_speed_x = -abs(self.ball_speed_x)
            self.ball_speed_x *= 1.1 # Bonus: Speed Up
            self.ball_speed_y *= 1.1
            self.ball_speed_y += (self.ball_y + BALL_SIZE/2 - (self.paddle2_y + PADDLE_HEIGHT/2)) * 0.1

        # Scoring
        if self.ball_x < 0:
            self.score2 += 1
            if self.score2 >= 11:
                self.game_over = True
                self.winner = 2
            else:
                self.reset_ball(2)
        
        if self.ball_x > WINDOW_WIDTH:
            self.score1 += 1
            if self.score1 >= 11:
                self.game_over = True
                self.winner = 1
            else:
                self.reset_ball(1)

    def draw(self):
        self.screen.fill(COLOR_BLACK)

        # Draw net
        for y in range(0, WINDOW_HEIGHT, 40):
            pygame.draw.rect(self.screen, COLOR_WHITE, (WINDOW_WIDTH // 2 - 2, y, 4, 20))

        # Draw paddles (Neon Green)
        pygame.draw.rect(self.screen, COLOR_NEON_GREEN, (30, self.paddle1_y, PADDLE_WIDTH, PADDLE_HEIGHT))
        pygame.draw.rect(self.screen, COLOR_NEON_GREEN, (WINDOW_WIDTH - 30 - PADDLE_WIDTH, self.paddle2_y, PADDLE_WIDTH, PADDLE_HEIGHT))

        # Draw ball (Yellow)
        pygame.draw.rect(self.screen, COLOR_YELLOW, (self.ball_x, self.ball_y, BALL_SIZE, BALL_SIZE))

        # Draw scores
        score1_text = self.font.render(str(self.score1), True, COLOR_WHITE)
        score2_text = self.font.render(str(self.score2), True, COLOR_WHITE)
        self.screen.blit(score1_text, (WINDOW_WIDTH // 4, 20))
        self.screen.blit(score2_text, (3 * WINDOW_WIDTH // 4, 20))

        if self.game_over:
            win_text = self.large_font.render(f"Player {self.winner} Wins!", True, COLOR_WHITE)
            restart_text = self.font.render("Press 'R' to Restart", True, COLOR_WHITE)
            self.screen.blit(win_text, (WINDOW_WIDTH // 2 - 250, WINDOW_HEIGHT // 2 - 50))
            self.screen.blit(restart_text, (WINDOW_WIDTH // 2 - 120, WINDOW_HEIGHT // 2 + 50))

        pygame.display.flip()

    def run(self):
        while True:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = PongGame()
    game.run()
