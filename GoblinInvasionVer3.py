import pygame
import random
import time
import sys
import os.path

begining = True

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def redrawGameWindow(first):
    win.blit(bg, (0, 0))
    if man.alive:
        if hits != 0:
            text = font.render('Time: ' + str(timeIs) + ' s', 1, (0, 0, 0))
            win.blit(text, ((W - 600) - 25, 75))
        text = font.render('Hits Needed: ' + str(hits), 1, (0, 0, 0))
        win.blit(text, ((W - 450) - 25, 10))
        text = font.render('Hits Scored: ' + str(score), 1, (0, 0, 0))
        win.blit(text, ((W - 450) - 25, 40))
        text = font.render('Ammo: ' + str(Ammo), 1, (0, 0, 255))
        win.blit(text, ((W - 700) - 25, 40))
        text = font.render('Lives: ' + str(lives), 1, (255, 0, 0))
        win.blit(text, ((W - 700) - 25, 10))
        font1 = pygame.font.SysFont('timesnewroman', 50, True)
        text = font1.render('Goblin Invasion!', 1, (0, 128, 0))
        win.blit(text, ((W - 670) - 25, 100))
    if hits == 0:
        if points == goblinHealth:
            text = font.render('Perfect Game!', 1, (0, 0, 255))
            win.blit(text, (380, 280))
        if goblinHealth > points >= score - (goblinHealth / 20):
            text = font.render('Good Game!', 0, (0, 0, 255))
            win.blit(text, (380, 280))
        if points < goblinHealth / 2:
            text = font.render('Better luck next time', 0, (0, 0, 255))
            win.blit(text, (320, 280))
        if goblinHealth - (goblinHealth / 10) > points >= goblinHealth - (goblinHealth / 2):
            text = font.render('Fair Game!', 0, (0, 0, 255))
            win.blit(text, (380, 280))
        text = font.render('Thank You For Playing Goblin Invasion', 1, (0, 0, 0))
        win.blit(text, (300, 420))
        text = font.render('You Deafeated the Goblin in ' + str(timeIs) + ' Seconds!', 1, (0, 0, 0))
        win.blit(text, (300, 360))

    if lives <= 0:
        man.alive = False
        pygame.mixer.music.stop()
        if first:
            isfade = True
            first = False
        else:
            win.fill((0, 0, 0))
            goblin.visible = False
            win.blit(Skull, (250, 0))
            pygame.mixer.music.pause()
            text = font.render('You Died', 1, (255, 0, 0))
            win.blit(text, (((W - (W / 2)) - 30), 40))


    if len(bullets2) == amo and lives != 0 and hits != 0:
        text = font.render('You Ran Out of Ammo! Try Again!!', 1, (255, 0, 0))
        win.blit(text, (300, 220))


    man.draw(win)
    if man.alive:
        if (__DEBUG_MODE__):
            print ("Man alive")
        if goblin.dead:
            goblin.visible = False
            text2 = font.render('Goblin Defeated!', 1, (255, 255, 0))
            win.blit(text2, (400, 250))
        else:
            goblin.visible = True
            goblin.draw(win)

        Mutebutton.draw(win, (0, 0, 0))
        GameQuitbutton.draw(win, (0, 0, 0))
        if hits != 0:
            Pausebutton.draw(win, (0, 0, 0))


        for x in bullets:
            x.draw(win)

    return first

def PythonTypeWriter(message):
    for char in message:
        sys.stdout.write(char)
        sys.stdout.flush()
        if char != "\n" and char != ',' and char != '.' and char != "!" and char != "?":
            time.sleep(0.15)
        else:
            time.sleep(1)

def Typer(text, WIDTH, HEIGHT, screen):
    #music = pygame.mixer.music.load(resource_path(r'C:\Users\Simmi\Downloads\Recording3.mp3'))
    #pygame.mixer.music.play(-1)
    class Board(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((WIDTH, HEIGHT))
            self.image.fill((13,13,13))
            self.image.set_colorkey((13,13,13))
            self.rect = self.image.get_rect()
            self.font = pygame.font.SysFont("monospace", 20)

        def add(self, letter, pos):
            s = self.font.render(letter, 1, (255, 255, 0))
            self.image.blit(s, pos)

    class Cursor(pygame.sprite.Sprite):
        def __init__(self, board):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((3, 20))
            self.image.fill((0, 0, 0))
            self.text_height = 25
            self.startText_height = 17
            self.text_width = 10
            #self.text_width = 15
            self.rect = self.image.get_rect(topleft=(self.text_width, self.startText_height))
            self.board = board
            self.text = ''
            self.cooldown = 0

        def write(self, text):
            self.text = list(text)


        def update(self):
            if not self.cooldown and self.text:
                letter = self.text.pop(0)
                if letter == '\n':
                    self.rect.move_ip((0, self.text_height))
                    self.rect.x = self.text_width
                    time.sleep(1)
                else:
                   if letter == ',' or letter == '.' or letter == '?' or letter == '"':
                        time.sleep(1)
                   self.board.add(letter, self.rect.topleft)
                   self.rect.move_ip((self.text_width, 0))
                   if self.rect.topleft[0] >= WIDTH - 50:
                        self.rect.move_ip((0, self.text_height))
                        self.rect.x = self.text_width

    all_sprites = pygame.sprite.Group()
    board = Board()
    cursor = Cursor(board)
    all_sprites.add(cursor, board)

    cursor.write(text)

    #Main loop
    running = True
    while running:

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
                pygame.quit()

        all_sprites.update()
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(10)

def endScreen(first):
    global lives, Ammo, hits, score, points
    lives = 10
    Ammo = round(100/ damage) + 200
    hits = bg_hits
    points = 0
    score = 0
    fade(W, H)
    man.alive = False
    pygame.mixer.music.stop()
    run = True
    while run:
        win.fill((0, 0, 0))
        win.blit(Skull, (250, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type in (pygame.KEYDOWN, pygame.KEYUP):
                run = False

def controlMenu():
    font1 = pygame.font.SysFont('timesnewroman', 30, True)
    begining = False
    looping = True
    print('dude')
    while looping:
        looping = True
        print('Ahhhh!')
        backButton.draw(win, (0, 0, 0))
        text = font1.render('Controls', 1, (255, 255, 255))
        win.blit(text, (350, 48))
        #text = font1.render('Use the left and right arrow keys to move around', 1, (128, 0, 0))
        # win.blit(text, (180, 200))
        # text = font1.render('Use the up arrow key to jump', 1, (128, 0, 0))
        # win.blit(text, (200, 240))
        # text = font1.render('Use the spacebar to shoot', 1, (128, 0, 0))
        # win.blit(text, (200, 280))
        # text = font1.render('Destroy the Goblin!', 1, (128, 0, 0))
        # win.blit(text, (250, 320))
        for event in pygame.event.get():
            if event.type == (pygame.MOUSEBUTTONDOWN):
                if backButton.isOver(pos):
                    looping = False
                    begining = True
            if event.type in (pygame.KEYDOWN, pygame.KEYUP):
                looping = False
        return begining
        pygame.display.update()

def MainMenu(start, begining):
    font1 = pygame.font.SysFont('timesnewroman', 30, True)
    win.blit(MainScreen, (0, 0))
    if begining:
        text = font1.render('Main Menu', 1, (255, 255, 255))
        win.blit(text, (400, 48))
        text = font1.render('Press a key to Start!', 1, (0, 0, 128))
        win.blit(text, (350, 200))
        MainQuitButton.draw(win, (0, 0, 0))
        #contolbutton.draw(win, (0, 0, 0))
    pos = pygame.mouse.get_pos()
    while start:
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if MainQuitButton.isOver(pos):
                    if (__DEBUG_MODE__):
                        print('clicked!')
                    pygame.quit()
                    start = False
                #if contolbutton.isOver(pos):
                    #print('hi')
                    #controlMenu()
                    #print("not good")

            if event.type == pygame.MOUSEMOTION:
                if MainQuitButton.isOver(pos):
                    if (__DEBUG_MODE__):
                        print('on top!')
                    MainQuitButton.color = (255, 0, 0)
                else:
                    MainQuitButton.color = (0, 0, 128)

                #if contolbutton.isOver(pos):
                    #contolbutton.color = (255, 0, 0)
                #else:
                    #contolbutton.color = (0, 0, 128)

            if event.type in (pygame.KEYDOWN, pygame.KEYUP):
                if not keys[pygame.K_f]:
                    start = False
                #isfade = True
            if event.type == pygame.QUIT:
                pygame.quit()

            return start
        #pygame.display.update()

def pauseMenu():
    font1 = pygame.font.SysFont('timesnewroman', 50, True)
    clock.tick(27)
    win.blit(bg, (0, 0))
    man.draw(win)
    goblin.pause = True
    goblin.draw(win)
    text = font1.render('PAUSED', 1, (0, 0, 0))
    win.blit(text, ((W - 590) - 25, 100))
    if(__DEBUG_MODE__):
        print("Pause Blitted ")
    #win.blit(standing, (350, 400))
    UnpauseButton.draw(win, (0, 0, 0))
    QuitButton.draw(win, (0, 0, 0))
    Mutebutton.draw(win, (0, 0, 0))
    #pygame.display.update()

        #pygame.time.wait(5000)
        #break

def unpause(pause):
    if(__DEBUG_MODE__):
        print('Unpausing')
    #fade(W, H, (255, 255, 255))
    pause = False
    return pause

def loading():
        pygame.event.get()
        win.fill((0, 0, 0))
        text = font.render('Loading...', 1, (255, 255, 255))
        win.blit(text, (350, 200))

def typeWriter(message, x=50, y=100):
    pygame.mixer.music.play(-1)
    x2 = x
    for char in message:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
        text = font.render(str(char), 0, red)
        win.blit(text, (x, y))
        if char != "\n" and char != ',' and char != '.' and char != '!' and char != "?":
            time.sleep(0.075)
            # time.sleep(0.15)
        else:
            time.sleep(1)

        if x >= W - 50:
            y += 30
            x = x2
        else:
            x += 17
        pygame.display.update()

def fade(width, height, color=(0, 0, 0)):
    fade = pygame.Surface((width, height))
    fade.fill(color)
    for alpha in range(0, 300):
        fade.set_alpha(alpha)
        redrawGameWindow(first)
        win.blit(fade, (0,0))
        pygame.display.update()
        #pygame.time.delay(5)

__DEBUG_MODE__ = False

pygame.init()

W = 1000
H = 580

win = pygame.display.set_mode((W, H), pygame.RESIZABLE)
pygame.display.set_caption("Goblin Invasion")
pygame.mixer.init()
music = pygame.mixer.music.load(resource_path('Game\music.mp3'))
pygame.mixer.music.play(-1)
Skull = pygame.transform.scale(pygame.image.load(resource_path('Game\Skull.png')), (570, (H - 10)))
bg = pygame.transform.scale(pygame.image.load(resource_path('Game/bg.jpg')), (W, (H + 20)))
MainScreen = pygame.transform.scale(pygame.image.load(resource_path('Game\MainMenu.png')), (W, (H + 20)))
Icon = pygame.image.load(resource_path('Game/SkullIicon.png'))
clock = pygame.time.Clock()

goblinHealth = 100
amo = goblinHealth + 150
hits = goblinHealth
score = 0
start_ticks = pygame.time.get_ticks()
lives = 10
pause = False
first = True
points = 0
FPS = 35

class player(object):
    walkRight = [pygame.image.load(resource_path('Game\R1.png')),
                 pygame.image.load(resource_path('Game\R2.png')),
                 pygame.image.load(resource_path('Game\R3.png')),
                 pygame.image.load(resource_path('Game\R4.png')),
                 pygame.image.load(resource_path('Game\R5.png')),
                 pygame.image.load(resource_path('Game\R6.png')),
                 pygame.image.load(resource_path('Game\R7.png')),
                 pygame.image.load(resource_path('Game\R8.png')),
                 pygame.image.load(resource_path('Game\R9.png'))]
    walkLeft = [pygame.image.load(resource_path('Game\L1.png')),
                pygame.image.load(resource_path('Game\L2.png')),
                pygame.image.load(resource_path('Game\L3.png')),
                pygame.image.load(resource_path('Game\L4.png')),
                pygame.image.load(resource_path('Game\L5.png')),
                pygame.image.load(resource_path('Game\L6.png')),
                pygame.image.load(resource_path('Game\L7.png')),
                pygame.image.load(resource_path('Game\L8.png')),
                pygame.image.load(resource_path('Game\L9.png'))]

    def __init__(self, x, y, width, height, label):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.hitCount = 0
        self.jumpCount = 10
        self.standing = True
        self.alive = True
        self.gameover = False
        self.label = label
        self.hit_box = (self.x + 22, self.y + 15, 35, 65)
        self.font = pygame.font.SysFont('comicsans', 40, True)

    def draw(self, window):
        if self.alive:
            if self.walkCount + 1 >= 27:
                self.walkCount = 0

            if not self.standing:
                if self.left:
                    window.blit(pygame.transform.scale(self.walkLeft[self.walkCount // 3], (80, 80)), (self.x, self.y))
                    self.walkCount += 1
                elif self.right:
                    window.blit(pygame.transform.scale(self.walkRight[self.walkCount // 3], (80, 80)), (self.x, self.y))
                    self.walkCount += 1
            else:
                if self.right:
                    window.blit(pygame.transform.scale(self.walkRight[0], (80, 80)), (self.x, self.y))
                else:
                    window.blit(pygame.transform.scale(self.walkLeft[0], (80, 80)), (self.x, self.y))
            self.hit_box = (self.x + 22, self.y + 15, 31, 62)
            # pygame.draw.rect(win, (255, 0, 0), self.hit_box, 2)

            if not self.gameover:
                text = self.font.render(str(self.label), 1, (0, 0, 230))
                win.blit(text, (self.x + 25, self.y - 10))

    def hit(self):
        if self.alive:
            self.isJump = False
            self.jumpCount = 10
            if self.x < (W / 2):
                self.x += 100
            if self.x > (W / 2):
                self.x -= 200
            self.y = H - 80
            self.walkCount = 0
            font1 = pygame.font.SysFont('timesnewroman', 100)
            self.hitCount += 1
            text = font1.render('Hit!', 1, (255, 0, 0))
            win.blit(text, (420, 200))
            pygame.display.update()
            i = 0
            while i < 100:
                pygame.time.delay(10)
                i += 1
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        i = 101
                        pygame.quit()
                        quit()

class projectile(object):
    def __init__(self, x, y, radius, color, direction):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = direction
        self.vel = 8 * direction
        self.manIsJump = False
    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)

class enemy(object):
    walkRight = [pygame.image.load(resource_path('Game\R1E.png')),
                 pygame.image.load(resource_path('Game\R2E.png')),
                 pygame.image.load(resource_path('Game\R3E.png')),
                 pygame.image.load(resource_path('Game\R4E.png')),
                 pygame.image.load(resource_path('Game\R5E.png')),
                 pygame.image.load(resource_path('Game\R6E.png')),
                 pygame.image.load(resource_path('Game\R7E.png')),
                 pygame.image.load(resource_path('Game\R8E.png')),
                 pygame.image.load(resource_path('Game\R9E.png')),
                 pygame.image.load(resource_path('Game\R10E.png')),
                 pygame.image.load(resource_path('Game\R11E.png'))]
    walkLeft = [pygame.image.load(resource_path('Game\L1E.png')),
                pygame.image.load(resource_path('Game\L2E.png')),
                pygame.image.load(resource_path('Game\L3E.png')),
                pygame.image.load(resource_path('Game\L4E.png')),
                pygame.image.load(resource_path('Game\L5E.png')),
                pygame.image.load(resource_path('Game\L6E.png')),
                pygame.image.load(resource_path('Game\L7E.png')),
                pygame.image.load(resource_path('Game\L8E.png')),
                pygame.image.load(resource_path('Game\L9E.png')),
                pygame.image.load(resource_path('Game\L10E.png')),
                pygame.image.load(resource_path('Game\L11E.png'))]

    def __init__(self, x, y, width, height, end, health):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 11
        self.hit_box = (self.x + 20, self.y + 2, 31, 65)
        self.health = health
        self.killhealth = health / 10
        self.isJump = False
        self.jumpCount = 10
        self.visible = True
        self.dead = False
        self.right = False
        self.left = False
        self.pause = False

    def draw(self, window):
        self.move()
        if self.visible:
            if (__DEBUG_MODE__):
                print('Goblin drawn!')
            if self.walkCount + 1 >= 33:
                self.walkCount = 0

            if self.vel > 0:
                window.blit(pygame.transform.scale(self.walkRight[self.walkCount // 3], (80, 80)), (self.x, self.y))
                self.walkCount += 1
            elif self.vel < 0:
                window.blit(pygame.transform.scale(self.walkLeft[self.walkCount // 3], (80, 80)), (self.x, self.y))
                self.walkCount += 1

            pygame.draw.rect(window, (0, 0, 0), (self.hit_box[0], self.hit_box[1] - 20, 50, 10))
            # pygame.draw.rect(window, (0, 128, 0), (self.hit_box[0], self.hit_box[1] - 20, 50, 10))
            pygame.draw.rect(window, (255, 0, 0), (self.hit_box[0], self.hit_box[1] - 20, 50 - (5 * (10 - (self.health / self.killhealth))) ,10))
            self.hit_box = (self.x + 30, self.y + 2, 31, 65)
            # pygame.draw.rect(win, (255,0,0), self.hit_box,2)

        if self.isJump:
            self.jump()
        if self.dead:
            self.visible = False
            if (__DEBUG_MODE__):
                print('goblin is dead')

    def move(self):
        if not self.pause:
            if self.vel > 0:
                if self.x + self.vel < self.path[1]:
                    self.x += self.vel
                else:
                    self.vel = self.vel * -1
                    self.walkCount = 0
            else:
                if self.x - self.vel > self.path[0]:
                    self.x += self.vel
                else:
                    self.vel = self.vel * -1
                    self.walkCount = 0

    def jump(self):
        if not self.pause:
            if self.jumpCount >= -10:
                neg = 1.5
                if self.jumpCount < 0:
                    neg = -1.5
                self.y -= (self.jumpCount ** 2) * 0.5 * neg
                self.jumpCount -= 1
            else:
                self.isJump = False
                self.jumpCount = 10

    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False

class button(object):
    def __init__(self, color, x, y, width, height, text='', size=20):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.size = size

    def draw(self, window, outline=None):
        if outline:
            pygame.draw.rect(window, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font1 = pygame.font.SysFont('timesnewroman', self.size)
            text = font1.render(self.text, 1, (0, 0, 0))
            window.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, position):
        if self.x < position[0] < self.x + self.width:
            if self.y < position[1] < self.y + self.height:
                return True

        return False

# mainloop
font = pygame.font.SysFont('timesnewroman', 30, True)
man = player((W - 300), (H - 80), 64, 64, 'P1')
goblin = enemy(10, (H - 80), 64, 64, (W - 50), goblinHealth)
Mutebutton = button((0, 128, 255), 20, 40, 70, 30, 'Mute')
Unmutebutton = button((255, 200, 0), 20, 90, 70, 30, "UnMute")
UnpauseButton = button((0, 255, 0), 250, 250, 220, 60, 'CONTINUE', 40)
QuitButton = button((255, 0, 0), 550, 250, 220, 60, 'QUIT', 40)
Pausebutton = button((0, 200, 0), (W - 90), 40, 70, 30, "Pause")
GameQuitbutton = button((255, 0, 0), (W - 90), 90, 70, 30, "Quit")
MainQuitButton = button((0, 0, 128), 750, 450, 160, 60, 'Quit', 40)
contolbutton = button((0, 0, 128), 250, 350, 160, 60, 'Controls', 40)
backButton = button((255, 128, 0), 20, 20, 70, 40, 'Back')
pygame.display.set_icon(Icon)
pygame.mixer.music.set_volume(0.3)
timer = time.perf_counter()
event = pygame.event.wait()
shootLoop = 0
bullets = []
bullets2 = []
run = True
start = True
isfade = False

while run:
    clock.tick(FPS)

    timeUp = time.perf_counter()
    goblin.pause = False
    Ammo = amo - len(bullets2)
    goblin.jumpList = random.randrange(0, 75)

    point2 = points
    if goblin.visible:
        if man.hit_box[1] < goblin.hit_box[1] + goblin.hit_box[3] and man.hit_box[1] + man.hit_box[3] > \
                goblin.hit_box[1]:
            if man.hit_box[0] + man.hit_box[2] > goblin.hit_box[0] and man.hit_box[0] < goblin.hit_box[0] + \
                    goblin.hit_box[2]:
                man.hit()
                points -= 2
                lives -= 1

    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0

    pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if hits != 0:
                if Pausebutton.isOver(pos):
                    if (__DEBUG_MODE__):
                        print("paused")
                    pause = True
            if Mutebutton.isOver(pos):
                pygame.mixer.music.set_volume(0)
                Mutebutton = Unmutebutton
            if Unmutebutton.isOver(pos):
                pygame.mixer.music.set_volume(0.3)
                Mutebutton = button((0, 128, 255), 20, 40, 70, 30, 'Mute')
            if UnpauseButton.isOver(pos):
                if (__DEBUG_MODE__):
                    print('unpaused')
                pause = False
            if QuitButton.isOver(pos):
                run = False
            if MainQuitButton.isOver(pos):
                run = False
            if not pause:
                if GameQuitbutton.isOver(pos):
                    run = False

        if event.type == pygame.MOUSEMOTION:
            if Mutebutton.isOver(pos):
                Mutebutton.color = (255, 128, 0)
            else:
                Mutebutton.color = (0, 128, 255)

            if Unmutebutton.isOver(pos):
                Unmutebutton.color = (255, 128, 0)
            else:
                Unmutebutton.color = (255, 200, 0)

            if UnpauseButton.isOver(pos):
                UnpauseButton.color = (255, 128, 0)
            else:
                UnpauseButton.color = (0, 255, 0)

            if QuitButton.isOver(pos):
                QuitButton.color = (255, 128, 0)
            else:
                QuitButton.color = (255, 0, 0)

            if Pausebutton.isOver(pos):
                Pausebutton.color = (255, 128, 0)
            else:
                Pausebutton.color = (0, 200, 0)

            if MainQuitButton.isOver(pos):
                MainQuitButton.color = (255, 0, 0)
            else:
                MainQuitButton.color = (0, 0, 128)

            if GameQuitbutton.isOver(pos):
                GameQuitbutton.color = (255, 128, 0)
            else:
                GameQuitbutton.color = (255, 0, 0)


    for bullet in bullets:
        if goblin.visible:
            if bullet.y - bullet.radius < goblin.hit_box[1] + goblin.hit_box[3] and bullet.y + bullet.radius > \
                    goblin.hit_box[1]:
                if bullet.x + bullet.radius > goblin.hit_box[0] and bullet.x - bullet.radius < goblin.hit_box[0] + \
                        goblin.hit_box[2]:
                    goblin.hit()
                    hits -= 1
                    score += 1
                    points += 1
                    bullets.pop(bullets.index(bullet))

        if W > bullet.x > 0:
            bullet.x += bullet.vel

        else:
            bullets.pop(bullets.index(bullet))


    keys = pygame.key.get_pressed()


    if keys[pygame.K_SPACE] and shootLoop == 0:
        if hits != 0:
            if man.left:
                facing = -1
            else:
                  facing = 1

            if len(bullets2) < amo:
                bullets.append(projectile(round(man.x + man.width // 2), round(man.y + man.height // 2), 6, (0, 0, 0), facing))
                bullets2.append(projectile(round(man.x + man.width // 2), round(man.y + man.height // 2), 6, (0, 0, 0), facing))

        shootLoop = 1

    if keys[pygame.K_LEFT] and man.x > man.vel:
        if not pause:
            man.x -= man.vel
            man.left = True
            man.right = False
            man.standing = False
        else:
            pause = False
    elif keys[pygame.K_RIGHT] and man.x < W - man.width - man.vel:
        if not pause:
            man.x += man.vel
            man.right = True
            man.left = False
            man.standing = False
        else:
            pause = False
    else:
        man.standing = True
        man.walkCount = 0

    if hits != 0:
        if keys[pygame.K_DOWN]:
            if not pause:
                pause = True

    if not man.isJump:
        if keys[pygame.K_UP]:
            projectile.manIsJump = True
            if not pause:
                man.isJump = True
                man.right = False
                man.left = False
                man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            neg = 1.5
            if man.jumpCount < 0:
                neg = -1.5
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10



    if keys[pygame.K_f]:
        win = pygame.display.set_mode((W, H), pygame.FULLSCREEN)

    elif keys[pygame.K_ESCAPE]:
        win = pygame.display.set_mode((W, H), pygame.RESIZABLE)


    if goblin.jumpList == 15:
        goblin.isJump = True

    if hits == 0:
        if (__DEBUG_MODE__):
            print('inside goblin dead if!')
        goblin.dead = True
        man.isJump = True
        man.right = True
        man.left = False
        goblin.visible = False
        man.x = 190
        man.gameover = True

    if score > goblinHealth:
        score -= 1

    if hits < 0:
        hits += 1
        if points > point2:
            points -= 1

    if lives == 0:
        if keys[pygame.K_ESCAPE]:
            run = False
        isfade = True

    if hits != 0:
        if not pause:
            timeIs = str(timeUp - timer)
            timeIs = '{:.2f}'.format(timeUp)

    if pause:
        pauseMenu()
    elif start:
        start = MainMenu(start, begining)
    #if lives <= 0:
        #endScreen(first)
        #if (__DEBUG_MODE__):
            #print("In the Endscreen!")
    elif isfade:
        fade(W, H)
        isfade = False
    else:
        first = redrawGameWindow(first)
    pygame.display.update()


pygame.quit()
print('\nThank you for playing Goblin Invasion')
