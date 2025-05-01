import pygame

class Image:
    def __init__(self, pos, image_path, scale=1.0, fixed_width=None, fixed_height=None, 
                 preserve_aspect_ratio=True, visible=True):
        
        self.pos = pos
        self.image_path = image_path
        self.scale = scale
        self.fixed_width = fixed_width
        self.fixed_height = fixed_height
        self.preserve_aspect_ratio = preserve_aspect_ratio
        self.visible = visible

        self.original_image = None
        self.original_rect = None
        self.image = None
        self.rect = None
        
        # load the image
        self._load_image()

    def _load_image(self):
        try:
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
            self.rect.center = self.pos

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
        
        # position the image
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def setPosition(self, pos):
        if pos != self.pos:
            self.pos = pos
            if self.rect:
                self.rect.center = pos

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

    def setVisibility(self, visible):
        self.visible = visible

    def draw(self, surface):
        if self.visible and self.image and self.rect:
            surface.blit(self.image, self.rect)
