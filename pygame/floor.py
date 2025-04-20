import pygame
import pygame.freetype

class floor(pygame.sprite.Sprite):

    def __init__(self, x, y, center_x, center_y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.center_x = center_x
        self.center_y = center_y
        self.surface = pygame.Surface((x, y))
        self.image = pygame.Surface((x, y))
        self.rect = self.surface.get_rect(center=(center_x, center_y))
        