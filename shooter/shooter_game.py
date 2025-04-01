from pygame import *
from random import *

mixer.init()
mixer.music.load('space.ogg')
clock = time.Clock()
fps = 60
width = 700
height = 500
game = True
background = transform.scale(image.load('galaxy.jpg'),(width,height))
window = display.set_mode((width, height)) 
display.set_caption('Shooter')

class GameSprite(sprite.Sprite):
    def __init__(self,x,y,wight,height,path):
        self.image = transform.scale(image.load(path),(wight,height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        super().__init__()
    def draw(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= 10  
        if self.rect.y < 0:
            self.kill()  
class Player(GameSprite):
    def update(self):
        reloading = 0
        if self.wait > 0:
            self.wait -= 1
            
        shift = 0
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LSHIFT]:
            shift = 2.5
        if keys_pressed[K_s]:
            self.rect.y += 2+shift
        if keys_pressed[K_w]:
            self.rect.y -= 2+shift
        if keys_pressed[K_a]:
            self.rect.x -= 2+shift
        if keys_pressed[K_d]:
            self.rect.x += 2+shift
        if keys_pressed[K_SPACE] and self.wait <= 0:
            self.shoot()
            self.wait = 15
            reloading += 1
            if reloading == 5:
                self.wait = 180
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top, 10,10, 'bullet.png')
        bullets.add(bullet)
    
class Enemy(GameSprite):
    def update(self):
        self.rect.y += 1
        if self.rect.y > height:
            self.rect.y = -self.rect.height  


rocket = Player(250,100,90,110,'rocket.png')
rocket.wait = 0
bullets = sprite.Group()
enemies = sprite.Group()

for i in range(5):
    randomm = randint(40,70)
    enemy = Enemy(randint(0, width - 50), randint(-100, -40),randomm , randomm, 'asteroid.png')
    enemies.add(enemy)
for i in range(2):
    ufo = Enemy(randint(0, width - 50), randint(-100, -40), 70, 70, 'ufo.png')
    enemies.add(ufo)
    

while game:
    window.blit(background,(0,0))

    rocket.draw()
    rocket.update()
    
    bullets.update()  
    bullets.draw(window)  

    enemies.update()  
    enemies.draw(window) 
    
    for e in event.get():
        if e.type == QUIT:
            game = False
    sprite_list = sprite.groupcollide(
        enemies,bullets, False,True
    )

        
    for i in sprite_list:
        i.rect.x = randint(0,650)
        i.rect.y = randint(-100,-50)
    
    clock.tick(fps)
    display.update()