import pygame 
from pygame.locals import *
from time import time

from scripts.tasks import TaskManager
from scripts.player import Player
from scripts.world import World
from scripts.utils import load_images_from_folder

class Game:
    
    def __init__(self) -> None:
        
        self.last_time = time()
        
        self.screen = pygame.display.set_mode((1920//2.5,1080//2.5), flags=FULLSCREEN|SCALED)
        self.clock = pygame.time.Clock()
        
        self.tasks = TaskManager()
        self.tasks.bind(K_ESCAPE, self.quit)
        
        self.assets = {
            "world" : load_images_from_folder("assets/world/")
        }
        
        self.world = World(self)
        self.world.load_world("1.wlr")
        self.world_surf = self.world.world_surface()
        
        
        self.player = Player()
    
    def update(self):
        
        dt = self.get_dt()
        
        self.clock.tick()
        
        self.player.update(dt)
        
        
        self.screen.fill((12,200,250))
        self.screen.blit(self.world_surf, (0,0))
        
        self.player.render(self.screen, [0,0])
        
    def get_dt(self):
        
        dt = time()- self.last_time
        self.last_time = time()
        return dt * 60
        
    
    def quit(self):
        import sys 
        sys.exit()
    
    def run(self):
        while True:
            
            self.update()
            
            for event in pygame.event.get():

                if event.type == QUIT:
                    self.quit()
                    
                if event.type == KEYDOWN:
                    self.tasks.do_binds(event)
                        
            pygame.display.update()
            
game = Game()
game.run()