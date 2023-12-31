import sys
import pygame
import time
import random

pygame.font.init()

WIDTH, HEIGHT = 500, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dodge")

BG = pygame.transform.scale(pygame.image.load("bg.jpeg"), (WIDTH, HEIGHT))

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 40
PLAYER_SCALE = 50
SCALE = 1.7

PLAYER_VEL = 5
STAR_WIDTH = 10
STAR_HEIGHT = 20
STAR_VEL = 3

FONT = pygame.font.SysFont("comicsans", 30)


def draw(player_image, player, elapsed_time, stars):
    WIN.blit(BG, (0, 0))

    time_text = FONT.render(f"Idő: {round(elapsed_time)}mp", 1, "lime")
    WIN.blit(time_text, (10, 10))

    # pygame.draw.rect(WIN, "orange", player)
    # pygame.draw.rect(WIN, "red", player)

    player_image.set_colorkey((255, 0, 0))
    WIN.blit(player_image, player)
    # player = pygame.image.load('racecar.png')

    # pygame.draw()

    for star in stars:
        pygame.draw.rect(WIN, "white", star)

    pygame.display.update()


def main():
    run = True

    # player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT,
    #                      PLAYER_WIDTH, PLAYER_HEIGHT)
    # player = pygame.transform.scale(player_image, (PLAYER_WIDTH, PLAYER_HEIGHT))

    player_image = pygame.image.load("rocket_3.png").convert_alpha()
    player_image = pygame.transform.scale(player_image,
                                          (player_image.get_width() * SCALE, player_image.get_height() * SCALE))

    player = player_image.get_rect(center=(player_image.get_width() // 2, player_image.get_height() // 2))

    player.x = WIDTH // 2 - player_image.get_width() // 2
    player.y = HEIGHT - player_image.get_height()

    print("Player initialized -", player)

    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    star_add_increment = 2000
    star_count = 0

    stars = []
    hit = False

    print("Starting game...")
    while run:
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT,
                                   STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)

            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL

        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                break

        if hit:
            lost_text = FONT.render("Vereség!", 1, "red")
            WIN.blit(lost_text, (WIDTH / 2 - lost_text.get_width() / 2, HEIGHT / 2 - lost_text.get_height() / 2))
            pygame.display.update()
            pygame.time.delay(2000)
            break

        draw(player_image, player, elapsed_time, stars)

    # pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
