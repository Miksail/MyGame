import pygame
import sys


class Menu:

    """
    This class is used for making menu screen

    options - list of tuples of menu options in form: (width, high, text of option, highlighted color, color, motion)
    win_information - game surface information
    game - used for get game information
    """

    background = pygame.image.load('images/backgrounds/menu_back.jpg')

    def __init__(self, options, win_information, game):
        self.options = options
        self.win_info = win_information
        self.game = game

    def render(self, font, num_option):
        for i in self.options:
            if num_option == i[5]:
                self.win_info.window.blit(font.render(i[2], 1, i[4]), (i[0], i[1]))
            else:
                self.win_info.window.blit(font.render(i[2], 1, i[3]), (i[0], i[1]))

    def menu(self):
        """
        Check which option is chosen and render it

        If player press Enter, it will do motion, which match to chosen option
        """
        done = True
        font_menu = pygame.font.Font('fonts/15431.otf', 70)
        option = 0
        while done:
            self.win_info.window.blit(self.background, (0, 0))
            self.render(font_menu, option)
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    sys.exit()
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_UP:
                        if option > 0:
                            option -= 1
                    if ev.key == pygame.K_DOWN:
                        if option < len(self.options) - 1:
                            option += 1
                    if ev.key == pygame.K_RETURN:
                        if self.options[option][6] == 'Start':
                            done = False
                        if self.options[option][6] == 'Exit':
                            sys.exit()
                        if self.options[option][6] == 'Save':
                            self.game.save_game()
                        if self.options[option][6] == 'Load':
                            if self.game.load_game():
                                return 'Load'
                        if self.options[option][6] == 'ExitFromGame':
                            self.game.run_game = False
                            return 'ExitFromGame'
            pygame.display.update()
        return 0


class InGameMenu(Menu):

    """
    This subclass Menu calls in game
    """

    def __init__(self, win_info, game):
        self.menu_options = [(win_info.window_width / 2 - 100, win_info.window_high / 5 * 1 - 50, 'Continue',
                             (71, 74, 81), (255, 255, 255), 0, 'Start'),
                             (win_info.window_width / 2 - 30, win_info.window_high / 5 * 2 - 50, 'Save',
                             (71, 74, 81), (255, 255, 255), 1, 'Save'),
                             (win_info.window_width / 2 - 30, win_info.window_high / 5 * 3 - 50, 'Exit',
                             (71, 74, 81), (255, 255, 255), 2, 'ExitFromGame')]

        super().__init__(self.menu_options, win_info, game)


class WelcomeMenu(Menu):

    """
    This subclass Menu calls to start new game
    """

    def __init__(self, win_info, game):
        self.welcome_options = [(win_info.window_width/2 - 100, win_info.window_high / 5 * 1, 'New Game',
                                (71, 74, 81), (255, 255, 255), 0, 'Start'),
                                (win_info.window_width/2 - 30, win_info.window_high / 5 * 2, 'Load',
                                (71, 74, 81), (255, 255, 255), 1, 'Load'),
                                (win_info.window_width/2 - 30, win_info.window_high / 5 * 3, 'Quit',
                                (71, 74, 81), (255, 255, 255), 2, 'Exit')]

        super().__init__(self.welcome_options, win_info, game)
