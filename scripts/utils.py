import pygame 
import os 

def render_rect(pos, offset, w=32,h=32):
    
    return pygame.FRect(pos[0]- offset[0], pos[1]-offset[1], w,h)

def load_images_from_folder(folder_path, rotation = 0, flip=False, sizeup= 1):
    images = []  # List to store loaded images
    
    folder_path = os.path.abspath(folder_path)
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            try:
                image_surface = pygame.transform.flip(pygame.transform.rotate(pygame.image.load(file_path), rotation),False if rotation ==90 or rotation == -90 else flip, False if rotation ==180 or rotation == 0 else flip).convert_alpha()
                
                img_width = image_surface.get_width()
                img_height = image_surface.get_height()
                
                image_surface = pygame.transform.scale(image_surface, (img_width *sizeup, img_height * sizeup))
                
                images.append(image_surface)
            except pygame.error as e:
                print(f"Error loading image {filename}: {e}")
    return images
        