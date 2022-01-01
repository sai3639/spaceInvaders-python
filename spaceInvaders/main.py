import pygame
import math
import random
from pygame import mixer


# Initialize the pygame
pygame.init()

# width, height - create screen
screen = pygame.display.set_mode((800, 600))
# background
background = pygame.image.load('background.png')
# background sound
mixer.music.load('background.wav')
mixer.music.play(-1)
# Changing Title and Icon
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('ufo (1).png')
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('battleship (1).png')
playerX = 370  # coordinates of where the player appears on the screen
playerY = 480
playerX_change = 0

# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('character.png'))
    enemyX.append(random.randint(0, 735))  # choose a random coordinate for the enemy to appear
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(2)
    enemyY_change.append(40)

# bullet

# ready state - you can't see the bullet on the screen
# fire - bullet is moving
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = 'ready'

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_Score(x, y):
    score = font.render('Score: ' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render('GAME OVER', True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    # blit means to draw
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    # blit means to draw
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y + 10))  # 16 and 10 to make sure it appears at center of spaceship


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game loop
running = True
while running:
    # events in game - how to exit the game window
    # changing color of screen
    # RGB = Red, Green Blue (values go up to 255)
    screen.fill((0, 0, 0))
    # background image - heavy background image makes player/enemy move slowly
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # running becomes false when player quits game
            running = False
        # if keystroke is pressed check whether it's right or left
        # if key is pressed down
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    # get the current x coordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        # when key is released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    # stop player from going off screen
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:  # 64 pixel ship - 800 - 64 = 736 - no part of ship will go off game window
        playerX = 736

    # enemy movement
    for i in range(num_of_enemies):
        # game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 2  # hits left size it should go to positive direction
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]

            # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion = mixer.Sound('explosion.wav')
            explosion.play()
            bulletY = 480
            bullet_state = 'ready'
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = 'ready'
    if bullet_state == 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # call player function
    # screen has to be "filled"/drawn first then player
    player(playerX, playerY)
    show_Score(textX, textY)
    # enemy(enemyX, enemyY)
    # update the screen
    pygame.display.update()
