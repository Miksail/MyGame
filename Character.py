import pygame
import time
from PYiostream import CinCout


class Player:

    """
    This class contains information about players character

    Items - list of items that are in inventory
    name - characters name
    """

    def __init__(self, player_name):
        self.items = []
        self.name = player_name
        self.money = 0

    def get_money(self, cash):

        """
        Method for change character's money

        It also sets maximum amount of money, which character could care
        """

        self.money += cash
        if self.money > 100000:
            self.money = 100000

    def get_item(self, item):

        """
        Helps to add items in inventory
        """

        self.items.append(item)

    def inventory_render(self, win_info):

        """
        Render inventory window which shows character's items
        """

        background = pygame.image.load('images/backgrounds/menu_back.jpg')
        win_info.window.blit(background, (0, 0))
        inventory_run = True
        while inventory_run:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    inventory_run = False
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE or e.key == pygame.K_i:
                        inventory_run = False
            win_info.window.blit(win_info.font.render("You have: ", 1, (255, 255, 255)),
                                 (20, win_info.font_size))
            for i in range(0, len(self.items)):
                win_info.window.blit(win_info.font.render(self.items[i], 1, (255, 255, 255)),
                                     (60, (2 + i) * win_info.font_size))
            pygame.display.update()
