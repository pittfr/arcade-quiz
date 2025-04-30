import pygame

class Label:
    def __init__(self, pos, text, font, text_color=(255, 255, 255),
                 visible=True, highlighted=False, highlight_color=None):
        
        self.text = text
        self.font = font
        self.text_color = text_color
        self.pos = pos
        self.visible = visible
        self.highlighted = highlighted
        self.highlight_color = highlight_color
        
        self._update_surface()
    
    def _update_surface(self):
        """update the text surface when text or font changes"""
        # use highlight color if highlighted and highlight_color is set
        render_color = self.highlight_color if self.highlighted and self.highlight_color else self.text_color
        self.text_surface = self.font.render(self.text, True, render_color)
        self.rect = self.text_surface.get_rect()
        
        if self.rect is not None:
            self.rect.center = self.pos
    
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
    
    def setVisibility(self, visible):
        """set visibility state"""
        self.visible = visible

    def setHighlighted(self, highlighted):
        """change highlighted state"""
        if highlighted != self.highlighted:
            self.highlighted = highlighted
            self._update_surface()
    
    def draw(self, surface):
        """draw label on the given surface"""
        if not self.visible:
            return
        
        surface.blit(self.text_surface, self.rect)
