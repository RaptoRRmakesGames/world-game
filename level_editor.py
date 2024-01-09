from scripts.world import World
from scripts.utils import load_images_from_folder
from scripts.tasks import TaskManager
import pygame 
from pygame.locals import *

pygame.font.init()

uifont = pygame.font.SysFont("arial", 24, False, False)

class BlockOption:
    
    def __init__(self, pos, option, game, images ):
        
        self.images = images
        
        self.rect = pygame.Rect(*pos, 32,32)
        self.pos = pos 
        
        self.game= game
        
        self.option = option
        
    def update(self, sidebartopleft):
        
        self.rect.x = sidebartopleft[0] + self.pos[0]
        self.rect.y = sidebartopleft[1] + self.pos[1]
        
        if self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            
            self.game.cur_image = self.option
        
    def render(self, screen):
        
        screen.blit(self.images[self.option], self.rect)
        if self.game.cur_image == self.option:
            pygame.draw.rect(screen,(255,255,255), self.rect, 3)


class LevelEditor(World):
    
    def __init__(self) -> None:
        super().__init__()
        
        self.load_world("1.wlr")
        self.images = load_images_from_folder("assets/world/")
        self.world_path = ''
        
        self.screen = pygame.display.set_mode((1920//2.5,1080//2.5), flags=FULLSCREEN|SCALED)
        self.clock = pygame.time.Clock()
        
        self.tasks = TaskManager()
        self.tasks.bind(K_ESCAPE, self.quit)
        self.tasks.bind(K_g, self.recenter)
        self.tasks.bind(K_0, self.clear)
        self.tasks.bind(K_b, self.toggle_sidebar)
        self.tasks.bind(K_UP, self.change_z, [1])
        self.tasks.bind(K_DOWN, self.change_z, [-1])
        self.tasks.bind(K_p, self.toggle_viewall)
        self.tasks.bind(K_k, self.toggle_climbable)
        self.tasks.bind(K_l, self.toggle_collidable)
        
        self.grid = self.get_grid()
        
        self.recenter()
        
        self.selected = [0,0]
        self.cur_image = 0
        self.cur_collidable = False
        self.cur_zlevel = 0 
        self.cur_climbable = False
        self.brush_size = 1
        self.viewfullworld = True
        
        self.world_image,self.world_surf = self.world_surface()
        
        self.load_world("1.wlr")
        
        self.clear_times = 0
        
        self.cur_sidebar = 25
        self.max_sidebar = 225
        self.sidebaropen = False
        
        self.block_options = []
        y = 0
        choice = 0 
        self.items_y = 0
        for y in range(len(self.images) // 3):
            for x in range(3):
                self.block_options.append(BlockOption((60 + (x * 40), 25 + (y * 40),), choice, self, self.images))
                choice += 1
                
    def toggle_collidable(self):
        self.cur_collidable = not self.cur_collidable
    def toggle_climbable(self):
        self.cur_climbable = not self.cur_climbable
            
    def change_z(self, val):
        self.cur_zlevel += val
        
    def toggle_viewall(self):
        self.viewfullworld = not self.viewfullworld
        
    def toggle_sidebar(self):
        self.sidebaropen = not self.sidebaropen
        
    def clear(self):
        self.clear_times += 1
        if self.clear_times > 2:
            self.tiles = {}
            self.world_image,self.world_surf = self.world_surface()
            self.clear_times = 0
        
    def write(self, text, pos):
        
        self.screen.blit(uifont.render(text, True, (255,255,255)), pos)
        
    def recenter(self):
        self.scroll = [60*32,60*32]
        
    def place_block(self):
        
        #self.tiles[f"{self.selected[0]};{self.selected[1]}"] = (self.cur_image, self.cur_collidable, self.cur_zlevel, self.cur_climbable)
        self.set_tile(self.selected, self.cur_image, self.cur_collidable, self.cur_zlevel, self.cur_climbable)
        self.world_image,self.world_surf = self.world_surface()
    
    def erase(self):
        
        self.er_tile(self.selected, self.cur_zlevel)
        self.world_image,self.world_surf = self.world_surface()
       
    def get_grid(self):
        grid = pygame.Surface((500*32, 500*32))
        for x in range(500):
            for y in range(500):
                pygame.draw.rect(grid, (100,100,100),pygame.Rect((x ) * 32, (y) * 32, 32,32), 1)
        grid.set_colorkey((0,0,0))
        return grid
    
    def calc_selected(self):
        mx,my = pygame.mouse.get_pos()
        mx += self.scroll[0] 
        my += self.scroll[1] 
        my //= 32
        mx //= 32
        self.selected = [round(mx),round(my)]
        
    def handle_sidebar(self):
        match self.sidebaropen:
            
            case True:
                if self.cur_sidebar != self.max_sidebar:
                    self.cur_sidebar += 1
            case False:
                if self.cur_sidebar != 25:
                    self.cur_sidebar -= 1
              
    def draw_brush(self):
        img = self.images[self.cur_image]
        # img.set_alpha(10)
        self.screen.blit(img, [((self.selected[0]) * 32)- self.scroll[0], ((self.selected[1]) * 32 ) - self.scroll[1]], special_flags=BLEND_RGB_ADD)
    
    def update(self):
        
        self.screen.fill((15,60,150))
        self.screen.blit(self.grid, ((-250*32)- self.scroll[0], (-250*32)- self.scroll[1]), )
        if self.viewfullworld:
            self.screen.blit(self.world_image, (- self.scroll[0], - self.scroll[1]), )
        else:
            self.screen.blit(self.world_surf[self.cur_zlevel], (- self.scroll[0], - self.scroll[1]), )
            
        self.draw_brush()
        pygame.draw.rect(self.screen, (25,25,25), pygame.Rect(self.screen.get_width() - self.cur_sidebar, 0, self.cur_sidebar,self.screen.get_height()))
        pygame.draw.rect(self.screen, (225,225,225), pygame.Rect(self.screen.get_width() - self.cur_sidebar, -5, self.cur_sidebar+5,self.screen.get_height()+10), 5)
        if not self.sidebaropen and self.cur_sidebar == 25:
            self.write("B", (10 +self.screen.get_width()-self.cur_sidebar, self.screen.get_height() - self.screen.get_height()//2- 12))

        for block in self.block_options:
            topleft = pygame.Rect(self.screen.get_width() - self.cur_sidebar, 0, self.cur_sidebar,self.screen.get_height())
            block.update([topleft[0], topleft[1] - self.items_y])
        
            block.render(self.screen)
        
        self.scroll[0] += ((pygame.key.get_pressed()[K_d] - pygame.key.get_pressed()[K_a]) * max(1,(pygame.key.get_pressed()[K_LSHIFT] * 3)) ) * 0.1
        self.scroll[1] += ((pygame.key.get_pressed()[K_s] - pygame.key.get_pressed()[K_w]) * max(1,(pygame.key.get_pressed()[K_LSHIFT] * 3)) ) * 0.1
        
        self.calc_selected()
        self.handle_sidebar()
        
        if pygame.mouse.get_pressed()[0] and not pygame.Rect(self.screen.get_width() - 100, 0, 100,self.screen.get_height()).collidepoint(pygame.mouse.get_pos()):
            self.place_block()
        if pygame.mouse.get_pressed()[2] and not pygame.Rect(self.screen.get_width() - 100, 0, 100,self.screen.get_height()).collidepoint(pygame.mouse.get_pos()):
            self.erase()
        
        self.write(f"{int(self.selected[0])};{ int(self.selected[1])}", (0,0))
        self.write(f"Collideable: {self.cur_collidable}", (0,48))
        self.write(f"Z level: {self.cur_zlevel}", (0,72))
        self.write(f"Can climb: {self.cur_climbable}", (0,96))
    
        
        
    def quit(self):
        import sys 
        self.save()
        sys.exit()
        
    def run(self):
        while True:
            
            self.update()
            
            for event in pygame.event.get():

                if event.type == QUIT:
                    self.quit()
                    
                if event.type == KEYDOWN:
                    self.tasks.do_binds(event)
                
                if event.type == MOUSEWHEEL and self.sidebaropen:
                    self.items_y -= event.y * 30
                    
                    if self.items_y > (len(self.images) //3 ) * 32:
                        self.items_y = (len(self.images) // 3 ) * 32
                    if self.items_y < -10:
                        self.items_y = -10
                    
                        
            pygame.display.update()
    
        
lv = LevelEditor()
lv.run()