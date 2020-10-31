import pygame
import random
import math

# Initialize the py-game
pygame.init()

# Creating the main screen
# set_mode((x_coordinate, y_coordinate))
screen = pygame.display.set_mode((800, 600))

# Background image
background = pygame.image.load('background.jpg')

# Caption and icon
pygame.display.set_caption("Space Adventures")
icon = pygame.image.load('banner_icon.png')
pygame.display.set_icon(icon)

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
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.16)
    enemyY_change.append(40)

# Bullets
# state: - 'ready' => bullet is ready to be shot (cannot be seen on the screen)
#        - 'fire' => bullet is currently moving
bulletImg = pygame.image.load('bullet_2.png')
bulletX = 0
bulletY = 600 - (90 + 20)
bulletX_change = 0
bulletY_change = 0.9
bullet_state = 'ready'


# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10


def show_score(x, y):
    score = font.render('Score: ' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


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


# GAME UPDATING IN A LOOP
# (everything has to be inside of this loop, otherwise it's gonna appear
# just for a fragment of time and then disappear)
running = True
while running:

    # Background RGB color
    screen.fill((10, 14, 37))

    # Background Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Check if a key has been pressed (and which one (L/R arrow))
        # Pressed keys
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.25
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.25
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        # Released keys
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Player spaceship screen boundaries
    playerX += playerX_change

    border = 150    # border pixels from end the screen
    if playerX <= (0 + border):
        playerX = (0 + border)
    elif playerX >= (710 - border):  # 800 - 90(image width) = 710px
        playerX = (710 - border)

    # Enemy spaceship screen boundaries and movement
    for i in range(num_of_enemies):
        enemyX[i] += enemyX_change[i]

        border = 30
        if enemyX[i] <= (0 + border):
            enemyX_change[i] = 0.16
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= (736 - border):  # 800 - 64(image width) = 736px
            enemyX_change[i] = -0.16
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:  # if it's Truthy
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
    show_score(textX, textY)

    pygame.display.update()
