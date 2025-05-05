import time
from utils import ease_in_out

class Animation:
    def __init__(self, start_value, target_value, duration, delay=0.0, easing_function=ease_in_out):
        self.start_value = start_value
        self.current_value = start_value
        self.target_value = target_value
        self.duration = duration
        self.delay = delay
        self.easing_function = easing_function
        
        self.delay_timer = 0.0
        self.progress = 0.0
        self.is_complete = False
        
    def reset(self):
        self.delay_timer = 0.0
        self.progress = 0.0
        self.is_complete = False
        self.current_value = self.start_value
        
    def update(self, delta_time):
        if self.is_complete:
            return self.target_value
            
        if self.delay_timer < self.delay:
            # count down the delay timer
            self.delay_timer += delta_time
            return self.current_value
            
        # once the delay is over, start the animation
        if self.progress <= 1:
            self.progress += delta_time / self.duration
            if self.progress >= 1:
                self.progress = 1
                self.is_complete = True
                
            eased_progress = self.easing_function(self.progress)
            self.current_value = self.start_value + (self.target_value - self.start_value) * eased_progress
            
        return self.current_value