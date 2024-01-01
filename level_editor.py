from scripts.world import World
from scripts.utils import load_images_from_folder
import pygame 
from pygame.locals import *

class LevelEditor(World):
    
    def __init__(self) -> None:
        super().__init__()
        
        self.load_world("1.wlr")
        self.images = load_images_from_folder("assets/world/")
        self.world_path = ''
        
    def run():
        pass 
    
        
lv = LevelEditor()
lv.run()