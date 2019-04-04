import pygame
import sys
import time
import os

pygame.init()
window_width = 1280
window_high = 720

# pygame.mixer.music.set_volume(1)
# pygame.mixer.music.load('Test.mp3')
# pygame.mixer.music.play()

window = pygame.display.set_mode((window_width, window_high))
pygame.display.set_caption('Quest')

pygame.font.init()
font_size = 23
mainFont = pygame.font.Font('fonts/15353.ttf', font_size)


class Game:
    def __init__(self):
        self.scenario_name = 0

    def play(self):
        global current_Scene, scenario_name, run_game, additional_time
        global player, player_name, start_time, run, need_load
        run_menu = True
        run_game = True
        while run_menu:
            Scene.AllScenes = []
            need_load = True
            additional_time = 0
            player = Player('')
            welcome_menu.menu()
            if need_load:
                player_name = graphic_input("ENTER YOUR NAME:")
                player = Player(player_name)
                scenario_name = 'myfirstscenario'
                current_Scene = Scene('startScene', scenario_name)
            # scenario_name = graphic_input("ENTER SCENARIO NAME:")
            run_game = True
            start_time = time.time()
            while run_game:
                current_Scene = current_Scene.get_stage()
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        run = False


class Menu:

    background = pygame.image.load('images/backgrounds/menu_back.jpg')

    def __init__(self, options):
        self.options = options

    def render(self, font, num_option):
        for i in self.options:
            if num_option == i[5]:
                window.blit(font.render(i[2], 1, i[4]), (i[0], i[1]))
            else:
                window.blit(font.render(i[2], 1, i[3]), (i[0], i[1]))

    def menu(self):
        done = True
        font_menu = pygame.font.Font('fonts/15431.otf', 70)
        option = 0
        while done:
            window.blit(self.background, (0, 0))
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
                            save_game()
                        if self.options[option][6] == 'Load':
                            done = load_game()
                        if self.options[option][6] == 'ExitFromGame':
                            global run_game
                            run_game = False
                            return 1
            pygame.display.update()
        return 0


class Player:
    def __init__(self, name):
        self.name = name
        self.money = 0
        self.items = []

    def get_money(self, cash):
        self.money += cash
        if self.money > 100000:
            self.money = 100000

    def get_item(self, item):
        self.items.append(item)


class Stage:
    def __init__(self, scene):
        self.text = self.get_text(scene)
        self.what_todo_choice = []
        self.choices = []
        self.get_choices(scene)

    def get_text(self, scene, res=None):
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

    def do_motion(self, option, current_scene):
        if len(self.what_todo_choice) <= option:
            return current_scene
        motions = self.what_todo_choice[option].split(' ')
        result = current_scene
        items_to_delete = []
        for i in motions:
            if i.startswith('nextscene'):
                t = True
                for sc in range(len(Scene.AllScenes)):
                    if i[11:] == Scene.AllScenes[sc].name:
                        result = Scene.AllScenes[sc]
                        t = False
                if t:
                    result = Scene(i[11:], scenario_name)

            if i.startswith('nextstage'):
                next_stage_info = i.split('::')
                have_this_scene = False
                for sc in range(len(Scene.AllScenes)):
                    if next_stage_info[1] == Scene.AllScenes[sc].name:
                        have_this_scene = True
                        if int(next_stage_info[2]) > Scene.AllScenes[sc].max_stages:
                            print('exception: stage oversize')
                        else:
                            Scene.AllScenes[sc].stage = int(next_stage_info[2])
                if not have_this_scene:
                    new_scene = Scene(next_stage_info[1], scenario_name)
                    new_scene.stage = int(next_stage_info[2])

            if i.startswith('getmoney'):
                if 0 <= player.money + int(i.split('::')[1]):
                    player.money += int(i.split('::')[1])
                else:
                    print_window("YOU DON'T HAVE ENOUGH MONEY")
                    break

            if i.startswith('getitem'):
                if i.split('::')[1] not in player.items:
                    player.get_item(i.split('::')[1])

            if i.startswith('dropitem'):
                if i.split('::')[1] in player.items:
                    items_to_delete.append(i.split('::')[1])

            if i.startswith('haveitems'):
                print(i.split('::')[1])
                if i.split('::')[1] not in player.items:
                    print_window("you don't have " + i.split('::')[1])
                    break
            global start_time
            if i.startswith('die'):
                player.money = 0
                Scene.AllScenes.clear()
                player.items.clear()
                result = Scene('startScene', scenario_name)
                death_scene("YOU DIED")
                start_time = time.time()
                break

            if i.startswith('end'):
                player.money = 0
                Scene.AllScenes.clear()
                player.items.clear()
                result = Scene('startScene', scenario_name)
                death_scene("YOU WON")
                start_time = time.time()
                break

            if i.split('::')[0].startswith('enter'):
                code = graphic_input('Enter:')
                if not code == i.split('::')[1]:
                    break

        for i in items_to_delete:
            motions.remove(i)
        return result


class Scene:
    AllScenes = []
    background = pygame.image.load('images/backgrounds/paint.jpg')

    def __init__(self, scene_name, scenario_name):
        self.name = scene_name
        self.stage = 1
        f = open('scenarios/' + scenario_name + '/' + scene_name + '.txt')
        self.data = f.readlines()
        length = len(self.data)
        for i in range(length):
            self.data[i] = self.data[i][:len(self.data[i]) - 1]
        f.close()
        self.max_stages = int(self.data[0])
        Scene.AllScenes.append(self)

    def render(self, font, option, cur_stage):
        length = len(cur_stage.text)
        window.blit(font.render(self.name + str(self.stage), 1, (255, 0, 0)),
                    (0, 0))
        # text
        for i in range(0, length):
            window.blit(font.render(cur_stage.text[i], 1, (255, 255, 255)),
                        (20, font_size * (i + 1)))
        # player stats
        window.blit(font.render(player_name, 1, (255, 255, 255)),
                    (820, 450))
        window.blit(font.render("money: " + str(player.money), 1, (255, 255, 255)),
                    (820, 450 + font_size))
        window.blit(font.render("press 'I' to open inventory ", 1, (255, 255, 255)),
                    (820, 450 + 3 * font_size))
        # choices
        for i in range(0, len(cur_stage.choices)):
            if i == option:
                window.blit(font.render(cur_stage.choices[i], 1, (255, 255, 255)),
                            (window_width / 100, 450 + font_size * i))
            else:
                window.blit(font.render(cur_stage.choices[i], 1, (71, 74, 81)),
                            (window_width / 100, 450 + font_size * i))

    def get_stage(self):
        if self.stage <= self.max_stages:
            current_stage = Stage(self)
            option = 0
            done = True
            font_stage = mainFont
            option_amount = len(current_stage.choices)
            while done:
                window.blit(self.background, (0, 0))
                self.render(font_stage, option, current_stage)
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
                                if main_menu.menu():
                                    done = False
                        if e.key == pygame.K_i:
                            inventory()

                pygame.display.update()
                pygame.time.delay(10)
            return current_stage.do_motion(option, self)


def print_window(word):
    buf_font = pygame.font.Font('fonts/15353.ttf', 40)
    window.blit(buf_font.render(word, 1, (0, 0, 0)),
                (window_width / 2 - 400, window_high / 2 - 100))
    pygame.display.update()
    pygame.time.delay(1000)


def death_scene(death_sentence):
    death_font = pygame.font.Font('fonts/15353.ttf', 90)
    background = pygame.image.load('images/backgrounds/menu_back.jpg')
    window.blit(background, (0, 0))
    window.blit(death_font.render(death_sentence, 1, (255, 255, 255)),
                (window_width/2 - 200, window_high/2 - 100))
    time_sentence = "your time: " + str(round(time.time() - start_time, 1) + int(additional_time)) + ' sec'
    window.blit(death_font.render(time_sentence, 1, (255, 255, 255)),
                (window_width/2 - 400, window_high/2 + 50))
    pygame.display.update()
    pygame.time.delay(4000)
    global run_game
    run_game = False


def graphic_input(graphic_input_sentence):
    if len(graphic_input_sentence) > 20:
        graphic_input_sentence = "ENTER:"
    background = pygame.image.load('images/backgrounds/menu_back.jpg')
    graphic_input_font = pygame.font.Font('fonts/15353.ttf', 60)
    word = ""
    done = True
    while done:
        window.blit(background, (0, 0))
        pygame.draw.rect(window, (250, 250, 250), (400, 310, 500, 60))
        window.blit(graphic_input_font.render(graphic_input_sentence, 1, (0, 0, 0)), (350, 200))
        window.blit(graphic_input_font.render(word, 1, (0, 0, 0)), (400, 300))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    word = word[:len(word) - 1]
                if event.key == pygame.K_RETURN:
                    done = False
                if event.key != pygame.K_BACKSPACE and event.key != pygame.K_RETURN and\
                        event.key != pygame.K_ESCAPE and len(word) <= 13 and event.key != pygame.K_LSHIFT:
                    if event.mod == pygame.KMOD_LSHIFT:
                        word += str(chr(event.key)).upper()
                    else:
                        word += str(chr(event.key))
        pygame.display.update()
        pygame.time.delay(10)
    return word


def inventory():
    background = pygame.image.load('images/backgrounds/menu_back.jpg')
    window.blit(background, (0, 0))
    inventory_run = True
    while inventory_run:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                inventory_run = False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE or e.key == pygame.K_i:
                    inventory_run = False
        window.blit(mainFont.render("You have: ", 1, (255, 255, 255)),
                    (20, font_size))
        for i in range(0, len(player.items)):
            window.blit(mainFont.render(player.items[i], 1, (255, 255, 255)),
                        (60, (2 + i) * font_size))
        pygame.display.update()


def save_game():
    save_number = 0
    done = True
    esc_but = False
    background = pygame.image.load('images/backgrounds/menu_back.jpg')
    saves_list = os.listdir('saves')
    for i in range(len(saves_list)):
        saves_list[i] = saves_list[i][:len(saves_list[i]) - 4]
    while done:
        window.blit(background, (0, 0))
        for i in range(len(saves_list) + 1):
            if i == len(saves_list):
                save_name = 'NEW SAVE'
            else:
                save_name = saves_list[i]
            if i == save_number:
                window.blit(mainFont.render(save_name, 1, (255, 255, 255)),
                            (20, font_size * (i + 1)))
            else:
                window.blit(mainFont.render(save_name, 1, (71, 74, 81)),
                            (20, font_size * (i + 1)))

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
            save_name = graphic_input('Enter save name')
        else:
            save_name = saves_list[save_number]
        global start_time
        f = open('saves/' + save_name + '.txt', 'w')
        f.write(scenario_name + '\n')
        f.write(player_name + '\n')
        f.write(str(round(time.time() - start_time)) + '\n')
        f.write(str(player.money) + '\n')
        f.write(current_Scene.name + '::' + str(current_Scene.stage) + '\n')
        for item in player.items:
            f.write(item + ';')
        f.write('\n')
        for sc in Scene.AllScenes:
            f.write(sc.name + '::' + str(sc.stage) + '\n')
        f.close()
        print_window('saved successfully')


def load_game():
    save_number = 0
    done = True
    esc_but = False
    background = pygame.image.load('images/backgrounds/menu_back.jpg')
    saves_list = os.listdir('saves')
    for i in range(len(saves_list)):
        saves_list[i] = saves_list[i][:len(saves_list[i]) - 4]
    while done:
        window.blit(background, (0, 0))
        for i in range(len(saves_list)):
            if i == save_number:
                window.blit(mainFont.render(saves_list[i], 1, (255, 255, 255)),
                            (20, font_size * (i + 1)))
            else:
                window.blit(mainFont.render(saves_list[i], 1, (71, 74, 81)),
                            (20, font_size * (i + 1)))

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
        return True
    else:
        f = open('saves/' + str(saves_list[save_number]) + '.txt', 'r')
        lines = f.read().split('\n')
        f.close()
        global scenario_name, player_name, current_Scene, additional_time
        scenario_name = lines[0]
        player_name = lines[1]
        additional_time = lines[2]
        player.money = int(lines[3])
        player.items = []
        for item in range(len(lines[5].split(';')) - 1):
            player.items.append(lines[5].split(';')[item])
        Scene.AllScenes = []
        for sc in range(6, len(lines) - 1):
            buf_scene = Scene((lines[sc].split('::'))[0], scenario_name)
            buf_scene.stage = int((lines[sc].split('::'))[1])
            Scene.AllScenes.append(buf_scene)
            if lines[sc] == lines[4]:
                current_Scene = buf_scene
        global need_load
        need_load = False
        return False


menu_options = [(window_width/2 - 100, window_high / 5 * 1 - 50, 'Continue',
                (71, 74, 81), (255, 255, 255), 0, 'Start'),
                (window_width/2 - 30, window_high / 5 * 2 - 50, 'Save',
                (71, 74, 81), (255, 255, 255), 1, 'Save'),
                (window_width/2 - 30, window_high / 5 * 3 - 50, 'Exit',
                (71, 74, 81), (255, 255, 255), 2, 'ExitFromGame')]
main_menu = Menu(menu_options)

welcome_options = [(window_width/2 - 100, window_high / 5 * 1, 'New Game',
                   (71, 74, 81), (255, 255, 255), 0, 'Start'),
                   (window_width/2 - 30, window_high / 5 * 2, 'Load',
                   (71, 74, 81), (255, 255, 255), 1, 'Load'),
                   (window_width/2 - 30, window_high / 5 * 3, 'Quit',
                   (71, 74, 81), (255, 255, 255), 2, 'Exit')]
welcome_menu = Menu(welcome_options)


game = Game()

game.play()
