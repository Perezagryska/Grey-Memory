import pygame
import asyncio
import sys

pygame.init()

# Устанавливаем фиксированный размер для веба
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))

async def main():
    # Создаем объекты внутри асинхронной функции
    font = pygame.font.SysFont("Arial", 50)
    btn_rect = pygame.Rect(WIDTH//2-100, HEIGHT//2-50, 200, 100)
    
    # Загрузка картинки с проверкой
    try:
        player = pygame.image.load("player.png").convert_alpha()
    except:
        player = pygame.Surface((100, 100))
        player.fill((255, 0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Если видим КРАСНЫЙ экран — значит код работает, но не видит логику меню
        # Если видим СИНИЙ экран — значит игра запустилась
        screen.fill((0, 0, 50)) 
        
        pygame.draw.rect(screen, (255, 255, 255), btn_rect, 2)
        text = font.render("START GAME", True, (255, 255, 255))
        screen.blit(text, (btn_rect.centerx - text.get_width()//2, btn_rect.centery - text.get_height()//2))

        pygame.display.flip()
        
        # Без этого в браузере будет черный экран!
        await asyncio.sleep(0)

asyncio.run(main())
