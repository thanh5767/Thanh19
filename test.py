import pygame
import sys
import math

pygame.init()

# Cấu hình cửa sổ
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Slash VFX')

# Màu sắc
white = (255, 255, 255)

# Hàm vẽ hiệu ứng slash
def draw_slash(x, y, length, angle):
    # Chuyển đổi góc sang radian
    angle_rad = math.radians(angle)
    
    # Tính toán các điểm cuối của đường slash
    end_x = x + length * math.cos(angle_rad)
    end_y = y - length * math.sin(angle_rad)
    
    # Vẽ đường slash
    pygame.draw.line(screen, white, (x, y), (end_x, end_y), 5)

# Vòng lặp chính
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Hiển thị frame của hiệu ứng slash
    screen.fill((0, 0, 0))  # Màu nền đen

    # Vẽ hiệu ứng slash
    draw_slash(width // 2, height // 2, 100, pygame.time.get_ticks() % 360)

    pygame.display.flip()
    pygame.time.Clock().tick(60)  # Giới hạn frames per second
