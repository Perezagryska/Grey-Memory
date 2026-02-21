import pygame
import asyncio
import sys

# Инициализация
pygame.init()

# Настройки экрана (в вебе/телефоне будет подстраиваться под окно)
# Для Mini App лучше использовать фиксированное соотношение или полное окно
screen = pygame.display.set_mode((1280, 720)) 
WIDTH, HEIGHT = 1280, 720
pygame.display.set_caption("Grey Memory")

# Цвета
WHITE = (240, 240, 240)
BLACK = (15, 15, 15)
GRAY = (60, 60, 60)
LIGHT_GRAY = (200, 200, 200)

# Шрифты (используем стандартные, чтобы везде работало)
font_title = pygame.font.SysFont("sans-serif", 90)
font_menu = pygame.font.SysFont("sans-serif", 45)
font_easter = pygame.font.SysFont("sans-serif", 15)

# Глобальные переменные состояния
class GameState:
    state = 'MENU'
    device = 'PC'
    theme = 'LIGHT'
    player_x = WIDTH // 2
    player_y = HEIGHT - 150
    player_speed = 10
    player_size = (120, 200) # Уменьшили рост, как ты просил

game = GameState()

# Загрузка персонажа
try:
    player_img = pygame.image.load("player.png")
    player_img = pygame.transform.scale(player_img, game.player_size)
except:
    player_img = pygame.Surface(game.player_size)
    player_img.fill(GRAY)

player_rect = player_img.get_rect()

# Кнопки (позиции)
btn_play = pygame.Rect(WIDTH//2 - 125, HEIGHT//2 - 40, 250, 70)
btn_pc = pygame.Rect(WIDTH//2 - 270, HEIGHT//2 + 60, 250, 70)
btn_android = pygame.Rect(WIDTH//2 + 20, HEIGHT//2 + 60, 250, 70)
btn_theme = pygame.Rect(WIDTH//2 - 125, HEIGHT//2 + 160, 250, 60)

# Кнопки для Андроида (сенсорные зоны)
left_zone = pygame.Rect(50, HEIGHT - 180, 200, 120)
right_zone = pygame.Rect(WIDTH - 250, HEIGHT - 180, 200, 120)

async def main():
    clock = pygame.time.Clock()

    while True:
        # 1. Цветовая схема
        bg_color = WHITE if game.theme == 'LIGHT' else BLACK
        main_color = BLACK if game.theme == 'LIGHT' else WHITE
        
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        # 2. Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game.state == 'MENU':
                    if btn_play.collidepoint(mouse_pos):
                        game.state = 'CHOOSE_DEVICE'
                elif game.state == 'CHOOSE_DEVICE':
                    if btn_pc.collidepoint(mouse_pos):
                        game.device = 'PC'
                        game.state = 'GAME'
                    elif btn_android.collidepoint(mouse_pos):
                        game.device = 'ANDROID'
                        game.state = 'GAME'
                    elif btn_theme.collidepoint(mouse_pos):
                        game.theme = 'DARK' if game.theme == 'LIGHT' else 'LIGHT'

        # 3. Логика игры
        if game.state == 'GAME':
            keys = pygame.key.get_pressed()
            move_left = keys[pygame.K_LEFT] or (game.device == 'ANDROID' and mouse_click[0] and left_zone.collidepoint(mouse_pos))
            move_right = keys[pygame.K_RIGHT] or (game.device == 'ANDROID' and mouse_click[0] and right_zone.collidepoint(mouse_pos))

            if move_left and player_rect.left > 0:
                player_rect.x -= game.player_speed
            if move_right and player_rect.right < WIDTH:
                player_rect.x += game.player_speed

        # 4. Отрисовка
        screen.fill(BLACK if game.state != 'GAME' else bg_color)

        if game.state == 'MENU':
            title = font_title.render("Grey Memory", True, WHITE)
            screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//4))
            
            pygame.draw.rect(screen, WHITE, btn_play, 2, border_radius=10)
            txt = font_menu.render("Начать", True, WHITE)
            screen.blit(txt, (btn_play.centerx - txt.get_width()//2, btn_play.centery - txt.get_height()//2))

        elif game.state == 'CHOOSE_DEVICE':
            pygame.draw.rect(screen, WHITE, btn_pc, 2, border_radius=10)
            pygame.draw.rect(screen, WHITE, btn_android, 2, border_radius=10)
            pygame.draw.rect(screen, WHITE, btn_theme, 2, border_radius=10)
            
            txt_pc = font_menu.render("ПК", True, WHITE)
            txt_and = font_menu.render("Андроид", True, WHITE)
            txt_th = font_menu.render(f"Тема: {game.theme}", True, WHITE)
            
            screen.blit(txt_pc, (btn_pc.centerx - txt_pc.get_width()//2, btn_pc.centery - txt_pc.get_height()//2))
            screen.blit(txt_and, (btn_android.centerx - txt_and.get_width()//2, btn_android.centery - txt_and.get_height()//2))
            screen.blit(txt_th, (btn_theme.centerx - txt_th.get_width()//2, btn_theme.centery - txt_th.get_height()//2))

        elif game.state == 'GAME':
            # Пол
            pygame.draw.line(screen, main_color, (0, HEIGHT - 150), (WIDTH, HEIGHT - 150), 5)
            
            # Игрок
            player_rect.bottom = HEIGHT - 150
            screen.blit(player_img, player_rect)
            
            # Кнопки для Андроид
            if game.device == 'ANDROID':
                pygame.draw.rect(screen, main_color, left_zone, 2, border_radius=15)
                pygame.draw.rect(screen, main_color, right_zone, 2, border_radius=15)
                l_arr = font_menu.render("<", True, main_color)
                r_arr = font_menu.render(">", True, main_color)
                screen.blit(l_arr, (left_zone.centerx - l_arr.get_width()//2, left_zone.centery - l_arr.get_height()//2))
                screen.blit(r_arr, (right_zone.centerx - r_arr.get_width()//2, right_zone.centery - r_arr.get_height()//2))

        # Пасхалка
        easter_col = (50, 50, 50) if game.theme == 'LIGHT' else (100, 100, 100)
        easter = font_easter.render("Марина любит пельмени", True, easter_col)
        screen.blit(easter, (WIDTH - 180, HEIGHT - 30))

        pygame.display.flip()
        
        # Важно для Web-версии!
        await asyncio.sleep(0) 
        clock.tick(60)

# Запуск асинхронного цикла
if __name__ == "__main__":
    asyncio.run(main())
