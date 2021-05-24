import pygame
import math
import random
from pygame import mixer
pygame.init()
#width and height
screen = pygame.display.set_mode((800, 600))

#Background
background = pygame.image.load('background.png')

#Background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

#caption and set icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)
#player

playering = pygame.image.load('space-invaders (1).png')
playerx = 370
playery = 480
playerx_change = 0

#enemy

enemying = []
enemyx = []
enemyy = []
enemyx_change = []
enemyy_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemying.append(pygame.image.load('alien.png'))
    enemyx.append(random.randint(0, 736))
    enemyy.append(random.randint(50, 150))
    enemyx_change.append(4)
    enemyy_change.append(40)

#bullet
#Ready - state means you cant see the bullet on the screen
#Fire - The bullet is currently moving

bulleting = pygame.image.load('bullet.png')
bulletx = 0
bullety = 480
bulletx_change = 0
bullety_change = 10
bullet_state = "ready"

#Score

score_value =0
font = pygame.font.Font('Happy Ending.otf',30)
textx = 10
texty = 10

#GameOver text

font_over = pygame.font.Font('Blood Thirst.ttf',1000)

def show_screen(x,y):
    score = font.render("SCORE :" +str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))
def game_over():
    overtt = font.render("GAME-OVER", True, (255, 255, 255))
    screen.blit(overtt, (450, 250))


def player(x,y):
    screen.blit(playering, (x, y))
def enemy(x,y, i):
    screen.blit(enemying[i],(x,y))
def fire_bullet(x,y):
    global bullet_state
    bullet_state ="fire"
    screen.blit(bulleting, (x+16, y+10))
    #drawing image on screen

def isCollision(enemyx, enemyy, bulletx, bullety):
    distance = math.sqrt(math.pow(enemyx-bulletx, 2)+math.pow(enemyy-bullety, 2))
    if distance < 27:
        return True
    else:
        return False





running = True
while running:
    screen.fill((0, 0, 0))
    #Background Image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    #if keystroke is pressed check whether its right or left

        if event.type == pygame.KEYDOWN:
           if event.key == pygame.K_LEFT:
               playerx_change = -4
           if event.key == pygame.K_RIGHT:
               playerx_change = 4
           if event.key == pygame.K_SPACE:
               if bullet_state == "ready":
                   bullet_sound = mixer.Sound('laser.wav')
                   bullet_sound.play()
                   bulletx = playerx
                   fire_bullet(bulletx, bullety)

        if event.type == pygame.KEYUP:
           if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
               playerx_change = 0
#checking for boundaries condition
#checking for space ship
    playerx += playerx_change
    if playerx <= 0:
        playerx = 0
    elif playerx >= 736:
        playerx = 736
#checking for enemy movement
    for i in range(num_of_enemies):

        #Game over if enemy and spaceship touch at 440 px
        if enemyy[i] > 440 :
            for j in range(num_of_enemies):
                #setting all the enemies out of the screen if game is over
                enemyy[j] = 2000
            game_over()
            break


        enemyx[i] += enemyx_change[i]
        if enemyx[i] <= 0:
            enemyx_change[i] = 4
            enemyy[i] += enemyy_change[i]
        elif enemyx[i] >= 736:
            enemyx_change[i] = -4
            enemyy[i] += enemyy_change[i]
        collision = isCollision(enemyx[i], enemyy[i], bulletx, bullety)
        if collision:
            boom_sound = mixer.Sound('explosion.wav')
            boom_sound.play()

            bullety = 480
            bullet_state = "ready"
            score_value += 1
            enemyx[i] = random.randint(0, 736)
            enemyy[i] = random.randint(50, 150)
        enemy(enemyx[i], enemyy[i],i)

    #Bullet movement
    if bullety <= 0:
        bullety = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletx, bullety)
        bullety -= bullety_change

    player(playerx, playery)
    show_screen(textx,texty)
    pygame.display.update()



