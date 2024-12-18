import pygame
import sys

# Inisialisasi Pygame
pygame.init()

# Konstanta
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 480
BALL_SIZE = 15
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 150
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60

# Posisi awal
INITIAL_BALL_SPEED_X = 5  # Kecepatan awal bola di sumbu X
INITIAL_BALL_SPEED_Y = 5  # Kecepatan awal bola di sumbu Y
ball_speed = [INITIAL_BALL_SPEED_X, INITIAL_BALL_SPEED_Y]
left_paddle_speed = 0
right_paddle_speed = 0
paddle_speed = 7

# Skor
left_score = 0
right_score = 0

# Membuat layar
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong Game")

# Membuat objek
ball = pygame.Rect(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, BALL_SIZE, BALL_SIZE)
left_paddle = pygame.Rect(10, SCREEN_HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(SCREEN_WIDTH - 30, SCREEN_HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)

# Font skor
font = pygame.font.Font(None, 72)

# Pengali kecepatan bola
SPEED_INCREMENT = 1.1 

# Load sound effect
score_sound = pygame.mixer.Sound("Sounds/score.mp3")
paddle_hit_sound = pygame.mixer.Sound("Sounds/paddle_hit.mp3")
wall_hit_sound = pygame.mixer.Sound("Sounds/wall_hit.mp3")

# Fungsi utama
def main():
    global ball_speed, left_paddle_speed, right_paddle_speed, left_score, right_score, ball

    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Kontrol paddle
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    right_paddle_speed = -paddle_speed
                if event.key == pygame.K_DOWN:
                    right_paddle_speed = paddle_speed
                if event.key == pygame.K_w:
                    left_paddle_speed = -paddle_speed
                if event.key == pygame.K_s:
                    left_paddle_speed = paddle_speed
            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_UP, pygame.K_DOWN]:
                    right_paddle_speed = 0
                if event.key in [pygame.K_w, pygame.K_s]:
                    left_paddle_speed = 0
        
        # Update paddle
        left_paddle.y += left_paddle_speed
        right_paddle.y += right_paddle_speed

        # Batasi paddle agar tidak keluar layar
        left_paddle.y = max(10, min(SCREEN_HEIGHT - PADDLE_HEIGHT - 10, left_paddle.y))
        right_paddle.y = max(10, min(SCREEN_HEIGHT - PADDLE_HEIGHT - 10, right_paddle.y))

        # Update bola
        ball.x += ball_speed[0]
        ball.y += ball_speed[1]

        # Pantulan bola di atas dan bawah
        if ball.top <= 10 or ball.bottom >= SCREEN_HEIGHT - 10:
            ball_speed[1] = -ball_speed[1]
            wall_hit_sound.play() 

        # Pantulan bola di paddle
        if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
            ball_speed[0] = -ball_speed[0]
            ball_speed[0] *= SPEED_INCREMENT  # Tingkatkan kecepatan X
            ball_speed[1] *= SPEED_INCREMENT  # Tingkatkan kecepatan Y
            paddle_hit_sound.play()

        # Cek skor jika bola keluar
        if ball.left <= 0:
            right_score += 1
            ball = pygame.Rect(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, BALL_SIZE, BALL_SIZE)
            ball_speed = [INITIAL_BALL_SPEED_X, INITIAL_BALL_SPEED_Y]  # Reset kecepatan bola
            score_sound.play() 

        if ball.right >= SCREEN_WIDTH:
            left_score += 1
            ball = pygame.Rect(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, BALL_SIZE, BALL_SIZE)
            ball_speed = [INITIAL_BALL_SPEED_X, INITIAL_BALL_SPEED_Y]  # Reset kecepatan bola
            score_sound.play() 

        # Gambar semua objek
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, pygame.Rect(0, 0, SCREEN_WIDTH, 10))  # Border atas
        pygame.draw.rect(screen, WHITE, pygame.Rect(0, SCREEN_HEIGHT-10, SCREEN_WIDTH, 10))  # Border bawah
        pygame.draw.rect(screen, WHITE, left_paddle)
        pygame.draw.rect(screen, WHITE, right_paddle)
        pygame.draw.ellipse(screen, WHITE, ball)
        pygame.draw.aaline(screen, WHITE, (SCREEN_WIDTH//2, 0), (SCREEN_WIDTH//2, SCREEN_HEIGHT))

        # Tampilkan skor
        left_text = font.render(str(left_score), True, WHITE)
        right_text = font.render(str(right_score), True, WHITE)
        screen.blit(left_text, (SCREEN_WIDTH//2 - 100, 20))
        screen.blit(right_text, (SCREEN_WIDTH//2 + 50, 20))

        # Update layar
        pygame.display.flip()
        clock.tick(FPS)

# Jalankan permainan
if __name__ == "__main__":
    main()
