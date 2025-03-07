import pygame
import os
import random
from .constants import constants
from .services import event_handler
from .services import event_states
from .gui.prepare_screen import GameScreen
from .gui.screen_loader import Title
from .gui.gui_objects_creator import LoadScreenState
from .services.states_loader import StateLoader
from .calculations.gui_collisions import GuiCollisions
import sys

class GameRunner:
    def __init__(self):
        self.SCREEN_HEIGHT = constants['SCREEN_HEIGHT']
        self.SCREEN_WIDTH = constants['SCREEN_WIDTH']
        self.full_screen = constants['FULL_SCREEN']
        self.background_color = constants['BACKGROUND_COLOR']
        self.game_container_color = constants['GAME_CONTAINER_COLOR']
        self.event_variable = event_states.EventVariables()
        self.gui_collisions = GuiCollisions(constants, self.event_variable)
        self.event_handle = event_handler.EventHandle(self.event_variable,
                                                    self.gui_collisions, constants)
        self.sounds = []  # List to store sound files
        self.player_name = ""

    def pygame_initializer(self):
        pygame.init()
        pygame.mixer.init()  # Initialize the mixer
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.FULLSCREEN)
        self.game_screen = GameScreen(self.screen, constants, self.event_variable)
        self.states = StateLoader(constants, self.event_variable, self.screen)
        self.states.load_fonts()
        self.states.load_speeds()
        title_font = self.event_variable.get_font("title",
                                                  self.event_variable.get_event_state())
        self.title = Title(font=title_font,
                                    colors=constants['TITLE_COLOR'],
                                    screen=self.screen,
                                    event_state=self.event_variable)
        self.screen_objects = LoadScreenState(constants, 
                                              self.title,
                                              self.event_variable, self.screen)
        self.screen_objects.create_state_objects()

        # Load all sound files from the assets/sounds directory
        sound_dir = "assets/sounds"
        for filename in os.listdir(sound_dir):
            if filename.endswith(".wav"):
                sound_path = os.path.join(sound_dir, filename)
                self.sounds.append(pygame.mixer.Sound(sound_path))

        # Play the first random sound
        self.play_random_sound()

    def play_random_sound(self):
        if self.sounds:
            sound = random.choice(self.sounds)
            sound.play()
            pygame.mixer.music.set_endevent(pygame.USEREVENT)

    def events(self):
        for event in pygame.event.get():
            self.event_handle.handle_event(event)
            if event.type == pygame.USEREVENT:  # Event when a sound ends
                self.play_random_sound()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.event_variable.update_high_scores(self.player_name)
                elif event.key == pygame.K_BACKSPACE:
                    self.player_name = self.player_name[:-1]
                else:
                    self.player_name += event.unicode

    def game_run(self):
        self.pygame_initializer()
        clock = pygame.time.Clock()  # Create a Clock object
        FPS = self.event_variable.get_fps()
        start_time = pygame.time.get_ticks()  # Get start time in milliseconds
        while self.event_variable.get_running():
            self.events()
            self.screen.fill(self.background_color)
            self.game_screen.draw_game_container(self.game_container_color)
            self.game_screen.draw_boundaries()
            self.screen_objects.draw_state()
            self.event_variable.set_mouse_pos(pygame.mouse.get_pos())
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - start_time
            self.event_variable.set_elapsed_seconds(elapsed_time)
            pygame.display.flip()
            clock.tick(FPS)
        sys.exit()