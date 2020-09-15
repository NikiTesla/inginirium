from random import randint
import pygame
import sqlite3
import time
import os


fox_rad = 130 // 2
dog_rad = 100 // 2

dog_path = os.path.dirname(__file__) + '/dog.jpg'
fox_path = os.path.dirname(__file__) + '/fox.png'
bg_path = os.path.dirname(__file__) + '/bg.jpg'
bg = pygame.image.load(bg_path)
dog = pygame.image.load(dog_path)
fox = pygame.image.load(fox_path)
fox = pygame.transform.scale(fox, (fox_rad * 2, fox_rad * 2))
dog = pygame.transform.scale(dog, (dog_rad * 2, dog_rad * 2))



class Hero():
    def __init__(self, x, y, rad = fox_rad):
        self.x, self.y = x, y
        self.rad = rad
        self.rect = fox.get_rect()
        fox.set_colorkey((0, 0, 0))

    def draw(self, sc):
        sc.blit(fox, self.rect)

    def move_by_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.y -= 4
        if keys[pygame.K_DOWN]:
            self.y += 4
        if keys[pygame.K_LEFT]:
            self.x -= 4
        if keys[pygame.K_RIGHT]:
            self.x += 4
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


class Enemy():
    def __init__(self, xr, yr, rad = dog_rad):
        self.xr, self.yr = xr, yr
        self.rad = rad
        dog.set_colorkey((255, 255, 255))
        self.rect = dog.get_rect()


    def draw(self, sc):
        sc.blit(dog, self.rect)

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

W = 1000
H = 800

fps = pygame.time.Clock()
sc = pygame.display.set_mode((W, H))
bg = pygame.transform.scale(bg, (W, H))

hero1 = Hero(W//2, H//2, 25)
list_of_enemies = []
t1 = time.time()
running = True
count = 0

while running:
    if time.time() - t1 >= 1:
        print(time.time() - t1)
        t1 = time.time()
        xr = randint(0, W)
        xy = randint(0, H)
        list_of_enemies.append(Enemy(xr, xy, 30))
        count += 1

    sc.blit(bg, (0, 0))

    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            exit()

    hero1.move_by_keys()
    hero1.draw(sc)
    hero1.borders(W, H)

    seconds=(pygame.time.get_ticks())/1000
    
    for i in list_of_enemies:
        i.move_to_hero(i.xr, i.yr, hero1.x, hero1.y)
        i.draw(sc)
        if (hero1.x - 50 < i.xr < hero1.x + 50) and (hero1.y - 50 < i.yr < hero1.y + 50):
            print("Your score: " + str(count))
            running = False

    pygame.display.update()
    if not running:
        pygame.display.quit()
    fps.tick(120)


name = input()

connect = sqlite3.connect('test.db')
cursor = connect.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS players(num INT, name TEXT)")
cursor.execute(f"INSERT INTO players VALUES({count}, '{name}')")
cursor.execute('SELECT * FROM players')
data_from_db = cursor.fetchall()

m_data = max(data_from_db, key=lambda x: x[0])
print("ТОП-1 ИГРОК: " + m_data[1] + " со счетом " + str(m_data[0]))

connect.commit()
connect.close()
