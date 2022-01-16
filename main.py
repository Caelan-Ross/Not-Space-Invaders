"""Imports go here"""
import pygame
import random2
import math

"""Main startup is here"""
pygame.init()
gameDisplay = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Not Space Invaders')
clock = pygame.time.Clock()
gameRunning = True
events = pygame.event.get()
screen = pygame.display.set_mode([800, 600])
gameExit = False
Intro = True

"""images are here"""
playerImg = pygame.image.load('Images\playerShip.png')
healthFullImg = pygame.image.load('Images\healthFull.png')
healthTwoImg = pygame.image.load('Images\healthTwo.png')
healthOneImg = pygame.image.load('Images\healthOne.png')
playerBullet = pygame.image.load('Images\playerBullet.png')
enemyImg = pygame.image.load('Images\enemy.png')
clearedEnemy = pygame.image.load('Images\enemy_empty.png')
gameOverScreen = pygame.image.load('Images\gameOver.png')
winScreen = pygame.image.load('Images\winScreen.png')
logo = pygame.image.load('Images\logo.png')
enemyBullet = pygame.image.load('Images\enemyBullet.png')

"""colours are here"""
black = (0, 0, 0)
white = (255, 255, 255)
green = (9, 164, 0)
lightGreen = (14, 247, 0)
red = (255, 0, 0)
darkRed = (220, 20, 60)

"""Fonts Are Here"""
text = pygame.font.SysFont('arial', 25)

"""Main Player Obj

        - Holds and changes all of the Players positioning and inputted information and parameters
        - Displays and changes the players health values 
        - Allows button inputs to changes the player objects position
"""


class Player:

    def __init__(self, x, y, name, playerImg, health):

        self.x = x
        self.y = y
        self.name = name
        self.playerImg = playerImg
        self.health = health
        self.player_rect = pygame.Rect(self.x, self.y, 48, 56)

    def displayPlayer(self):
        self.player_rect.x = self.x
        self.player_rect.y = self.y

        gameDisplay.blit(self.playerImg, (self.x, self.y))
        if self.health == 3:

            gameDisplay.blit(healthFullImg, (10, 10))
        elif self.health == 2:

            gameDisplay.blit(healthTwoImg, (10, 10))
        elif self.health == 1:

            gameDisplay.blit(healthOneImg, (10, 10))

    def playerMove(self):

        keys = pygame.key.get_pressed()  # checking pressed keys
        if keys[pygame.K_LEFT] and self.y >= 0:
            self.y -= 5
        if keys[pygame.K_RIGHT] and self.y <= 600 - 55:
            self.y += 5

    def player_looseHealth(self):

        if self.health == 3:

            self.health -= 1
        elif self.health == 2:

            self.health -= 1
        elif self.health == 1:

            self.health -= 1


"""Main Enemy Obj

        - Holds all the information for each of the enemies on screen and displays them based
        off of it 
"""


class Enemy:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hitBox = [0, 0, 0, 0]
        self.health = 1
        self.active = False
        self.enemyImage = enemyImg
        self.enemy_rect = pygame.Rect(self.x, self.y, 37, 13)

    def displayEnemy(self, x, y):
        self.enemy_rect.x = self.x
        self.enemy_rect.y = self.y
        if self.health == 1:
            gameDisplay.blit(self.enemyImage, (x, y))
        elif self.health == 0:
            self.enemyImage = clearedEnemy
            gameDisplay.blit(clearedEnemy, (x, y))


"""Main Enemies Array Obj

        - Checks for positioning, and moves them all uniformly 
        - Generates all the enemies at the start of the game
        - Checks for the bounds of the group of enemies and redirects them when hitting bounds of
        screen
"""


class Enemies:

    def __init__(self, arr):

        self.arr = arr
        self.yChange = -20
        self.dirChanged = 0

    def genEnemies(self, xAm, yAm, startX, startY):

        for i in range(6):

            for j in range(6):
                self.arr[i][j] = Enemy((startX + (i * xAm)), (startY + (j * yAm)))

    def Update(self):

        for i in range(6):

            for j in range(6):
                startX = self.arr[i][j].x
                startY = self.arr[i][j].y
                self.arr[i][j].displayEnemy(startX, startY)

    def enemyDraw(self, xChange):

        for i in range(6):

            for j in range(6):
                self.arr[i][j].x += xChange
                self.arr[i][j].y += self.yChange

    def moveAll(self):

        if self.checkBounds() and self.dirChanged == 1:
            self.yChange *= -1
            self.enemyDraw(-30)
            self.dirChanged = 0
        if not self.checkBounds() and self.dirChanged == 0:
            self.enemyDraw(0)

    def checkBounds(self):
        for i in range(6):

            if self.arr[0][i].y <= 0 or self.arr[5][i].y >= 590:
                if self.yChange < 0:
                    self.yChange -= 5
                elif self.yChange > 0:
                    self.yChange += 5
                self.dirChanged += 1
                return True

        return False


"""Main Bullet Obj

        - Displays and holds the information for each bullet that is generated
"""


class Bullet:

    def __init__(self, version, inpx, inpy):
        self.version = version
        self.x = 0
        self.y = 0
        self.inpX = inpx
        self.inpY = inpy
        self.used = 0
        self.bullet_rect = pygame.Rect(self.x, self.y, 34, 17)
        self.prevSet = 0
        self.offScreen = False

    def movePlayerBullet(self, change):
        self.bullet_rect.x = self.x
        self.bullet_rect.y = self.y

        if self.prevSet == 0 and self.version == 0:
            self.x = player.x + 30
            self.y = player.y + 20
            self.bullet_rect.x = self.x
            self.bullet_rect.y = self.y
            self.prevSet += 1

        if self.version == 0 and self.used == 0:
            self.x += 10
            gameDisplay.blit(playerBullet, (self.x, self.y))

        if self.version == 0 and self.used == 1:
            self.x += 800
            gameDisplay.blit(clearedEnemy, (self.x, self.y))

    def moveEnemyBullet(self, change):

        if self.prevSet == 0 and self.version == 1:
            self.x = enemies.arr[self.inpY][self.inpX].x
            self.y = enemies.arr[self.inpY][self.inpX].y
            self.bullet_rect.x = self.x
            self.bullet_rect.y = self.y
            self.prevSet += 1

        if self.version == 1 and self.used == 0:
            self.bullet_rect.x -= 5
            self.x -= 5
            gameDisplay.blit(enemyBullet, (self.x, self.y))

        if self.version == 1 and self.used == 1:
            gameDisplay.blit(clearedEnemy, (self.x, self.y))


"""Main Bullets Array Obj

        - Checks for positioning, and moves them all uniformly 
"""


class Bullets:

    def __init__(self):

        self.array = list1
        self.pMax = 0
        self.eMax = 0

    def addBullet(self, inp):
        if 0 <= self.pMax <= 5:
            if inp.version == 0:
                if self.pMax <= 5:
                    self.pMax += 1
                    self.array.append(inp)

        if 0 <= self.eMax <= 4:
            if inp.version == 1:
                if self.eMax <= 4:
                    self.eMax += 1
                    self.array.append(inp)

    def moveBullets(self):

        for i in range(len(self.array) - 1):

            if self.array[i].version == 0:

                if 800 <= self.array[i].x <= 805 and self.array[i].offScreen == False:

                    self.pMax -= 1
                    self.array[i].offScreen = True
                    self.array[i].movePlayerBullet(1)

                elif self.array[i].x < 800:

                    self.array[i].movePlayerBullet(0)

            if self.array[i].version == 1:
                if -5 <= self.array[i].x <= 0 and self.array[i].offScreen == False:
                    print(self.eMax)
                    self.eMax -= 1
                    self.array[i].offScreen = True
                    self.array[i].moveEnemyBullet(1)

                elif self.array[i].x > 0:
                    self.array[i].moveEnemyBullet(0)


"""Button Function
    - Inputs allow the creation of buttons whatever place and size desired
"""


def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))

        if click[0] == 1 and action is not None:
            action()
            return False

    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))

    smallText = pygame.font.SysFont("arial", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    gameDisplay.blit(textSurf, textRect)


"""Text Objects function
    - Creates text at the specified buttons center and in whatever font you want
"""


def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


'''Initial Startup'''
list1 = []
'''2d array'''
twod = [[[], [], [], [], [], []],
        [[], [], [], [], [], []],
        [[], [], [], [], [], []],
        [[], [], [], [], [], []],
        [[], [], [], [], [], []],
        [[], [], [], [], [], []]
        ]
bullets = Bullets()
player = Player(40, 280, "Player 1", playerImg, 3)
enemies = Enemies(twod)
enemyUpdate = 0
enemyFirstRun = True
bulletUpdate = 0
score = 0
enemies.genEnemies(40, 40, 500, 30)
enemyShootInt = 0
"""Main Intro Loop"""


def gameIntro():
    global Intro
    while Intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(white)
        gameDisplay.blit(logo, (60, 150))
        button("Start Game", 350, 450, 120, 50, green, lightGreen, game_loop)
        pygame.display.update()
        clock.tick(15)


"""Main Game Loop"""


def gameOverCheck():
    for i in range(6):
        for j in range(6):
            if enemies.arr[i][j].health == 1:
                return True
    return False


def enemyPlayerCollision():
    for i in range(6):

        for j in range(6):

            if player.player_rect.colliderect(enemies.arr[i][j].enemy_rect) and enemies.arr[i][j] \
                    .enemyImage == enemyImg:
                return True
    return False


def restartGame():
    global enemies
    global player
    global enemyUpdate
    global enemyImg
    global bullets
    global bulletUpdate
    global score
    global enemyFirstRun
    global events
    global twod
    global list1
    global enemyShootInt
    list1 = []
    '''2d array'''
    twod = [[[], [], [], [], [], []],
            [[], [], [], [], [], []],
            [[], [], [], [], [], []],
            [[], [], [], [], [], []],
            [[], [], [], [], [], []],
            [[], [], [], [], [], []]
            ]
    bullets = Bullets()
    player = Player(40, 280, "Player 1", playerImg, 3)
    enemies = Enemies(twod)
    enemyUpdate = 0
    enemyFirstRun = True
    bulletUpdate = 0
    score = 0
    enemies.genEnemies(40, 40, 500, 30)
    enemyShootInt = 0


def enemyShoot():
    targetX = math.floor(random2.randint(0, 5))
    targetY = math.floor(random2.randint(0, 5))
    bullets.addBullet(Bullet(1, targetX, targetY))


def bulletCheck():
    global score
    for i in range(len(bullets.array) - 1):

        for j in range(6):

            for k in range(6):

                if enemies.arr[j][k].enemy_rect.colliderect(bullets.array[i].bullet_rect) and \
                        bullets.array[i].version == 0:

                    if enemies.arr[j][k].health == 1 and bullets.array[i].used == 0:
                        enemies.arr[j][k].health = 0
                        bullets.array[i].used = 1
                        score += 25
                        bullets.array[i].offScreen = True
                        bullets.pMax -= 1

    for i in range(len(bullets.array) - 1):
        if player.player_rect.colliderect(bullets.array[i].bullet_rect) and \
                bullets.array[i].version == 1:
            if bullets.array[i].used == 0 and player.health > 0:
                player.player_looseHealth()
                bullets.array[i].used = 1
                if score >= 10:
                    score -= 10
                bullets.array[i].offScreen = True


def game_loop():
    global enemies
    global player
    global enemyUpdate
    global enemyImg
    global bullets
    global bulletUpdate
    global score
    global enemyFirstRun
    global events
    global text
    global enemyShootInt
    while not gameExit:
        screen.fill(black)

        """Line 217 - 242 is the primary movement and updates"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        click = pygame.mouse.get_pressed()

        if click[0] == 1:

            if bulletUpdate >= 25:

                bulletUpdate = 0
                if bullets.pMax <= 5:
                    bullets.addBullet(Bullet(0, -1, -1))

        bulletCheck()

        if enemyPlayerCollision() and score < 900:
            player.health -= 3

        if enemyFirstRun:
            enemies.moveAll()
            enemyShoot()
            enemyFirstRun = False

        if enemyUpdate == 20:
            enemyUpdate = 0
            enemyShoot()
            enemies.moveAll()

        if enemyShootInt == 20:
            enemyShoot()

        enemyUpdate += 1
        player.displayPlayer()
        player.playerMove()
        bulletUpdate += 1
        enemyShootInt += 1
        bullets.moveBullets()
        enemies.Update()
        scoreText = text.render("Score: " + str(score), False, white)
        screen.blit(scoreText, (700, 5))

        if player.health <= 0:
            gameDisplay.blit(gameOverScreen, (50, 200))
            button("Restart", 350, 450, 120, 50, darkRed, red, restartGame)

        if score == 900:
            gameDisplay.blit(winScreen, (200, 150))
            button("Restart", 350, 450, 120, 50, darkRed, red, restartGame)

        pygame.display.update()
        clock.tick(60)


gameIntro()
pygame.quit()
quit()
