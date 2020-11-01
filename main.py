import pygame
import random
import math
from pygame import mixer

# Initialize the py-game
pygame.init()
pygame.mixer.init()

# Creating the main screen
# set_mode((x_coordinate, y_coordinate))
screen = pygame.display.set_mode((800, 600))

# Background image
background = pygame.image.load('background.jpg')

# Background music
mixer.music.load('EerieToneMusicBackgroundLoop.wav')
mixer.music.play(-1)    # the '-1' will make it play on a LOOP

# Caption and icon
pygame.display.set_caption("Space Adventures")
icon = pygame.image.load('banner_icon.png')
pygame.display.set_icon(icon)

# Player lives
heartImg = pygame.image.load('heart(45x45).png')
startX = 800 - 10
startY = 10    # 45x45px image
lives = 3
times_hit = 0

# Player's ship
playerImg = pygame.image.load('spaceship.png')
playerX = (800 / 2) - (90 / 2)  # image width = 90px
playerY = 600 - (90 + 20)
playerX_change = 0

# Enemy's ship
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 5  #TODO (Have to randomize the # of enemies)

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('ufo.png'))
    enemyX.append(random.randint((0 + 20), (800 - 90 - 20)))  # image width = 64px
    enemyY.append(random.randint(70, 150))
    enemyX_change.append(0.3)
    enemyY_change.append(64)

# Bullets
# state: - 'ready' => bullet is ready to be shot (cannot be seen on the screen)
#        - 'fire' => bullet is currently moving
bulletImg = pygame.image.load('bullet_2.png')
bulletX = 0
bulletY = 600 - (90 + 20)
bulletX_change = 0
bulletY_change = 0.9
bullet_state = 'ready'

# Explosion animation

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game Over text
gameOverFont = pygame.font.Font('freesansbold.ttf', 70)


def show_score(x, y):
    score = font.render('Score: ' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    gameOverText = gameOverFont.render('GAME OVER', True, (255, 255, 255))
    screen.blit(gameOverText, (200, 250))


def show_final_score(score):
    finalScore = font.render('Final score: ' + str(score), True, (255, 255, 0))
    screen.blit(finalScore, (300, (250 + 70)))


def player(x, y):
    screen.blit(playerImg, (x, y))  # blit => draw


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + ((90/2) - (22/2)), y + 10))
    # bulletWidth = 22px --- spaceshipWidth = 90px


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2)))
    if distance < 40:
        return True
    else:
        return False

def player_hit(enemyX, enemyY, playerX, playerY):
    distance = math.sqrt((math.pow(enemyX - playerX, 2) + math.pow(enemyY - playerY, 2)))
    if distance < 60:
        return True
    else:
        return False

def draw_lives(startX, startY, lives):
    for i in range(1, lives + 1):
        screen.blit(heartImg, (startX - (i * (45 + 7)), startY))    # 45px image width + 7px border


# GAME UPDATING IN A LOOP
# (everything has to be inside of this loop, otherwise it's gonna appear
# just for a fragment of time and then disappear)
running = True
while running:

    # Background RGB color
    screen.fill((10, 14, 37))

    # Background Image
    screen.blit(background, (0, 0))

    # Lives
    draw_lives(startX, startY, lives)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Check if a key has been pressed (and which one (L/R arrow))
        # Pressed keys
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bullet_sound = mixer.Sound('bulletSound.wav')
                    bullet_sound.set_volume(0.3)
                    bullet_sound.play()   # it will only be played once
                    bulletX = playerX   # Getting the 'x' coordinate of the spaceship
                    fire_bullet(bulletX, bulletY)

        # Released keys
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Player spaceship screen boundaries
    playerX += playerX_change

    border = 100    # border pixels from end the screen
    if playerX <= (0 + border):
        playerX = (0 + border)
    elif playerX >= (710 - border):  # 800 - 90(image width) = 710px
        playerX = (710 - border)

    # Enemy spaceship screen boundaries and movement
    for i in range(num_of_enemies):

        # Game Over text
        playerGotHit = player_hit(enemyX[i], enemyY[i], playerX, playerY)

        if playerGotHit:
            damaged = mixer.Sound('damaged.wav')
            damaged.play()
            times_hit += 1
            enemyX[i] = random.randint((0 + 20), (800 - 90 - 20))  # image width = 64px
            enemyY[i] = random.randint(50, 150)
            lives -= 1
            draw_lives(startX, startY, lives)

        if times_hit == 3:
            destroyed = mixer.Sound('ship_destroyed.wav')
            destroyed.play()
            gameOverSound = mixer.Sound('gameOverSound.wav')
            gameOverSound.set_volume(0.5)
            times_hit += 1      # This gets incremented so that this if-statement runs only once
                                # (Avoids infinite repetitions)

        if lives == 0:
            game_over_text()
            show_final_score(score_value)
            break

        enemyX[i] += enemyX_change[i]

        border = 30
        if enemyX[i] <= (0 + border):
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= (736 - border):  # 800 - 64(image width) = 736px
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:  # if it's Truthy
            explosionSound = mixer.Sound('explosionSound.wav')
            explosionSound.set_volume(0.42)
            explosionSound.play()
            bulletY = 600 - (90 + 20)
            bullet_state = 'ready'
            score_value += 1
            # When the enemy ship gets shot, a new one respawns randomly
            enemyX[i] = random.randint((0 + 20), (800 - 90 - 20))  # image width = 64px
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Motion
    if bulletY <= 0:
        bulletY = 600 - (90 + 20)
        bullet_state = 'ready'

    if bullet_state == 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    if lives != 0:
        show_score(textX, textY)

    pygame.display.update()
