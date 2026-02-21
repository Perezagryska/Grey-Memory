import pygame
import asyncio
import sys

pygame.init()

WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))

WHITE = (240, 240, 240)
BLACK = (15, 15, 15)
GRAY = (60, 60, 60)

font = pygame.font.SysFont("sans-serif", 50)

state = "MENU"

try:
    player_img = pygame.image.load("player.png").convert_alpha()
    player_img = pygame.transform.scale(player_img, (120, 200))
except:
    player_img = pygame.Surface((120, 200))
    player_img.fill(GRAY)

player_rect = player_img.get_rect(midbottom=(WIDTH//2, HEIGHT-150))
btn_play = pygame.Rect(WIDTH//2-100, HEIGHT//2-35, 200, 70)

async def main():
    global state
    clock = pygame.time.Clock()
    
    while True:
        m_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if state == "MENU" and btn_play.collidepoint(m_pos):
                    state = "GAME"

        screen.fill(BLACK)

        if state == "MENU":
            pygame.draw.rect(screen, WHITE, btn_play, 2)
            txt = font.render("ИГРАТЬ", True, WHITE)
            screen.blit(txt, (btn_play.centerx - txt.get_width()//2, btn_play.centery - txt.get_height()//2))
        
        else:
            screen.fill(WHITE)
            pygame.draw.line(screen, BLACK, (0, HEIGHT-150), (WIDTH, HEIGHT-150), 4)
            screen.blit(player_img, player_rect)

        pygame.display.flip()
        await asyncio.sleep(0)
        clock.tick(60)

asyncio.run(main())
