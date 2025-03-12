import pygame, sys
from os import walk

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,collisionSprite):
        super().__init__()
        
        self.importAssets()
        self.frameIndex = 0
        self.status = 'down'
        self.image = self.animations[self.status][self.frameIndex]
        self.rect = self.image.get_rect(center = pos)
        
        self.pos = pygame.math.Vector2(self.rect.center)
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 200
        
        self.collisionSprite = collisionSprite
        self.hitbox = self.rect.inflate(0,-self.rect.height/2)
    
    def collision(self,direction):
        if direction == 'horizontal':
            for sprite in self.collisionSprite.sprites():
                if sprite.hitbox.colliderect(self.hitbox):
                    if hasattr(sprite,'name') and sprite.name == 'car':
                        pygame.quit()
                        sys.exit()
                    
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx
                    
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx
                        
        elif direction == 'vertical':
            for sprite in self.collisionSprite.sprites():
                if sprite.hitbox.colliderect(self.hitbox):
                    if hasattr(sprite,'name') and sprite.name == 'car':
                        pygame.quit()
                        sys.exit()
                        
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery
                    
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery
                    
    def importAssets(self):
        self.animations = {}
        
        for index, folder in enumerate(walk('graphics/player')):
            if index == 0:
                for name in folder[1]:
                    self.animations[name] = []
        
            else:
                for file_name in folder[2]:
                    path = folder[0]+ '/' + file_name
                    surf = pygame.image.load(path).convert_alpha()
                    key = folder[0].split('/')[2]
                    self.animations[key].append(surf)

    def move(self,dt):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        
        #HORIZONTAL MOVEMENT
        self.pos.x += self.speed * self.direction.x * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        self.collision('horizontal')
        
        #VERTICAL MOVEMENT
        self.pos.y += self.speed * self.direction.y * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.collision('vertical')
        
    def animate(self,dt):
        currentAnimation = self.animations[self.status]
        
        if self.direction.magnitude() != 0:
            self.frameIndex += 10 * dt
            if self.frameIndex >= len(currentAnimation):
                self.frameIndex = 0
        
        else:
            self.frameIndex = 0
            
        self.image = currentAnimation[int(self.frameIndex)]
    
    def input(self):
        keys = pygame.key.get_pressed()
        
        #HORIZONTAL MOVEMENT
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = 'right'
            
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = 'left'
            
        else:
            self.direction.x =  0
            
        
        #VERTICAL MOVEMENT
        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.status = 'up'
            
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.status = 'down'
            
        else:
            self.direction.y = 0
 
    def restrict(self):
        if self.rect.left < 640:
            self.pos.x = 640 + self.rect.width / 2
            self.hitbox.left = 640
            self.rect.left = 640
        
        if self.rect.right > 2560:
            self.pos.x = 2560 - self.rect.width / 2
            self.hitbox.right = 2560
            self.rect.right = 2560
            
        if self.rect.bottom > 3500:
            self.pos.y = 3500 - self.rect.height / 2
            self.rect.bottom = 3500
            self.hitbox.centery = self.rect.centery
              
    def update(self,dt):
        self.input()
        self.move(dt)
        self.animate(dt)
        self.restrict()
