import time
import pygame
import random
pygame.init()  # Initialize Pygame

# Set up display
WIDTH, HEIGHT = 800, 500
MAP_WIDTH, MAP_HEIGHT = 850, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooter Game")
offset_x = 0
row1, row2, row3, row4 = 350, 290, 230, 170

# Sprites
bg = pygame.image.load('bg.jpg')
ship = pygame.image.load('Ship.png')
ship = pygame.image.load('ship.png')
char = pygame.image.load('standing.png')
fistR = pygame.image.load('Fist.png')
fistL = pygame.transform.flip(fistR, True, False)

# Obstacle Sprites
box = pygame.image.load('Box.png')
barrier = pygame.image.load('Barrier.png')

# initialize Time
startTime = time.time()
shieldstartTime = time.time()
clock = pygame.time.Clock()

# Text
fonts = pygame.font.get_fonts()
font = pygame.font.SysFont("Retro Gaming", 25)
# #text, boolean anti aliasing, text color, background

# UI
userinterface = (0, 360, WIDTH, 140)
button1 = (10, 430, 45, 45)  # placeholder button, need to create actual ones
pygame.draw.rect(win, (255, 219, 59), userinterface)
pygame.draw.rect(win, (255, 255, 255), button1)

# Sounds
bulletSound = pygame.mixer.Sound("Assault_trim.mp3")
bulletSound.set_volume(0.0)
hitSound = pygame.mixer.Sound("hit.mp3")
hitSound.set_volume(0.1)
shieldSound = pygame.mixer.Sound("personalShield.mp3")
# Soundtracks
classicSound = pygame.mixer.music.load("cantina.mp3")
pygame.mixer.music.set_volume(0.4)
# pygame.mixer.music.play(-1)
soundtrack = classicSound

# captain rex intro voice track from starwars battlefront**

# Character State
shieldActivated = False
gameOver = False
# Background Scroll
scrollWidth = 150
# Up/down movement
strafeWidth = 60

# Collision Detection
future_x = 0

# Global Weighted Variables
attackChoice = 1.0

# Map (Coordinate System)
# Rows in array go from bottom to top
Map = [['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
       ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x',
           'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
       ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x',
           'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
       ['x', 'x', 'x', 'b', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x']]
Grid_Size = 60
# Select grid numbers
rows, cols = 4, round(MAP_WIDTH/Grid_Size)+1
# Spawn Spaces
# Clones = -100
# Droids = 9


# CLASSES


class player():  # new Player Class
    walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load(
        'R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
    walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load(
        'L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]

    # walkRight = [pygame.image.load('C1 (1).png'), pygame.image.load('C2 (1).png')]
    # walkLeft = [pygame.image.load('C1 (2).png'), pygame.image.load('C2 (2).png')]

    # intial
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # Movement
        self.vel = 5
        self.isJump = False
        self.left = False
        self.right = False
        self.walkDistance = 0
        self.jumpDistance = 10
        self.standing = True
        self.startpos = True

        # Game
        self.score = 0
        self.hitbox = (self.x + 17 - offset_x, self.y + 11, 29, 52)
        self.hitbox_rect = pygame.Rect(
            self.hitbox[0] + future_x, self.hitbox[1], self.hitbox[2], self.hitbox[3])
        self.health = 3
        self.row = 1
        self.magSize = 10
        self.stun = False
        self.spawnYes = False

        # Coordinates
        self.xcoord = ((self.x + 100) // Grid_Size)  # Manual adjust for error
        self.ycoord = (self.y - 60) // Grid_Size

    # method (aka a function/action)

    def draw(self, win):
        # Shadow
        # print(self.x)
        pygame.draw.ellipse(win, (83, 80, 82),
                            (self.hitbox[0] - 5, 400 - ((self.row - 1) * 60), 40, 10))
        # Animation
        if self.walkDistance + 1 >= 9:
            self.walkDistance = 0

        if not (self.standing):
            if self.left:
                win.blit(self.walkLeft[self.walkDistance//3],
                         (self.x - offset_x, self.y))
                self.walkDistance += 1
            elif self.right:
                win.blit(self.walkRight[self.walkDistance//3],
                         (self.x - offset_x, self.y))
                self.walkDistance += 1
        else:
            if self.startpos:
                win.blit(char, (self.x - offset_x, self.y))
            if self.right:
                win.blit(self.walkRight[0], (self.x - offset_x, self.y))
            elif self.left:
                win.blit(self.walkLeft[0], (self.x - offset_x, self.y))

        self.hitbox = (self.x + 17 - offset_x, self.y + 11, 29, 52)
        self.hitbox_rect = pygame.Rect(
            self.hitbox[0], self.hitbox[1], self.hitbox[2], self.hitbox[3])
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)
        self.difficulty()
        self.coordinates()

    def hit(self, attackChoice):
        hitSound.play()
        self.health -= 1
        attackChoice += 0.3
        damage = font.render("-1", True, (255, 0, 0))
        win.blit(damage, (p1.x + 15, p1.y - 20))
        pygame.display.update()

        i = 0
        shieldSound.play()
        while i < 100:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 101
                    pygame.quit()

    def coordinates(self):
        # print(self.y)
        # print(self.x)
        self.oldxcoord = self.xcoord
        self.oldycoord = self.ycoord

        self.xcoord = ((self.x + 100) // Grid_Size)  # Manual adjust for error
        self.ycoord = (self.y - 60) // Grid_Size
        # print(f"This is player X and Y {self.xcoord} {self.ycoord}")
        Map[self.oldycoord - 1][self.oldxcoord - 1] = 'x'
        Map[self.ycoord - 1][self.xcoord - 1] = 'p'

    def difficulty(self):
        if self.score != 0:
            if self.spawnYes:
                if self.score % 10 == 0:
                    print("spawn superdroid")
                    enemy_name = f'Superdroid{p1.score + 2}'
                    enemy_name = spawnSuperDroid()
                    enemies.append(enemy_name)
                    self.spawnYes = False
                elif self.score % 5 == 0:
                    print("spawn droid")
                    enemy_name = f'Droid{p1.score + 2}'
                    enemy_name = spawnEnemy()
                    enemies.append(enemy_name)
                    self.spawnYes = False

            if self.score % 5 != 0:
                self.spawnYes = True


class droid():  # ** fix support function
    walkRight = [pygame.image.load('DR1.png'), pygame.image.load(
        'DR2.png'), pygame.image.load('DR3.png')]
    walkLeft = [pygame.image.load('DL1.png'), pygame.image.load(
        'DL2.png'), pygame.image.load('DL3.png')]
    test = pygame.image.load('standing.png')  # * Find processing image

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.path = [x, end]  # path that enemy walks
        self.walkDistance = 0
        self.vel = 3
        # Bullets
        self.facing = 1
        self.bullets = []
        self.last_shot = 0
        self.bulletshot = 0
        self.reloadStart = time.time()
        self.emptyMag = False

        self.hitbox = (self.x + 14, self.y + 4, 29, 52)
        # self.hp = (self.x, self.y, 29, 3)
        self.damage = 0
        self.health = 3
        self.alive = True

        # Status Modes
        self.processing = False
        # Time Counters
        self.alertedTime = time.time()

        # Coordinates
        self.xcoord = ((self.x + 100) // Grid_Size) - \
            1  # Manual adjust for error
        self.ycoord = ((self.y - 60) // Grid_Size) - 1
        self.row = -1*(-4+(self.y-170)//60)
        self.target_x, self.target_y = 0, 0

        # Status
        self.neutral = True
        self.attack = False

    def draw(self, win):

        if self.alive:
            if self.walkDistance + 1 >= 9:
                self.walkDistance = 0

            if self.vel > 0:
                win.blit(
                    self.walkRight[self.walkDistance//3], (self.x - offset_x, self.y))
                self.walkDistance += 1

                self.hitbox = (self.x + 14 - offset_x, self.y + 4, 29, 52)
                # self.hp = (self.x + 14, self.y - 5, 29, 3)
            else:
                win.blit(self.walkLeft[self.walkDistance//3],
                         (self.x - offset_x, self.y))
                self.walkDistance += 1

                self.hitbox = (self.x + 15 - offset_x, self.y + 4, 29, 52)
                # self.hp = (self.x + 24, self.y - 5, 29, 3)

            # Health Bars
            pygame.draw.rect(win, (255, 0, 0),
                             (self.hitbox[0], self.hitbox[1] - 10, 30, 5))
            pygame.draw.rect(
                win, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 10, 30 - (10*self.damage), 5))

            # Hitbox
            # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)
            self.coordinates()
            self.changePath()

        # Death Animation
        if not self.alive:
            pass

    def changePath(self):
        # print(self.path[0])
        # print(self.path[1])
        for obj in objects:
            # Check for obstacles on the same row
            if self.row == (-1*(-4+(obj.y-170)//60)):
                if obj.rect.colliderect(self.hitbox[0] + self.vel + offset_x, self.hitbox[1], self.hitbox[2], self.hitbox[3]) and self.vel > 0:
                    # print("Right Collision detected!")
                    self.path[1] = obj.x
                    # Set full path to 300 pixels or to the nearest boundry
                    if obj.x - 200 >= 0:
                        self.path[0] = obj.x - 200
                    else:
                        self.path[0] = 0
                    # Turn around once changes are made
                    self.vel = -3

                if obj.rect.colliderect(self.hitbox[0] - self.vel + offset_x, self.hitbox[1], self.hitbox[2], self.hitbox[3]) and self.vel < 0:
                    # print("Left Collision detected!")
                    self.path[0] = obj.x
                    if obj.x + 200 <= 860:
                        self.path[1] = obj.x + 200
                    else:
                        self.path[1] = 860

                    self.vel = 3

        # Path Boundries
        if self.path[0] < 0:
            self.path[0] = 0
        if self.path[1] > 810:
            self.path[1] = 810
            self.path[0] = 810 - random.uniform(150, 300)
        self.move()

    def move(self):
        shot_interval = random.uniform(0.5, 1)
        current_time = time.time()
        shotMade = False
        if self.vel > 0:
            self.facing = 1
            # Check if the player is in the LOS Right Facing
            if p1.x <= self.path[1] and self.x <= p1.x and p1.row == self.row:
                # print(-1*(-4+(self.y-170)//60))
                # print("This is the player row %d" % p1.row)
                # Chase the Player if in attack range
                if abs(self.x - p1.x) <= 150:
                    shotMade = True
                    self.takeShot(current_time, shot_interval)
            # General Movement
            if not shotMade and not self.processing:
                if self.x < self.path[1] + self.vel - offset_x:
                    self.vel = 3
                    self.x += self.vel
                else:
                    self.vel = self.vel * -1
                    self.x += self.vel
                    self.walkDistance = 0

        elif self.vel < 0:
            # Shoot condition
            self.facing = -1
            # Check player in LOS Left Facing
            if self.x >= p1.x and p1.x >= self.path[0]:
                # Check player in attack range
                if p1.row == self.row:
                    if abs(self.x - p1.x) <= 150:
                        shotMade = True
                        self.takeShot(current_time, shot_interval)
                        self.attack = False

            # General Movement
            if not shotMade and not self.processing:
                if self.x > self.path[0] - self.vel - offset_x:
                    self.x += self.vel
                else:
                    self.vel = self.vel * -1
                    self.x += self.vel
                    self.walkDistance = 0

    def hit(self, bullet):
        hitSound.play()
        self.damage += 1
        if self.damage < self.health:
            if bullet.vel > 0:
                print("Droid detect fire from left")
            elif bullet.vel < 0:
                print("Droid detect fire form right")
        else:
            Map[self.ycoord][self.xcoord] = 'x'
            self.alive = False
            print("Dead")

    def takeShot(self, current_time, shot_interval):
        # WHEN TAKING SHOT, STOP MOVING. This is done through the function as movement takes place after the completion of this function.
        reloadTime = current_time - self.reloadStart
        # print(reloadTime)
        self.shotMade = False
        self.attack = True
        Map[self.ycoord][self.xcoord] = 'a'

        if self.emptyMag:
            if reloadTime >= 2:
                self.emptyMag = False
                print("Mag In")

        if self.bulletshot < 5 and not self.emptyMag and (current_time - self.last_shot > shot_interval):
            self.bulletshot += 1
            self.bullets.append(shot(round(self.x+self.width//2),
                                     round(self.y + self.height//2), 6, 'red blaster', self.facing))
            self.last_shot = current_time
        elif self.bulletshot == 5:
            self.emptyMag = True
            self.reloadStart = time.time()
            self.bulletshot = 0
            print("Droid Reloading...")

    def coordinates(self):
        self.row = -1*(-4+(self.y-170)//60)

        self.oldxcoord = self.xcoord
        self.oldycoord = self.ycoord

        self.xcoord = ((self.x + 100) // Grid_Size) - \
            1  # Manual adjust for error
        self.ycoord = ((self.y - 60) // Grid_Size) - 1
        # Reset Coordinates
        Map[self.oldycoord][self.oldxcoord] = 'x'
        Map[self.ycoord][self.xcoord] = 'o'
        self.scout()

    def scout(self):
        # Test and set the scout grids to blue
        currentTime = time.time()
        i_start = self.xcoord - 1
        i_end = self.xcoord + 1
        j_start = self.ycoord - 1
        j_end = self.ycoord + 1

# Error where droids will move past the designated scout grid
        if not self.processing:
            for j in range(j_start, j_end + 1):
                for i in range(i_start, i_end + 1):
                    # Check boundries
                    if 0 <= i < len(Map[0]) and 0 <= j < len(Map):
                        if (i == self.xcoord and j == self.ycoord):
                            continue
                        if j == self.ycoord:
                            #  if i * 60 > self.xcoord * 60 and i * 60 < self.xcoord * 60:
                            continue
                        # if ally is across, check and change path once only
                        #     if i * 60 < self.path[0] or i * 60 > self.path[1]:
                        #         print(f"Ally found across at {i+1} {j+1}")
                        #         self.target_x, self.target_y = i,j
                        #         self.alertedTime = time.time()
                        #         self.processing = True
                        # If the space is occupied by an enemy -> Check attack == True
                        if Map[j][i] == 'a':
                            # Move and change path
                            # convert from array/0 index to 1 index
                            print(f"Ally Found at {i+1} {j+1}")
                            self.target_x, self.target_y = i, j
                            self.alertedTime = time.time()
                            self.processing = True
                        # else:
                        #     Map[j][i] = 's' Test Line
        elif self.processing:
            # Check if processing time has reached 2 second
            if currentTime - self.alertedTime >= 2:
                self.processing = False
                self.support(self.target_x, self.target_y)

    def support(self, i, j):
        if j != self.ycoord:
            if j > self.ycoord:
                if not obj.rect.colliderect(self.hitbox[0] + offset_x, self.hitbox[1] + 60, self.hitbox[2], self.hitbox[3]):
                    # print(j)
                    # print(self.ycoord + 1)
                    print("moving down")
                    self.y += 60
                    self.path = [self.x - 150, self.x + 150]
            if j < self.ycoord:
                if not obj.rect.colliderect(self.hitbox[0] + offset_x, self.hitbox[1] - 60,  self.hitbox[2], self.hitbox[3]):
                    # print(j)
                    # print(self.ycoord)
                    print("Moving up")
                    self.y -= 60
                    self.path = [self.x - 150, self.x + 150]
        if i != self.xcoord:
            print(i * 60)
            print(self.path[0])
            print(self.path[1])
            if i < self.xcoord:
                # and out of path range
                print("Ally on left fighting!")
                self.path[0] -= 150
                # self.takeShot()
            if i > self.xcoord:
                print("Ally on right fighting!")
                self.path[1] += 150
                # self.takeShot()


class SuperDroid():
    walkRight = [pygame.image.load('SR1.png'), pygame.image.load(
        'SR2.png'), pygame.image.load('SR3.png')]
    walkLeft = [pygame.image.load('SL1.png'), pygame.image.load(
        'SL2.png'), pygame.image.load('SL3.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.path = [x, end]  # path that enemy walks
        self.walkDistance = 0
        self.vel = 3
        # Bullets
        self.facing = 1
        self.bullets = []
        self.last_shot = 0
        self.bulletshot = 0
        self.reloadStart = time.time()
        self.emptyMag = False
        self.magSize = 3

        self.hitbox = (self.x + 14, self.y + 4, 29, 52)
        # self.hp = (self.x, self.y, 29, 3)
        self.damage = 0
        self.health = 5
        self.alive = True

        # Coordinates (0 index)
        self.xcoord = ((self.x + 100) // Grid_Size) - \
            1  # Manual adjust for error
        self.ycoord = ((self.y - 60) // Grid_Size) - 1
        self.row = -1*(-4+(self.y-170)//60)
        self.processing = False

        # Combat States
        self.attack = False
        self.retreat = False
        self.retreatChoice = 1.0
        self.random = random.randint(1, 3)

    def draw(self, win):

        if self.alive:
            if self.walkDistance + 1 >= 9:
                self.walkDistance = 0

            if self.vel > 0:
                win.blit(
                    self.walkRight[self.walkDistance//3], (self.x - offset_x, self.y))
                self.walkDistance += 1

                self.hitbox = (self.x + 14 - offset_x, self.y + 4, 30, 52)
                # self.hp = (self.x + 14, self.y - 5, 29, 3)
            else:
                win.blit(self.walkLeft[self.walkDistance//3],
                         (self.x - offset_x, self.y))
                self.walkDistance += 1

                self.hitbox = (self.x + 24 - offset_x, self.y + 4, 30, 52)
                # self.hp = (self.x + 24, self.y - 5, 29, 3)
            # Health
            pygame.draw.rect(win, (255, 0, 0),
                             (self.hitbox[0], self.hitbox[1] - 10, 30, 5))  # hit box already accounts for offset. dont need to add it here
            pygame.draw.rect(
                win, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 10, 30 - (5*self.damage), 5))
            # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

            self.coordinates()
            self.changePath()

    def changePath(self):
        #****
        for obj in objects:
            # Check for obstacles on the same row
            if self.row == (-1*(-4+(obj.y-170)//60)):
                if obj.rect.colliderect(self.hitbox[0] + self.vel + offset_x, self.hitbox[1], self.hitbox[2], self.hitbox[3]) and self.vel > 0:
                    print("Right Collision detected!")
                    self.path[1] = obj.x
                    # Set full path to 300 pixels or to the nearest boundry
                    if obj.x - 200 >= 0:
                        self.path[0] = obj.x - 200
                    else:
                        self.path[0] = 0
                    # Turn around once changes are made
                    self.vel = -3

                if obj.rect.colliderect(self.hitbox[0] - self.vel + offset_x, self.hitbox[1], self.hitbox[2], self.hitbox[3]) and self.vel < 0:
                    print("Left Collision detected!")
                    self.path[0] = obj.x
                    if obj.x + 200 <= 860:
                        self.path[1] = obj.x + 200
                    else:
                        self.path[1] = 860
                    self.vel = 3

        # Path Boundries
        if self.path[0] < 0:
            self.path[0] = 0
        if self.path[1] > 810:
            self.path[1] = 810
            self.path[0] = 810 - random.uniform(300, 500)

        self.move()

    def move(self):
        shot_interval = random.uniform(1.5, 2)
        current_time = time.time()
        shotMade = False

        if self.vel > 0:
            self.facing = 1
            # Check player in LOS Right Facing
            if p1.x <= self.path[1] and self.x <= p1.x and p1.row == self.row:
                if abs(self.x - p1.x) <= 200:
                    shotMade = True
                    self.takeShot(current_time, shot_interval)
            if not shotMade:
                if self.x < self.path[1] + self.vel - offset_x:
                    self.vel = 3
                    self.x += self.vel
                else:
                    self.vel = self.vel * -1
                    self.x += self.vel
                    self.walkDistance = 0

        elif self.vel < 0:
            self.facing = -1
            if self.x >= p1.x and p1.x >= self.path[0] and p1.row == self.row:
                if abs(self.x - p1.x) <= 200:
                    shotMade = True
                    self.takeShot(current_time, shot_interval)
            # General Movement
            if not shotMade:
                if self.x > self.path[0] - self.vel - offset_x:
                    self.x += self.vel
                else:
                    self.vel = self.vel * -1
                    self.x += self.vel
                    self.walkDistance = 0

    def hit(self, bullet):
        hitSound.play()
        self.damage += 1
        self.retreat += 0.1
        if self.damage < self.health:
            if bullet.vel > 0:
                print("Hit from left")
                # Run thorugh retreat, if retreat is true then face away and extend path past, if not possible then swap rows
                if self.decision() == "attack":
                    if self.vel > 0:
                        self.vel *= -1
                else:
                    self.retreatMode()
            if bullet.vel < 0:
                print("Hit from right")
                if self.decision() == "attack":
                    if self.vel < 0:
                        self.vel *= -1
                else:
                    self.retreatMode()
        else:
            self.alive = False
            print("Super Droid Defeated")
            Map[self.ycoord][self.xcoord] = 'x'

    def takeShot(self, current_time, shot_interval):
        # WHEN TAKING SHOT, STOP MOVING.
        # This is done through the function as movement takes place after the completion of this function.
        reloadTime = current_time - self.reloadStart
        self.shotMade = False
        self.attack = True
        # Map[self.ycoord][self.xcoord] = 'a'

        if self.emptyMag:
            if reloadTime >= 2:
                self.emptyMag = False
                print("Mag In")

        if self.bulletshot < self.magSize and not self.emptyMag and (current_time - self.last_shot > shot_interval):
            self.bulletshot += 1
            self.bullets.append(shot(round(self.x+self.width//2),
                                     round(self.y + self.height//2), 6, 'missile', self.facing))
            self.last_shot = current_time
        elif self.bulletshot == self.magSize:
            self.emptyMag = True
            self.reloadStart = time.time()
            self.bulletshot = 0
            print("Super Droid Reloading...")

    def coordinates(self):
        self.oldxcoord = self.xcoord
        self.oldycoord = self.ycoord

        self.xcoord = ((self.x + 100) // Grid_Size) - \
            1  # Manual adjust for error
        self.ycoord = ((self.y - 60) // Grid_Size) - 1
        # Reset Coordinates
        Map[self.oldycoord][self.oldxcoord] = 'x'
        Map[self.ycoord][self.xcoord] = 'o'
        self.scout()

    def scout(self):  # ***
        # Scout Strategy
        # check grid and 2 more left and right
        # if in left and right vicinity, will face opponent
        # if attacked, it will change path by checking location of shot
        # attacks if higher or equal health
        # moves forward
        # retreats if lower health
        # moves back or up down
        # Slightly random retreat decision making
        # if self.health - random.randint(0, 5) <= p1.health:
        # print(f"p: {p1.health} e: {self.health - random.randint(0, 5)}")

        i_start = self.xcoord - 1
        i_end = self.xcoord + 1
        j_start = self.ycoord - 1
        j_end = self.ycoord + 1
        # target_x,target_y = 0,0

# Error where doirds will move past the designated scout grid
        if not self.processing:
            for j in range(j_start, j_end + 1):
                for i in range(i_start, i_end + 1):
                    # Check boundries
                    if 0 <= i < len(Map[0]) and 0 <= j < len(Map):
                        # Pass on self grid
                        if i == self.xcoord and j == self.ycoord:
                            # Player detection on row
                            for a in range(i_start - 2, i_end + 3):
                                # check to ensure it doesnt go past the boundries again
                                if 0 <= a < len(Map[0]):
                                    if Map[j][a] == 'p':
                                        # Attack player
                                        self.proximity(a)

                        if Map[j][i] == 'a':
                            # Move and change path
                            # convert from array/0 index to 1 index
                            print(f"Ally Found at {i+1} {j+1}")
                            self.target_x, self.target_y = i+1, j+1
                            self.alertedTime = time.time()
                            self.processing = True
                        # else:
                        #     Map[j][i] = 's' #Test Line
        elif self.processing:
            # Check if processing time has reached 2 second
            if currentTime - self.alertedTime >= 2:
                self.processing = False
                self.support(self.target_x, self.target_y)

    def support(self, i, j):
        if j != self.ycoord:
            if j > self.ycoord:
                if not obj.rect.colliderect(self.hitbox[0] + offset_x, self.hitbox[1] - 60, self.hitbox[2], self.hitbox[3]):
                    # print(j)
                    # print(self.ycoord + 1)
                    print("moving down")
                    self.y += 60
                    self.path = [self.x - 150, self.x + 150]
            if j < self.ycoord:
                if not obj.rect.colliderect(self.hitbox[0] + offset_x, self.hitbox[1] + 60,  self.hitbox[2], self.hitbox[3]):
                    # print(j)
                    # print(self.ycoord)
                    print("Moving up")
                    self.y -= 60
                    self.path = [self.x - 150, self.x + 150]
        if i != self.xcoord:
            if i < self.xcoord:
                # and out of path range
                print("Ally on left fighting!")
                self.path[0] -= 150
                # self.takeShot()
            if i > self.xcoord:
                print("Ally on right fighting!")
                self.path[1] += 150
                # self.takeShot()

    def proximity(self, a):
        self.attack = True
        # If the space is occupied by an enemy -> Check attack == True
        if a > self.xcoord:
            print("player detected on the right")
            if self.decision() == "attack":
                self.vel = 3
                if self.path[1] < 800:
                    self.path[1] += 100
                    self.path[0] += 100
            else:
                self.retreatMode()
        if a < self.xcoord:
            print("Player detected on the left")
            if self.decision() == "attack":
                self.vel = -3
                if self.path[0] > 10:
                    self.path[0] -= 100
                    self.path[1] -= 100
            else:
                self.retreatMode()

    def decision(self):
        print(
            f'This is the attack outcome {self.health * self.random * attackChoice}')
        print(
            f'This is the retreat outcome {p1.health * self.random  *self.retreatChoice}')
        if self.health * attackChoice >= p1.health * self.random * self.retreatChoice:
            print("attack chosen")
            return ("attack")
        elif self.health * attackChoice <= p1.health * self.random * self.retreatChoice:
            return ("retreat")

    def retreatMode(self):

        if self.vel == -3:
            print("walking away to the left")
            if self.path[0] > 10 + 100:
                self.path[0] -= 100
                self.path[1] -= 100
            else:
                self.path[0] = 0

        if self.vel == 3:
            print("walking away to the right")
            if self.path[1] < 800 - 100:
                self.path[0] += 100
                self.path[1] += 100
            else:
                self.path[1] = 800
                self.path[0] = 800 - random.randint(300, 500)


class shot():
    # Player Bullets
    blueBulletLeft = pygame.image.load('Blue_Bullet.png')
    blueBulletRight = pygame.image.load('Blue_BulletR.png')
    # Droid Bullets
    redBulletLeft = pygame.image.load('RedBulletL.png')
    redBulletRight = pygame.image.load('RedBulletR.png')
    # Missles
    missileLeft = pygame.image.load('missileL.png')
    missileRight = pygame.image.load('missileR.png')

    def __init__(self, x, y, rad, type, facing):
        self.x = x - offset_x
        self.y = y
        self.radius = rad
        self.type = type
        self.facing = facing
        self.vel = 8 * facing
        self.xpos = 0

    def draw(self, win):
        # needs to be able to continue off screen
        # pygame.draw.circle(win, (0,0,0), (self.x, self.y), self.radius)
        if self.type == 'missile':
            if self.facing < 0:
                win.blit(self.missileLeft, (self.x-20, self.y-25))
            if self.facing > 0:
                win.blit(self.missileRight, (self.x-20, self.y-25))
        if self.type == 'red blaster':
            if self.facing < 0:
                win.blit(self.redBulletLeft, (self.x-15, self.y-20))
            if self.facing > 0:
                win.blit(self.redBulletRight, (self.x-15, self.y-20))
        if self.type == 'blue blaster':
            if self.facing < 0:
                win.blit(self.blueBulletLeft, (self.x-15, self.y-15))
            if self.facing > 0:
                win.blit(self.blueBulletRight, (self.x-15, self.y-15))


class object():
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect(
            topleft=(self.x, self.y))  # for collision detection
        # Create a grid coordinate for each object so that the ai can calculate the closest one to it

    def draw(self, win):
        pygame.draw.ellipse(win, (83, 80, 82),
                            (self.rect.x + 13 - offset_x, self.y + 35, 40, 20))
        offset_position = (
            self.rect.topleft[0] - offset_x + 10, self.rect.topleft[1] + 10)
        win.blit(self.image, offset_position)


class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(
            image, (int(width*scale), int(height*scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):

        # Put Button on the Screen
        win.blit(self.image, (self.rect.x, self.rect.y))

# Functions


def spawnEnemy():
    while True:
        # Randomly select a row for the enemy to spawn
        y = random.randint(0, 3)
        # Determine the enemy's spawn side based on player's xcoord
        # Player is on the right, spawn enemy on the left (off-screen)
        if p1.xcoord > 7:
            x = 0  # Off-screen on the left
        else:  # Player is on the left, spawn enemy on the right (off-screen)
            x = 15  # Off-screen on the right

        # Ensure that the spawn point on the map is valid (no obstacles)
        if Map[y][x] == 'x':
            break  # Valid spawn point found

    # Calculate true x and y positions for the enemy
    truex = x * Grid_Size
    truey = y * Grid_Size + 170

    # Calculate the enemy's path end point
    calculated_end = truex - offset_x + 450

    # Return a new droid enemy instance with the calculated position and path
    return droid(truex - offset_x, truey, 64, 64, calculated_end)


def spawnSuperDroid():
    # Same logic as spawnEnemy()
    while True:
        if p1.xcoord > 7:
            x = random.randint(0, 7)
            y = random.randint(0, 3)
            if Map[y][x] == 'x':
                break
        if p1.xcoord < 7:
            x = random.randint(8, 15)
            y = random.randint(0, 3)
            if Map[y][x] == 'x':
                break
        # Transform coordinates into actual values
    truex = x * 60
    truey = y * 60 + 170
    calculated_end = truex - offset_x + 450

    return SuperDroid(truex - offset_x, truey, 64, 64, calculated_end)
    # Offset_x is used to allow for enemy spawns off screen


def drawMap():  # **Draw color grid

    for row in range(rows):
        for col in range(cols):
            x = col * Grid_Size - offset_x
            if Map[row][col] == 'x':
                pygame.draw.rect(win, (230, 230, 230), pygame.Rect(
                    x, 250 + ((row-1) * 60), Grid_Size, Grid_Size), 1)
            if Map[row][col] == 'o':
                pygame.draw.rect(win, (255, 0, 0), pygame.Rect(
                    x, 250 + ((row-1) * 60), Grid_Size, Grid_Size), 1)
            if Map[row][col] == 'b':
                # win.blit(box, (x, (row + 1)*60 + 190))
                pygame.draw.rect(win, (255, 165, 0), pygame.Rect(
                    x, 250 + ((row-1) * 60), Grid_Size, Grid_Size), 1)

            # Player Check
            if Map[row][col] == 'p':
                pygame.draw.rect(win, (0, 255, 0), pygame.Rect(
                    x, 250 + ((row-1) * 60), Grid_Size, Grid_Size), 1)
            # Enemy Check

            # Scout Grids
            # if Map[row][col] == 's':
            #     pygame.draw.rect(win, (0, 100, 255), pygame.Rect(
            #         x, 250 + ((row-1) * 60), Grid_Size, Grid_Size), 1)


def drawWindow():
    # Ground and Background
    # Default BG
    # win.blit(bg, (-offset_x, -60))  # Adjust the background position

    # Ship BG
    pygame.draw.rect(win, (200, 200, 200), (0, 0, 900, 60), 0, 2)
    win.blit(ship, (-offset_x, 20))
    win.blit(ship, (-offset_x + 180, 20))

    # Map
    pygame.draw.rect(win, (173, 173, 173), (0, 370, 900, 60), 0, 2)
    pygame.draw.rect(win, (173, 173, 173), (0, 310, 900, 60), 0, 2)
    pygame.draw.rect(win, (173, 173, 173), (0, 250, 900, 60), 0, 2)
    pygame.draw.rect(win, (173, 173, 173), (0, 190, 900, 60), 0, 2)
    drawMap()

    for obj in objects:
        obj.draw(win)

    score = font.render("Score: %d" % p1.score, True, (0, 0, 0))
    win.blit(score, (360, 10))
    playerHealth = font.render("Hp: %d " % p1.health, True, (0, 0, 0))
    win.blit(playerHealth, (20, 10))

    # Player
    if shieldActivated:
        pygame.draw.rect(
            win, (78, 173, 209), (p1.hitbox[0] - 2, p1.hitbox[1] - 5, 40, 55), 0, 0, 5, 5, 5, 5)
    p1.draw(win)

    # Enemies

    for target in enemies:
        target.draw(win)
        for bullet in target.bullets:
            bullet.draw(win)

    for bullet in bullets:
        bullet.draw(win)

    pygame.display.update()

# **


def GameScreen():
    pass


def OptionsScreen():
    pass


def MenuScreen():
    pass


# CHARACTER SPAWN
p1 = player(300, 345, 64, 64)
bullets = []
shotMade = False
bulletShot = 0
emptyMag = False
leftCollide = False
rightCollide = False
upMove = False
downMove = False

# Use this to track each enemy
goblin1 = droid(400, row1, 64, 64, 450)
goblin2 = droid(400, row2, 64, 64, 450)
goblin3 = droid(400, row3, 64, 64, 450)
Superdroid = SuperDroid(0, row4, 64, 64, 450)
enemies = [goblin3, goblin2, goblin1,  Superdroid]

# Objects
# Left Side obstacles
box1 = object(180, 3 * 60 + 190, box)
box2 = object(240, 1 * 60 + 190, box)
box3 = object(10 * 60, 2 * 60 + 190, box)
box4 = object(9 * 60, 0 * 60 + 190, box)
# box5 = object(180, 3 * 60 + 190, box)
# box6 = object(180, 3 * 60 + 190, box)


# Right Side Obstacles
objects = [box4]

run = True

while run:
    clock.tick(27)
    # mouse to see coordinates
    # print(pygame.mouse.get_pos())

    # Use This for time delays
    currentTime = time.time()
    elapsedTime = currentTime - startTime
    shieldelapsedTime = currentTime - shieldstartTime

    for event in pygame.event.get():  # checks inputs
        if event.type == pygame.QUIT:  # checks if close button is clicked
            run = False

# Keyboard Commands
    keys = pygame.key.get_pressed()  # letting keys = dictionary of keyboard inputs

    # if left key is pressed or a, also checks for boundries.
    # Move Left
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and (p1.x - offset_x) > -5 and not leftCollide:
        p1.x -= p1.vel  # Move left by velocity
        p1.left = True  # Set left movement flag
        p1.right = False  # Reset right movement flag
        future_x -= p1.vel  # Update future x position
        p1.standing = False  # Player is not standing (moving)
        p1.startpos = False  # Turn off starting position

    # Move Right
    elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and (p1.x + p1.width + offset_x) < 810 and not rightCollide:
        p1.x += p1.vel  # Move right by velocity
        p1.left = False  # Reset left movement flag
        p1.right = True  # Set right movement flag
        future_x += p1.vel  # Update future x position
        p1.standing = False  # Player is not standing (moving)
        p1.startpos = False  # Turn of starting position

    # If no movement keys are pressed, player is standing
    else:
        p1.standing = True  # Player is standing

    # and not shotMade ##BE CARFEUL WITH THESE IF STATEMENTS, ENSURE PROPER BRACKETS
    if ((keys[pygame.K_o] or keys[pygame.K_SPACE]) and not shotMade):
        shotMade = True
        if p1.left:
            facing = -1
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            facing = 0
        else:
            facing = 1

        if emptyMag:
            if elapsedTime >= 2:
                emptyMag = False
                print("Mag In")

        # spawn bullet from the middle of the character
        if not shieldActivated:
            if bulletShot < p1.magSize and not emptyMag:
                bulletShot += 1
                bulletSound.play()
                # Does not account for player offset
                bullets.append(shot(round(p1.x+p1.width//2),
                                    round(p1.y + p1.height//2), 6, 'blue blaster', facing))
                # print("%d" % len(bullets))
                # print("%d" % bulletShot)

            elif bulletShot == p1.magSize:
                emptyMag = True
                startTime = time.time()
                bulletShot = 0
                print("Reloading...")

    if not (keys[pygame.K_o] or keys[pygame.K_SPACE]):
        shotMade = False

# Row (up/down) Movement
    if (keys[pygame.K_UP] or keys[pygame.K_w]) and not upCollide and p1.row < 4 and not upMove:
        p1.y -= strafeWidth
        # ^print(p1.y)
        upMove = True
        p1.row += 1

    elif not (keys[pygame.K_UP] or keys[pygame.K_w]):
        upMove = False

    if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and not downCollide and p1.row > 1 and not downMove:
        p1.y += strafeWidth
        # ^print(p1.y)
        downMove = True
        p1.row -= 1

    elif not (keys[pygame.K_DOWN] or keys[pygame.K_s]):
        downMove = False

# Bullets movement
    for bullet in bullets:
        if bullet.x + offset_x < (902) and bullet.x + offset_x > (-75) and bullet.y < 480 and bullet.y > 0:
            if not bullet.vel == 0:
                bullet.x += bullet.vel
            else:
                bullet.y += -8
        else:
            bullets.pop(bullets.index(bullet))

    for target in enemies:
        for bullet in target.bullets:
            if bullet.x + offset_x < (902) and bullet.x + offset_x > (-75) and bullet.y < 480 and bullet.y > 0:
                if not bullet.vel == 0:
                    bullet.x += bullet.vel
                else:
                    bullet.y += -8
            else:
                target.bullets.pop(target.bullets.index(bullet))

    # Bullet contact Enemy
    for target in enemies:
        for bullet in bullets:
            if (bullet.y + bullet.radius) >= target.hitbox[1] and (bullet.y - bullet.radius) <= (target.hitbox[1] + target.hitbox[3]):
                if (bullet.x + bullet.radius) >= target.hitbox[0] and (bullet.x - (2*bullet.radius)) <= (target.hitbox[0] + target.hitbox[2]):
                    # Send bullet information to A.I.
                    target.hit(bullet)
                    bullets.pop(bullets.index(bullet))
                    # create new enemy
                    if isinstance(target, droid):
                        if not target.alive:
                            p1.score += 1
                            enemies.remove(target)
                            enemy_name = f'droid{p1.score + 2}'
                            enemy_name = spawnEnemy()
                            enemies.append(enemy_name)
                            # Face the nearest player
                            # if goblin1.x > (p1.x + p1.width):
                            #     goblin1.vel = -3
                            # else:
                            #     goblin1.vel = 3
                    if isinstance(target, SuperDroid):
                        if not Superdroid.alive:
                            p1.score += 1
                            enemies.remove(target)
                            enemy_name = f'Superdroid{p1.score + 2}'
                            enemy_name = spawnSuperDroid()
                            enemies.append(enemy_name)
    # Bullet contact Player
    for target in enemies:
        for bullet in target.bullets:
            if (bullet.y + bullet.radius) >= p1.hitbox[1] and (bullet.y - bullet.radius) <= (p1.hitbox[1] + p1.hitbox[3]):
                if (bullet.x + bullet.radius) >= p1.hitbox[0] and (bullet.x - (2*bullet.radius)) <= (p1.hitbox[0] + p1.hitbox[2]):
                    if not shieldActivated:
                        p1.hit(attackChoice)
                        shieldActivated = True
                        target.bullets.pop(target.bullets.index(bullet))
                        shieldstartTime = time.time()
                        shieldActivated = True
                    elif shieldActivated:
                        hitSound.play()
                        target.bullets.pop(target.bullets.index(bullet))

# COLLISION CHECKS
# Player Collision
    for target in enemies:
        if (p1.hitbox[1] > target.hitbox[1]) and (p1.hitbox[1] < target.hitbox[1] + target.hitbox[3]):
            if (p1.hitbox[0] > target.hitbox[0]) and (p1.hitbox[0] < target.hitbox[0] + target.hitbox[2]):
                if not shieldActivated:
                    if p1.health == 1:
                        print("Game over")
                        gameOver = True
                    print("Player Hit")
                    p1.hit(attackChoice)
                    shieldstartTime = time.time()
                    shieldActivated = True
                    # print("Immunity Activated")

# Object Collision Player
    leftCollide = False
    rightCollide = False
    upCollide = False
    downCollide = False
    for obj in objects:

        # This placement is not correct. The only a single box will be detected
        # Update Obj.rect pos

        # Collision detection for player
        if obj.rect.colliderect(p1.hitbox[0] + p1.vel + offset_x, p1.hitbox[1], p1.hitbox[2], p1.hitbox[3]) and p1.right:
            print("Right Collision detected!")
            # print("Crouch can be enabled")
            rightCollide = True
        if obj.rect.colliderect(p1.hitbox[0] - p1.vel + offset_x, p1.hitbox[1], p1.hitbox[2], p1.hitbox[3]) and p1.left:
            print("Left Collision detected!")
            leftCollide = True

        if obj.rect.colliderect(p1.hitbox[0] + offset_x, p1.hitbox[1] + 60,  p1.hitbox[2], p1.hitbox[3]):
            print("Down Collision Detected")
            downCollide = True

        if obj.rect.colliderect(p1.hitbox[0] + offset_x, p1.hitbox[1] - 60, p1.hitbox[2], p1.hitbox[3]):
            print("Up Collision Detected")
            upCollide = True

    for obj in objects:
        # Bullet Detection
        for bullet in bullets:
            if (bullet.y + bullet.radius) >= obj.rect.top and (bullet.y - bullet.radius) <= obj.rect.bottom:
                if (bullet.x + bullet.radius) >= obj.rect.left - offset_x and (bullet.x - (2*bullet.radius)) <= (obj.rect.right - offset_x):
                    bullets.pop(bullets.index(bullet))

# Object Collision Bots
        for enemy in enemies:
            for bullet in enemy.bullets:
                if (bullet.y + bullet.radius) >= obj.rect.top and (bullet.y - bullet.radius) <= obj.rect.bottom:
                    if (bullet.x + bullet.radius) >= obj.rect.left - offset_x and (bullet.x - (2*bullet.radius)) <= (obj.rect.right - offset_x):
                        enemy.bullets.pop(enemy.bullets.index(bullet))

# Shield Activation
    if shieldActivated:
        if currentTime - shieldstartTime >= 5:
            shieldActivated = False
            # print("Immunity deactivated")

# Scroll Background (Move Map)
    if (((p1.x + p1.width - offset_x >= WIDTH - scrollWidth) and p1.right) or (p1.x - offset_x <= scrollWidth) and p1.left):
        if p1.right and (p1.x + p1.width + offset_x) < 750:
            offset_x += p1.vel

        if p1.left and (p1.x + offset_x) > 150:
            offset_x -= p1.vel

# Draw Window
    # if not gameOver: FREEZE SCREEN WHEN GAME OVER ****
    drawWindow()


pygame.quit()  # Quits program after exiting main loop
