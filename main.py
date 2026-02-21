import pygame
import asyncio
import sys

pygame.init()

WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Grey Memory")

WHITE = (240, 240, 240)
BLACK = (15, 15, 15)
GRAY = (60, 60, 60)

font_title = pygame.font.SysFont("sans-serif", 80)
font_menu = pygame.font.SysFont("sans-serif", 40)
font_easter = pygame.font.SysFont("sans-serif", 15)

class GameState:
    def __init__(self):
        self.state = 'MENU'
        self.device = 'PC'
        self.theme = 'LIGHT'
        self.player_size = (120, 200)

game = GameState()

try:
    player_img = pygame.image.load("player.png").convert_alpha()
    player_img = pygame.transform.scale(player_img, game.player_size)
except:
    player_img = pygame.Surface(game.player_size)
    player_img.fill(GRAY)

player_rect = player_img.get_rect()
player_rect.bottom = HEIGHT - 150
player_rect.centerx = WIDTH // 2

btn_play = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 - 35, 200, 70)
btn_pc = pygame.Rect(WIDTH//2 - 250, HEIGHT//2 + 80, 200, 70)
btn_android = pygame.Rect(WIDTH//2 + 50, HEIGHT//2 + 80, 200, 70)

async def main():
    clock = pygame.time.Clock()
    
    while True:
        bg_color = WHITE if game.theme == 'LIGHT' else BLACK
        main_color = BLACK if game.theme == 'LIGHT' else WHITE
        
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

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

        if game.state == 'GAME':
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                player_rect.x -= 10
            if keys[pygame.K_RIGHT]:
                player_rect.x += 10

        screen.fill(BLACK if game.state != 'GAME' else bg_color)

        if game.state == 'MENU':
            txt = font_title.render("Grey Memory", True, WHITE)
            screen.blit(txt, (WIDTH//2 - txt.get_width()//2, HEIGHT//3))
            pygame.draw.rect(screen, WHITE, btn_play, 2)
            lbl = font_menu.render("Играть", True, WHITE)
            screen.blit(lbl, (btn_play.centerx - lbl.get_width()//2, btn_play.centery - lbl.get_height()//2))

        elif game.state == 'CHOOSE_DEVICE':
            pygame.draw.rect(screen, WHITE, btn_pc, 2)
            pygame.draw.rect(screen, WHITE, btn_android, 2)
            p_txt = font_menu.render("ПК", True, WHITE)
            a_txt = font_menu.render("Андроид", True, WHITE)
            screen.blit(p_txt, (btn_pc.centerx - p_txt.get_width()//2, btn_pc.centery - p_txt.get_height()//2))
            screen.blit(a_txt, (btn_android.centerx - a_txt.get_width()//2, btn_android.centery - a_txt.get_height()//2))

        elif game.state == 'GAME':
            pygame.draw.line(screen, main_color, (0, HEIGHT - 150), (WIDTH, HEIGHT - 150), 4)
            screen.blit(player_img, player_rect)

        easter = font_easter.render("Марина любит пельмени", True, (80, 80, 80))
        screen.blit(easter, (WIDTH - 180, HEIGHT - 25))

        pygame.display.flip()
        
        await asyncio.sleep(0) 
        clock.tick(60)

if __name__ == "__main__":
    asyncio.run(main())
