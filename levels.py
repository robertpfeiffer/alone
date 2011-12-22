import pygame
from config import *

import game
Game=game.Game
import animals 
import __main__ as main


def level1():
    Game.player=main.Girl()
    Game.torch=main.Torch(Game.player)
    Game.player.place=(20,180)
    Game.ground=[]

    Game.ground.append(main.Ground(10,200))
    Game.ground.append(main.Ground(20,198))
    Game.ground.append(main.Ground(30,195))
    Game.ground.append(main.Ground(40,193))
    Game.ground.append(main.Ground(50,191))
    Game.ground.append(main.Ground(90,188))

    Game.background = main.make_background()
    Game.sprites = pygame.sprite.OrderedUpdates(Game.ground+
                                                [Game.player,Game.player.feet,Game.torch]+
                                                [main.Portal(90,150)])

def level2():
    Game.player=main.Girl()
    Game.torch=main.Torch(Game.player)
    Game.player.place=(20,180)
    Game.ground=[]

    for i in range (1+400/30):
        Game.ground.append(main.Ground(30*i,YRES-5))
        
    Game.ground.append(main.Ground(250,180))

    Game.background = main.make_background()
    sprites= (Game.ground+
              [Game.player,Game.player.feet,Game.torch]+
              [animals.Bat(80,YRES),
               animals.Bat(150,YRES),animals.Fox(250,YRES)]+
              [main.Portal(350,YRES)])

    Game.sprites = pygame.sprite.OrderedUpdates(sprites)

def level3():
    Game.player=main.Girl()
    Game.torch=main.Torch(Game.player)
    Game.player.place=(20,180)
    Game.ground=[]
    
    for i in range (1+(XRES/2)/30):
        Game.ground.append(main.Ground(30*i,YRES-5))

    for i in range (2+(YRES/2)/30):
        Game.ground.append(main.Wall(XRES/2,YRES-30*i))
    
    Game.ground.append(main.Ground(50,YRES/2))
    
    Game.ground.append(main.Ground(150,3*YRES/4))

    Game.ground.append(main.Ground(XRES/2-30,YRES/2-30))
    Game.ground.append(main.Ground(XRES/2+90,YRES/2-30))

    Game.ground.append(main.Ground(XRES/2+60,YRES/2+60))


    Game.background = main.make_background()
    sprites= (Game.ground+
              [Game.player,Game.player.feet,Game.torch]+
              [main.Portal(XRES/2+60,YRES/2+60)])

    Game.sprites = pygame.sprite.OrderedUpdates(sprites)

def level4():
    Game.player=main.Girl()
    Game.torch=main.Torch(Game.player)
    Game.player.place=(20,180)
    Game.ground=[]

    mobs=[]
    
    Game.ground.append(main.Ground(5,200))
    Game.ground.append(main.Ground(25,200))
    Game.ground.append(main.Ground(45,200))

    mobs.append(animals.Bat(80,220))
        
    Game.ground.append(main.Ground(130,200))
    mobs.append(animals.Rabbit(130,200))

    mobs.append(animals.Bat(180,220))

    Game.ground.append(main.Ground(250,200))
    mobs.append(animals.Rabbit(250,200))

    Game.ground.append(main.Ground(300,200))

    Game.background = main.make_background()
    sprites= (Game.ground+mobs+
              [Game.player,Game.player.feet,Game.torch]+
              [main.Portal(300,200)])

    Game.sprites = pygame.sprite.OrderedUpdates(sprites)

def level5():
    Game.player=main.Girl()
    Game.torch=main.Torch(Game.player)
    Game.player.place=(20,180)
    Game.ground=[]

    for i in range (1+400/30):
        Game.ground.append(main.Ground(30*i,YRES-5))
        
    Game.ground.append(main.Ground(200,150))
    Game.ground.append(main.Ground(100,180))
    Game.ground.append(main.Ground(300,140))

    Game.background = main.make_background()
    sprites= (Game.ground+
              [Game.player,Game.player.feet,Game.torch]+
              [animals.Wolf (160,YRES),animals.Snake(220,YRES)]+
              [main.Portal(350,YRES)])

    Game.sprites = pygame.sprite.OrderedUpdates(sprites)


def level6():
    Game.player=main.Girl()
    Game.torch=main.Torch(Game.player)
    Game.player.place=(20,180)
    Game.ground=[]

    Game.ground.append(main.Ground(10,200))
    Game.ground.append(main.Ground(40,200))

        
    Game.ground.append(main.Ground(200,200))
    Game.ground.append(main.Ground(100,200))
    Game.ground.append(main.Ground(300,200))
    Game.ground.append(main.Ground(330,200))
    Game.ground.append(main.Ground(360,200))
    Game.ground.append(main.Ground(390,200))

    Game.background = main.make_background()
    Game.background.blit(pygame.image.load("assets/sprites/home.png"), (310,120))
    
    sprites= (Game.ground+
              [Game.player,Game.player.feet,Game.torch]+
              [main.Portal(300,200)])

    Game.sprites = pygame.sprite.OrderedUpdates(sprites)

def tutorial1():
    Game.player=main.Girl() # HEAL
    Game.torch=main.Torch(Game.player)
    Game.player.place=(20,180)
    Game.ground=[]
    for i in range(15):
        Game.ground.append(main.Ground(10*i,200-3*i))
    for i in range(40):
        Game.ground.append(main.Ground(-15,200-3*i))
    Game.background = main.make_background()

    font=pygame.font.Font("assets/ui/Ostrich Black.ttf",20)
    ren = font.render("use WASD keys to walk home" ,1,(200,200,200))
    Game.background.blit(ren, (20,20))

    Game.sprites = pygame.sprite.OrderedUpdates(Game.ground+
                                                [Game.player,Game.player.feet,Game.torch]+
                                                [main.Portal(150,150)])

def tutorial2():
    Game.player=main.Girl( )
    Game.torch=main.Torch(Game.player)
    Game.player.place=(20,180)
    Game.ground=[]

    Game.ground.append(main.Ground(10,200))
    Game.ground.append(main.Ground(40,200))
    Game.ground.append(main.Ground(10,120))
    Game.ground.append(main.Ground(120,200))
    Game.ground.append(main.Ground(150,200))
    Game.ground.append(main.Ground(180,200))
    Game.ground.append(main.Ground(210,150))
    Game.ground.append(main.Ground(240,150))
    Game.ground.append(main.Ground(270,150))

    Game.background = main.make_background()

    font=pygame.font.Font("assets/ui/Ostrich Black.ttf",24)
    ren = font.render("point and click to illuminate your path" ,1,(200,200,200))
    Game.background.blit(ren, (20,20))

    Game.sprites = pygame.sprite.OrderedUpdates(Game.ground+
                                                [Game.player,Game.player.feet,Game.torch]+
                                                [main.Portal(270,150)])

def tutorial3():
    Game.player=main.Girl()
    Game.torch=main.Torch(Game.player)
    Game.player.place=(20,180)
    Game.ground=[]

    for i in range (1+400/30):
        Game.ground.append(main.Ground(30*i,YRES-5))

    Game.background = main.make_background()

    font=pygame.font.Font("assets/ui/Ostrich Black.ttf",24)
    ren = font.render("stay clear of the Monsters" ,1,(200,200,200))
    Game.background.blit(ren, (20,20))

    Game.sprites = pygame.sprite.OrderedUpdates(Game.ground+
                                                [Game.player,Game.player.feet,Game.torch]+
                                                [animals.Bat(150,150)]+
                                                [main.Portal(350,YRES)])

def tutorial4():
    Game.player=main.Girl()
    Game.torch=main.Torch(Game.player)
    Game.player.place=(20,180)
    Game.ground=[]

    for i in range (1+400/30):
        Game.ground.append(main.Ground(30*i,YRES-5))

    Game.background = main.make_background()

    font=pygame.font.Font("assets/ui/Ostrich Black.ttf",24)
    ren = font.render("Rabbits are harmless" ,1,(200,200,200))
    Game.background.blit(ren, (20,20))

    Game.sprites = pygame.sprite.OrderedUpdates(Game.ground+
                                                [Game.player,Game.player.feet,Game.torch]+
                                                [animals.Rabbit(150,235)]+
                                                [main.Portal(350,YRES)])

levels=[tutorial1,tutorial2,tutorial3,tutorial4,level1,level2,level3,level4,level5,level6]

