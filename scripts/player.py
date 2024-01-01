import pygame 
from pygame.locals import *

from scripts.utils import *

class Player:
    
    def __init__(self) -> None:
        self.rect = pygame.FRect(0,0, 32,32)
        self.dpos = [0,0]
        
    def update(self, dt):
        self.dpos = [0,0]
        
        self.dpos[0] = (pygame.key.get_pressed()[K_d] - pygame.key.get_pressed()[K_a] ) * 3 * dt
        self.dpos[1] = (pygame.key.get_pressed()[K_s] - pygame.key.get_pressed()[K_w] ) * 3 * dt
        
        self.rect.x += self.dpos[0]
        self.rect.y += self.dpos[1]
    
    def render(self, screen, offset):
        rrect = render_rect(self.rect.topleft, offset)
        pygame.draw.rect(screen, (255,255,255), rrect)