#Создай собственный Шутер!

from pygame import *
from random import randint
# import time

score = 0 #сбито кораблей
lost = 0 #пропущено кораблей

font.init()
font1 = font.SysFont('Arial', 36)
font2 = font.SysFont('Arial', 70)


winner = font2.render('YOU WIN!', True, (255, 215, 0))
loser = font2.render('YOU LOSE!', True, (180, 0, 0))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, x, y, size_x, size_y, speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def draw_sprite(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 615:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx-7, self.rect.top, 15, 20, 15)
        BULL.add(bullet)
   
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.x = randint(80, 700 - 80)
            self.rect.y = 0
            lost = lost + 1
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 15, 20, 15)
        BULL.add(bullet)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        #исчезает, если дойдет до края экрана
        if self.rect.y < 0:
            self.kill()



win = display.set_mode((700, 500))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'), (700, 500))
rocket = Player('rocket.png', 320, 370, 80, 120, 4)

UFO = sprite.Group()
for i in range(5):
    ufo = Enemy('ufo.png', randint(80,700-80), -100, 80, 50, randint(1, 5))
    UFO.add(ufo)

BULL = sprite.Group()


mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

fire_sound = mixer.Sound('fire.ogg')

clock = time.Clock()
FPS = 60

finish = False
game = True
while game:
    for i in event.get():
        if i.type == QUIT:
            game = False
        elif i.type == KEYDOWN:
            if i.key == K_SPACE:
                fire_sound.play()
                rocket.fire()
    if not finish:
        win.blit(background, (0,0))    

        rocket.update()  
        UFO.update()
        BULL.update()

        rocket.draw_sprite()
        UFO.draw(win)
        BULL.draw(win)

        text_score = font1.render("Счет: " + str(score), 1, (255, 255, 255))
        win.blit(text_score, (10, 20))
        text_lost = font1.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        win.blit(text_lost, (10, 50))

        


        collides = sprite.groupcollide(UFO, BULL, True, True) # возвращает список ufo, которых коснулась пуля
        for c in collides:
            score = score + 1
            ufo = Enemy('ufo.png', randint(80,700-80), -100, 80, 50, randint(1, 5))
            UFO.add(ufo)    
        
        # условие проигрыша
        if sprite.spritecollide(rocket, UFO, False) or lost >= 3:# возвращает список ufo, столкнувшихся с ракетой
            win.blit(loser, (200, 200))
            finish = True

        # условие выигрыша
        if score >= 10:
            win.blit(winner, (200, 200))
            finish = True

        display.update()
        clock.tick(FPS)















'''
#создай игру "Лабиринт"!
from pygame import *

class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.wall_width = wall_width
        self.wall_height = wall_height
        self.image = Surface((self.wall_width, self.wall_height))
        self.image.fill((color_1, color_2, color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
   
    def draw_wall(self):
        win.blit(self.image, (self.rect.x, self.rect.y))
        #draw.rect(window, (self.color_1, self.color_2, self.color_3), (self.rect.x, self.rect.y, self.width, self.height))


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, x, y, speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (55, 55))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def draw_sprite(self):
        win.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 700 - 80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < 500 - 80:
            self.rect.y += self.speed



class Enemy(GameSprite):
    def update(self):
        if self.rect.x <= 470:
            self.side = "right"
        if self.rect.x >= 700 - 85:
            self.side = "left"
        if self.side == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed


    


win = display.set_mode((700, 500))
display.set_caption('Лабиринт')
background = transform.scale(image.load('background.jpg'), (700, 500))

hero = Player('hero.png', 5, 420, 4)
cyborg = Enemy('cyborg.png', 620, 280, 2)
treasure = GameSprite('treasure.png', 580, 420, 0)


w1 = Wall(222, 107, 242, 100, 20 , 450, 10)
w2 = Wall(222, 107, 242, 100, 480, 350, 10)
w3 = Wall(222, 107, 242, 100, 20 , 10, 380)


mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()

clock = time.Clock()
FPS = 60

font.init()
font = font.Font(None, 70)
winner = font.render('YOU WIN!', True, (255, 215, 0))
loser = font.render('YOU LOSE!', True, (180, 0, 0))

money = mixer.Sound('money.ogg')
kick = mixer.Sound('kick.ogg')


finish = False
game = True
while game:
    if finish != True:

        win.blit(background, (0,0))
        hero.update()
        cyborg.update()

        hero.draw_sprite()
        cyborg.draw_sprite()
        treasure.draw_sprite()

        w1.draw_wall()
        w2.draw_wall()
        w3.draw_wall()

        #Ситуация "Проигрыш"
        if sprite.collide_rect(hero, cyborg) or sprite.collide_rect(hero, w1) or sprite.collide_rect(hero, w2) or sprite.collide_rect(hero, w3):
            finish = True
            win.blit(loser, (200, 200))
            kick.play()


        #Ситуация "Выигрыш"
        if sprite.collide_rect(hero, treasure):
            finish = True
            win.blit(winner, (200, 200))
            money.play()


    for i in event.get():
        if i.type == QUIT:
            game = False

    display.update()
    clock.tick(FPS)

'''