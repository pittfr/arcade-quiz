import pygame

class Label:
    def __init__(self, pos, text, font, text_color=(255, 255, 255),
                 visible=True, highlighted=False, highlight_color=None,
                 anchor="center", opacity=255, max_width=None, padding=(0, 0)):
        
        self.text = text
        self.font = font
        self.text_color = text_color
        self.pos = pos
        self.visible = visible
        self.highlighted = highlighted
        self.highlight_color = highlight_color
        self.anchor = anchor
        self.opacity = max(0, min(255, opacity))
        self.max_width = max_width
        self.padding = padding
        self.text_surfaces = []
        
        self._update_surface()
    
    def _update_surface(self):
        """update the text surface when text or font changes"""
        # use highlight color if highlighted and highlight_color is set
        render_color = self.highlight_color if self.highlighted and self.highlight_color else self.text_color
        
        font_height = self.font.get_height()
        
        if self.max_width is None:
            # no word wrapping needed
            self.text_surfaces = [self.font.render(self.text, True, render_color)]
            text_width = self.text_surfaces[0].get_width()
            text_height = font_height
        else:
            max_text_width = self.max_width - (self.padding[0] * 2)
            
            self.text_surfaces = []
            words = self.text.split()
            current_line = ""
            
            for word in words:
                test_line = current_line + word + " " if current_line else word + " "
                test_surface = self.font.render(test_line.strip(), True, render_color)
                
                if test_surface.get_width() <= max_text_width:
                    current_line = test_line
                else:
                    if current_line:
                        self.text_surfaces.append(self.font.render(current_line.strip(), True, render_color))
                    current_line = word + " "
            
            if current_line:
                self.text_surfaces.append(self.font.render(current_line.strip(), True, render_color))
            
            if not self.text_surfaces:
                self.text_surfaces = [self.font.render(self.text, True, render_color)]
            
            text_width = max([surf.get_width() for surf in self.text_surfaces])
            text_height = len(self.text_surfaces) * font_height
        
        self.text_surface = pygame.Surface((text_width + self.padding[0] * 2, 
                                          text_height + self.padding[1] * 2), pygame.SRCALPHA)
        self.text_surface.fill((0, 0, 0, 0))
        
        for i, line_surface in enumerate(self.text_surfaces):
            line_rect = line_surface.get_rect(
                midtop=(text_width // 2 + self.padding[0], 
                       i * font_height + self.padding[1])
            )
            self.text_surface.blit(line_surface, line_rect)
        
        if self.opacity < 255:
            self.text_surface.set_alpha(self.opacity)
        
        self.rect = self.text_surface.get_rect()
        
        if self.rect is not None:
            setattr(self.rect, self.anchor, self.pos)

    def setText(self, text):
        """change the displayed text"""
        if text != self.text:
            self.text = text
            self._update_surface()
    
    def setColor(self, color):
        """change the text color"""
        if color != self.text_color:
            self.text_color = color
            self._update_surface()
    
    def setPosition(self, pos):
        """change the position of the label"""
        if pos != self.pos:
            self.pos = pos
            self._update_surface()

    def setAnchor(self, anchor):
        """change the anchor point"""
        if anchor != self.anchor:
            self.anchor = anchor
            self._update_surface()
    
    def setVisibility(self, visible):
        """set visibility state"""
        self.visible = visible

    def setHighlighted(self, highlighted):
        """change highlighted state"""
        if highlighted != self.highlighted:
            self.highlighted = highlighted
            self._update_surface()
    
    def setOpacity(self, opacity):
        """set the transparency of the text (0-255)"""
        # ensure opacity is within valid range
        opacity = max(0, min(255, int(opacity)))
        
        if opacity != self.opacity:
            self.opacity = opacity
            self._update_surface()
            
    def setMaxWidth(self, max_width):
        """set the maximum width for text wrapping"""
        if max_width != self.max_width:
            self.max_width = max_width
            self._update_surface()

    def draw(self, surface):
        """draw label on the given surface"""
        if not self.visible:
            return
        
        surface.blit(self.text_surface, self.rect)
