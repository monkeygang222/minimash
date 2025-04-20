import pygame
import config

class consumable(pygame.sprite.Sprite):

    def __init__(self, image, center, effect, border):

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.border = pygame.image.load(border)
        self.center = center
        self.rect = self.image.get_rect(center=self.center)
        self.isConsumed = False
        self.effect = effect

    def down(self):
        self.rect = self.rect.move([0, 20])
        config.screen.blit(self.border, self.rect)
        config.screen.blit(self.image, self.rect)

    def grounded(self):
        grounded = False
        #false moves down, true doesn't move
        for floor in config.floorobjects:
            if (self.rect.bottom < floor.rect.top):
                grounded = False 
            elif floor.rect.right > self.rect.left and self.rect.right > floor.rect.left and self.check_collision(floor):        
                if abs(floor.rect.top - self.rect.bottom) <= 15:
                    grounded = True
                    self.snap(floor)
                    return grounded
        return grounded
    
    def snap(self, floor):    
        self.rect = self.rect.move([0, floor.rect.top - self.rect.bottom + 15])
        config.screen.blit(self.image, self.rect)

    def check_collision(self, object):
        if pygame.sprite.collide_mask(self, object) == None:
            return False    
        else:
            return True

    def consumed(self):
        self.isConsumed = True

        