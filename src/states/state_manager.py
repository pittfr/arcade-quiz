class StateManager:
    def __init__(self, game):
        self.game = game
        self.states = {}
        self.current_state = None
        
    def addState(self, state_id, state):
        """add a state to the state manager"""
        self.states[state_id] = state
        
    def changeState(self, state_id):
        """change to a different state"""
        if state_id in self.states:
            if self.current_state:
                self.current_state.exit()
            self.current_state = self.states[state_id]
            self.current_state.enter()
        else:
            print(f"state {state_id} not found!")
            
    def handleEvents(self, events):
        """handle events in the current state"""
        if self.current_state:
            self.current_state.handle_events(events)
            
    def update(self):
        """update the current state"""
        if self.current_state:
            self.current_state.update()
            
    def draw(self, delta_time, screen):
        """draw the current state"""
        if self.current_state:
            self.current_state.draw(delta_time, screen)