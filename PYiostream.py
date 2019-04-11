import pygame
import time


class CinCout:

    """
    This class is used to get data from player, print phrases on the screen and show end cam

    It contains information about game surface
    """

    def __init__(self, window_width, window_high, window, start_time, main_font, font_size):
        self.window = window
        self.window_width = window_width
        self.window_high = window_high
        self.start_time = start_time
        self.font = main_font
        self.font_size = font_size

    def end_scene(self, death_sentence, game):

        """
        The scene that plays then the game is over
        """

        death_font = pygame.font.Font('fonts/15353.ttf', 90)
        background = pygame.image.load('images/backgrounds/menu_back.jpg')
        self.window.blit(background, (0, 0))
        self.window.blit(death_font.render(death_sentence, 1, (255, 255, 255)),
                         (self.window_width / 2 - 200, self.window_high / 2 - 100))
        time_sentence = "your time: " + str(round(time.time() - self.start_time + game.additional_time, 1)) + ' sec'
        self.window.blit(death_font.render(time_sentence, 1, (255, 255, 255)),
                         (self.window_width / 2 - 400, self.window_high / 2 + 50))
        pygame.display.update()
        pygame.time.delay(4000)
        global run_game
        run_game = False

    def graphic_input(self, graphic_input_sentence):

        """
        This method works as input() with graphic interface
        """

        if len(graphic_input_sentence) > 20:
            graphic_input_sentence = "ENTER:"
        background = pygame.image.load('images/backgrounds/menu_back.jpg')
        graphic_input_font = pygame.font.Font('fonts/15353.ttf', 60)
        word = ""
        done = True
        while done:
            self.window.blit(background, (0, 0))
            pygame.draw.rect(self.window, (250, 250, 250), (400, 310, 500, 60))
            self.window.blit(graphic_input_font.render(graphic_input_sentence, 1, (0, 0, 0)), (350, 200))
            self.window.blit(graphic_input_font.render(word, 1, (0, 0, 0)), (400, 300))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        word = word[:len(word) - 1]
                    if event.key == pygame.K_RETURN:
                        done = False
                    if event.key != pygame.K_BACKSPACE and event.key != pygame.K_RETURN and \
                            event.key != pygame.K_ESCAPE and len(word) <= 13 and event.key != pygame.K_LSHIFT:
                        if event.mod == pygame.KMOD_LSHIFT:
                            word += str(chr(event.key)).upper()
                        else:
                            word += str(chr(event.key))
            pygame.display.update()
            pygame.time.delay(10)
        return word

    def print_window(self, word):

        """
        This method works as output() with graphic interface
        """

        buf_font = pygame.font.Font('fonts/15353.ttf', 40)
        self.window.blit(buf_font.render(word, 1, (0, 0, 0)),
                         (self.window_width / 2 - 400, self.window_high / 2 - 100))
        pygame.display.update()
        pygame.time.delay(1000)
