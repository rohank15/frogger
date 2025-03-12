import pygame
from os import walk
import random

class Car(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.name = 'car'
        
        self.importAssets()
        self.image = random.choice(self.diffCars)
        self.rect = self.image.get_rect(center = pos)
        
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200
        
        self.hitbox = self.rect.inflate(-self.rect.width * 0.5,-self.rect.height/2)
        self.hitbox.bottom = self.rect.bottom + 10
        
        if self.pos.x > 400:
            self.direction = pygame.math.Vector2(-1,0)
            self.image = pygame.transform.flip(self.image,True,False)
            
        else:
            self.direction = pygame.math.Vector2(1,0)
        
    def importAssets(self):
        self.diffCars = []
        
        for car in list(walk('graphics/cars'))[0][2]:
            path = list(walk('graphics/cars'))[0][0] + '//' + car
            surf = pygame.image.load(path).convert_alpha()
            self.diffCars.append(surf)
            
    def update(self,dt):
        self.pos += self.direction * self.speed * dt
        self.hitbox.center = (round(self.pos.x),round(self.pos.y))
        self.rect.center = self.hitbox.center
        
        if self.pos.x < -200 or self.pos.x > 3500:
            self.kill()