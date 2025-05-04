import pygame

class Button:
    def __init__(self, pos, action=None, text="", font=None, text_color=(255, 255, 255), 
                 bg_color=None, padding=(0, 0), border_radius=5, sound=None, key=None, 
                 width=None, height=None, anchor="center"):
        
        self.action = action
        self.clicked = False
        self.key_pressed = False
        self.border_radius = border_radius
        self.sound = sound
        self.key = key
        self.anchor = anchor
                
        self.text = text
        self.font = font
        self.text_color = text_color
        self.bg_color = bg_color
        self.starting_bg_color = bg_color
        self.target_bg_color = bg_color
        self.transition_progress = 1
        self.transition_duration = 0.3

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
        
        # position the button based on anchor
        setattr(self.visual_rect, self.anchor, pos)
            
        # set hitbox to match visual dimensions
        self.rect = self.visual_rect.copy()
        
    def update(self, events, delta_time, showingFeedback):
        # reset state
        self.clicked = False

        if 0 <= self.transition_progress <= 1:
            self.transition_progress += delta_time / self.transition_duration
            self.transition_progress = min(self.transition_progress, 1)

            # Here - interpolate between starting color and target color
            r1, g1, b1 = self.starting_bg_color
            r2, g2, b2 = self.target_bg_color
            
            # Linear interpolation for each color component
            r = r1 + (r2 - r1) * self.transition_progress
            g = g1 + (g2 - g1) * self.transition_progress
            b = b1 + (b2 - b1) * self.transition_progress
            
            # Update the current background color
            self.bg_color = (int(r), int(g), int(b))
        else:
            if self.bg_color != self.target_bg_color:
                self.bg_color = self.target_bg_color
                self.starting_bg_color = self.bg_color
        
        for event in events:
            # handle key press
            if event.type == pygame.KEYDOWN and event.key == self.key:
                if not showingFeedback:

                    if not self.key_pressed:
                        self.key_pressed = True
                        self.clicked = True
                        if self.sound:
                            self.sound.play()
                        if self.action:
                            self.action()
                        print(f"{self.text} button has been pressed")
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
        if(self.text != new_text):
            self.text = new_text

            # recreate text surface with new text
            self.text_surface = self.font.render(self.text, True, self.text_color)
            text_width = self.text_surface.get_width()
            
            # store original anchor position to keep the button positioned correctly
            old_pos = getattr(self.visual_rect, self.anchor)
            
            # recalculate visual dimensions based on new text
            self.visual_width = text_width + self.padding[0] * 2
            self.visual_height = self.font.get_height() + self.padding[1] * 2

            if self.fixed_width is not None and self.fixed_width > self.visual_width:
                self.visual_width = self.fixed_width
            if self.fixed_height is not None and self.fixed_height > self.visual_height:
                self.visual_height = self.fixed_height
            
            self.visual_rect = pygame.Rect(0, 0, self.visual_width, self.visual_height)
            
            # maintain the button's position based on anchor
            setattr(self.visual_rect, self.anchor, old_pos)
            
            # update hitbox to match new visual dimensions
            self.rect = self.visual_rect.copy()
    
    def setBgColor(self, color):
        """set the target background color for smooth transition"""
        if self.bg_color != color:
            self.target_bg_color = color
            self.starting_bg_color = self.bg_color
            self.transition_progress = 0
            
    def setPosition(self, pos):
        """change the position of the button"""
        current_pos = getattr(self.visual_rect, self.anchor)
        if pos != current_pos:
            setattr(self.visual_rect, self.anchor, pos)
            self.rect = self.visual_rect.copy()
            
    def setAnchor(self, anchor):
        """change the anchor point of the button"""
        if anchor != self.anchor:
            # get current position based on old anchor
            old_pos = getattr(self.visual_rect, self.anchor)
            
            # update anchor
            self.anchor = anchor
            
            # reposition using new anchor
            self.visual_rect = pygame.Rect(0, 0, self.visual_width, self.visual_height)
            setattr(self.visual_rect, self.anchor, old_pos)
            
            # update hitbox
            self.rect = self.visual_rect.copy()

    def resetKeyState(self):
        """reset the key pressed state"""
        self.key_pressed = False