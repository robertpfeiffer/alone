import pygame,math,random
from pygame.locals import *

pygame.init()
pygame.font.init()

XRES=400
YRES=240
SCALE=2
GRAVITY = 1

class Game(object):
    over = False
    win = False
    # Singleton God class.

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
    def __init__(self):
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

    def place(self,x,y):
        self.feet.rect.bottomleft=(x,y)
        self.rect.midbottom=self.feet.rect.midtop

    def hit(self,other):
        self.hitsound.play()
        Game.over=True

    def move(self,x,y):
        self.rect=self.rect.move(x,y)
        self.feet.rect.midtop=self.rect.midbottom

    def test_standing(self):
        for sprite in Game.ground:
            if pygame.sprite.collide_rect(self.feet,sprite) and pygame.sprite.collide_mask(self.feet,sprite):
                if sprite.rect.top + 5 >=  self.feet.rect.bottom: #standing on it
                    return True
        return False

    def hit_head(self):
        for sprite in Game.ground:
            if pygame.sprite.collide_rect(self,sprite) and pygame.sprite.collide_mask(self,sprite):
                if sprite.rect.bottom - 5 <=  self.rect.top:
                    return True
        return False

    def hit_side(self):
        coll=pygame.sprite.collide_circle_ratio(1.2)
        for sprite in pygame.sprite.spritecollide(self, Game.ground, False, coll):
            if (sprite.rect.left + 5 > self.rect.right):
                self.move(- 3, 0)
                return True
            elif (sprite.rect.right < self.rect.right - 5):
                self.move( 3, 0)
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
        hit_side=self.hit_side()
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_a]:
            self.direction=-1
            if not hit_side:
                self.move(-5, 0)
            self.image = self.img_left
            self.mask = self.mask_left

        if pressed[pygame.K_d]:
            self.direction=1
            if not hit_side:
                self.move(5, 0)
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
        if self.holder.direction == -1 :
            if self.angle > 5:
                self.rect.topright = self.holder.rect.center
            elif self.angle < .5:
                self.rect.bottomright = self.holder.rect.center
            else:
                self.rect.midright = self.holder.rect.center
        else:
            if self.angle > 5:
                self.rect.bottomleft = self.holder.rect.center
            elif self.angle < .5:
                self.rect.topleft = self.holder.rect.center
            else:
                self.rect.midleft = self.holder.rect.center

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
                Game.levels[Game.level]()

class Animal(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        my_class=type(self)
        path_lit=my_class.name+".png"
        path_dark=my_class.name+"-eyes.png"
        self.image_dark = pygame.image.load(path_dark)
        self.image_light= pygame.image.load(path_lit)
        self.mask = pygame.mask.from_surface(self.image_light, 30)
        self.lit = False
        self.image = self.image_dark
        self.rect = self.image.get_rect()
        self.rect.bottomleft=x,y
        self.origin = self.rect

    def is_hostile(self):
        return False

    def update(self):
        self.lit = pygame.sprite.collide_mask(Game.torch,self)
        if pygame.sprite.collide_mask(Game.player,self):
            self.lit = True
            if self.is_hostile():
                Game.player.hit(self)
        
        if self.lit:
            self.image = self.image_light
        else:
            self.image = self.image_dark

class Rabbit(Animal):
    name = "rabbit"

class Bat(Animal):
    name = "bat"
    flight_range=80
    def __init__(self,x,y):
        Animal.__init__(self,x,y)
        self.direction=(0,1)
        self.rect=self.rect.move((0,-Bat.flight_range/2))

    def is_hostile(self):
        return True
    
    def update(self):
        Animal.update(self)
        ox,oy=self.origin.x,self.origin.y
        x,y=self.rect.x,self.rect.y
        
        if self.lit:
            self.rect=self.rect.move(self.direction)
            if oy-y>Bat.flight_range or oy-y<0:
                self.direction = (-1*self.direction[0],-1*self.direction[1])
                self.rect=self.rect.move(self.direction)
                self.rect=self.rect.move(self.direction)

class Fox(Animal):
    name = "fox"
    def __init__(self,x,y):
        Animal.__init__(self,x,y)
        self.direction=(1,0)

    def is_hostile(self):
        return True
    
    def update(self):
        Animal.update(self)

        self.direction = (-3*Game.player.direction,0)
        if Game.player.direction == -1:
            self.image = pygame.transform.flip(self.image,True,False)
            self.mask = pygame.mask.from_surface(self.image_light, 30)

        if self.lit:
            self.rect=self.rect.move(self.direction)

mainloop, x,y, color, fontsize, delta, fps =  True, 25 , 0, (32,32,32), 35, 1, 30
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

    background.blit(moon,(random.randint(0,XRES),random.randint(0,YRES)))

    pygame.draw.ellipse(background, (9, 6, 3), (0, 120, 400, 240), 0)

    for i in range(5):
        x1=random.randint(0,XRES)
        y1=random.randint(YRES*4/10,YRES*6/10)
        pygame.draw.ellipse(background, (9+random.randint(0,3),
                                         6+random.randint(0,3),
                                         3+random.randint(0,3)), 
                            (x1, y1, x1+100, 240), 0)

    background.blit(tree3,(random.randint(0,XRES),random.randint(YRES*1/10,YRES*2/10)))
    background.blit(tree1,(random.randint(0,XRES),random.randint(YRES*1/10,YRES*2/10)))
    background.blit(tree2,(random.randint(0,XRES),random.randint(YRES*1/10,YRES*2/10)))

    return background

def level2():
    Game.player=Girl()
    Game.torch=Torch(Game.player)
    Game.player.place=(10,YRES-20)
    Game.ground=[]

    for i in range (1+400/30):
        Game.ground.append(Ground(30*i,YRES-5))
        
    Game.ground.append(Ground(250,180))

    Game.background = make_background()
    Game.sprites = pygame.sprite.OrderedUpdates(Game.ground+
                                                [Game.player,Game.player.feet,Game.torch]+
                                                [Bat(80,YRES),Bat(150,YRES),Fox(250,YRES)]+
                                                [Portal(350,YRES)])

def level3():
    Game.player=Girl()
    Game.torch=Torch(Game.player)
    Game.player.place(10, 200)
    Game.ground=[]

    Game.ground.append(Ground(10,200))
    Game.ground.append(Ground(20,198))
    Game.ground.append(Ground(30,195))
    Game.ground.append(Ground(40,193))
    Game.ground.append(Ground(50,191))
    Game.ground.append(Ground(90,188))

    Game.background = make_background()
    Game.sprites = pygame.sprite.OrderedUpdates(Game.ground+
                                                [Game.player,Game.player.feet,Game.torch]+
                                                [Portal(90,150)])

def tutorial1():
    Game.player=Girl()
    Game.torch=Torch(Game.player)
    Game.player.place(10, 200)
    Game.ground=[]
    for i in range(15):
        Game.ground.append(Ground(10*i,200-3*i))
    for i in range(40):
        Game.ground.append(Ground(-15,200-3*i))
    Game.background = make_background()

    font=pygame.font.Font("Ostrich Black.ttf",20)
    ren = font.render("use WASD keys to walk home" ,1,(200,200,200))
    Game.background.blit(ren, (20,20))

    Game.sprites = pygame.sprite.OrderedUpdates(Game.ground+
                                                [Game.player,Game.player.feet,Game.torch]+
                                                [Portal(150,150)])

def tutorial2():
    Game.player=Girl()
    Game.torch=Torch(Game.player)
    Game.player.place(10, 200)
    Game.ground=[]

    Game.ground.append(Ground(10,200))
    Game.ground.append(Ground(40,200))
    Game.ground.append(Ground(10,120))
    Game.ground.append(Ground(120,200))
    Game.ground.append(Ground(150,200))
    Game.ground.append(Ground(180,200))
    Game.ground.append(Ground(210,150))
    Game.ground.append(Ground(240,150))
    Game.ground.append(Ground(270,150))

    Game.background = make_background()

    font=pygame.font.Font("Ostrich Black.ttf",24)
    ren = font.render("point and click to illuminate your path" ,1,(200,200,200))
    Game.background.blit(ren, (20,20))

    Game.sprites = pygame.sprite.OrderedUpdates(Game.ground+
                                                [Game.player,Game.player.feet,Game.torch]+
                                                [Portal(270,150)])

def tutorial3():
    Game.player=Girl()
    Game.torch=Torch(Game.player)
    Game.player.place=(10,YRES-20)
    Game.ground=[]

    for i in range (1+400/30):
        Game.ground.append(Ground(30*i,YRES-5))

    Game.background = make_background()

    font=pygame.font.Font("Ostrich Black.ttf",24)
    #ren = font.render("point and click to illuminate your path" ,1,(200,200,200))
    ren = font.render("stay clear of the Monsters" ,1,(200,200,200))
    Game.background.blit(ren, (20,20))

    Game.sprites = pygame.sprite.OrderedUpdates(Game.ground+
                                                [Game.player,Game.player.feet,Game.torch]+
                                                [Bat(150,150)]+
                                                [Portal(350,YRES)])

def tutorial4():
    Game.player=Girl()
    Game.torch=Torch(Game.player)
    Game.player.place=(10,YRES-20)
    Game.ground=[]

    for i in range (1+400/30):
        Game.ground.append(Ground(30*i,YRES-5))

    Game.background = make_background()

    font=pygame.font.Font("Ostrich Black.ttf",24)
    #ren = font.render("point and click to illuminate your path" ,1,(200,200,200))
    ren = font.render("Rabbits are harmless" ,1,(200,200,200))
    Game.background.blit(ren, (20,20))

    Game.sprites = pygame.sprite.OrderedUpdates(Game.ground+
                                                [Game.player,Game.player.feet,Game.torch]+
                                                [Rabbit(150,235)]+
                                                [Portal(350,YRES)])


Game.levels=[tutorial1,tutorial2,tutorial3,tutorial4,level3,level2]

def startgame():
    Game.level=0
    Game.levels[0]()

startgame()

while mainloop:
    tick_time = clock.tick(fps) # milliseconds since last frame
    pygame.display.set_caption("press Esc to quit. FPS: %.2f" % (clock.get_fps()))

    surface = Game.background.copy()

    Game.sprites.update()
    Game.sprites.draw(surface);
    pygame.transform.scale(Game.background, [XRES*SCALE,YRES*SCALE], screen)
    pygame.transform.scale(surface, [XRES*SCALE,YRES*SCALE], screen)
    
    if Game.over or Game.win:
        font=pygame.font.Font("Ostrich Black.ttf",100)
        ren = font.render("THE END" if Game.win else "GAME OVER",1,(50,50,255))
        screen.blit(ren, (20,20))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainloop = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                mainloop = False
    pygame.display.update()
