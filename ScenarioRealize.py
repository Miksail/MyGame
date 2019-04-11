import pygame
import sys
from MenuScreen import InGameMenu


class Scene:

    """
    This file realizes Scenario playback with help of two classes: Scene and Stage

    This class contains information about scenes. All scenes are divided on stages

    name - scene name (first scene in new game must be named as firstScene)
    scenario_name - name of scene's scenario
    stage - stage of scene (must be < max_stages)
    data - information about scene (list with lines from scene file)
    """

    background = pygame.image.load('images/backgrounds/paint.jpg')

    def __init__(self, scene_name, scenario_name):
        self.name = scene_name
        self.scenario_name = scenario_name
        self.stage = 1
        self.data = []
        self.get_data()
        self.max_stages = int(self.data[0])

    def get_data(self):

        """
        Read scene file and get data
        """

        f = open('scenarios/' + self.scenario_name + '/' + self.name + '.txt')
        self.data = f.readlines()
        length = len(self.data)
        for i in range(length):
            self.data[i] = self.data[i][:len(self.data[i]) - 1]
        f.close()

    def render(self, win_info, option, cur_stage, player):

        """
        Render scene text, choices, player status
        """

        length = len(cur_stage.text)
        win_info.window.blit(win_info.font.render(self.name + str(self.stage), 1, (255, 0, 0)), (0, 0))
        # text
        for i in range(0, length):
            win_info.window.blit(win_info.font.render(cur_stage.text[i], 1, (255, 255, 255)),
                                 (20, win_info.font_size * (i + 1)))
        # player stats
        win_info.window.blit(win_info.font.render(player.name, 1, (255, 255, 255)),
                             (820, 450))
        win_info.window.blit(win_info.font.render("money: " + str(player.money), 1, (255, 255, 255)),
                             (820, 450 + win_info.font_size))
        win_info.window.blit(win_info.font.render("press 'I' to open inventory ", 1, (255, 255, 255)),
                             (820, 450 + 3 * win_info.font_size))
        # choices
        for i in range(0, len(cur_stage.choices)):
            if i == option:
                win_info.window.blit(win_info.font.render(cur_stage.choices[i], 1, (255, 255, 255)),
                                     (win_info.window_width / 100, 450 + win_info.font_size * i))
            else:
                win_info.window.blit(win_info.font.render(cur_stage.choices[i], 1, (71, 74, 81)),
                                     (win_info.window_width / 100, 450 + win_info.font_size * i))

    def get_stage(self, player, win_info, game):

        """
        Main function which process players_choice/InGameMenu_call/Player_inventory and do motion

        Returns the scene to be played next
        """

        current_stage = Stage(self)
        option = 0
        done = True
        option_amount = len(current_stage.choices)
        while done:
            win_info.window.blit(self.background, (0, 0))
            self.render(win_info, option, current_stage, player)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_UP:
                        if option > 0:
                            option -= 1
                    if e.key == pygame.K_DOWN:
                        if option < option_amount - 1:
                            option += 1
                    if e.key == pygame.K_RETURN:
                        if option >= 0:
                            done = False
                    if e.type == pygame.KEYDOWN:
                        if e.key == pygame.K_ESCAPE:
                            Menu = InGameMenu(win_info, game)
                            if Menu.menu() == 'ExitFromGame':
                                done = False
                    if e.key == pygame.K_i:
                        player.inventory_render(win_info)

            pygame.display.update()
            pygame.time.delay(10)
        return current_stage.do_motion(option, self, game.all_scenes, game.player, win_info, game)
    

class Stage:

    """
    This class contains information about scene's stages

    text - scenario's text for the stage
    what_to_do_choice - actions that will occur when choosing an item
    choices - character response options
    """

    def __init__(self, scene):
        self.text = self.get_text(scene)
        self.what_todo_choice = []
        self.choices = []
        self.get_choices(scene)

    def get_text(self, scene, res=None):

        """
        Get stage's text
        """

        if res is None:
            res = []
        length = len(scene.data)
        for i in range(0, length):
            if scene.data[i] == 'stagenumber::' + str(scene.stage):
                i += 1
                while scene.data[i].startswith('T::'):
                    res.append(scene.data[i][3:])
                    i += 1
                return res

    def get_choices(self, scene):

        """
        Get stage's response options
        """

        length = len(scene.data)
        for i in range(0, length):
            if scene.data[i] == 'stagenumber::' + str(scene.stage):
                i += 1
                while not scene.data[i].startswith('choice'):
                    i += 1
                while i < length and \
                        scene.data[i].startswith('choice'):
                    res = scene.data[i].split(';')
                    self.choices.append(res[0][9:])
                    if len(res) > 1:
                        self.what_todo_choice.append(res[1].lstrip())
                    i += 1

    def do_motion(self, option, current_scene, all_scenes, player, win_info, game):

        """
        Makes an action corresponding to the selected answer

        Actions:
        1)go to the next scene
        2)change stage of the scene
        3)receive incoming from player data (like combination lock)
        4)change characters money
        5)add/delete items from inventory
        6)end game and come back to the WelcomeMenu
        """

        if len(self.what_todo_choice) <= option:
            return current_scene
        motions = self.what_todo_choice[option].split(' ')
        result = current_scene
        items_to_delete = []
        for i in motions:
            if i.startswith('nextscene'):
                t = True
                for sc in range(len(all_scenes)):
                    if i[11:] == all_scenes[sc].name:
                        result = all_scenes[sc]
                        t = False
                if t:
                    result = Scene(i[11:], current_scene.scenario_name)
                    all_scenes.append(result)

            if i.startswith('nextstage'):
                next_stage_info = i.split('::')
                have_this_scene = False
                for sc in range(len(all_scenes)):
                    if next_stage_info[1] == all_scenes[sc].name:
                        have_this_scene = True
                        if int(next_stage_info[2]) > all_scenes[sc].max_stages:
                            print('exception: stage oversize')
                        else:
                            all_scenes[sc].stage = int(next_stage_info[2])
                if not have_this_scene:
                    new_scene = Scene(next_stage_info[1], current_scene.scenario_name)
                    new_scene.stage = int(next_stage_info[2])
                    result = new_scene
                    all_scenes.append(new_scene)

            if i.startswith('getmoney'):
                if 0 <= player.money + int(i.split('::')[1]):
                    player.money += int(i.split('::')[1])
                else:
                    win_info.print_window("YOU DON'T HAVE ENOUGH MONEY")
                    break

            if i.startswith('getitem'):
                if i.split('::')[1] not in player.items:
                    player.get_item(i.split('::')[1])

            if i.startswith('dropitem'):
                if i.split('::')[1] in player.items:
                    items_to_delete.append(i.split('::')[1])

            if i.startswith('haveitems'):
                if i.split('::')[1] not in player.items:
                    win_info.print_window("you don't have " + i.split('::')[1])
                    break
            if i.startswith('die'):
                player.money = 0
                all_scenes.clear()
                player.items.clear()
                result = Scene('startScene', current_scene.scenario_name)
                win_info.end_scene("YOU DIED", game)
                game.run_game = False
                break

            if i.startswith('end'):
                player.money = 0
                all_scenes.clear()
                player.items.clear()
                result = Scene('startScene', current_scene.scenario_name)
                win_info.end_scene("YOU WON", game)
                game.run_game = False
                break

            if i.split('::')[0].startswith('enter'):
                code = win_info.graphic_input('Enter:')
                if not code == i.split('::')[1]:
                    break

        for i in items_to_delete:
            motions.remove(i)
        return result

