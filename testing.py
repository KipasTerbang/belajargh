import math
import pygame
from pygame import gfxdraw

pygame.init()

SCREEN_WIDTH = 1260
SCREEN_HEIGHT = 720
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("ILUSTRASI GLBB")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
KUNING = (255, 255, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 200)
BLACK = (0, 0, 0)
GREY = (64, 64, 64)

circle_radius = 50
init_circle_radius = circle_radius

# Slider horizontal di bagian bawah layar
horizontal_slider_rect = pygame.Rect(50, SCREEN_HEIGHT - 50, SCREEN_WIDTH - 100, 20)
horizontal_slider_grabbed = False
min_slider_x = horizontal_slider_rect.x - circle_radius
max_slider_x = horizontal_slider_rect.x + horizontal_slider_rect.width - circle_radius

# Slider vertikal di sebelah kanan dinding
vertical_slider_rect = pygame.Rect(SCREEN_WIDTH - 25, 20, 20, SCREEN_HEIGHT//1.1 - 80)
vertical_slider_grabbed = False
min_slider_y = vertical_slider_rect.y - circle_radius
max_slider_y = vertical_slider_rect.y + vertical_slider_rect.height - circle_radius

circle_center = (horizontal_slider_rect.x + circle_radius, round(SCREEN_HEIGHT / 1.31))

a = 1
velocity = 0  # Kecepatan pergerakan lingkaran (awalnya 0)
rotation_angle = 0  # Sudut rotasi lingkaran

gravity = 0.98 # Gravitasi, dapat disesuaikan sesuai kebutuhan
velocity_y = 0  # Kecepatan awal pada sumbu y

# Kotak input menggunakan pygame.rect
input_rect = pygame.Rect((SCREEN_WIDTH//2)-20, SCREEN_HEIGHT-100, 100, 30)
input_font = pygame.font.Font(None, 24)
input_text = ""


circle_height = SCREEN_HEIGHT - 120 - circle_center[1]  # Menghitung ketinggian bola dari dasar layar
distance_percentage = (SCREEN_HEIGHT - 120 - circle_center[1]) / (SCREEN_HEIGHT - 120)  # Menghitung persentase jarak bola dari batas atas layar
circle_radius = max(30, init_circle_radius * (1.2 - distance_percentage))

def lingkaran():
    gfxdraw.aacircle(SCREEN, round(circle_center[0]), round(circle_center[1]), round(circle_radius), KUNING)
    gfxdraw.filled_circle(SCREEN, round(circle_center[0]), round(circle_center[1]), round(circle_radius), KUNING)


def sumbu():
    line_length = circle_radius
    x = circle_center[0]
    y = circle_center[1]

    rotation_angle_rad = math.radians(rotation_angle)

    x_line_start = (x - line_length * math.cos(rotation_angle_rad), y - line_length * math.sin(rotation_angle_rad))
    x_line_end = (x + line_length * math.cos(rotation_angle_rad), y + line_length * math.sin(rotation_angle_rad))

    y_line_start = (x - line_length * math.sin(rotation_angle_rad), y + line_length * math.cos(rotation_angle_rad))
    y_line_end = (x + line_length * math.sin(rotation_angle_rad), y - line_length * math.cos(rotation_angle_rad))

    pygame.draw.aaline(SCREEN, RED, x_line_start, x_line_end)
    pygame.draw.aaline(SCREEN, BLUE, y_line_start, y_line_end)


def draw_input_box():
    pygame.draw.rect(SCREEN, WHITE, input_rect)
    pygame.draw.rect(SCREEN, BLACK, input_rect, 2)
    input_surface = input_font.render(str(input_text), True, BLACK)
    SCREEN.blit(input_surface, (input_rect.x + 5, input_rect.y + 5))


def draw_horizontal_slider():
    pygame.draw.rect(SCREEN, WHITE, horizontal_slider_rect)
    pygame.draw.rect(SCREEN, BLACK, horizontal_slider_rect, 2)
    slider_grabbed_color = BLUE if horizontal_slider_grabbed else GREY
    slider_x = horizontal_slider_rect.x + (horizontal_slider_rect.width - 10) * (
            (circle_center[0] - circle_radius) / (SCREEN_WIDTH - circle_radius * 2))
    slider_rect = pygame.Rect(slider_x, horizontal_slider_rect.y, 20, horizontal_slider_rect.height)
    pygame.draw.rect(SCREEN, slider_grabbed_color, slider_rect)


def draw_vertical_slider():
    pygame.draw.rect(SCREEN, WHITE, vertical_slider_rect)
    pygame.draw.rect(SCREEN, BLACK, vertical_slider_rect, 2)
    slider_grabbed_color = BLUE if vertical_slider_grabbed else GREY
    slider_y = vertical_slider_rect.y + (vertical_slider_rect.height - 10) * (
                (circle_center[1] - circle_radius) / (SCREEN_HEIGHT//1.185 - circle_radius * 2))
    slider_rect = pygame.Rect(vertical_slider_rect.x, slider_y, vertical_slider_rect.width, 20)
    pygame.draw.rect(SCREEN, slider_grabbed_color, slider_rect)


def update_velocity():
    global velocity
    try:
        velocity = int(input_text)
    except ValueError:
        print("Invalid input. Please enter a valid number.")

# Variabel penyimpanan
original_velocity = velocity
original_a = a
original_velocity_y = velocity_y
original_circle_radius = circle_radius


def main():
    global circle_center, velocity, rotation_angle, a, input_text, horizontal_slider_grabbed, gravity, vertical_slider_grabbed, velocity_y, circle_radius, gravity_input_text, circle_height
    run = True
    velocity_setx = True  # Tambahkan variabel untuk memeriksa apakah kecepatan telah diatur
    velocity_sety = True

    while run:
        SCREEN.fill(WHITE)
        events = pygame.event.get()

        lingkaran()
        sumbu()
        gfxdraw.line(SCREEN, 0, 600, SCREEN_WIDTH, 600, BLACK)

        draw_horizontal_slider()
        draw_vertical_slider()
        draw_input_box()
        pygame.display.flip()

        for event in events:
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    update_velocity()
                    # input_text = ""
                elif event.key == pygame.K_DOWN:
                    velocity_sety = True
                elif event.key == pygame.K_DELETE:
                    input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if horizontal_slider_rect.collidepoint(event.pos):
                    horizontal_slider_grabbed = True
                elif vertical_slider_rect.collidepoint(event.pos):
                    vertical_slider_grabbed = True
            elif event.type == pygame.MOUSEBUTTONUP:
                horizontal_slider_grabbed = False
                vertical_slider_grabbed = False
            elif event.type == pygame.MOUSEMOTION:
                if horizontal_slider_grabbed:
                    slider_x = event.pos[0] - circle_radius
                    slider_x = max(min_slider_x, min(max_slider_x, slider_x))
                    circle_center = (slider_x + circle_radius, circle_center[1])
                    rotation_angle = round(slider_x)
                elif vertical_slider_grabbed:
                    velocity_sety = False
                    slider_y = event.pos[1] - circle_radius
                    slider_y = max(min_slider_y + (circle_radius//2) + 5, min(max_slider_y-(circle_radius*2)-10, slider_y))
                    circle_center = (circle_center[0], slider_y + circle_radius)
        
        if velocity_setx:  # Perbarui posisi lingkaran hanya jika kecepatan telah diatur
            circle_center = (circle_center[0] + velocity, circle_center[1])

            # Memeriksa batas dinding pada sumbu x
            if circle_center[0] - circle_radius <= 0 or circle_center[0] + circle_radius >= SCREEN_WIDTH:
                velocity *= -1  # Mengubah arah kecepatan bola agar bola memantul
                circle_center = (
                max(circle_radius, min(SCREEN_WIDTH - circle_radius, circle_center[0])), circle_center[1])  # Memastikan bola tidak melewati batas dinding

            # Mengurangi kecepatan bola seiring waktu
            if velocity < 0:
                velocity += a
                velocitytemp = velocity
                input_text = velocitytemp * -1
            elif velocity > 0:
                velocity -= a
                velocitytemp = velocity
                input_text = velocitytemp 
            else:
                velocity = 0

        if velocity_sety:
            # Memperbarui posisi lingkaran dengan kecepatan pada sumbu y
            circle_center = (circle_center[0], circle_center[1] + velocity_y)

            circle_height = SCREEN_HEIGHT - 120 - circle_center[1]  # Menghitung ketinggian bola dari dasar layar
            # Menghitung persentase jarak bola dari batas atas layar
            distance_percentage = (SCREEN_HEIGHT - 120 - circle_center[1]) / (SCREEN_HEIGHT - 120)
            circle_radius = max(30, init_circle_radius * (1.2 - distance_percentage))

            # Memeriksa batas dinding pada sumbu y
            if circle_center[1] + circle_radius > SCREEN_HEIGHT - 120:
                if velocity_y > 0:
                    velocity_y *= -0.9  # Mengubah arah kecepatan bola dan mengurangi kecepatannya
                    circle_center = (circle_center[0], SCREEN_HEIGHT - 120 - circle_radius)  # Memastikan bola tidak melewati batas bawah
                    if velocity == 0:
                        circle_center = (circle_center[0], SCREEN_HEIGHT - 120 - circle_radius)

            # Mengatur kecepatan pada sumbu y
            velocity_y += gravity

            # Mengurangi kecepatan bola seiring waktu
            if velocity > 0:
                velocity_y -= abs(a)  # Mengurangi kecepatan positif
                if velocity_y < 0:
                    velocity_y = 0  # Menghentikan bola jika kecepatannya menjadi negatif
            elif velocity_y < 0:
                velocity_y += abs(a)  # Mengurangi kecepatan negatif
                if velocity_y > 0:
                    velocity_y = 0  # Menghentikan bola jika kecepatannya menjadi positif
            

            # Memperbarui sudut rotasi lingkaran berdasarkan pergerakan lingkaran
        rotation_angle += velocity

        if velocity == 0:
                # Mengembalikan nilai-nilai asli
            velocity = original_velocity
            a = original_a
                # velocity_y = original_velocity_y
            circle_radius = original_circle_radius
                
            circle_height = SCREEN_HEIGHT - 120 - circle_center[1]  # Menghitung ketinggian bola dari dasar layar
            distance_percentage = (SCREEN_HEIGHT - 120 - circle_center[1]) / (SCREEN_HEIGHT - 120)  # Menghitung persentase jarak bola dari batas atas layar
            circle_radius = max(30, init_circle_radius * (1.2 - distance_percentage))

        clock.tick(30)


if __name__ == "__main__":
    main()

pygame.quit()
