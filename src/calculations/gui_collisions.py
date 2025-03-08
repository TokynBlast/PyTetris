import json

class GuiCollisions:
    def __init__(self, constants, event_state):
        self.constants = constants
        self.event_state = event_state
        self.func_mapper = {0:self.main_menu_collisions,
                            4:self.game_screen_collisions,
                            3:self.game_over_collisions}

    def main_menu_collisions(self, name):
        if name.lower() == "start":
            self.event_state.set_current_shape(None)
            self.event_state.set_bag_of_7(None)
            self.event_state.set_event_state(4)
            self.event_state.set_score(0)
            self.event_state.set_verticle_speed(self.constants['BLOCK_SIZE'])
            
        if name.lower() == "highscores":
            pass
            # Currently, there is only one high score.
        if name.lower() == "about":
            pass
            """
            This is what about will look like (Should make a text function)



            Originally developed by AnandSrikumar on GitHub
            
            PyTetris is a Python version of the INCREDIBLE Tetris!
            Developed in Germany of course!

            To play, click 'play'


            
            There could also be something for reporting bugs and suggestions.
            """
        if name.lower() == "exit":
            self.event_state.set_running(False)
    
    def level_score_reset(self):
        current_score = self.event_state.get_score()
        # Reload high scores from file or from an updated state
        high_scores = self.event_state.get_high_scores()
        
        # Convert keys to strings if needed, ensuring we compare against key "1"
        top_score = high_scores.get("1", {"name": "", "score": 0})

        if current_score > top_score["score"]:
            # Update the top three scores:
            updated_high_scores = {
                "1": {"name": self.event_state.player_name, "score": current_score},
                "2": high_scores.get("1", {"name": "", "score": 0}),
                "3": high_scores.get("2", {"name": "", "score": 0})
            }
            with open('src/services/highscore.json', 'w') as f:
                json.dump(updated_high_scores, f, indent=4)
            # Also update the in-memory state if necessary.
            self.event_state.set_high_scores(updated_high_scores)
        
        # Reset game-related parameters
        self.event_state.set_game_over(False)
        self.event_state.set_score(0)
        self.event_state.set_current_shape(None)
        self.event_state.set_level(1)
        movement_delay = self.constants['movement_delay'][1]
        self.event_state.set_movement_delay(movement_delay)
        
    def game_screen_collisions(self, name):
        if name.lower() == "exit":
            self.level_score_reset()
            self.event_state.set_event_state(0)
    
    def game_over_collisions(self, name):
        self.level_score_reset()
        if name.lower() == 'play_again':
            self.event_state.set_event_state(4)
        elif name.lower() == 'exit':
            self.event_state.set_event_state(0)

    def mouse_down_collisions(self):
        state = self.event_state.get_event_state()
        rectangles = self.event_state.get_menu_rectangles()
        if rectangles is not None and state in rectangles and state in self.func_mapper:
            rectangles = rectangles[state]
            mouse_x, mouse_y = self.event_state.get_mouse_pos()
            for rect_data in rectangles:
                if rect_data["rect"].collidepoint(mouse_x, mouse_y):
                    func_handle = self.func_mapper[state]
                    func_handle(rect_data['name'])
            