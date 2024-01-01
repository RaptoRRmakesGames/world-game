import pygame, pickle  

# !!!!!! SEPERATOR IS ';' 

tsize = 16

class World:
    def __init__(self, game=None) -> None:
        self.tiles = {}
        self.game = game 
        self.images = game.assets["world"]
        self.world_path = ''
        
    def load_world(self, world_path):
        
        with open("worlds/"+world_path, 'rb') as f:
            self.tiles = pickle.load(f)
            self.world_path = world_path
            
    def world_surface(self):
        largest_x = 0
        largest_y = 0
        
        for key in list(self.tiles.keys()):
            x,y = map(int, key.split(";"))
            largest_x = max(largest_x, x)
            largest_y = max(largest_y, y)
                
        surf = pygame.Surface(((largest_x + 1) * 16,(largest_y + 1) * 16))
        
        for key in list(self.tiles.keys()):
            x,y = map(int, key.split(";"))
            t_info = self.tiles[key]
            
            
            surf.blit(self.images[t_info[0]], (x*tsize,y*tsize))
            
        surf.set_colorkey((0,0,0))
        return surf
    
    def save(self):
        
        with open("worlds/"+self.world_path, 'wb') as f:
            pickle.dump(self.tiles, f)
    
    def set_tile(self, pos, type, col=False):
        self.tiles[f"{pos[0]};{pos[1]}"] = (type, col)
        
    