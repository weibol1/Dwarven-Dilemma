import pygame
import random
import pygame.joystick

# Resolution and Startup
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1280, 720), pygame.HWSURFACE | pygame.DOUBLEBUF)
pygame.display.set_caption("Dwarven Dilemma")

# image load
shop_light = pygame.image.load("img/light.png").convert_alpha()
shop_light = pygame.transform.scale(shop_light, (48, 48))
shop_light.set_alpha(20)

boulder_1 = boulder_2 = boulder_3 = boulder_4 = boulder_5 = boulder_6 = boulder_7 = pygame.image.load("img/boulder.png").convert_alpha()

minecart = pygame.image.load("img/minecart.png").convert_alpha()
minecart = pygame.transform.scale(minecart, (84, 56))

dwarf = pygame.image.load("img/dwarf.png").convert_alpha()
dwarf = pygame.transform.scale(dwarf, (65, 100))

fullplatform = pygame.image.load("img/platform.png").convert_alpha()
fullplatform = pygame.transform.scale(fullplatform, (500, 60))

singleplatform = pygame.image.load("img/platform-single.png").convert_alpha()
singleplatform = pygame.transform.scale(singleplatform, (129, 60))

pickup_coin = pygame.image.load("img/pickup coin.png").convert_alpha()
pickup_coin = pygame.transform.scale(pickup_coin, (75, 75))

pickup_gem = gem = pygame.image.load("img/gem.png").convert_alpha()
pickup_gem = pygame.transform.scale(pickup_gem, (64, 64))
gem = pygame.transform.scale(gem, (64, 64))
shopgem = pygame.transform.scale(gem, (160, 160))

heart4 = pygame.image.load("img/Heart.png").convert_alpha()

moleman = pygame.image.load("img/moleman-npc.png").convert_alpha()
moleman = pygame.transform.scale(moleman, (118, 123))

hangsign = pygame.image.load("img/hanging-left.png").convert_alpha()
hangsign = pygame.transform.scale(hangsign, (129, 75))

coin = pygame.image.load("img/coin.png").convert_alpha()
coin = pygame.transform.scale(coin, (68, 68))

watch = pygame.image.load("img/watch.png").convert_alpha()
watch = pygame.transform.scale(watch, (150, 150))

shield = shieldshown = pygame.image.load("img/shield.png").convert_alpha()
shield = pygame.transform.scale(shield, (140, 170))
shieldshown = pygame.transform.scale(shieldshown, (56, 68))

interact = pygame.image.load("img/interact.png").convert_alpha()
interact = pygame.transform.scale(interact, (90, 90))

# Buttons
tierbuyempty = pygame.image.load("img/tier buy empty.png").convert_alpha()
tierbuyempty = pygame.transform.scale(tierbuyempty, (160, 276))
tierbuy1 = pygame.image.load("img/tier buy 1.png").convert_alpha()
tierbuy2 = pygame.image.load("img/tier buy 2.png").convert_alpha()
tierbuy3 = pygame.image.load("img/tier buy 3.png").convert_alpha()

coffeebutton = pygame.image.load("img/coffee.png").convert_alpha()
coffeebutton = pygame.transform.scale(coffeebutton, (110, 110))

# shopmenu stuff
speedboots = pygame.image.load("img/speedboots.png").convert_alpha()
speedboots = pygame.transform.scale(speedboots, (160, 125))

shopkeeper1 = pygame.image.load("img/shopkeeper1.png").convert_alpha()
shopkeeper2 = pygame.image.load("img/shopkeeper2.png").convert_alpha()

# dwarf animation
dwarf1 = pygame.image.load("img/dwarfrun1.png").convert_alpha()
dwarf2 = pygame.image.load("img/dwarfrun2.png").convert_alpha()
dwarf3 = pygame.image.load("img/dwarfrun3.png").convert_alpha()
dwarf4 = pygame.image.load("img/dwarfrun4.png").convert_alpha()
dwarf5 = pygame.image.load("img/dwarfrun5.png").convert_alpha()
dwarf6 = pygame.image.load("img/dwarfrun6.png").convert_alpha()
dwarf7 = pygame.image.load("img/dwarfrun7.png").convert_alpha()
dwarf8 = pygame.image.load("img/dwarfrun8.png").convert_alpha()

# Scale factor
scale_factor = 2.5  # Adjust this as needed

# Scale images
dwarf1 = pygame.transform.scale(dwarf1, (dwarf1.get_width() * scale_factor, dwarf1.get_height() * scale_factor))
dwarf2 = pygame.transform.scale(dwarf2, (dwarf2.get_width() * scale_factor, dwarf2.get_height() * scale_factor))
dwarf3 = pygame.transform.scale(dwarf3, (dwarf3.get_width() * scale_factor, dwarf3.get_height() * scale_factor))
dwarf4 = pygame.transform.scale(dwarf4, (dwarf4.get_width() * scale_factor, dwarf4.get_height() * scale_factor))
dwarf5 = pygame.transform.scale(dwarf5, (dwarf5.get_width() * scale_factor, dwarf5.get_height() * scale_factor))
dwarf6 = pygame.transform.scale(dwarf6, (dwarf6.get_width() * scale_factor, dwarf6.get_height() * scale_factor))
dwarf7 = pygame.transform.scale(dwarf7, (dwarf7.get_width() * scale_factor, dwarf7.get_height() * scale_factor))
dwarf8 = pygame.transform.scale(dwarf8, (dwarf8.get_width() * scale_factor, dwarf8.get_height() * scale_factor))

pygame.mixer.music.load('img/dwarves.wav')
pygame.mixer.music.play(-1)
pygame.mixer.music.pause()

# Classes
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, movement_speed=4):
        super().__init__()
        self.movement_speed = movement_speed
        self.x = x
        self.y = y
        self.image = dwarf
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.platform_rect = pygame.Rect(int(x), int(y), 40, 10)
        self.hitbox_rect = pygame.Rect(int(x), int(y), 68, 100)

    def move(self):
        global movement, joystick, is_jumping, falling

        # game borders
        if self.x >= 1215:
            self.x = 1215
        if self.x <= 0:
            self.x = 0
        if game_state.state == 'maingame':
            if self.y >= 600:
                self.y = 600

        if movement:
            self.platform_rect.x = self.x + 15
            self.platform_rect.y = self.y + 93
            self.hitbox_rect.x = self.x
            self.hitbox_rect.y = self.y

            if controllercontrols:
                # Check joystick axes
                joystick_axes = [joystick.get_axis(i) for i in range(joystick.get_numaxes())]
                # Adjust movement based on joystick input
                self.x += int(joystick_axes[0] * self.movement_speed)  # Assuming left stick controls horizontal movement

            if keyboardcontrols:
                if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                    self.x -= self.movement_speed
                if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                    self.x += self.movement_speed

    def draw(self):
        screen.blit(self.image, (self.x, self.y))


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.x = x
        self.y = y
        self.image = image

        # different images
        if self.image == fullplatform:
            self.hitbox = pygame.Rect(x, y, 500, 15)
        if self.image == singleplatform:
            self.hitbox = pygame.Rect(x, y, 129, 15)

    def move(self):
        self.hitbox.x = self.x
        self.hitbox.y = self.y

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

class Boulder(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.x = x
        self.y = y
        self.image = image

        # images for the different boulders
        if self.image == pickup_coin:
            self.hitbox_rect = pygame.Rect(x, y, 75, 75)

        elif self.image == heart4:
            self.hitbox_rect = pygame.Rect(x, y, 60, 56)

        elif self.image == minecart:
            self.hitbox_rect = pygame.Rect(x, y, 84, 56)

        elif self.image == pickup_gem:
            self.hitbox_rect = pygame.Rect(x, y, 64, 64)

        else:
            self.boulderscale = random.randint(100, 150)
            self.hitbox_rect = pygame.Rect(x, y, self.boulderscale, self.boulderscale)

    def move(self):
        self.hitbox_rect.x = self.x
        self.hitbox_rect.y = self.y

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

class Button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self):
        action = False

        # mouse position
        pos = pygame.mouse.get_pos()

        # mouse over button and click
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action


# Functions
def shopkeeper_animation():
    screen.blit(shopkeeper_list[shopframe], (170, 350))
    screen.blit(shopkeeper_list[shopframe], (810, 350))
    screen.blit(shopkeeper_list[shopframe], (170, 30))

def dwarf_animation():
    global dwarf_frame, dwarf_steps, last_update
    # animate dwarf
    current_time = pygame.time.get_ticks()
    if current_time - last_update >= dwarf_cooldown:
        dwarf_frame += 1
        last_update = current_time
        if dwarf_frame >= len(dwarf_images):
            dwarf_frame = 0
    screen.blit(dwarf_images[dwarf_frame], (900, 579))

def show_coins():
    # code for the money going up
    coin_text = coin_font.render(str(coins), False, (255, 255, 255))
    gem_text = coin_font.render(str(gems), False, (255, 255, 255))
    if game_state.state == 'maingame':
        screen.blit(coin_text, (975, -3))
        screen.blit(gem, (230, 8))
        screen.blit(gem_text, (305, -3))

        # music stuff
        if gamestart:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()

    if game_state.state == 'shops':
        screen.blit(coin_text, (1150, -3))
        screen.blit(gem, (900, 8))
        screen.blit(gem_text, (975, -3))


def timer():
    # code for the timer going down
    timer_text = timer_font.render(str(timer_num), False, (255, 255, 255))
    survive_text = timer_font.render("Survive:", False, (255, 255, 255))
    screen.blit(timer_text, (650, -3))
    screen.blit(survive_text, (450, -3))


def show_level():
    # code for level showing on screen
    levelnum_text = timer_font.render(str(level), False, (255, 255, 255))
    level_text = timer_font.render("level:", False, (255, 255, 255))
    screen.blit(levelnum_text, (1200, -3))
    screen.blit(level_text, (1060, -3))


def falsing_stuff():
    global movement, gamestart, coffeeboost, signinteract_shown, shopinteract_shown, is_jumping, coinshowntimer
    global coin_timer, heartshowntimer, gemshowntimer, gemshown, heartshown, coinshown
    movement = gamestart = coffeeboost = signinteract_shown = shopinteract_shown = is_jumping = False
    boulder1.y = boulder2.y = boulder3.y = boulder4.y = boulder5.y = boulder6.y = coin1.y = heart5.y = gem1.y = 1300
    coinshowntimer = coin_timer = heartshowntimer = gemshowntimer = 0
    gemshown = heartshown = coinshown = False


# Gamestate
class GameState:
    def __init__(self):
        self.state = 'mainmenu'

    def mainmenu(self):
        global boulder_7, angle, controllercontrols, keyboardcontrols, joystick, b_timer, y_timer, running
        global a_index, b_index, x_index, y_index, pause_index, button_a, button_b, button_x, button_y, pause_button
        screen.fill((25, 25, 25))
        b_timer += 1
        y_timer += 1

        if controllercontrols:
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
            button_a = joystick.get_button(a_index)  # Replace 0 with the correct index for the A button
            button_b = joystick.get_button(b_index)  # Replace 1 with the correct index for the B button
            button_x = joystick.get_button(x_index)  # Replace 2 with the correct index for the X button
            button_y = joystick.get_button(y_index)  # Replace 3 with the correct index for the Y button
            pause_button = joystick.get_button(pause_index)  # Replace 3 with the correct index for the Y button

        # image load
        startbut = pygame.image.load('img/start button.png').convert()
        exitbut = pygame.image.load('img/exit button.png').convert()
        optionsbut = pygame.image.load('img/options button.png').convert()
        creditsbut = pygame.image.load('img/credits button.png').convert()
        title = pygame.image.load('img/title.png').convert_alpha()

        # image resize
        startbut = pygame.transform.scale(startbut, (270, 114))
        exitbut = pygame.transform.scale(exitbut, (198, 114))
        optionsbut = pygame.transform.scale(optionsbut, (348, 124))
        creditsbut = pygame.transform.scale(creditsbut, (342, 114))
        title = pygame.transform.scale(title, (720, 102))
        boulder_7 = pygame.transform.scale(boulder_7, (276, 276))

        # making the buttons
        start_button = Button(10, 210, startbut, 1)
        credits_button = Button(10, 340, creditsbut, 1)
        options_button = Button(10, 470, optionsbut, 1)
        exit_button = Button(10, 600, exitbut, 1)

        # logic for the rotating image
        angle -= 1
        rotated_image = pygame.transform.rotate(boulder_7, angle)
        rotation_point = (700, 580)
        rotated_rect = rotated_image.get_rect(center=rotation_point)

        if controllercontrols:
            # joystick stuff
            bbutton = pygame.image.load("img/b-button.png").convert_alpha()
            bbutton = pygame.transform.scale(bbutton, (66, 66))
            abutton = pygame.image.load("img/a-button.png").convert_alpha()
            abutton = pygame.transform.scale(abutton, (66, 66))
            xbutton = pygame.image.load("img/x-button.png").convert_alpha()
            xbutton = pygame.transform.scale(xbutton, (66, 66))
            ybutton = pygame.image.load("img/y-button.png").convert_alpha()
            ybutton = pygame.transform.scale(ybutton, (66, 66))
            screen.blit(abutton, (300, 235))
            screen.blit(ybutton, (370, 365))
            screen.blit(xbutton, (370, 500))
            screen.blit(bbutton, (225, 625))

        screen.blit(title, (310, 20))
        screen.blit(rotated_image, rotated_rect.topleft)
        dwarf_animation()
        if start_button.draw() or controllercontrols and button_a == 1:
            self.state = 'introscreen'
        if credits_button.draw() or controllercontrols and button_y == 1 and y_timer >= 20:
            self.state = 'creditsmenu'
            y_timer = 0
        if options_button.draw() or controllercontrols and button_x == 1:
            self.state = 'optionsmenu'
        if exit_button.draw() or controllercontrols and button_b == 1 and b_timer >= 20:
            running = False

    def optionsmenu(self):
        global keyboardcontrols, controllercontrols, joystick, keyboardshown, controllershown
        global b_timer, windowedshown, fullscreenshown, screen, volume, a_index, b_index, x_index, y_index, pause_index
        global button_a, button_b, button_x, button_y, pause_button, noconshown
        screen.fill((25, 25, 25))

        b_timer += 1

        keyboardimg = pygame.image.load("img/keyboardimg.png").convert_alpha()
        controllerimg = pygame.image.load("img/controllerimg.png").convert_alpha()
        keyboardimg = pygame.transform.scale(keyboardimg, (188, 112))
        controllerimg = pygame.transform.scale(controllerimg, (144, 99))

        larrow = rarrow = pygame.image.load("img/left arrow.png").convert_alpha()
        rarrow = pygame.transform.rotate(rarrow, 180)
        larrow = pygame.transform.scale(larrow, (80, 130))
        rarrow = pygame.transform.scale(rarrow, (80, 130))

        apply = pygame.image.load("img/apply button.png").convert_alpha()
        apply = pygame.transform.scale(apply, (198, 84))

        abutton = pygame.image.load("img/a-button.png").convert_alpha()
        abutton = pygame.transform.scale(abutton, (55, 55))
        bbutton = bbutton2 = pygame.image.load("img/b-button.png").convert_alpha()
        bbutton = pygame.transform.scale(bbutton, (55, 55))
        xbutton = pygame.image.load("img/x-button.png").convert_alpha()
        xbutton = pygame.transform.scale(xbutton, (55, 55))

        joysticklr = pygame.image.load("img/joystickLR.png").convert_alpha()
        joysticklr = pygame.transform.scale(joysticklr, (90, 48))
        pauseb = pygame.image.load("img/pauseb.png").convert_alpha()
        pauseb = pygame.transform.scale(pauseb, (64, 36))

        # Code for exiting the options menu
        esc_font = pygame.font.Font('FieldGuide.ttf', 72)
        credit7_text = esc_font.render('Press [ESC] to Exit', True, (255, 255, 255))
        credit7controler_text = esc_font.render('Press     to Exit', True, (255, 255, 255))

        volume_font = pygame.font.Font('FieldGuide.ttf', 72)
        volume_text = volume_font.render(f'Volume: {volume}', True, (255, 255, 255))

        windowed_text = esc_font.render('Windowed', True, (255, 255, 255))
        fullscreen_text = esc_font.render('Fullscreen', True, (255, 255, 255))

        # Main code for the options menu
        left_button1 = Button(20, 50, larrow, 1)
        right_button1 = Button(400, 50, rarrow, 1)
        left_button2 = Button(700, 50, larrow, 1)
        right_button2 = Button(1100, 50, rarrow, 1)
        left_button3 = Button(700, 350, larrow, 1)
        right_button3 = Button(1150, 350, rarrow, 1)
        applybut = Button(840, 200, apply, 1)

        screen.blit(volume_text, (800, 360))

        controls_font = pygame.font.Font('FieldGuide.ttf', 48)
        # controls for keyboard
        controls1key = controls_font.render('[Q] or [ESC] : Exit or Pause', True, (255, 255, 255))
        controls2key = controls_font.render('[A] & [D] : To Move', True, (255, 255, 255))
        controls3key = controls_font.render('[E] : To Interact', True, (255, 255, 255))
        controls4key = controls_font.render('[SPACE], [W] or [UP-ARROW] : To Jump', True, (255, 255, 255))
        # controls for controller
        controls1con = controls_font.render(': Exit', True, (255, 255, 255))
        controls2con = controls_font.render(': To Move', True, (255, 255, 255))
        controls3con = controls_font.render(': To Jump', True, (255, 255, 255))
        controls4con = controls_font.render(': To Interact', True, (255, 255, 255))
        controls5con = controls_font.render(': Pause', True, (255, 255, 255))
        nocon = controls_font.render('No Controller Found!', True, (255, 255, 255))

        if keyboardshown:
            screen.blit(keyboardimg, (150, 60))
            keyboardcontrols = True
            controllercontrols = False
            screen.blit(controls1key, (10, 280))
            screen.blit(controls2key, (10, 350))
            screen.blit(controls3key, (10, 420))
            screen.blit(controls4key, (10, 490))

        if controllershown:
            screen.blit(controllerimg, (180, 70))
            keyboardcontrols = False
            controllercontrols = True
            screen.blit(controls1con, (100, 260))
            screen.blit(controls2con, (100, 330))
            screen.blit(controls3con, (100, 400))
            screen.blit(controls4con, (100, 470))
            screen.blit(controls5con, (100, 540))
            screen.blit(abutton, (25, 405))
            screen.blit(bbutton, (25, 265))
            screen.blit(xbutton, (25, 475))
            screen.blit(joysticklr, (5, 340))
            screen.blit(pauseb, (20, 550))

        if controllercontrols:
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
            if joystick.get_name() == 'PS4 Controller':
                pause_index = 6
            if joystick.get_name() == 'Sony Interactive Entertainment Wireless Controller':
                pause_index = 9
            button_a = joystick.get_button(a_index)  # Replace 0 with the correct index for the A button
            button_b = joystick.get_button(b_index)  # Replace 1 with the correct index for the B button
            button_x = joystick.get_button(x_index)  # Replace 2 with the correct index for the X button
            button_y = joystick.get_button(y_index)  # Replace 3 with the correct index for the Y button
            pause_button = joystick.get_button(pause_index)  # Replace 3 with the correct index for the Y button

        if left_button1.draw():
            controllershown = False
            keyboardshown = True

        if right_button1.draw():
            keyboardshown = False
            if pygame.joystick.get_count() == 1:
                controllershown = True
                noconshown = False
            if pygame.joystick.get_count() == 0:
                noconshown = True
                keyboardshown = True

        if noconshown:
            screen.blit(nocon, (20, 200))

        if left_button2.draw():
            fullscreenshown = False
            windowedshown = True

        if right_button2.draw():
            windowedshown = False
            fullscreenshown = True

        if volume >= 100:
            volume = 100
        if volume <= 0:
            volume = 0

        if left_button3.draw() and b_timer >= 8:
            b_timer = 0
            volume -= 1

        if right_button3.draw() and b_timer >= 8:
            b_timer = 0
            volume += 1

        if windowedshown:
            screen.blit(windowed_text, (810, 70))
        if fullscreenshown:
            screen.blit(fullscreen_text, (790, 70))

        if applybut.draw() and b_timer >= 60:
            b_timer = 0
            if fullscreenshown:
                screen = pygame.display.set_mode((1280, 720), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.FULLSCREEN)
            if windowedshown:
                screen = pygame.display.set_mode((1280, 720), pygame.HWSURFACE | pygame.DOUBLEBUF)

        if controllercontrols:
            screen.blit(credit7controler_text, (350, 630))
            bbutton2 = pygame.transform.scale(bbutton2, (66, 66))
            screen.blit(bbutton2, (540, 650))
        if keyboardcontrols:
            screen.blit(credit7_text, (350, 630))

        if keyboardcontrols and keys[pygame.K_ESCAPE] or controllercontrols and button_b == 1:
            b_timer = 0
            self.state = 'mainmenu'

    def creditsmenu(self):
        global controllercontrols, keyboardcontrols, joystick, b_timer, button_b, a_index, b_index, x_index, y_index, pause_index
        global button_a, button_b, button_x, button_y, pause_button
        screen.fill((25, 25, 25))

        # font & text
        credits_font = pygame.font.Font('FieldGuide.ttf', 45)
        esc_font = pygame.font.Font('FieldGuide.ttf', 72)
        credit1_text = credits_font.render("Dwarven Dilemma", True, (255, 255, 255))
        credit2_text = credits_font.render('Team Members:', True, (255, 255, 255))
        credit3_text = credits_font.render('Lead Programmer and Art Designer: Corey Stuckey', True, (255, 255, 255))
        credit4_text = credits_font.render('Programming Consultant: woogotheboogo', True, (255, 255, 255))
        credit5_text = credits_font.render('Sound Design: Jakeb Ranew', True, (255, 255, 255))
        credit6_text = credits_font.render('Music Design: Crusty Trayson', True, (255, 255, 255))
        credit7_text = credits_font.render('www.ghastlygames.net', True, (255, 255, 255))
        credit9_text = esc_font.render('Press [ESC] to Exit', True, (255, 255, 255))
        credit7controler_text = esc_font.render('Press     to Exit', True, (255, 255, 255))
        screen.blit(credit1_text, (100, 75))
        screen.blit(credit2_text, (100, 150))
        screen.blit(credit3_text, (100, 225))
        screen.blit(credit4_text, (100, 300))
        screen.blit(credit5_text, (100, 375))
        screen.blit(credit6_text, (100, 450))
        screen.blit(credit7_text, (100, 525))
        if keyboardcontrols:
            screen.blit(credit9_text, (400, 625))
        if controllercontrols:
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
            button_a = joystick.get_button(a_index)  # Replace 0 with the correct index for the A button
            button_b = joystick.get_button(b_index)  # Replace 1 with the correct index for the B button
            button_x = joystick.get_button(x_index)  # Replace 2 with the correct index for the X button
            button_y = joystick.get_button(y_index)  # Replace 3 with the correct index for the Y button
            pause_button = joystick.get_button(pause_index)  # Replace 3 with the correct index for the Y button
            bbutton = pygame.image.load("img/b-button.png").convert_alpha()
            bbutton = pygame.transform.scale(bbutton, (66, 66))
            screen.blit(bbutton, (590, 640))
            screen.blit(credit7controler_text, (400, 625))

        if keyboardcontrols and keys[pygame.K_ESCAPE] or controllercontrols and button_b == 1:
            b_timer = 0
            self.state = 'mainmenu'

    def introscreen(self):
        global introy, b_timer, controllercontrols, keyboardcontrols, joystick, text_y_change
        global a_index, b_index, x_index, y_index, pause_index

        b_timer += 1
        screen.fill((25, 25, 25))

        intro_font = pygame.font.Font('FieldGuide.ttf', 30)
        introtext1 = intro_font.render("In the heart of the majestic Dwarven Kingdom of Stoneshield, nestled deep",
                                       True, (255, 255, 255))
        introtext2 = intro_font.render("within the craggy peaks of the Ironspire Mountains, lies a treacherous mine",
                                       True, (255, 255, 255))
        introtext3 = intro_font.render("known as Durak's Delve. This mine, once a thriving source of precious gems",
                                       True, (255, 255, 255))
        introtext4 = intro_font.render("and rare metals, has long been abandoned due to an ancient curse that befell",
                                       True, (255, 255, 255))
        introtext5 = intro_font.render("the dwarven miners.", True, (255, 255, 255))
        introtext6 = intro_font.render("Legend has it that Durak Ironheart, the legendary Dwarven King and master",
                                       True, (255, 255, 255))
        introtext7 = intro_font.render("smith, became obsessed with a mythical gem known as the Heartstone. Said to",
                                       True, (255, 255, 255))
        introtext8 = intro_font.render("possess unimaginable power, Durak believed that harnessing its energy would",
                                       True, (255, 255, 255))
        introtext9 = intro_font.render("bring unparalleled prosperity to Stoneshield. In his pursuit, he ordered the",
                                       True, (255, 255, 255))
        introtext10 = intro_font.render("miners to delve deeper into the earth than ever before, reaching the very",
                                        True, (255, 255, 255))
        introtext11 = intro_font.render("heart of the mountains.", True, (255, 255, 255))
        introtext12 = intro_font.render("However, as the miners unearthed the Heartstone, a malevolent force was", True,
                                        (255, 255, 255))
        introtext13 = intro_font.render("unleashed, cursing the mine and turning it into a perilous labyrinth. The",
                                        True, (255, 255, 255))
        introtext14 = intro_font.render("Heartstone's magic caused the very earth to rebel against the dwarves,", True,
                                        (255, 255, 255))
        introtext15 = intro_font.render("with colossal boulders and rocks becoming animated guardians that now", True,
                                        (255, 255, 255))
        introtext16 = intro_font.render("relentlessly patrol the cursed depths.", True, (255, 255, 255))
        introtext17 = intro_font.render("Enter our protagonist, a brave young dwarf named Thrain Stoneforge,", True,
                                        (255, 255, 255))
        introtext18 = intro_font.render("a descendant of the once-proud Ironheart lineage. Driven by the honor of his",
                                        True, (255, 255, 255))
        introtext19 = intro_font.render("ancestors and the desire to lift the curse that plagues his people,", True,
                                        (255, 255, 255))
        introtext20 = intro_font.render("Thrain embarks on a perilous journey into Durak's Delve.", True,
                                        (255, 255, 255))
        introtext21 = intro_font.render("Armed with his trusty hammer and an ancestral map, Thrain must navigate the",
                                        True, (255, 255, 255))
        introtext22 = intro_font.render("treacherous corridors, solving intricate puzzles and battling malevolent",
                                        True, (255, 255, 255))
        introtext23 = intro_font.render("creatures born from the Heartstone's curse. However, the true test lies in",
                                        True, (255, 255, 255))
        introtext24 = intro_font.render("the constant threat of falling boulders that rain down unpredictably from",
                                        True, (255, 255, 255))
        introtext25 = intro_font.render("the cavern's unstable ceilings.", True, (255, 255, 255))
        introtext26 = intro_font.render("As Thrain descends deeper into the mine, the challenge intensifies. The", True,
                                        (255, 255, 255))
        introtext27 = intro_font.render("Heartstone's influence not only animates the boulders but also distorts", True,
                                        (255, 255, 255))
        introtext28 = intro_font.render("reality itself. Gravity becomes unpredictable, and the very ground beneath",
                                        True, (255, 255, 255))
        introtext29 = intro_font.render("Thrain's feet shifts and tilts. The once-sturdy mine turns into a dynamic",
                                        True, (255, 255, 255))
        introtext30 = intro_font.render("and hazardous environment where quick reflexes and strategic thinking are",
                                        True, (255, 255, 255))
        introtext31 = intro_font.render("the only keys to survival.", True, (255, 255, 255))
        introtext32 = intro_font.render("Thrain must confront the Dwarven Dilemma, the choice between securing the",
                                        True, (255, 255, 255))
        introtext33 = intro_font.render("Heartstone to break the curse or abandoning the pursuit to save his people",
                                        True, (255, 255, 255))
        introtext34 = intro_font.render("from the relentless dangers that lurk within the depths of Durak's Delve.",
                                        True, (255, 255, 255))
        introtext35 = intro_font.render("The fate of Stoneshield rests on Thrain's shoulders as he faces falling", True,
                                        (255, 255, 255))
        introtext36 = intro_font.render("boulders, mystical puzzles, and the dark forces that guard the cursed", True,
                                        (255, 255, 255))
        introtext37 = intro_font.render("Heartstone.", True, (255, 255, 255))

        skiptext1 = intro_font.render("Press      To Skip", True, (255, 255, 255))
        skiptext2 = intro_font.render("Hold      To Speed", True, (255, 255, 255))
        skiptext3 = intro_font.render("[Q]", True, (255, 255, 255))
        skiptext4 = intro_font.render("Hold [SPACE] To Speed", True, (255, 255, 255))

        keys = pygame.key.get_pressed()

        if controllercontrols:
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
            button_a = joystick.get_button(a_index)  # Replace 0 with the correct index for the A button
            button_b = joystick.get_button(b_index)  # Replace 1 with the correct index for the B button
            button_x = joystick.get_button(x_index)  # Replace 2 with the correct index for the X button
            button_y = joystick.get_button(y_index)  # Replace 3 with the correct index for the Y button
            pause_button = joystick.get_button(pause_index)  # Replace 3 with the correct index for the Y button
            bbutton = pygame.image.load("img/b-button.png").convert_alpha()
            bbutton = pygame.transform.scale(bbutton, (44, 44))
            abutton = pygame.image.load("img/a-button.png").convert_alpha()
            abutton = pygame.transform.scale(abutton, (44, 44))
            screen.blit(skiptext2, (1000, 600))
            screen.blit(bbutton, (1075, 400))
            screen.blit(abutton, (1060, 600))

        if keyboardcontrols and keys[pygame.K_SPACE] or controllercontrols and button_a == 1:
            text_y_change = 3
        else:
            text_y_change = 0.4

        if b_timer >= 100:
            if controllercontrols and button_b == 1 or keyboardcontrols and keys[pygame.K_q]:
                introy = -1800
                b_timer += 5

        # 40 pixels between each line and 80 when a paragraph ends
        screen.blit(skiptext1, (1000, 400))
        if keyboardcontrols:
            screen.blit(skiptext3, (1082, 400))
            screen.blit(skiptext4, (1000, 600))

        intro_texts = [introtext1, introtext2, introtext3, introtext4, introtext5,
                       introtext6, introtext7, introtext8, introtext9, introtext10,
                       introtext11, introtext12, introtext13, introtext14, introtext15,
                       introtext16, introtext17, introtext18, introtext19, introtext20,
                       introtext21, introtext22, introtext23, introtext24, introtext25,
                       introtext26, introtext27, introtext28, introtext29, introtext30,
                       introtext31, introtext32, introtext33, introtext34, introtext35,
                       introtext36, introtext37]

        text_y_positions = [introy + i * 40 for i in range(len(intro_texts))]

        for text_surface, y_pos in zip(intro_texts, text_y_positions):
            screen.blit(text_surface, (10, y_pos))
        introy -= text_y_change

        if introy <= -1550:
            self.state = "maingame"
            b_timer = 0

    def shops(self):
        global controllercontrols, keyboardcontrols, is_jumping, jumpcount, falling, last_update, shopframe
        global shop1shown, shop2shown, shop3shown, shop4shown, shopinteract_shown, leave_interactshown, coffeeboost
        global shoptimer, pausemenu, pausemenutimer, bootsbuy_timer, tieremptyshown, tier1shown
        global tier2shown, tier3shown, coins, coffeetier1, coffeetier2, volume, coffeebutton
        global mainleavetimer, movement, stopwatchtier1, stopwatchtier2, shieldtier1, shieldtier2, joystick
        global shieldprot, gems, gemselltimer, watchactive
        screen.fill((25, 25, 25))

        # image loading & resizing
        abutton = pygame.image.load("img/a-button.png").convert_alpha()
        bbutton = pygame.image.load("img/b-button.png").convert_alpha()
        xbutton = pygame.image.load("img/x-button.png").convert_alpha()
        xbutton = pygame.transform.scale(xbutton, (55, 55))
        ybutton = pygame.image.load("img/y-button.png").convert_alpha()

        # music loading
        buysound = pygame.mixer.Sound('img/buysound.wav')
        pygame.mixer.Sound.set_volume(buysound, volume / 100)

        # showing the coins and blitting the lights
        show_coins()
        screen.blit(coin, (1070, 5))

        # calling jumping and platform hitboes
        platforms = [plat1shop, plat3shop, plat4shop, plat5shop, plat6shop]
        for platform in platforms:
            platform.draw()
            platform.move()
        screen.blit(hangsign, (-10, 500))
        shopkeeper_animation()

        # blitting the lights for the different shops
        screen.blit(shop_light, (319, 66))
        screen.blit(shop_light, (319, 388))
        screen.blit(shop_light, (959, 388))

        # blitting the shop signs
        gemshopsign = pygame.image.load("img/gemshopsign.png").convert_alpha()
        gemshopsign = pygame.transform.scale(gemshopsign, (218, 74))

        bootshopsign = pygame.image.load("img/bootshopsign.png").convert_alpha()
        bootshopsign = pygame.transform.scale(bootshopsign, (238, 55))

        watchshopsign = pygame.image.load("img/watchshopsign.png").convert_alpha()
        watchshopsign = pygame.transform.scale(watchshopsign, (238, 55))

        screen.blit(gemshopsign, (400, 100))
        screen.blit(bootshopsign, (385, 425))
        screen.blit(watchshopsign, (1020, 425))

        # blitting the player
        player.draw()
        player.move()

        # the controller shit
        if controllercontrols:
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
            button_a = joystick.get_button(a_index)  # Replace 0 with the correct index for the A button
            button_b = joystick.get_button(b_index)  # Replace 1 with the correct index for the B button
            button_x = joystick.get_button(x_index)  # Replace 2 with the correct index for the X button
            button_y = joystick.get_button(y_index)  # Replace 3 with the correct index for the Y button
            pause_button = joystick.get_button(pause_index)  # Replace 3 with the correct index for the Y button

        # hitbox code for the different shops
        shoprect1 = pygame.Rect(170, 350, 158, 210)
        shoprect2 = pygame.Rect(810, 350, 158, 210)
        shoprect3 = pygame.Rect(170, 30, 158, 210)

        # code for player collision with the different platforms
        for plat in platforms:
            if player.platform_rect.colliderect(plat.hitbox):
                player.y = plat.y - 100

        # jumping for the player
        if not is_jumping:
            if (keyboardcontrols and (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP])) or (controllercontrols and button_a == 1):
                if not shop1shown and not shop2shown and not shop3shown:
                    falling = False
                    is_jumping = True
        else:
            if jumpcount >= -30:
                neg = 1
                if jumpcount < 0:
                    neg = -1
                player.y -= (jumpcount ** 2) * 0.020 * neg
                jumpcount -= 1

            else:
                is_jumping = False
                falling = True
                jumpcount = 30

        # falling and player bounderies
        if falling:
            player.y += 9

        if player.y >= 620:
            player.y = 620

        # Animate shopkeeper
        current_time = pygame.time.get_ticks()
        if current_time - last_update >= shopkeeper_cooldown:
            shopframe += 1
            last_update = current_time
            if shopframe >= len(shopkeeper_list):
                shopframe = 0

        # timers
        mainleavetimer += 1
        shoptimer += 1

        # hitbox collision for the different shop menus
        if (player.hitbox_rect.colliderect(shoprect1) or
                player.hitbox_rect.colliderect(shoprect2) or
                player.hitbox_rect.colliderect(shoprect3)):

            shopinteract_shown = True
        else:
            shopinteract_shown = False

        if shopinteract_shown or leave_interactshown:
            if controllercontrols:
                screen.blit(xbutton, (player.x + 4, player.y - 70))

            if keyboardcontrols:
                screen.blit(interact, (player.x - 15, player.y - 70))

        if not is_jumping and shoptimer >= 20:
            if player.hitbox_rect.colliderect(shoprect1) and shopinteract_shown:
                if keyboardcontrols and keys[pygame.K_e] or controllercontrols and button_x == 1:  # bottom left shop
                    shop1shown = True
                    shoptimer = 0

            if player.hitbox_rect.colliderect(shoprect2) and shopinteract_shown:
                if keyboardcontrols and keys[pygame.K_e] or controllercontrols and button_x == 1:  # bottom left shop
                    shop2shown = True
                    shoptimer = 0

            if player.hitbox_rect.colliderect(shoprect3) and shopinteract_shown:
                if keyboardcontrols and keys[pygame.K_e] or controllercontrols and button_x == 1:  # bottom left shop
                    shop3shown = True
                    shoptimer = 0

        if leave_interactshown and not is_jumping and mainleavetimer >= 10:
            if keyboardcontrols and keys[pygame.K_e] or controllercontrols and button_x == 1:
                player.x = 1100
                player.y = 620
                self.state = 'maingame'
                mainleavetimer = 0

        shopmenu = pygame.image.load("img/shopkeeper blank.png").convert_alpha()
        shopmenu = pygame.transform.scale(shopmenu, (896, 576))

        # Shop items and prices font
        tier_font = pygame.font.Font('FieldGuide.ttf', 30)
        tierdesc_font = pygame.font.Font('FieldGuide.ttf', 30)
        shopitemdesc_font = pygame.font.Font('FieldGuide.ttf', 35)
        price_font = pygame.font.Font('FieldGuide.ttf', 35)
        gem_font = pygame.font.Font('FieldGuide.ttf', 100)

        tier_empty = tier_empty1 = pygame.image.load("img/tier buy coffee empty.png").convert_alpha()
        tier_full = tier_full1 = pygame.image.load("img/tier buy coffee full.png").convert_alpha()
        tier_empty = pygame.transform.scale(tier_empty, (160, 104))
        tier_full = pygame.transform.scale(tier_full, (160, 104))
        tier_empty1 = pygame.transform.scale(tier_empty1, (160, 104))
        tier_full1 = pygame.transform.scale(tier_full1, (160, 104))

        if not shop1shown or not shop2shown or not shop3shown:
            movement = True

        sellbut = pygame.image.load("img/sell button.png").convert_alpha()
        sellbut = pygame.transform.scale(sellbut, (232, 136))

        if shop1shown:
            movement = False
            # text for the shop items
            bootsdesc = shopitemdesc_font.render("Speed Increase", True, (255, 255, 255))
            tier1 = tier_font.render("Tier 1", True, (255, 255, 255))
            tier1desc = tierdesc_font.render("+ 50%", True, (255, 255, 255))
            tier2 = tier_font.render("Tier 2", True, (255, 255, 255))
            tier2desc = tierdesc_font.render("+ 75%", True, (255, 255, 255))
            tier3 = tier_font.render("Tier 3", True, (255, 255, 255))
            tier3desc = tierdesc_font.render("+ 100%", True, (255, 255, 255))
            tier1price = price_font.render("$10", True, (255, 255, 255))
            tier2price = price_font.render("$20", True, (255, 255, 255))
            tier3price = price_font.render("$30", True, (255, 255, 255))

            coffeedesc = shopitemdesc_font.render("Coffee", True, (255, 255, 255))
            coffeetierprice = price_font.render("$5", True, (255, 255, 255))
            coffeetierdesc = price_font.render("+ 250%", True, (255, 255, 255))
            coffeetierdesc2 = price_font.render("Speed", True, (255, 255, 255))
            coffeetierdesc3 = price_font.render("10 Second", True, (255, 255, 255))
            coffeetierdesc4 = price_font.render("Duration", True, (255, 255, 255))
            instuctions1 = tier_font.render("Press       to Close", True, (255, 255, 255))
            instuctions1keyboard = tier_font.render("[Q]", True, (255, 255, 255))

            # buttons
            tier1coffee_button = Button(740, 350, tier_empty, 1)

            # blitting shop items to screen
            screen.blit(shopmenu, (200, 100))
            screen.blit(speedboots, (325, 150))
            screen.blit(bootsdesc, (320, 290))
            screen.blit(tier1, (250, 355))
            screen.blit(tier1desc, (250, 395))
            screen.blit(tier1price, (520, 380))
            screen.blit(tier2, (250, 445))
            screen.blit(tier2desc, (250, 485))
            screen.blit(tier2price, (520, 465))
            screen.blit(tier3, (250, 535))
            screen.blit(tier3desc, (250, 575))
            screen.blit(tier3price, (520, 550))
            screen.blit(coffeedesc, (770, 290))
            screen.blit(coffeetierprice, (910, 380))
            screen.blit(coffeetierdesc, (630, 375))
            screen.blit(coffeetierdesc2, (640, 410))
            screen.blit(coffeetierdesc3, (750, 460))
            screen.blit(coffeetierdesc4, (760, 500))
            is_jumping = False

            if shoptimer >= 20:
                if keyboardcontrols and keys[pygame.K_q] or controllercontrols and button_b == 1:
                    shop1shown = False

            if controllercontrols:
                bbutton = pygame.transform.scale(bbutton, (44, 44))
                abutton = pygame.transform.scale(abutton, (44, 44))
                ybutton = pygame.transform.scale(ybutton, (44, 44))

                screen.blit(bbutton, (900, 605))
                screen.blit(abutton, (800, 380))
                screen.blit(ybutton, (410, 380))

            screen.blit(instuctions1, (820, 605))
            bootsbuy_timer += 1
            if keyboardcontrols:
                screen.blit(instuctions1keyboard, (905, 605))

            tierbuyempty_button = Button(350, 350, tierbuyempty, 1)
            tierbuy1_button = Button(350, 350, tierbuy1, 1)
            tierbuy2_button = Button(350, 350, tierbuy2, 1)

            # code for the shop to buy boots
            if tieremptyshown:
                if tierbuyempty_button.draw() and coins >= 10 and bootsbuy_timer > 30 or controllercontrols and coins >= 10 and button_y == 1 and bootsbuy_timer > 30:
                    coins -= 10
                    tieremptyshown = False
                    tier1shown = True
                    player.movement_speed = 6
                    bootsbuy_timer = 0
                    buysound.play()
            if tier1shown:
                if tierbuy1_button.draw() and coins >= 20 and bootsbuy_timer > 30 or controllercontrols and button_y == 1 and coins >= 20 and bootsbuy_timer > 30:
                    coins -= 20
                    tier1shown = False
                    tier2shown = True
                    player.movement_speed = 7
                    bootsbuy_timer = 0
                    buysound.play()
                if controllercontrols:
                    screen.blit(ybutton, (410, 465))
            if tier2shown:
                if tierbuy2_button.draw() and coins >= 30 and bootsbuy_timer > 30 or controllercontrols and button_y == 1 and coins >= 30 and bootsbuy_timer > 30:
                    coins -= 30
                    tier2shown = False
                    tier3shown = True
                    player.movement_speed = 8
                    bootsbuy_timer = 0
                    buysound.play()
                if controllercontrols:
                    screen.blit(ybutton, (410, 550))
            if tier3shown:
                screen.blit(tierbuy3, (350, 350))
                player.movement_speed = 8

            screen.blit(coffeebutton, (750, 150))
            if coffeetier1:
                if tier1coffee_button.draw() and coins >= 5 or controllercontrols and button_a == 1 and coins >= 5:
                    coffeeboost = coffeetier2 = True
                    coffeetier1 = False
                    coins -= 5
                    buysound.play()

            if coffeetier2:
                screen.blit(tier_full, (740, 350))

            if not shop1shown:
                bootsbuy_timer = 0
                movement = True

        if shop2shown:
            movement = False
            # text for the shop items
            instuctions1 = tier_font.render("Press       to Close", True, (255, 255, 255))
            instuctions1keyboard = tier_font.render("[Q]", True, (255, 255, 255))
            watchdesc = shopitemdesc_font.render("Watch", True, (255, 255, 255))
            watchtierprice = price_font.render("$15", True, (255, 255, 255))
            watchtierdesc = price_font.render("Slows", True, (255, 255, 255))
            watchtierdesc2 = price_font.render("Time", True, (255, 255, 255))
            watchtierdesc3 = price_font.render("10 Second", True, (255, 255, 255))
            watchtierdesc4 = price_font.render("Duration", True, (255, 255, 255))

            shielddesc = shopitemdesc_font.render("Shield", True, (255, 255, 255))
            shieldtierprice = price_font.render("$15", True, (255, 255, 255))
            shieldtierdesc = price_font.render("+1 charge", True, (255, 255, 255))
            shieldtierdesc2 = price_font.render("Lose no health", True, (255, 255, 255))
            shieldtierdesc3 = price_font.render("when damaged", True, (255, 255, 255))

            # buttons
            tier1stopwatch_button = Button(365, 400, tier_empty, 1)
            tier1shield_button = Button(765, 400, tier_empty1, 1)

            # blitting shop items to screen
            screen.blit(shopmenu, (200, 100))
            screen.blit(watch, (370, 180))
            screen.blit(shield, (770, 180))
            screen.blit(shielddesc, (800, 350))
            screen.blit(shieldtierprice, (700, 410))
            screen.blit(shieldtierdesc, (620, 450))
            screen.blit(shieldtierdesc2, (750, 500))
            screen.blit(shieldtierdesc3, (755, 530))
            screen.blit(watchdesc, (405, 350))  # begins the watch text blitting
            screen.blit(watchtierprice, (290, 395))
            screen.blit(watchtierdesc, (280, 425))
            screen.blit(watchtierdesc2, (290, 455))
            screen.blit(watchtierdesc3, (380, 500))
            screen.blit(watchtierdesc4, (390, 530))
            is_jumping = False

            if controllercontrols:
                bbutton = pygame.transform.scale(bbutton, (44, 44))
                abutton = pygame.transform.scale(abutton, (44, 44))
                ybutton = pygame.transform.scale(ybutton, (44, 44))

                screen.blit(bbutton, (900, 605))
                screen.blit(abutton, (820, 430))
                screen.blit(ybutton, (420, 430))

            screen.blit(instuctions1, (820, 605))
            bootsbuy_timer += 1
            if keyboardcontrols:
                screen.blit(instuctions1keyboard, (905, 605))

            # stopwatch buying stuff
            if stopwatchtier1:
                if tier1stopwatch_button.draw() and coins >= 15 or controllercontrols and button_y == 1 and coins >= 15:
                    stopwatchtier2 = True
                    stopwatchtier1 = False
                    coins -= 15
                    buysound.play()

            if stopwatchtier2:
                screen.blit(tier_full1, (365, 400))
                watchactive = True

            # shield buying stuff
            if shieldtier1:
                if tier1shield_button.draw() and coins >= 15 or controllercontrols and button_a == 1 and coins >= 15:
                    shieldtier2 = True
                    shieldtier1 = False
                    coins -= 15
                    buysound.play()

            if shieldtier2:
                screen.blit(tier_full, (765, 400))
                shieldprot = True

            if shoptimer >= 20:
                if keyboardcontrols and keys[pygame.K_q] or controllercontrols and button_b == 1:
                    shop2shown = False

        if shop3shown:
            movement = False
            is_jumping = False
            # text for the shop items
            gemdesc = gem_font.render("$2", True, (255, 255, 255))
            instuctions1 = tier_font.render("Press       to Close", True, (255, 255, 255))
            instuctions1keyboard = tier_font.render("[Q]", True, (255, 255, 255))

            # buttons
            sellbut = Button(535, 325, sellbut, 1)

            # blitting shop items to screen
            screen.blit(shopmenu, (200, 100))
            screen.blit(shopgem, (350, 312))
            screen.blit(gemdesc, (800, 325))

            if shoptimer >= 20:
                if keyboardcontrols and keys[pygame.K_q] or controllercontrols and button_b == 1:
                    shop3shown = False

            if controllercontrols:
                bbutton = pygame.transform.scale(bbutton, (44, 44))
                abutton = pygame.transform.scale(abutton, (88, 88))

                screen.blit(bbutton, (900, 605))
                screen.blit(abutton, (610, 470))

            screen.blit(instuctions1, (820, 605))
            if keyboardcontrols:
                screen.blit(instuctions1keyboard, (905, 605))

            # main code
            gemselltimer += 1
            if sellbut.draw() or controllercontrols and button_a == 1:
                if gems >= 1 and gemselltimer >= 10:
                    gems -= 1
                    coins += 2
                    gemselltimer = 0

        # code for leaving the shops scene
        shopleave = pygame.Rect(0, 595, 100, 125)
        if player.hitbox_rect.colliderect(shopleave):
            leave_interactshown = True
        else:
            leave_interactshown = False

        # pausemenu stuff
        pausemenutimer += 1
        if not is_jumping and pausemenutimer >= 60 and not shop1shown and not shop2shown and not shop3shown:
            if keyboardcontrols and keys[pygame.K_ESCAPE] or controllercontrols and pause_button == 1:
                pausemenu = True

        pausebackground = pygame.image.load("img/pause backg.png").convert()
        pausebackground = pygame.transform.scale(pausebackground, (1280, 720))
        pausebackground.set_alpha(160)

        resumebutton = pygame.image.load("img/resume button.png").convert()
        resumebutton = pygame.transform.scale(resumebutton, (342, 100))

        exitbutton = pygame.image.load("img/exit button.png").convert()
        exitbutton = pygame.transform.scale(exitbutton, (198, 122))

        resumebut = Button(460, 300, resumebutton, 1)
        exitbut = Button(535, 430, exitbutton, 1)

        if pausemenu:
            falsing_stuff()
            pausemenutimer = 0
            screen.blit(pausebackground, (0, 0))

            if controllercontrols:
                bbutton = pygame.transform.scale(bbutton, (66, 66))
                screen.blit(bbutton, (375, 320))
                ybutton = pygame.transform.scale(ybutton, (66, 66))
                screen.blit(ybutton, (450, 460))

            if resumebut.draw():
                pausemenu = False
                movement = True

            if exitbut.draw():
                pausemenu = False
                self.state = 'mainmenu'

        if controllercontrols and pausemenu and button_b == 1:
            pausemenu = False

        if controllercontrols and pausemenu and button_y == 1:
            pausemenu = False
            self.state = 'mainmenu'
            y_timer = 0

    def maingame(self):
        global falling, coins, movement, jumpcount, pause_button, coin1_y_change, coinshown, coinshowntimer
        global is_jumping, last_update, shopframe, signinteract_shown, gamestart, hearts, game_over, coin_timer, hit_timer
        global boulder1_y_change, boulder2_y_change, boulder3_y_change, boulder4_y_change, boulder5_y_change, boulder6_y_change
        global timercounter, timer_num, platmove, level, blankbuttonshown, gamefinishednum, blankbuttonshown2

        # 1.1 Update stuff
        global gameovertimer, b_timer, boosttimer, coffeeboost, xbuttonx
        global caution1shown, caution2shown, caution3shown, caution4shown, caution5shown, caution6shown
        global minecart1timer, minecart1_x_change, minecart1side, minecartleftside, minecartrightside, pausemenu
        global keyboardcontrols, controllercontrols, joystick, a_index, b_index, x_index, y_index, pause_index
        global heart1_y_change, heartshown, heartshowntimer, pausemenutimer, shoptimer, volume, y_timer

        # 1.2 update stuff
        global leave_interactshown, mainleavetimer, shieldprot, shieldtier1, shieldtier2, stopwatchtier1, stopwatchtier2
        global gem1_y_change, gem1shown, gemshowntimer, gemshown, gems, watchtimer, watchactive, coffeetier1, coffeetier2

        # sound load
        coinsound = pygame.mixer.Sound('img/coin_pickup.wav')
        hitsound = pygame.mixer.Sound('img/hit_sound.wav')
        heartsound = pygame.mixer.Sound('img/heart_pickup.wav')
        shieldsound = pygame.mixer.Sound('img/shieldsound.wav')
        gemsound = pygame.mixer.Sound('img/gempickup.wav')
        pygame.mixer.Sound.set_volume(coinsound, volume/100)
        pygame.mixer.Sound.set_volume(hitsound, volume/100)
        pygame.mixer.Sound.set_volume(heartsound, volume / 100)
        pygame.mixer.Sound.set_volume(shieldsound, volume / 100)
        pygame.mixer.Sound.set_volume(gemsound, volume / 100)
        pygame.mixer.music.set_volume(volume / 100)

        # image load
        coin = pygame.image.load("img/coin.png").convert_alpha()
        startsign = pygame.image.load("img/start sign.png").convert_alpha()
        pausebackground = pygame.image.load("img/pause backg.png").convert()
        heart_img = pygame.image.load("img/Heart.png").convert_alpha()
        heart1 = heart2 = heart3 = heart_img
        resumebutton = pygame.image.load("img/resume button.png").convert()
        exitbutton = pygame.image.load("img/exit button.png").convert()
        shopblank = pygame.image.load("img/shopkeeper blank.png").convert_alpha()

        shopbubble1 = shopbubble2 = pygame.image.load("img/shopkeeper bubble.png").convert_alpha()

        caution = pygame.image.load("img/caution.png").convert_alpha()
        caution = pygame.transform.scale(caution, (65, 40))

        track = pygame.image.load("img/minecart-track.png").convert_alpha()
        track = pygame.transform.scale(track, (96, 16))

        # the four buttons for the contoller/joystick mapping
        abutton = pygame.image.load("img/a-button.png").convert_alpha()
        bbutton = pygame.image.load("img/b-button.png").convert_alpha()
        xbutton = pygame.image.load("img/x-button.png").convert_alpha()
        ybutton = pygame.image.load("img/y-button.png").convert_alpha()

        # image resize and other stuff
        coin = pygame.transform.scale(coin, (68, 68))
        startsign = pygame.transform.scale(startsign, (100, 100))
        pausebackground = pygame.transform.scale(pausebackground, (1280, 720))
        pausebackground.set_alpha(160)
        resumebutton = pygame.transform.scale(resumebutton, (342, 100))
        exitbutton = pygame.transform.scale(exitbutton, (198, 122))
        xbutton = pygame.transform.scale(xbutton, (55, 55))
        heart1 = pygame.transform.scale(heart1, (80, 70))
        heart2 = pygame.transform.scale(heart2, (80, 70))
        heart3 = pygame.transform.scale(heart3, (80, 70))
        shopblank = pygame.transform.scale(shopblank, (896, 448))
        shopbubble1 = pygame.transform.scale(shopbubble1, (48, 48))
        shopbubble2 = pygame.transform.scale(shopbubble2, (32, 32))

        # precalling stuff before game
        screen.fill((25, 25, 25))
        screen.blit(coin, (900, 5))
        screen.blit(startsign, (775, 630))
        show_coins()
        show_level()

        if controllercontrols:
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
            button_a = joystick.get_button(a_index)  # Replace 0 with the correct index for the A button
            button_b = joystick.get_button(b_index)  # Replace 1 with the correct index for the B button
            button_x = joystick.get_button(x_index)  # Replace 2 with the correct index for the X button
            button_y = joystick.get_button(y_index)  # Replace 3 with the correct index for the Y button
            pause_button = joystick.get_button(pause_index)  # Replace 3 with the correct index for the Y button

        # calling platforms and player to screen
        platforms = [plat1, plat2, plat3, plat4, plat5, plat6]

        for platform in platforms:
            platform.draw()
            platform.move()

        # Minecart moving and track
        tracky = 709
        track_width = track.get_width()
        for x in range(0, screen.get_width(), track_width):
            screen.blit(track, (x, tracky))

        if minecart1side == 1:
            minecartleftside = True
            minecartrightside = False
        if minecart1side == 2:
            minecartleftside = False
            minecartrightside = True

        if level >= 4 and gamestart:
            minecart1.draw()
            minecart1.move()
            if minecartleftside:
                minecart1.x += minecart1_x_change

            if minecartrightside:
                minecart1.x -= minecart1_x_change

            if minecart1.x >= 1500:
                minecart1_x_change = random.randint(3, 7)
                minecart1side = 2

            if minecart1.x <= -200:
                minecart1_x_change = random.randint(3, 7)
                minecart1side = 1

        if game_over or not gamestart or pausemenu:
            minecart1.x = -400

        # code for leaving the maingame going to shops scene
        if not gamestart:
            screen.blit(hangsign, (-10, 500))
        gameleave = pygame.Rect(0, 595, 100, 125)
        if player.hitbox_rect.colliderect(gameleave):
            leave_interactshown = True
        else:
            leave_interactshown = False

        mainleavetimer += 1

        if leave_interactshown and not is_jumping and mainleavetimer >= 10 and not gamestart:
            if keyboardcontrols and keys[pygame.K_e] or controllercontrols and button_x == 1:
                player.x = 1100
                player.y = 620
                self.state = 'shops'
                mainleavetimer = 0

        if leave_interactshown and not gamestart:
            if controllercontrols:
                screen.blit(xbutton, (player.x + 4, player.y - 70))

            if keyboardcontrols:
                screen.blit(interact, (player.x - 15, player.y - 70))

        # calling the player to the screen
        player.draw()
        player.move()

        # instructions text from the moleman for game start and game end
        instructions_font = pygame.font.Font('FieldGuide.ttf', 26)
        instructions_fontbig = pygame.font.Font('FieldGuide.ttf', 30)
        instuctions1 = instructions_font.render(
            "Welcome to Dwarven Dilemma, where dwarves embark on an exciting journey!", True, (255, 255, 255))
        instuctions2controller = instructions_font.render(
            "Use the Joystick or left thumbstick to move and use the       button to move.", True, (255, 255, 255))
        instuctions2keyboard = instructions_font.render(
            "Use [A] & [D] keys to move left and right, use [SPACE] and [W] keys to jump!", True, (255, 255, 255))
        instuctions4 = instructions_font.render(
            "Collect coins to buy upgrades from me in the shop as levels get tougher.", True, (255, 255, 255))
        instuctions5 = instructions_font.render("Master the controls, gather coins, and dodge boulders to conquer the",
                                                True, (255, 255, 255))
        instuctions6 = instructions_font.render("challenges that await in this enchanting dwarf adventure!", True,
                                                (255, 255, 255))
        instuctions7 = instructions_font.render("Press       to Close", True, (255, 255, 255))

        # instructions for the game getting harder after the 3rd level
        instuctionsf1 = instructions_font.render(
            "As you keep moving forward, you may notice that the levels are getting", True, (255, 255, 255))
        instuctionsf2 = instructions_font.render(
            "harder. Try to Watch out for the minecarts, other dwarves send them this", True, (255, 255, 255))
        instuctionsf3 = instructions_font.render("way all the time when they are bored.", True, (255, 255, 255))
        instuctionsf4 = instructions_font.render("Make sure to visit me in the shop to upgrade and equip yourself",
                                                 True, (255, 255, 255))
        instuctionsf5 = instructions_font.render("for the coming storm, and remember Coffee is half priced!", True,
                                                 (255, 255, 255))
        instuctionsf6 = instructions_font.render("Foward Adventurer! Through The Dwarven Dilemma!", True,
                                                 (255, 255, 255))
        instuctionsf7 = instructions_font.render("Press       to Close", True, (255, 255, 255))
        instuctionsf8keyboard = instructions_fontbig.render("[Q]", True, (255, 255, 255))
        b_timer -= 1

        if blankbuttonshown:  # the instructions given by the moleman
            movement = is_jumping = False
            screen.blit(shopblank, (200, 100))
            screen.blit(moleman, (5, 590))
            screen.blit(shopbubble1, (145, 545))
            screen.blit(shopbubble2, (110, 585))
            screen.blit(instuctions1, (220, 125))

            if controllercontrols:
                screen.blit(instuctions2controller, (220, 165))
                abutton = pygame.transform.scale(abutton, (44, 44))
                bbutton = pygame.transform.scale(bbutton, (44, 44))
                screen.blit(abutton, (835, 160))
                screen.blit(bbutton, (885, 485))

            if keyboardcontrols:
                screen.blit(instuctions2keyboard, (220, 165))
                screen.blit(instuctionsf8keyboard, (890, 487))

            screen.blit(instuctions4, (220, 205))
            screen.blit(instuctions5, (220, 245))
            screen.blit(instuctions6, (220, 285))
            screen.blit(instuctions7, (820, 490))

            if controllercontrols:
                if button_b == 1 and b_timer <= -30:
                    blankbuttonshown = False
            if keyboardcontrols:
                if keys[pygame.K_q] and b_timer <= -30:
                    blankbuttonshown = False

        if blankbuttonshown2:  # the instructions for the 4th level for the game getting harder given by the moleman
            screen.blit(shopblank, (200, 100))
            screen.blit(moleman, (5, 590))
            movement = is_jumping = False
            player.x = 1100
            player.y = 615
            screen.blit(shopbubble1, (145, 545))
            screen.blit(shopbubble2, (110, 585))
            screen.blit(instuctionsf1, (220, 125))
            screen.blit(instuctionsf2, (220, 165))

            if controllercontrols:
                bbutton = pygame.transform.scale(bbutton, (33, 33))
                screen.blit(bbutton, (885, 492))

            if keyboardcontrols:
                screen.blit(instuctionsf8keyboard, (890, 488))

            screen.blit(instuctionsf3, (220, 205))
            screen.blit(instuctionsf4, (220, 245))
            screen.blit(instuctionsf5, (220, 285))
            screen.blit(instuctionsf6, (220, 325))
            screen.blit(instuctionsf7, (820, 490))

        if controllercontrols and button_b == 1 and blankbuttonshown2 or keyboardcontrols and keys[pygame.K_q] and blankbuttonshown2:
            level = 5
            blankbuttonshown2 = False

        if level == 4 and not gamestart:
            blankbuttonshown2 = True

        # boost code
        if boosttimer >= 600:
            coffeeboost = False
            boosttimer = 0
            coffeetier2 = False
            coffeetier1 = True

        if gamestart and coffeeboost:
            boosttimer += 1
            player.movement_speed = 10

        elif tier1shown:
            player.movement_speed = 6

        elif tier2shown:
            player.movement_speed = 7

        elif tier3shown:
            player.movement_speed = 8

        else:
            player.movement_speed = 4

        # interact with the sign to start the game

        # if you move signinteract_shown below shopinteract_shown then it will pop up the shopkeeper screen when you try to start the game

        if signinteract_shown:

            if controllercontrols:
                screen.blit(xbutton, (player.x + 4, player.y - 70))

            if keyboardcontrols:
                screen.blit(interact, (player.x - 15, player.y - 70))

            if keyboardcontrols and keys[pygame.K_e] or controllercontrols and button_x == 1:
                gamestart = True
                minecart1.x = -400

        if 700 <= player.x <= 890 and player.y >= 550 and not pausemenu:
            signinteract_shown = True
        else:
            signinteract_shown = False

        if not blankbuttonshown:
            movement = True

        # falling, platform rects
        if falling:
            player.y += 9

        platforms = [plat1, plat2, plat3, plat4, plat5, plat6]
        for plat in platforms:
            if player.platform_rect.colliderect(plat.hitbox):
                player.y = plat.y - 100

        # jumping for the player
        if not is_jumping:
            if (keyboardcontrols and (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP])) or (controllercontrols and button_a == 1):
                falling = False
                is_jumping = True
        else:
            if jumpcount >= -30:
                neg = 1
                if jumpcount < 0:
                    neg = -1
                player.y -= (jumpcount ** 2) * 0.020 * neg
                jumpcount -= 1

            else:
                is_jumping = False
                falling = True
                jumpcount = 30

        if gamestart:
            # boulder draw, move, and random y change shit
            timer()
            hit_timer += 1
            boulders = [boulder1, boulder2, boulder3, boulder4, boulder5, boulder6]

            for boulder in boulders:
                boulder.draw()
                boulder.move()

            watchtimer += 1
            if not watchactive:
                boulder1.y += boulder1_y_change
                boulder2.y += boulder2_y_change
                boulder3.y += boulder3_y_change
                boulder4.y += boulder4_y_change
                boulder5.y += boulder5_y_change
                boulder6.y += boulder6_y_change

            if watchactive:
                boulder1.y += boulder1_y_change/2
                boulder2.y += boulder2_y_change/2
                boulder3.y += boulder3_y_change/2
                boulder4.y += boulder4_y_change/2
                boulder5.y += boulder5_y_change/2
                boulder6.y += boulder6_y_change/2

            if watchtimer >= 600:
                watchactive = False
                stopwatchtier1 = True
                stopwatchtier2 = False
                watchtimer = 0

            # falsing and coin stuff
            coin_timer += 1
            coinshowntimer += 1
            heartshowntimer += 1
            gemshowntimer += 1
            signinteract_shown = False

            # timer stuff
            timercounter += 1
            if timercounter >= 60:
                timer_num -= 1
                timercounter = 0

            if timer_num == 0:
                level += 1
                gamestart = False
                timer_num = 45  # Number that changes levels timer at top
                boulder1.y = boulder2.y = boulder3.y = boulder4.y = boulder5.y = boulder6.y = coin1.y = heart5.y = gem1.y = 1300
                coinshowntimer = heartshowntimer = gemshowntimer = 0

            # caution signs for the falling boulders
            global boulder1x, boulder2x, boulder3x, boulder4x, boulder5x, boulder6x
            global boulder_scale1, boulder_scale2, boulder_scale3, boulder_scale4, boulder_scale5, boulder_scale6

            if gamestart:

                if caution1shown:
                    screen.blit(caution, (boulder1x + boulder_scale1 / 2 - 33, 100))

                if boulder1.y >= 0:
                    caution1shown = False
    
                if caution2shown:
                    screen.blit(caution, (boulder2x + boulder_scale2 / 2 - 33, 100))

                if boulder2.y >= 0:
                    caution2shown = False
    
                if caution3shown:
                    screen.blit(caution, (boulder3x + boulder_scale3 / 2 - 33, 100))

                if boulder3.y >= 0:
                    caution3shown = False
    
                if caution4shown:
                    screen.blit(caution, (boulder4x + boulder_scale4 / 2 - 33, 100))

                if boulder4.y >= 0:
                    caution4shown = False
    
                if caution5shown:
                    screen.blit(caution, (boulder5x + boulder_scale5 / 2 - 33, 100))

                if boulder5.y >= 0:
                    caution5shown = False
    
                if caution6shown:
                    screen.blit(caution, (boulder6x + boulder_scale6 / 2 - 33, 100))

                if boulder6.y >= 0:
                    caution6shown = False

            # boulder 1
            if boulder1.y >= screen.get_height() + 100:
                caution1shown = True
                boulder1.y = - 400
                boulder1_y_change = random.randint(2, 6)
                boulder1x = random.randint(0, screen.get_width() - 100)
                boulder1.x = boulder1x
                boulder_scale1 = random.randint(100, 150)  # Use a different variable for boulder1 scale
                boulder1.image = pygame.transform.scale(boulder_1, (boulder_scale1, boulder_scale1))
                boulder1.hitbox_rect = pygame.Rect(boulder1.x, boulder1.y, boulder_scale1, boulder_scale1)

            # boulder 2
            if boulder2.y >= screen.get_height() + 100:
                caution2shown = True
                boulder2.y = - 400
                boulder2_y_change = random.randint(2, 6)
                boulder2x = random.randint(0, screen.get_width() - 100)
                boulder2.x = boulder2x
                boulder_scale2 = random.randint(100, 150)
                boulder2.image = pygame.transform.scale(boulder_2, (boulder_scale2, boulder_scale2))
                boulder2.hitbox_rect = pygame.Rect(boulder2.x, boulder2.y, boulder_scale2, boulder_scale2)

            # boulder 3
            if boulder3.y >= screen.get_height() + 100:
                caution3shown = True
                boulder3.y = - 400
                boulder3_y_change = random.randint(2, 7)
                boulder3x = random.randint(0, screen.get_width() - 100)
                boulder3.x = boulder3x
                boulder_scale3 = random.randint(100, 150)
                boulder3.image = pygame.transform.scale(boulder_3, (boulder_scale3, boulder_scale3))
                boulder3.hitbox_rect = pygame.Rect(boulder3.x, boulder3.y, boulder_scale3, boulder_scale3)

            # boulder 4
            if boulder4.y >= screen.get_height() + 100:
                caution4shown = True
                boulder4.y = - 400
                boulder4_y_change = random.randint(2, 7)
                boulder4x = random.randint(0, screen.get_width() - 100)
                boulder4.x = boulder4x
                boulder_scale4 = random.randint(100, 150)
                boulder4.image = pygame.transform.scale(boulder_4, (boulder_scale4, boulder_scale4))
                boulder4.hitbox_rect = pygame.Rect(boulder4.x, boulder4.y, boulder_scale4, boulder_scale4)

            # boulder 5
            if boulder5.y >= screen.get_height() + 100:
                caution5shown = True
                boulder5.y = - 300
                boulder5_y_change = random.randint(2, 7)
                boulder5x = random.randint(0, screen.get_width() - 100)
                boulder5.x = boulder5x
                boulder_scale5 = random.randint(100, 150)
                boulder5.image = pygame.transform.scale(boulder_5, (boulder_scale5, boulder_scale5))
                boulder5.hitbox_rect = pygame.Rect(boulder5.x, boulder5.y, boulder_scale5, boulder_scale5)

            # boulder 6
            if boulder6.y >= screen.get_height() + 100:
                caution6shown = True
                boulder6.y = - 300
                boulder6_y_change = random.randint(2, 7)
                boulder6x = random.randint(0, screen.get_width() - 100)
                boulder6.x = boulder6x
                boulder_scale6 = random.randint(100, 150)
                boulder6.image = pygame.transform.scale(boulder_6, (boulder_scale6, boulder_scale6))
                boulder6.hitbox_rect = pygame.Rect(boulder6.x, boulder6.y, boulder_scale6, boulder_scale6)

            # List of platforms
            platforms = [plat1, plat2, plat3, plat4, plat5, plat6]

            # coin stuff
            if coinshown:
                coin1.draw()
                coin1.move()
                coin1.y += coin1_y_change
                if coin1.y >= screen.get_height() + 100:
                    coin1.y = - 100
                    coin1_y_change = 2
                    coin1x = random.randint(0, screen.get_width() - 100)
                    coin1.x = coin1x

                # Collision detection loop
                for plat in platforms:
                    if coin1.hitbox_rect.colliderect(plat.hitbox):
                        coin1.y = plat.y - 70
                        coin1_y_change = 0

                if player.hitbox_rect.colliderect(coin1.hitbox_rect):
                    coin1.y = 1300
                    coins += 1
                    coinshown = False
                    coinshowntimer = 0
                    coin1x = random.randint(0, screen.get_width() - 100)
                    coin1.x = coin1x
                    coinsound.play()

            if coinshowntimer >= 420 and not coinshown:
                coinshown = True
                coinshowntimer = 0

            # heart stuff
            if heartshown:
                heart5.draw()
                heart5.move()
                heart5.y += heart1_y_change

                if heart5.y >= screen.get_height() + 100:
                    heart5.y = - 100
                    heart1_y_change = 2
                    heart1x = random.randint(0, screen.get_width() - 100)
                    heart5.x = heart1x

                # Collision detection loop
                for plat in platforms:
                    if heart5.hitbox_rect.colliderect(plat.hitbox):
                        heart5.y = plat.y - 56
                        heart1_y_change = 0

                if player.hitbox_rect.colliderect(heart5.hitbox_rect):
                    hearts += 1
                    heartshown = False
                    heart5.y = 1300
                    heart1x = random.randint(0, screen.get_width() - 100)
                    heart5.x = heart1x
                    heartshown = False
                    heartshowntimer = 0
                    heartsound.play()

            if heartshowntimer >= 1800 and not heartshown:
                heartshown = True
                heartshowntimer = 0

            # gem stuff
            if gemshown:
                gem1.draw()
                gem1.move()
                gem1.y += gem1_y_change

                if gem1.y >= screen.get_height() + 100:
                    gem1.y = - 100
                    gem1_y_change = 2
                    gem1x = random.randint(0, screen.get_width() - 100)
                    gem1.x = gem1x

                # Collision detection loop
                for plat in platforms:
                    if gem1.hitbox_rect.colliderect(plat.hitbox):
                        gem1.y = plat.y - 64
                        gem1_y_change = 0

                if player.hitbox_rect.colliderect(gem1.hitbox_rect):
                    gemsound.play()
                    gems += 1
                    gemshown = False
                    gem1.y = 1300
                    gem1x = random.randint(0, screen.get_width() - 100)
                    gem1.x = gem1x
                    gemshown = False
                    gemshowntimer = 0

            if gemshowntimer >= 900 and not gemshown:
                gemshown = True
                gemshowntimer = 0

            # boulder collision with player
            # List of boulders
            boulders = [boulder1, boulder2, boulder3, boulder4, boulder5, boulder6, minecart1]

            if shieldprot:
                screen.blit(shieldshown, (player.x + 5, player.y + 35))
            # Collision detection loop
            for boulder in boulders:
                if player.hitbox_rect.colliderect(boulder.hitbox_rect) and hit_timer >= 60 and shieldprot:
                    shieldsound.play()
                    shieldprot = False
                    hit_timer = 0
                    shieldtier2 = False
                    shieldtier1 = True
                    if controllercontrols:
                        joystick.rumble(1, 1, 100)

                if player.hitbox_rect.colliderect(boulder.hitbox_rect) and hit_timer >= 60 and not shieldprot:
                    hearts -= 1
                    hit_timer = 0
                    hitsound.play()
                    if controllercontrols:
                        joystick.rumble(1, 1, 100)

            # player collisions with the platform
            if coin_timer >= 300:
                coins += 1
                coin_timer = 0

            # levels within the game
            if level >= 2:
                plat1.x += platmove
                if plat1.x >= 200:
                    platmove = -1
                if plat1.x <= 50:
                    platmove = 1
                plat2.x += platmove
                plat3.x -= platmove
                plat4.x -= platmove
                plat5.x += platmove
                plat6.x += platmove

        # hearts and hearts shown

        if hearts <= 0:
            game_over = True

        if heart1shown and hearts >= 1:
            screen.blit(heart1, (10, 10))

        if heart2shown and hearts >= 2:
            screen.blit(heart2, (70, 10))

        if heart3shown and hearts >= 3:
            hearts = 3
            screen.blit(heart3, (130, 10))

        # Pausemenu
        resumebut = Button(460, 300, resumebutton, 1)
        exitbut = Button(535, 430, exitbutton, 1)
        pausemenutimer += 1
        if pausemenu:
            falsing_stuff()
            pausemenutimer = hit_timer = 0
            screen.blit(pausebackground, (0, 0))
            timer_num = 45

            if controllercontrols:
                bbutton = pygame.transform.scale(bbutton, (66, 66))
                screen.blit(bbutton, (375, 320))
                ybutton = pygame.transform.scale(ybutton, (66, 66))
                screen.blit(ybutton, (450, 460))

            if resumebut.draw():
                pausemenu = False
                movement = True

            if exitbut.draw():
                pausemenu = False
                self.state = 'mainmenu'

        if not is_jumping and not blankbuttonshown and not blankbuttonshown2 and pausemenutimer >= 60 and not game_over:
            if keyboardcontrols and keys[pygame.K_ESCAPE] or controllercontrols and pause_button == 1:
                pausemenu = True

        if controllercontrols and pausemenu and button_b == 1:
            pausemenu = False

        if controllercontrols and pausemenu and button_y == 1:
            pausemenu = False
            self.state = 'mainmenu'
            y_timer = 0

        # game over, and restart
        game_over_font = pygame.font.Font('FieldGuide.ttf', 80)
        game_over_text = game_over_font.render("Game Over", True, (255, 255, 255))
        if game_over:
            falsing_stuff()
            game_over_on_screen = True

            if game_over_on_screen:
                screen.blit(game_over_text, (500, 300))
            gameovertimer += 1
        if gameovertimer >= 300:
            player.x = 1100
            player.y = 600
            hearts = 3
            game_over = gamestart = False
            movement = True
            timer_num = 45
            timercounter = coins = gameovertimer = gems = 0

    def state_manager(self):
        state_methods = {
            'mainmenu': self.mainmenu,
            'creditsmenu': self.creditsmenu,
            'optionsmenu': self.optionsmenu,
            'introscreen': self.introscreen,
            'maingame': self.maingame,
            'shops': self.shops,
        }

        method = state_methods.get(self.state)
        if method:
            method()


# shopkeeper list and animation
shopkeeper_list = [shopkeeper1, shopkeeper2]
shopframe = 0
shopkeeper_steps = 2
shopkeeper_cooldown = 1500
last_update = pygame.time.get_ticks()
# dwarf list and animation
dwarf_images = [dwarf1, dwarf2, dwarf3, dwarf4, dwarf5, dwarf6, dwarf7, dwarf8]
dwarf_frame = 0
dwarf_steps = 8
dwarf_cooldown = 50

# Coins, gems and Timer
coins = 0  # starting coins the person has
gems = 0  # starting gems the person has
coin_font = pygame.font.Font('FieldGuide.ttf', 60)
timercounter = 0
timer_num = 45  # changes the number at the top that the player has to survive when the game starts
timer_font = pygame.font.Font('FieldGuide.ttf', 60)

# Shopmenu
shopinteract_shown = False
tieremptyshown = True
tier1shown = tier2shown = tier3shown = False

bootsbuy_timer = 0
angle = 0

# classes and groups
player = Player(1100, 620)
# platforms for maingame
plat1 = Platform(150, 225, fullplatform)  # top left
plat2 = Platform(779, 225, fullplatform)  # top right
plat3 = Platform(0, 385, fullplatform)  # middle left
plat4 = Platform(650, 385, fullplatform)  # middle right
plat5 = Platform(150, 545, fullplatform)  # bottom left
plat6 = Platform(779, 545, fullplatform)  # bottom right
# platforms for the shop
plat1shop = Platform(150, 240, fullplatform)  # top left
plat2shop = Platform(779, 240, fullplatform)  # top right
plat3shop = Platform(0, 400, singleplatform)  # middle left
plat4shop = Platform(650, 400, singleplatform)  # middle left
plat5shop = Platform(150, 560, fullplatform)  # bottom left
plat6shop = Platform(779, 560, fullplatform)  # bottom right

# random integers for the boulders
boulder1_y_change = random.randint(6, 14)  # random y value for falling
boulder2_y_change = random.randint(6, 14)
boulder3_y_change = random.randint(6, 14)
boulder4_y_change = random.randint(6, 14)
boulder5_y_change = random.randint(6, 14)
boulder6_y_change = random.randint(6, 14)
boulder1x = random.randint(0, screen.get_width() - 100)  # random x coords
boulder2x = random.randint(0, screen.get_width() - 100)
boulder3x = random.randint(0, screen.get_width() - 100)
boulder4x = random.randint(0, screen.get_width() - 100)
boulder5x = random.randint(0, screen.get_width() - 100)
boulder6x = random.randint(0, screen.get_width() - 100)

# boulders
boulder1 = Boulder(boulder1x, 1300, boulder_1)
boulder2 = Boulder(boulder2x, 1300, boulder_2)
boulder3 = Boulder(boulder3x, 1300, boulder_3)
boulder4 = Boulder(boulder4x, 1300, boulder_4)
boulder5 = Boulder(boulder5x, 1300, boulder_5)
boulder6 = Boulder(boulder6x, 1300, boulder_6)

minecart1 = Boulder(-100, 660, minecart)

# coin stuff & heart stuff & gem stuff
coin1_y_change = random.randint(4, 12)
coin1x = random.randint(0, screen.get_width() - 100)
coin1 = Boulder(coin1x, 1300, pickup_coin)
coinshown = heartshown = gemshown = False
coinshowntimer = heartshowntimer = gemshowntimer = gemselltimer = 0
heart1_y_change = random.randint(4, 12)
heart1x = random.randint(0, screen.get_width() - 100)
heart5 = Boulder(heart1x, 1300, heart4)
gem1_y_change = random.randint(4, 12)
gem1x = random.randint(0, screen.get_width() - 100)
gem1 = Boulder(gem1x, 1300, pickup_gem)

# References for main game
FPS = 60
movement = blankbuttonshown = True
gamestart = signinteract_shown = game_over_on_screen = game_over = blankbuttonshown2 = pausemenu = False
game_state = GameState()
clock = pygame.time.Clock()
coin_timer = gamefinishednum = creditstimer = exittimer = hit_timer = pausemenutimer = shoptimer = 0
platmove = level = 1  # changes the starting level
introy = 720

# caution and random stuff
b_timer = gameovertimer = boosttimer = 0
xbuttonx = 380
caution1shown = caution2shown = caution3shown = caution4shown = caution5shown = caution6shown = False

# minecart stuff
minecart1_x_change = random.randint(2, 7)
minecart1side = random.randint(1, 2)
minecartleftside = minecartrightside = fullscreenshown = False
# player jump, collision, and hearts
jumpcount = 30
is_jumping = False
heart1shown = heart2shown = heart3shown = falling = windowedshown = True
hearts = 3
volume = 50

# controller
keyboardcontrols = True
keyboardshown = True
controllercontrols = False
controllershown = False
a_index = 0
b_index = 1
x_index = 2
y_index = 3
pause_index = 7
y_timer = 0
noconshown = False

# shops stuff
shop1shown = False
shop2shown = False
shop3shown = False
shop4shown = False
# coffee stuff
coffeeboost = coffeetier2 = False
coffeetier1 = True
# stopwatch stuff
stopwatchtier1 = True
stopwatchtier2 = False
watchactive = False
watchtimer = 0
# shield stuff
shieldtier1 = True
shieldtier2 = False
shieldprot = False

# interactions between the different scenes
leave_interactshown = False
interact_timer = 0
mainleavetimer = 0

# Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    clock.tick(FPS)
    game_state.state_manager()
    keys = pygame.key.get_pressed()

    pygame.display.flip()
pygame.quit()
