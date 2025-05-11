import os
import pygame

def load_image(image_path, convert_alpha=True, fallback_color=(255, 0, 255)):

    try:
        img = pygame.image.load(image_path)
        if convert_alpha and img.get_alpha():
            return img.convert_alpha()
        elif not convert_alpha:
            return img.convert()
        return img
    except Exception as e:
        print(f"Error loading image {image_path}: {e}")
        # create a blank surface as placeholder
        surface = pygame.Surface((300, 200))
        surface.fill(fallback_color)
        return surface

def preload_images_by_theme(themes_dict, base_path, placeholder_path=None):
    image_cache = {}
    theme_image_dict = {}
    
    # load placeholder image if provided
    if placeholder_path and os.path.exists(placeholder_path):
        placeholder = load_image(placeholder_path)
        image_cache[placeholder_path] = placeholder
    else:
        # create a blank purple surface as default placeholder
        placeholder = pygame.Surface((300, 200))
        placeholder.fill((255, 0, 255))
        
    # set default theme with placeholder
    theme_image_dict["default"] = [placeholder]
    
    # load all images from each theme folder
    for theme, count in themes_dict.items():
        theme_image_dict[theme] = []
        for i in range(1, count + 1):
            img_path = os.path.join(base_path, theme, f"{i}.jpg")
            try:
                img = load_image(img_path)
                image_cache[img_path] = img
                theme_image_dict[theme].append(img)
            except Exception as e:
                print(f"Error loading theme image {img_path}: {e}")
                theme_image_dict[theme].append(placeholder)
                
    return image_cache, theme_image_dict

def get_random_image_for_theme(theme_image_dict, theme):
    import random
    if theme in theme_image_dict and theme_image_dict[theme]:
        return random.choice(theme_image_dict[theme])
    # fallback to default theme
    return random.choice(theme_image_dict["default"])