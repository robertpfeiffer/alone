import pygame,math,random
from pygame.locals import *
from config import *

import game
Game=game.Game
import animals
import levels

pygame.init()
pygame.font.init()

class Feet(pygame.sprite.Sprite):

    """The Feet have their own hitbox, so we can test if we can stand or climb on anything."""
    def __init__(self,girl):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.image = pygame.image.load("girl-feet.png")
        self.img_right = self.image
        self.img_left = pygame.transform.flip(self.image,True,False)
        self.girl=girl
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image, 30)
        self.mask_right = self.mask
        self.mask_left = pygame.mask.from_surface(self.img_left, 30)

    def update(self):
        if self.girl.direction==-1:
            self.image = self.img_left
            self.mask = self.mask_left

        else:
            self.image = self.img_right
            self.mask = self.mask_right

class Girl(pygame.sprite.Sprite):
    def __init__(self,lives=LIVES):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        girl_png = pygame.image.load("girl-body.png")
        self.image = girl_png# pygame.transform.scale2x(girl_png)
        self.img_right = self.image
        self.img_left = pygame.transform.flip(self.image,True,False)
        self.mask = pygame.mask.from_surface(self.image, 30)
        self.mask_right = self.mask
        self.mask_left = pygame.mask.from_surface(self.img_left, 30)
        self.rect = self.image.get_rect()
        self.direction = 1
        self.hitsound = pygame.mixer.Sound("Explosion2.wav")
        self.vert_speed = 0
        self.standing= False
        self.feet=Feet(self)
        self.lives=lives
        self.hurt_time=30

    def place(self,x,y):
        self.feet.rect.bottomleft=(x,y)
        self.rect.midbottom=self.feet.rect.midtop

    def hit(self,other):
        if self.hurt_time < 1:
            self.hitsound.play()
            self.lives -=1
            self.hurt_time = 30

        if self.lives == 0:
            Game.over=True

    def move(self,x,y):
        self.rect=self.rect.move(x,y)
        self.feet.rect.midtop=self.rect.midbottom

    def test_standing(self):
        for sprite in Game.ground:
            if (pygame.sprite.collide_rect(self.feet,sprite) 
                and pygame.sprite.collide_mask(self.feet,sprite)):
                if sprite.rect.top + 5 >=  self.feet.rect.bottom: #standing on it
                    return True
        return False

    def hit_head(self):
        for sprite in Game.ground:
            if (pygame.sprite.collide_rect(self,sprite)
                and pygame.sprite.collide_mask(self,sprite)):
                if sprite.rect.bottom - 5 <=  self.rect.top:
                    return True
        return False

    def hit_side(self):
        coll=pygame.sprite.collide_rect_ratio(1.1)
        for sprite in pygame.sprite.spritecollide(self, Game.ground, False, coll):
            x1,y1=self.rect.center
            x2,y2=sprite.rect.center
            xd = 0
            if x1 < x2:
                xd = -3
            if x1 >= x2:
                xd = 3
            if y1 < y2:
                yd = -3
            if y1 >= y2:
                yd = 3
            self.move(xd, yd)

            return True
        return False

    def climb(self):
        for sprite in Game.ground:
            if pygame.sprite.collide_rect(self.feet,sprite) and pygame.sprite.collide_mask(self.feet,sprite):
                while sprite.rect.top < self.feet.rect.bottom:
                    self.move(0,-1)

    def fall(self):
        self.standing=False

        for i in range(abs(self.vert_speed)):
            if self.test_standing():
                self.standing=True
                break
            if self.vert_speed>0 and self.hit_head():
                self.vert_speed=-1
            self.move(0, -1 if self.vert_speed > 0 else 1)

        if not self.standing:
            self.vert_speed -= GRAVITY
        else:
            self.climb()

        if self.rect.midtop[1] > YRES:
            Game.over = True

    def update(self):
        if Game.win:
            return
        if self.hurt_time > 0:
            self.hurt_time -= 1

        hit_side=self.hit_side()
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_a]:
            if self.direction == 1:
                self.direction=-1
            else:
                for i in range(5):
                    if not hit_side:
                        self.move(-1, 0)
                    else:
                        break
            self.image = self.img_left
            self.mask = self.mask_left

        if pressed[pygame.K_d]:
            if self.direction == -1:
                self.direction=1
            else:
                for i in range(5):
                    if not hit_side:
                        self.move(1, 0)
                    else:
                        break
            self.image = self.img_right
            self.mask = self.mask_right

        self.hit_side()
        if pressed[pygame.K_w]:
            if self.standing:
                self.move(0, -3)
                self.vert_speed = 12
        self.fall()

class Torch(pygame.sprite.Sprite):
    def __init__(self,holder):
        self.holder = holder

        pygame.sprite.Sprite.__init__(self) #call Sprite intializer

        self.lit_image = pygame.image.load("light.png")
        self.unlit_image = pygame.image.load("torch-off.png")

        self.image = self.unlit_image
        self.mask = pygame.mask.from_surface(self.image, 30)
        self.rect = self.image.get_rect()
        self.rect.midleft = self.holder.rect.center
        self.angle = 0

    def update(self):
        self.lit=bool(pygame.mouse.get_pressed()[0])

        mx,my=pygame.mouse.get_pos()
        mx=mx/SCALE
        my=my/SCALE
        gx,gy=self.holder.rect.centerx,self.holder.rect.centery
        self.angle=-180.0*math.atan(float(my-gy)/float(mx-gx))/math.pi if mx-gx else 90
        if (mx-gx)*self.holder.direction < 0:
            self.angle *= -1

        if self.lit:
            self.image = self.lit_image
        else:
            self.image = self.unlit_image

        if self.holder.direction == -1 :
            self.image = pygame.transform.flip(self.image,True,False)

        self.image = pygame.transform.rotate(self.image,self.angle)
        self.mask = pygame.mask.from_surface(self.image, 30)
        self.rect = self.image.get_rect()
        if self.lit:
            if self.holder.direction == -1 :
                if self.angle > 1:
                    self.rect.topright = self.holder.rect.midtop
                elif self.angle < -1:
                    self.rect.bottomright = self.holder.rect.midbottom
                else:
                    self.rect.midright = self.holder.rect.center
            else:
                if self.angle > 1:
                    self.rect.bottomleft = self.holder.rect.midbottom
                elif self.angle < -1:
                    self.rect.topleft = self.holder.rect.midtop
                else:
                    self.rect.midleft = self.holder.rect.center
        else:
            if self.holder.direction == -1 :
                self.rect.center=self.holder.rect.midleft
            else:
                self.rect.center=self.holder.rect.midright

class Ground(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.image_dark = pygame.image.load("stone-dark.png")
        self.image_light =  pygame.image.load("stone.png")
        self.image = self.image_dark
        self.rect = self.image.get_rect()
        self.mask = pygame.Mask(self.rect.size)
        self.mask.fill()
        self.lit = False
        self.rect.center=x,y

    def update(self):
        self.lit = pygame.sprite.collide_mask(Game.torch,self)
        if self.lit:
            self.image = self.image_light
        else:
            self.image = self.image_dark

class Wall(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.image_dark = pygame.transform.rotate(
            pygame.image.load("stone-dark.png"),90)
        self.image_light = pygame.transform.rotate(
            pygame.image.load("stone.png"),90)
        self.image = self.image_dark
        self.rect = self.image.get_rect()
        self.mask = pygame.Mask(self.rect.size)
        self.mask.fill()
        self.lit = False
        self.rect.topleft=x,y

    def update(self):
        self.lit = pygame.sprite.collide_mask(Game.torch,self)
        if self.lit:
            self.image = self.image_light
        else:
            self.image = self.image_dark


class Portal(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.image = pygame.image.load("portal.png")
        self.mask = pygame.mask.from_surface(self.image, 30)
        self.rect = self.image.get_rect()
        self.rect.bottomleft=x,y

    def update(self):
        if pygame.sprite.collide_mask(Game.player,self):
            Game.level+=1
            if Game.level>=len(Game.levels):
                Game.win=True
            else:
                lives = Game.player.lives
                Game.levels[Game.level]()
                Game.player.lives= lives


mainloop = True
clock = pygame.time.Clock() # create clock object

screen = pygame.display.set_mode([XRES*SCALE,YRES*SCALE],pygame.DOUBLEBUF)
screen.fill([0,0,0])
pygame.key.set_repeat(1, 1)

def make_background():
    star=pygame.image.load("star.png")
    moon=pygame.image.load("moon3.png")
    tree2=pygame.image.load("tree2.png")
    tree3=pygame.image.load("tree3.png")

    tree1=pygame.transform.scale(tree2, (2*tree2.get_rect().size[0],2*tree2.get_rect().size[1]))
    tree2=pygame.transform.scale(tree3, (3*tree3.get_rect().size[0],3*tree3.get_rect().size[1]))

    background = pygame.Surface((XRES,YRES))
    background.fill((0,0,15))
    for i in range(20):
        background.blit(star,(random.randint(0,XRES),random.randint(0,YRES)))

    background.blit(moon,(random.randint(0,XRES),random.randint(0,YRES/3)))

    pygame.draw.ellipse(background, (9, 6, 3), (0, 120, 400, 240), 0)

    for i in range(5):
        x1=random.randint(0,XRES)
        y1=random.randint(YRES*4/10,YRES*6/10)
        pygame.draw.ellipse(background, (9+random.randint(0,3),
                                         6+random.randint(0,3),
                                         3+random.randint(0,3)),
                            (x1, y1, x1+100, 240), 0)

    background.blit(tree1,(random.randint(0,XRES),random.randint(YRES*1/10,YRES*2/10)))
    background.blit(tree1,(random.randint(0,XRES),random.randint(YRES*1/10,YRES*2/10)))
    background.blit(tree2,(random.randint(0,XRES),random.randint(YRES*1/10,YRES*2/10)))

    return background

Game.levels=levels.levels

def startgame():
    Game.level=0
    Game.levels[0]()

startgame()

heart=pygame.transform.scale(pygame.image.load("heart.png"),(30,30))

game_over_time=180

while mainloop:
    tick_time = clock.tick(FPS) # milliseconds since last frame
    pygame.display.set_caption("press Esc to quit. FPS: %.2f" % (clock.get_fps()))

    surface = Game.background.copy()

    Game.sprites.update()
    Game.sprites.draw(surface);
    pygame.transform.scale(Game.background, [XRES*SCALE,YRES*SCALE], screen)
    pygame.transform.scale(surface, [XRES*SCALE,YRES*SCALE], screen)

    for i in range(Game.player.lives):
        screen.blit(heart,[20 + 35*i,YRES*SCALE - 50 ])

    if Game.over or Game.win:
        font=pygame.font.Font("Ostrich Black.ttf",100)
        ren = font.render("THE END" if Game.win else "GAME OVER",1,(50,50,255))
        screen.blit(ren, (20,20))
        game_over_time -= 1
        if game_over_time < 0:
            mainloop=False

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainloop = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                mainloop = False
    pygame.display.update()
