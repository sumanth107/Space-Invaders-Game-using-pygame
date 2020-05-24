import pygame
import n as np

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('spaceship.png')
bg = pygame.image.load('background.png')
pygame.display.set_icon(icon)
running = True
playerImg = pygame.image.load('spaceship.png')
X = 370
Y = 500
enemyImg = []
enemyY = []
enemyX = []
for i in range(6):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(np.random.randint(0, 735))
    enemyY.append(np.random.randint(40, 200))
change = 0
score = 0
temp = 0
enemyChangeX = [7, 7, 7, 7, 7, 7]
enemyChangeY = [40, 40, 40, 40, 40, 40]
bulletImg = pygame.image.load('bullet.png')
bulletY = 500
bulletChangeY = 10
bullet_state = 'ready'
font = pygame.font.Font('freesansbold.ttf', 32)
over_font = pygame.font.Font('freesansbold.ttf', 64)
textX = 10
textY = 10
pygame.mixer.music.load('background.wav')
pygame.mixer.music.play(-1)


def show_score(x, y):
    score_value = font.render('Score : ' + str(score), True, (255, 255, 255))
    screen.blit(score_value, (x, y))

def game_over_text():
    over = over_font.render('GAME OVER' , True, (255, 255, 255))
    screen.blit(over, (205, 260))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y + 10))


def Collision(x1, y1, x2, y2):
    dist = np.sqrt(np.power(x2 - x1, 2) + np.power(y2 - y1, 2))
    if dist < 27:
        return True
    else:
        return False


while running:
    screen.fill((0, 0, 0))
    screen.blit(bg, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                change = -8
            if event.key == pygame.K_RIGHT:
                change = 8
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bullet_Sound = pygame.mixer.Sound('laser.wav')
                    bullet_Sound.play()
                    temp = X
                    fire_bullet(temp, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                change = 0
    X += change
    if X <= 0:
        X = 0
    if X >= 736:
        X = 736
    for i in range(6):
        if enemyY[i] >= 460:
            for j in range(6):
                enemyY[j] = 1000
            game_over_text()
            break

        enemyX[i] += enemyChangeX[i]
        if enemyX[i] <= 0:
            enemyChangeX[i] = 7
            enemyY[i] += enemyChangeY[i]
        if enemyX[i] >= 736:
            enemyChangeX[i] = -7
            enemyY[i] += enemyChangeY[i]
        if Collision(temp, bulletY, enemyX[i], enemyY[i]):
            collision_Sound = pygame.mixer.Sound('explosion.wav')
            collision_Sound.play()
            bullet_state = 'ready'
            bulletY = 500
            score += 1
            enemyX[i] = np.random.randint(0, 735)
            enemyY[i] = np.random.randint(40, 200)
        enemy(enemyX[i], enemyY[i], i)
    if bulletY <= 0:
        bulletY = 500
        bullet_state = 'ready'
    if bullet_state == 'fire':
        fire_bullet(temp, bulletY)
        bulletY -= bulletChangeY

    show_score(textX, textY)
    player(X, Y)
    pygame.display.update()
print('Final score : ', score)
