import pygame,sys
from settings import *
from player import Player
from car import Car
from random import choice,randint
from sprite import SimpleSprite, LongSprite

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = pygame.math.Vector2()
        self.bg = pygame.image.load('graphics/main/map.png').convert()
        self.fg = pygame.image.load('graphics/main/overlay.png').convert_alpha()
        
    def customDraw(self):
        
        self.offset.x = player.rect.centerx - WINDOW_WIDTH/2
        self.offset.y = player.rect.centery - WINDOW_HEIGHT/2
        
        displaySurface.blit(self.bg,-self.offset)
        
        for sprite in sorted(self.sprites(),key = lambda sprite :sprite.rect.centery):
            offsetPos = sprite.rect.topleft - self.offset
            displaySurface.blit(sprite.image,offsetPos)

        displaySurface.blit(self.fg,-self.offset)

pygame.init()  

displaySurface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption('Frogger')

clock = pygame.time.Clock()

#GROUP
allSprites = AllSprites()
obstacleSprite = pygame.sprite.Group()

#PLAYER SPRITE
player = Player((2062,3274),obstacleSprite)
allSprites.add(player)

#CAR TIMER
carTimer = pygame.event.custom_type()
pygame.time.set_timer(carTimer,80)
posList = []

#TEXT
font = pygame.font.Font(None,150)
textSurf = font.render('VICTORY',True,'White')
textRect = textSurf.get_rect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2))

#SOUND
bgMusic = pygame.mixer.Sound('audio/music.mp3')
bgMusic.play(loops = -1)

for fileName, posList in SIMPLE_OBJECTS.items():
    path = f'graphics/objects/simple/{fileName}.png'
    surf = pygame.image.load(path).convert_alpha()
    for pos in posList:
        simpleSprite = SimpleSprite(surf,pos)
        allSprites.add(simpleSprite)
        obstacleSprite.add(simpleSprite)
        
for fileName, posList in LONG_OBJECTS.items():
    path = f'graphics/objects/long/{fileName}.png'
    surf = pygame.image.load(path).convert_alpha()
    for pos in posList:
        longSprite = LongSprite(surf,pos)
        allSprites.add(longSprite)
        obstacleSprite.add(simpleSprite)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
                
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
            
        if event.type == carTimer:
            randomPos = choice(CAR_START_POSITIONS)
            if randomPos not in posList:
                posList.append(randomPos)    
                pos = (randomPos[0],randomPos[1] + randint(-8,8))
                car = Car(pos)
                allSprites.add(car)
                obstacleSprite.add(car)
            
            if len(posList) > 5:
                del posList[0]
            
            
    dt = clock.tick() / 1000
    
    displaySurface.fill('black')
    
    if player.pos.y > 1180:
        allSprites.update(dt)
        
        allSprites.customDraw()
        
    else:
        displaySurface.fill('teal')
        displaySurface.blit(textSurf,textRect)
        
    pygame.display.update()