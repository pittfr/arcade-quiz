import pygame

class Button:
    def __init__(self, pos, action=None, text="", font=None, text_color=(255, 255, 255), 
                 bg_color=None, padding=(0, 0), border_radius=5, sound=None, key=None, width=None, height=None):
        
        self.action = action
        self.clicked = False
        self.key_pressed = False
        self.border_radius = border_radius
        self.sound = sound
        self.key = key
                
        self.text = text
        self.font = font
        self.text_color = text_color
        self.bg_color = bg_color
        self.padding = padding
        self.fixed_width = width
        self.fixed_height = height
            
        # get font height
        font_height = self.font.get_height()
            
        # create text surfaces
        self.text_surface = self.font.render(self.text, True, self.text_color)
        text_width = self.text_surface.get_width()
            
        # calculate visual dimensions based on the font size
        self.visual_width = text_width + padding[0] * 2
        self.visual_height = font_height + padding[1] * 2
        
        # override with fixed dimensions if provided and larger than calculated dimensions
        if self.fixed_width is not None and self.fixed_width > self.visual_width:
            self.visual_width = self.fixed_width
        if self.fixed_height is not None and self.fixed_height > self.visual_height:
            self.visual_height = self.fixed_height
        
        self.visual_rect = pygame.Rect(0, 0, self.visual_width, self.visual_height)
        self.visual_rect.center = pos
            
        # set hitbox to match visual dimensions
        self.rect = self.visual_rect.copy()
        
    def update(self, events):
        # reset state
        self.clicked = False

        for event in events:
            # handle key press
            if event.type == pygame.KEYDOWN and event.key == self.key:
                if not self.key_pressed:
                    self.key_pressed = True
                    self.clicked = True
                    if self.sound:
                        self.sound.play()
                    if self.action:
                        self.action()

                    return True
            
            # reset key_pressed when key is released
            elif event.type == pygame.KEYUP and event.key == self.key:
                self.key_pressed = False
                
        return False
                
    def draw(self, surface):
        # draw background if there is one and it's not transparent
        pygame.draw.rect(surface, self.bg_color, self.visual_rect, border_radius=self.border_radius)
            
        # draw text
        text_surf = self.font.render(self.text, True, self.text_color)
            
        # center text in the button
        text_rect = text_surf.get_rect(center=self.visual_rect.center)
        surface.blit(text_surf, text_rect)

    def getText(self):
        return self.text

    def setText(self, new_text):
        self.text = new_text
        
        # recreate text surface with new text
        self.text_surface = self.font.render(self.text, True, self.text_color)
        text_width = self.text_surface.get_width()
        
        # store original center position to keep the button in the same spot
        old_center = self.visual_rect.center
        
        # recalculate visual dimensions based on new text
        self.visual_width = text_width + self.padding[0] * 2
        self.visual_height = self.font.get_height() + self.padding[1] * 2

        if self.fixed_width is not None and self.fixed_width > self.visual_width:
            self.visual_width = self.fixed_width
        if self.fixed_height is not None and self.fixed_height > self.visual_height:
            self.visual_height = self.fixed_height
        
        self.visual_rect = pygame.Rect(0, 0, self.visual_width, self.visual_height)
        
        # maintain the button's position
        self.visual_rect.center = old_center
        
        # update hitbox to match new visual dimensions
        self.rect = self.visual_rect.copy()