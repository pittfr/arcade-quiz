import pygame
import time

class Image:
    def __init__(self, pos, image_path, scale=1.0, fixed_width=None, fixed_height=None, 
                 preserve_aspect_ratio=True, visible=True, anchor="center", opacity=255,
                 border_radius=0, fade_duration=0.5):
        
        self.pos = pos
        self.image_path = image_path
        self.scale = scale
        self.fixed_width = fixed_width
        self.fixed_height = fixed_height
        self.preserve_aspect_ratio = preserve_aspect_ratio
        self.visible = visible
        self.anchor = anchor
        self.opacity = max(0, min(255, opacity))
        self.border_radius = border_radius
        self.fade_duration = fade_duration

        self.original_image = None
        self.original_rect = None
        self.image = None
        self.rect = None
        
        # animation properties
        self.animating = False
        self.animation_start_time = 0
        self.animation_target_opacity = self.opacity
        self.animation_start_opacity = self.opacity
        self.temp_image_path = None
        self.transition_image = None
        self.current_image = None
        
        # load the image
        self._load_image()

    def _load_image(self):
        try:
            if hasattr(self, 'quiz_manager') and self.quiz_manager:
                self.original_image = self.quiz_manager.get_cached_image(self.image_path)
            else:
                self.original_image = pygame.image.load(self.image_path)
                
            if(self.original_image.get_alpha() is not None):
                self.original_image = self.original_image.convert_alpha()
            else:
                self.original_image = self.original_image.convert()
            
            self.original_rect = self.original_image.get_rect()
            self._apply_transformations()
            
        except Exception as e:
            print(f"could not load image {self.image_path}: {e}")
            # create a placeholder for failed loads
            self.image = pygame.Surface((100, 100))
            self.image.fill((255, 0, 255))
            self.rect = self.image.get_rect()
            setattr(self.rect, self.anchor, self.pos)

    def _apply_transformations(self):
        if self.original_image is None:
            return

        orig_width = self.original_rect.width
        orig_height = self.original_rect.height
        
        # calculate new dimensions
        if self.fixed_width is not None and self.fixed_height is not None:
            # both dimensions fixed
            new_width = self.fixed_width
            new_height = self.fixed_height
        elif self.fixed_width is not None:
            # width fixed, calculate height
            new_width = self.fixed_width
            new_height = int(new_width * orig_height / orig_width) if self.preserve_aspect_ratio else orig_height
        elif self.fixed_height is not None:
            # height fixed, calculate width
            new_height = self.fixed_height
            new_width = int(new_height * orig_width / orig_height) if self.preserve_aspect_ratio else orig_width
        else:
            # apply scale factor
            new_width = int(orig_width * self.scale)
            new_height = int(orig_height * self.scale)
        
        # create scaled image
        if new_width > 0 and new_height > 0:
            self.image = pygame.transform.smoothscale(self.original_image, (new_width, new_height))
        else:
            # prevent zero-sized images
            self.image = self.original_image
            
        # apply border radius if needed
        if self.border_radius > 0:
            self._apply_border_radius()
            
        # apply opacity if not fully opaque
        if self.opacity < 255:
            # create a copy that supports alpha
            if self.image.get_alpha() is None:
                self.image = self.image.convert_alpha()
            
            # set the alpha value
            self.image.set_alpha(self.opacity)
        
        # position the image based on anchor
        self.rect = self.image.get_rect()
        setattr(self.rect, self.anchor, self.pos)
    
    def _apply_border_radius(self):
        """apply rounded corners to the image"""
        if self.border_radius <= 0 or self.image is None:
            return
            
        # create a surface with per-pixel alpha
        sized_image = self.image.copy()
        if sized_image.get_alpha() is None:
            sized_image = sized_image.convert_alpha()
            
        w, h = sized_image.get_size()
        radius = min(self.border_radius, min(w, h) // 2)  # limit radius to half of smallest dimension
        
        # create a mask surface with rounded corners
        mask = pygame.Surface((w, h), pygame.SRCALPHA)
        mask.fill((0, 0, 0, 0))  # transparent
        
        # draw rounded rectangle on the mask
        pygame.draw.rect(mask, (255, 255, 255, 255), (0, 0, w, h), 
                         border_radius=radius)
        
        # apply the mask to our image
        sized_image.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
        self.image = sized_image

    def update(self):
        """update animation states"""
        if not self.animating:
            return
            
        # calculate current progress of the animation
        current_time = time.time()
        progress = min(1.0, (current_time - self.animation_start_time) / self.fade_duration)
                
        if progress >= 1.0:
            # animation complete
            self.animating = False
            self.opacity = self.animation_target_opacity
            
            # if we were fading out to change image, now load the new image
            if self.temp_image_path:
                self.image_path = self.temp_image_path
                self.temp_image_path = None
                self._load_image()
                
                # start fade in
                self.animation_start_opacity = 0
                self.animation_target_opacity = 255
                self.opacity = 0
                self.animation_start_time = time.time()
                self.animating = True
        else:
            # update opacity based on progress
            current_opacity = int(self.animation_start_opacity + 
                              (self.animation_target_opacity - self.animation_start_opacity) * progress)
            self.opacity = current_opacity
            self._apply_transformations()

    def setPosition(self, pos):
        """change the position of the image"""
        if pos != self.pos:
            self.pos = pos
            if self.rect:
                setattr(self.rect, self.anchor, pos)

    def setAnchor(self, anchor):
        """change the anchor point"""
        if anchor != self.anchor:
            # store current position
            old_pos = self.pos
            
            # update anchor
            self.anchor = anchor
            
            # reapply position with new anchor
            if self.rect:
                setattr(self.rect, self.anchor, old_pos)

    def setScale(self, scale):
        if scale != self.scale:
            self.scale = scale
            self._apply_transformations()

    def setDimensions(self, width=None, height=None):
        changed = False
        if width != self.fixed_width:
            self.fixed_width = width
            changed = True
        if height != self.fixed_height:
            self.fixed_height = height
            changed = True
        
        if changed:
            self._apply_transformations()

    def getDimensions(self):
        if self.rect:
            return (self.rect.width, self.rect.height)
        return (0, 0)

    def setAspectRatioMode(self, preserve):
        if preserve != self.preserve_aspect_ratio:
            self.preserve_aspect_ratio = preserve
            self._apply_transformations()

    def setImage(self, image_path):
        if image_path != self.image_path:
            self.image_path = image_path
            self._load_image()
            
    def setPath(self, image_path, animate=True):
        """change the image with a fade transition"""
        if image_path == self.image_path:
            return
            
        if animate:
            # start fade out animation
            self.temp_image_path = image_path
            self.animation_start_opacity = self.opacity
            self.animation_target_opacity = 0
            self.animation_start_time = time.time()
            self.animating = True
        else:
            # change immediately without animation
            self.image_path = image_path
            self._load_image()

    def setBorderRadius(self, radius):
        """set rounded corners radius"""
        if radius != self.border_radius:
            self.border_radius = radius
            self._apply_transformations()
            
    def setFadeDuration(self, duration):
        """set the duration of fade animations in seconds"""
        self.fade_duration = max(0.1, duration)  # ensure minimum sensible duration

    def setVisibility(self, visible):
        self.visible = visible
        
    def setOpacity(self, opacity):
        # ensure opacity is within valid range
        opacity = max(0, min(255, int(opacity)))
        
        if opacity != self.opacity:
            self.opacity = opacity
            self._apply_transformations()

    def draw(self, surface):
        if self.visible and self.image and self.rect:
            surface.blit(self.image, self.rect)
