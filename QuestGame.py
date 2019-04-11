import pygame
import sys
import time
import os
from PYiostream import CinCout
from ScenarioRealize import Scene
from Character import Player
from MenuScreen import WelcomeMenu


class Game:

    """
        This class contains main game loop and information about current game

        scenario_name - name of scenario, which will play
        all_scenes - list which contains scenes from scenario (they are added the first time a player goes into scene)
        player - contains information about players character
        win_info - contains information about surface of the game
        additional time - time, which adding in the end of a game(using only if game loaded from save)
        current_scene - scene, which is playing now
        run_game - bool, which used to run main game loop and stop it from another classes
    """

    def __init__(self):
        self.scenario_name = ''
        self.all_scenes = []
        self.player = Player('')
        self.win_info = None
        self.get_win_info()
        self.additional_time = 0
        self.current_scene = Scene
        self.run_game = True

    def get_win_info(self):

        """
        This function initialize win_info (game surface)
        """

        window_width = 1280
        window_high = 720
        window = pygame.display.set_mode((window_width, window_high))
        pygame.display.set_caption('Quest')
        pygame.font.init()
        font_size = 23
        font = pygame.font.Font('fonts/15353.ttf', font_size)
        self.win_info = CinCout(window_width, window_high, window, time.time(), font, font_size)

    def play(self):

        """
        This function run game

        Firstly it sets game parameters
        Then Scene.get_stage() play current scene and return next scene which will be played
        """

        run_menu = True
        while run_menu:
            self.set_game()
            while self.run_game:
                self.current_scene = self.current_scene.get_stage(self.player, self.win_info, self)
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        self.run_game = False
                        run_menu = False

    def set_game(self):

        """
        Set start parameters of the game

        Menu checks if we need to load game from save file
        if we need it, we load from chosen file else se default parameters and ask for the player name
        """

        self.all_scenes.clear()
        self.player = Player('')
        Menu = WelcomeMenu(self.win_info, self)
        if not Menu.menu() == 'Load':
            player_name = self.win_info.graphic_input("ENTER YOUR NAME:")
            if player_name == '':
                player_name = 'Unknown'
            self.player = Player(player_name)
            self.scenario_name = 'myfirstscenario'
            self.current_scene = Scene('startScene', self.scenario_name)
        # scenario_name = graphic_input("ENTER SCENARIO NAME:")
        self.run_game = True
        self.win_info.start_time = time.time()

    def save_game(self):

        """
        This method is used for create game save file, which includes main game information

        To save your game in new file you need to choose 'New save' and write name. If name will be empty,
        this function will automatically set name to 'save' + str(amount of saves)

        If your choose already existing file, it will clear it and write new data
        """

        save_number = 0
        done = True
        esc_but = False
        background = pygame.image.load('images/backgrounds/menu_back.jpg')
        saves_list = os.listdir('saves')
        for i in range(len(saves_list)):
            saves_list[i] = saves_list[i][:len(saves_list[i]) - 4]
        while done:
            self.win_info.window.blit(background, (0, 0))
            for i in range(len(saves_list) + 1):
                if i == len(saves_list):
                    save_name = 'NEW SAVE'
                else:
                    save_name = saves_list[i]
                if i == save_number:
                    self.win_info.window.blit(self.win_info.font.render(save_name, 1, (255, 255, 255)),
                                              (20, self.win_info.font_size * (i + 1)))
                else:
                    self.win_info.window.blit(self.win_info.font.render(save_name, 1, (71, 74, 81)),
                                              (20, self.win_info.font_size * (i + 1)))

            for es in pygame.event.get():
                if es.type == pygame.QUIT:
                    sys.exit()
                if es.type == pygame.KEYDOWN:
                    if es.key == pygame.K_UP:
                        if save_number > 0:
                            save_number -= 1
                    if es.key == pygame.K_DOWN:
                        if save_number < len(saves_list):
                            save_number += 1
                    if es.key == pygame.K_RETURN:
                        if save_number >= 0:
                            done = False
                    if es.key == pygame.K_ESCAPE:
                        done = False
                        esc_but = True
            pygame.display.update()

        if esc_but:
            pass
        else:
            if save_number == len(saves_list):
                save_name = self.win_info.graphic_input('Enter save name')
                if save_name == '':
                    save_name = 'save' + str(len(saves_list))
            else:
                save_name = saves_list[save_number]
            f = open('saves/' + save_name + '.txt', 'w')
            f.write(self.scenario_name + '\n')
            f.write(self.player.name + '\n')
            f.write(str(round(time.time() - self.win_info.start_time + self.additional_time)) + '\n')
            f.write(str(self.player.money) + '\n')
            f.write(self.current_scene.name + '::' + str(self.current_scene.stage) + '\n')
            for item in self.player.items:
                f.write(item + ';')
            f.write('\n')
            for sc in self.all_scenes:
                f.write(sc.name + '::' + str(sc.stage) + '\n')
            f.close()
            self.win_info.print_window('saved successfully')

    def load_game(self):

        """
        This function load game from save file
        """

        save_number = 0
        done = True
        esc_but = False
        background = pygame.image.load('images/backgrounds/menu_back.jpg')
        saves_list = os.listdir('saves')
        for i in range(len(saves_list)):
            saves_list[i] = saves_list[i][:len(saves_list[i]) - 4]
        while done:
            self.win_info.window.blit(background, (0, 0))
            for i in range(len(saves_list)):
                if i == save_number:
                    self.win_info.window.blit(self.win_info.font.render(saves_list[i], 1, (255, 255, 255)),
                                              (20, self.win_info.font_size * (i + 1)))
                else:
                    self.win_info.window.blit(self.win_info.font.render(saves_list[i], 1, (71, 74, 81)),
                                              (20, self.win_info.font_size * (i + 1)))

            for es in pygame.event.get():
                if es.type == pygame.QUIT:
                    sys.exit()
                if es.type == pygame.KEYDOWN:
                    if es.key == pygame.K_UP:
                        if save_number > 0:
                            save_number -= 1
                    if es.key == pygame.K_DOWN:
                        if save_number < len(saves_list) - 1:
                            save_number += 1
                    if es.key == pygame.K_RETURN:
                        if save_number >= 0:
                            done = False
                    if es.key == pygame.K_ESCAPE:
                        done = False
                        esc_but = True
            pygame.display.update()

        if esc_but:
            return False
        else:
            f = open('saves/' + str(saves_list[save_number]) + '.txt', 'r')
            lines = f.read().split('\n')
            f.close()
            scenario_name = lines[0]
            self.player.name = lines[1]
            self.additional_time = int(lines[2])
            self.player.money = int(lines[3])
            self.player.items = []
            for item in range(len(lines[5].split(';')) - 1):
                self.player.items.append(lines[5].split(';')[item])
            self.all_scenes = []
            for sc in range(6, len(lines) - 1):
                buf_scene = Scene((lines[sc].split('::'))[0], scenario_name)
                buf_scene.stage = int((lines[sc].split('::'))[1])
                self.all_scenes.append(buf_scene)
                if lines[sc] == lines[4]:
                    self.current_scene = buf_scene
            return True
