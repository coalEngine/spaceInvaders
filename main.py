import pygame
from pygame import mixer
import random
import math


# initializing the module
pygame.init()


# window (width and height)
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("res/background.jpg")

# Background Sound
mixer.music.load("sound/si_song.wav")
mixer.music.set_volume(1.0)
mixer.music.play(-1)


# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("res/logo.png")
pygame.display.set_icon(icon)

# Player
player_img = pygame.image.load("res/player.png")
playerX = 380
playerY = 510
player_speed = 0


# Enemy
enemy_img = []
enemyX = []
enemyY = []
enemy_speed = []
enemy_descent = []

num_of_enemy = 5

for i in range(num_of_enemy):

    enemy_img.append(pygame.image.load("res/enemy2.png"))
    enemyX.append(random.randint(0, 768))
    enemyY.append(random.randint(50, 150))
    enemy_speed.append(1)
    enemy_descent.append(35)

# Bullet - ready means the bullet isn't visible on the screen
# Fire - the bullet is currently moving
bullet_img = pygame.image.load("res/bullet.png")
bulletX = 0
bulletY = 510
bullet_ascend = 5
bullet_state = "ready"

# Score
core_value = 0
font = pygame.font.Font("gfx/dogicapixelbold.ttf", 29)
textX = 10
textY = 10

# Game over Text

font_gameover = pygame.font.Font("gfx/dogicapixelbold.ttf", 39)


def game_over_text(x,y):
    font_gameOver = font_gameover.render("GAME OVER", True, (255, 255, 255))
    screen.blit(font_gameOver, (x,y))



def show_score(x,y):
    score = font.render("Score: " + str(core_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    # blit means draw
    screen.blit(player_img, (x, y))


def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 16, y + 10))


def collide(ex, ey, bx, by):
    distance = math.sqrt((math.pow((ex - bx), 2)) + (math.pow((ey - by), 2)))
    if distance < 27:
        return True
    else:
        return False


# game loop
running = True
while running:
    # RGB = Red, Green, Blue
    screen.fill((0, 0, 255))
    screen.blit(background, (0, 0))
    for evt in pygame.event.get():
        if evt.type == pygame.QUIT:
            running = False

        # If keystroke is pressed, check if its left or right
        if evt.type == pygame.KEYDOWN:
            if evt.key == pygame.K_a:
                player_speed = -2
            if evt.key == pygame.K_d:
                player_speed = 2

        if evt.type == pygame.MOUSEBUTTONDOWN:
            if bullet_state == "ready":
                bullet_sound = mixer.Sound('sound/lazer.wav')
                bullet_sound.play()
                # stores current player position in "bulletX"
                bulletX = playerX
                # that x coord is the path the bullet will take
                # the y coord is the literal position of the bullet
                fire_bullet(bulletX, bulletY)

                '''
                 this code only runs when the bullet is in the "ready" state
                '''

        if evt.type == pygame.KEYUP:
            if evt.key == pygame.K_a or evt.key == pygame.K_d:
                player_speed = 0


# Bound checks for both the player and the enemy ships

    playerX += player_speed
    if playerX <= 0:
        playerX = 0
    elif playerX >= 768:
        playerX = 768

    for i in range(num_of_enemy):

        # Game over
        if enemyY[i] > 450:
            for j in range(num_of_enemy):
                enemyY[j] = 2000
            game_over_text(240, 285)
            break

        enemyX[i] += enemy_speed[i]
        if enemyX[i] <= 0:
            enemy_speed[i] = 1
            enemyY[i] += enemy_descent[i]
        elif enemyX[i] >= 768:
            enemy_speed[i] = -1
            enemyY[i] += enemy_descent[i]

        # Collision
        collision = collide(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound("sound/invader_death.wav")
            explosion_sound.play()
            bulletY = 510
            bullet_state = "ready"
            core_value += 100
            enemyX[i] = random.randint(0, 768)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <= 0:
        bulletY = 510
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bullet_ascend

    player(playerX, playerY)
    show_score(textX, textY)
    # updating the screen
    pygame.display.update()
