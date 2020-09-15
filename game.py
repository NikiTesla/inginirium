from random import randint
import pygame
import sqlite3
import time


connect = sqlite3.connect('test.db')
cursor = connect.cursor()

list = []
count = 0

fox = pygame.image.load(r"C:\Users\krech\Desktop\krechetovn\dev\sqlite\fox.png")
dog = pygame.image.load(r"C:\Users\krech\Desktop\krechetovn\dev\sqlite\photo_2020-09-15_12-54-17.jpg")


class Hero():
    def __init__(self, x, y, color, rad):
        self.x, self.y = x, y
        self.rad = rad
        self.col = color
        self.image = pygame.Surface((self.rad*2, self.rad*2))
        pygame.draw.circle(self.image, self.col, (self.rad, self.rad), self.rad)
        self.rect = self.image.get_rect()
        self.image.set_colorkey((0, 0, 0))

    def draw(self, sc):
        sc.blit(self.image, self.rect)

    def move_by_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.y -= 3
        if keys[pygame.K_DOWN]:
            self.y += 3
        if keys[pygame.K_LEFT]:
            self.x -= 3
        if keys[pygame.K_RIGHT]:
            self.x += 3
        if keys[pygame.K_ESCAPE]:
            exit()
        self.rect[0] = self.x - self.rad
        self.rect[1] = self.y - self.rad

    def borders(self, W, H):
        if self.x > W:
            self.x = 0
        if self.y > H:
            self.y = 0
        if self.x < 0:
            self.x = W
        if self.y < 0:
            self.y = H


class Enemy(pygame.sprite.Sprite):
    def __init__(self, xr, yr, color, rad):
        self.xr, self.yr = xr, yr
        self.rad = rad
        self.col = color
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((self.rad*2, self.rad*2))
        self.image.set_colorkey((0, 0, 0))

        pygame.draw.circle(self.image, self.col, (self.rad, self.rad), self.rad)
        self.rect = self.image.get_rect()


    def draw(self, sc):
        sc.blit(self.image, self.rect)

    def move_to_hero(self, xr, yr, x, y):
        if self.xr > x:
            self.xr -= 2
        if self.xr <= x:
            self.xr += 2 
        if self.yr >= y:
            self.yr -= 2 
        if self.yr < y:
            self.yr += 2 
        self.rect[0] = self.xr - self.rad
        self.rect[1] = self.yr - self.rad
        
    

pygame.init()

all_sprites = pygame.sprite.Group()

W = 1000
H = 800

fps = pygame.time.Clock()
sc = pygame.display.set_mode((W, H))


hero1 = Hero(W//2, H//2, (180, 190, 50), 25)

list_of_enemies = []

t1 = time.time()
running = True

while running:
    if time.time() - t1 >= 1:
        print(time.time() - t1)
        t1 = time.time()
        xr = randint(0, W)
        xy = randint(0, H)
        list_of_enemies.append(Enemy(xr, xy, (100, 100, 100), 30))
        count += 1
    

    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            exit()

    sc.fill((200, 200, 200))

    hero1.move_by_keys()
    hero1.draw(sc)
    hero1.borders(W, H)

    seconds=(pygame.time.get_ticks())/1000
    
    for i in list_of_enemies:
        i.move_to_hero(i.xr, i.yr, hero1.x, hero1.y)
        i.draw(sc)
        if (hero1.x - 25 < i.xr < hero1.x + 25) and (hero1.y - 25 < i.yr < hero1.y + 25):
            print("Your score: " + str(count))
            running = False

            

    pygame.display.update()
    if not running:
        pygame.display.quit()
    fps.tick(120)

name = input()


# ворос: как добавить name и count в таблицу???
cursor.execute("INSERT INTO players VALUES(21, 1212)")
cursor.execute('''SELECT * FROM players''')
data_from_db = cursor.fetchall()

connect.commit()
connect.close()