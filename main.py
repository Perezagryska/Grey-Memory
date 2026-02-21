import pygame
import asyncio
import sys

pygame.init()

WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))

WHITE = (240, 240, 240)
BLACK = (15, 15, 15)
GRAY = (60, 60, 60)

font_title = pygame.font.SysFont("sans-serif", 80)
font_menu = pygame.font.SysFont("sans-serif", 40)

state = 'MENU'
device = 'PC'

try:
    player_img = pygame.image.load("player.png").convert_alpha()
    player_img = pygame.transform.scale(player_img, (120, 200))
except:
    player_img = pygame.Surface((120, 200))
    player_img.fill(GRAY)

player_rect = player_img.get_rect()
player_rect.bottom = HEIGHT - 150
player_rect.centerx = WIDTH // 2

btn_play = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 - 35, 200, 70)
btn_pc = pygame.Rect(WIDTH//2 - 250, HEIGHT//2 + 80, 200, 70)
btn_android = pygame.Rect(WIDTH//2 + 50, HEIGHT//2 + 80, 200, 70)

async def main():
    global state, device
    clock = pygame.time.Clock()
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if state == 'MENU':
                    if btn_play.collidepoint(mouse_pos):
                        state = 'CHOOSE_DEVICE'
                elif state == 'CHOOSE_DEVICE':
                    if btn_pc.collidepoint(mouse_pos):
                        device = 'PC'
                        state = 'GAME'
                    elif btn_android.collidepoint(mouse_pos):
                        device = 'ANDROID'
                        state = 'GAME'

        screen.fill(BLACK)

        if state == 'MENU':
            txt = font_title.render("Grey Memory", True, WHITE)
            screen.blit(txt, (WIDTH//2 - txt.get_width()//2, HEIGHT//3))
            pygame.draw.rect(screen, WHITE, btn_play, 2)
            lbl = font_menu.render("Играть", True, WHITE)
            screen.blit(lbl, (btn_play.centerx - lbl.get_width()//2, btn_play.centery - lbl.get_height()//2))

        elif state == 'CHOOSE_DEVICE':
            pygame.draw.rect(screen, WHITE, btn_pc, 2)
            pygame.draw.rect(screen, WHITE, btn_android, 2)
            screen.blit(font_menu.render("ПК", True, WHITE), (btn_pc.centerx - 20, btn_pc.centery - 20))
            screen.blit(font_menu.render("Андроид", True, WHITE), (btn_android.centerx - 60, btn_android.centery - 20))

        elif state == 'GAME':
            screen.fill(WHITE)
            pygame.draw.line(screen, BLACK, (0, HEIGHT - 150), (WIDTH, HEIGHT - 150), 4)
            screen.blit(player_img, player_rect)

        pygame.display.flip()
        await asyncio.sleep(0)
        clock.tick(60)

asyncio.run(main())
