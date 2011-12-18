import pygame
import game
Game=game.Game

class Animal(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        my_class=type(self)
        path_lit=my_class.name+".png"
        path_dark=my_class.name+"-eyes.png"
        self.image_dark = pygame.image.load(path_dark)
        self.image_light= pygame.image.load(path_lit)
        self.mask_light = pygame.mask.from_surface(self.image_light, 30)
        self.mask_dark = pygame.mask.from_surface(self.image_dark, 30)
        self.mask = self.mask_dark
        self.lit = False
        self.image = self.image_dark
        self.rect = self.image.get_rect()
        self.rect.midbottom=x,y
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
            self.mask = self.mask_light
        else:
            self.image = self.image_dark
            self.mask = self.mask_dark

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

class Wolf(Animal):
    name = "wolf"
    def __init__(self,x,y):
        Animal.__init__(self,x,y)
        self.direction=(1,0)

    def is_hostile(self):
        return True

    def update(self):
        Animal.update(self)

        self.direction = (-5*Game.player.direction,0)
        if Game.player.direction == -1:
            self.image = pygame.transform.flip(self.image,True,False)
            self.mask = pygame.mask.from_surface(self.image_light, 30)

        if self.lit:
            self.rect=self.rect.move(self.direction)

class Snake(Animal):
    name = "snake"

    def is_hostile(self):
        return True
