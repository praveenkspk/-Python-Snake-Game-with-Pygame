import pygame
import sys
import random
import math

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

# Colors
BACKGROUND = (15, 20, 25)
GRID_COLOR = (30, 40, 50)
SNAKE_HEAD = (50, 200, 100)
SNAKE_BODY = (40, 180, 80)
FOOD_COLOR = (220, 80, 60)
TEXT_COLOR = (220, 220, 220)
GAME_OVER_BG = (0, 0, 0, 180)  # Semi-transparent black

# Game settings
FPS = 10
SNAKE_SPEED = GRID_SIZE

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Font setup
font = pygame.font.SysFont("Arial", 25)
title_font = pygame.font.SysFont("Arial", 50, bold=True)

class Snake:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.length = 3
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        self.score = 0
        self.grow_to = 3
        
    def get_head_position(self):
        return self.positions[0]
    
    def update(self):
        head = self.get_head_position()
        x, y = self.direction
        new_x = (head[0] + x) % GRID_WIDTH
        new_y = (head[1] + y) % GRID_HEIGHT
        new_position = (new_x, new_y)
        
        # Game over if snake hits itself
        if new_position in self.positions[1:]:
            return False
            
        self.positions.insert(0, new_position)
        
        if len(self.positions) > self.grow_to:
            self.positions.pop()
            
        return True
    
    def render(self, surface):
        for i, pos in enumerate(self.positions):
            color = SNAKE_HEAD if i == 0 else SNAKE_BODY
            rect = pygame.Rect((pos[0] * GRID_SIZE, pos[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, (20, 30, 40), rect, 1)
            
            # Draw eyes on the snake head
            if i == 0:
                # Determine eye positions based on direction
                dx, dy = self.direction
                eye_size = GRID_SIZE // 5
                
                # Left eye
                left_eye_x = pos[0] * GRID_SIZE + GRID_SIZE // 3
                left_eye_y = pos[1] * GRID_SIZE + GRID_SIZE // 3
                
                # Right eye
                right_eye_x = pos[0] * GRID_SIZE + 2 * GRID_SIZE // 3
                right_eye_y = pos[1] * GRID_SIZE + GRID_SIZE // 3
                
                # Adjust for direction
                if dx == 1:  # Moving right
                    left_eye_y += GRID_SIZE // 3
                    right_eye_y += GRID_SIZE // 3
                elif dx == -1:  # Moving left
                    left_eye_y += GRID_SIZE // 3
                    right_eye_y += GRID_SIZE // 3
                elif dy == 1:  # Moving down
                    left_eye_x += GRID_SIZE // 3
                    right_eye_x -= GRID_SIZE // 3
                elif dy == -1:  # Moving up
                    left_eye_x += GRID_SIZE // 3
                    right_eye_x -= GRID_SIZE // 3
                
                pygame.draw.circle(surface, (0, 0, 0), (left_eye_x, left_eye_y), eye_size)
                pygame.draw.circle(surface, (0, 0, 0), (right_eye_x, right_eye_y), eye_size)

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.randomize_position()
        
    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), 
                         random.randint(0, GRID_HEIGHT - 1))
    
    def render(self, surface):
        rect = pygame.Rect((self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE), 
                          (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, FOOD_COLOR, rect)
        pygame.draw.rect(surface, (180, 50, 30), rect, 1)
        
        # Draw a shine effect
        shine_rect = pygame.Rect((self.position[0] * GRID_SIZE + GRID_SIZE//4, 
                                 self.position[1] * GRID_SIZE + GRID_SIZE//4), 
                                (GRID_SIZE//4, GRID_SIZE//4))
        pygame.draw.ellipse(surface, (255, 200, 180), shine_rect)

def draw_grid(surface):
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(surface, GRID_COLOR, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(surface, GRID_COLOR, (0, y), (WIDTH, y))

def draw_score(surface, score):
    score_text = font.render(f"Score: {score}", True, TEXT_COLOR)
    surface.blit(score_text, (10, 10))

def draw_game_over(surface, score):
    # Semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill(GAME_OVER_BG)
    surface.blit(overlay, (0, 0))
    
    # Game Over text
    game_over_text = title_font.render("GAME OVER", True, (220, 80, 60))
    text_rect = game_over_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
    surface.blit(game_over_text, text_rect)
    
    # Score text
    score_text = font.render(f"Final Score: {score}", True, TEXT_COLOR)
    score_rect = score_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 20))
    surface.blit(score_text, score_rect)
    
    # Restart instruction
    restart_text = font.render("Press SPACE to restart", True, TEXT_COLOR)
    restart_rect = restart_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 70))
    surface.blit(restart_text, restart_rect)

def main():
    snake = Snake()
    food = Food()
    game_over = False
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if game_over and event.key == pygame.K_SPACE:
                    snake.reset()
                    food.randomize_position()
                    game_over = False
                elif not game_over:
                    if event.key == pygame.K_UP and snake.direction != (0, 1):
                        snake.direction = (0, -1)
                    elif event.key == pygame.K_DOWN and snake.direction != (0, -1):
                        snake.direction = (0, 1)
                    elif event.key == pygame.K_LEFT and snake.direction != (1, 0):
                        snake.direction = (-1, 0)
                    elif event.key == pygame.K_RIGHT and snake.direction != (-1, 0):
                        snake.direction = (1, 0)
        
        if not game_over:
            # Update snake position
            if not snake.update():
                game_over = True
            
            # Check if snake ate food
            if snake.get_head_position() == food.position:
                snake.grow_to += 1
                snake.score += 10
                food.randomize_position()
                # Make sure food doesn't appear on snake
                while food.position in snake.positions:
                    food.randomize_position()
        
        # Draw everything
        screen.fill(BACKGROUND)
        draw_grid(screen)
        snake.render(screen)
        food.render(screen)
        draw_score(screen, snake.score)
        
        if game_over:
            draw_game_over(screen, snake.score)
        
        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()