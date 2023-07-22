import pygame
import sys

# Constants
WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100
BALL_SIZE = 70
PADDLE_SPEED = 5
BALL_SPEED_X, BALL_SPEED_Y = 3.75, 3.75
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WINNING_SCORE = 5

# Initialize pygame
pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong Game")

# Loading images
basketball_image = pygame.image.load("basketball.png")
basketball_image = pygame.transform.scale(basketball_image, (BALL_SIZE, BALL_SIZE))

def draw_board(paddle_a, paddle_b, ball, score_a, score_b, game_over):
    window.fill(BLACK)
    pygame.draw.rect(window, BLUE, (paddle_a[0], paddle_a[1], PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(window, RED, (paddle_b[0], paddle_b[1], PADDLE_WIDTH, PADDLE_HEIGHT))
    
    if not game_over and ball is not None:
        window.blit(basketball_image, (ball[0] - BALL_SIZE // 2, ball[1] - BALL_SIZE // 2))
    
    font = pygame.font.Font(None, 74)
    score_display = font.render(f"Blue {score_a} - {score_b} Red", True, WHITE)
    window.blit(score_display, (WIDTH // 2 - score_display.get_width() // 2, 20))
    
    if game_over:
        game_over_text = font.render("Game Over", True, WHITE)
        window.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
        winner_text = font.render(f"{ 'Blue' if score_a >= WINNING_SCORE else 'Red' } wins!", True, WHITE)
        window.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2 + 50))

    pygame.display.update()

def move_paddle(paddle, direction):
    paddle[1] += direction
    paddle[1] = max(0, min(HEIGHT - PADDLE_HEIGHT, paddle[1]))

def main():
    # Initial Positions & Velocities
    paddle_a = [50, HEIGHT // 2 - PADDLE_HEIGHT // 2]
    paddle_b = [WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2]
    ball = [WIDTH // 2, HEIGHT // 2]
    ball_velocity = [BALL_SPEED_X, BALL_SPEED_Y]

    score_a = 0
    score_b = 0

    game_over = False

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            move_paddle(paddle_a, -PADDLE_SPEED)
        if keys[pygame.K_s]:
            move_paddle(paddle_a, PADDLE_SPEED)
        if keys[pygame.K_UP]:
            move_paddle(paddle_b, -PADDLE_SPEED)
        if keys[pygame.K_DOWN]:
            move_paddle(paddle_b, PADDLE_SPEED)

        if not game_over and ball is not None:
            ball[0] += ball_velocity[0]
            ball[1] += ball_velocity[1]

            # Ball Collisions - Top & Bottom
            if ball[1] <= 0 or ball[1] >= HEIGHT:
                ball_velocity[1] = -ball_velocity[1]
            
            # Ball Collision - Paddles
            if paddle_a[0] + PADDLE_WIDTH >= ball[0] >= paddle_a[0] and paddle_a[1] + PADDLE_HEIGHT >= ball[1] >= paddle_a[1]:
                ball_velocity[0] = abs(ball_velocity[0])
            elif paddle_b[0] <= ball[0] <= paddle_b[0] + PADDLE_WIDTH and paddle_b[1] + PADDLE_HEIGHT >= ball[1] >= paddle_b[1]:
                ball_velocity[0] = -abs(ball_velocity[0])

            # Ball Bounds
            if ball[0] <= 0:
                score_b += 1
                ball = [WIDTH // 2, HEIGHT // 2]
                ball_velocity = [BALL_SPEED_X, BALL_SPEED_Y]
            elif ball[0] >= WIDTH:
                score_a += 1
                ball = [WIDTH // 2, HEIGHT // 2]
                ball_velocity = [-BALL_SPEED_X, BALL_SPEED_Y]

            if score_a >= WINNING_SCORE or score_b >= WINNING_SCORE:
                game_over = True

        draw_board(paddle_a, paddle_b, ball, score_a, score_b, game_over)

        if game_over:
            pygame.time.delay(2000)
            pygame.quit()
            sys.exit()

        clock.tick(90)

if __name__ == "__main__":
    main()
