"""
This file is for new game: pygame
Created by: Arman Hovhannisyan
Date: 29 May
"""
import time
import random
import pygame

pygame.init()

width = 800
height = 600
FPS = 60

star_width = 7
star_height = 30
star_speed = 5
star_rate = 0.03
increase_rate = 0.1
DINO_SPEED = 5

try:
    background = pygame.transform.scale(pygame.image.load("back.jpg"), (width, height))
    dino_right = pygame.image.load("dinor.png")
    dino_left = pygame.image.load("dinol.png")
except FileNotFoundError:
    print("Error loading image")
    pygame.quit()
    exit()

font = pygame.font.SysFont("roman", 30)

def draw(player, direction, finish, stars, window):
    """
    Function: draw
    Brief: Draws the game in screen
    Params: player:pygame.rect
            direction: the direction of the player
            finish: the time
            stars: the list of falling stars
            window: the game window
    """
    window.blit(background, (0, 0))
    time_text = font.render(f"Time: {round(finish)}", 1, "white")
    window.blit(time_text, (10, 10))

    if direction == "right":
        window.blit(dino_right, (player.x, player.y))
    else:
        window.blit(dino_left, (player.x, player.y))

    for star in stars:
        pygame.draw.rect(window, "white", star)

    pygame.display.update()

def star_fall(stars):
    """
    Function: star_fall
    Brief: Generates stars random times
    Params: stars: the list of stars
    """
    if random.random() < star_rate:
        star_x = random.randint(0, width - star_width)
        stars.append(pygame.Rect(star_x, 0, star_width, star_height))

def game_over(stars, player, window):
    """
    Function: game_over
    Brief: Checks it stars hit and removes stars
    Params: stars: the list of stars, player: pygamr.rect, window: the game window
    Retrun: true or false
    """
    for star in stars[:]:
        if star.colliderect(player):
            lose_text = font.render("You lose", 1, "red")
            window.blit(lose_text, (width // 2 - lose_text.get_width() // 2,
                height // 2 - lose_text.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(2000)
            return True
        if star.y > height:
            stars.remove(star)
    return False

def play_again(window):
    """
    Function: play_again
    Brief: asks the palyer if player want to play again
    Params: window: the game window
    Return: returns True if player want to play otherwise False
    """
    window.blit(background, (0,0))
    message = font.render("Play again (y/n)", 2, "yellow")
    window.blit(message, (width // 2 - message.get_width() // 2,height // 2 - message.get_height() // 2))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    return True
                elif event.key == pygame.K_n:
                    return False

def main():
    """
    Function: main
    Entry point for the game.
    """
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Dino")

    run = True
    player = pygame.Rect(200, height - dino_right.get_height(),
            dino_right.get_width(), dino_right.get_height())
    clock = pygame.time.Clock()
    start = time.time()
    stars = []
    direction = "right"

    while run:
        clock.tick(FPS)
        finish = time.time() - start

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        key = pygame.key.get_pressed()
        if key[pygame.K_RIGHT] and player.right < width:
            player.move_ip(DINO_SPEED, 0)
            direction = "right"
        elif key[pygame.K_LEFT] and player.left > 0:
            player.move_ip(-DINO_SPEED, 0)
            direction = "left"

        star_fall(stars)

        star_v = star_speed + finish * increase_rate
        for star in stars:
            star.y += star_v

        if game_over(stars, player, window):
            run = False
            if play_again(window):
                main()
                return

        draw(player, direction, finish, stars, window)

    pygame.quit()

if __name__ == "__main__":
    main()
