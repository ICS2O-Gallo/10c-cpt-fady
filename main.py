import arcade
import math
import random

WIDTH = 840
HEIGHT = 580

class Bullet(arcade.Sprite):
    def update(self):
        # Barrier checks (Image must completely disappear from screen)
        if self.center_x - self.width > WIDTH:
            self.kill()
        elif self.center_x + self.width < 0:
            self.kill()
        elif self.center_y - self.height > HEIGHT:
            self.kill()
        elif self.center_y + self.height < 0:
            self.kill()

        self.center_x += self.change_x
        self.center_y += self.change_y

class Bolder(arcade.Sprite):
    def update(self):
        # Border checks
        if self.center_x - self.width / 2 < 0:
            self.change_x *= -1
        elif self.center_x + self.width / 2 > WIDTH:
            self.change_x *= -1

        elif self.center_y + self.height / 2 > HEIGHT:
            self.change_y *= -1
        elif self.center_y - self.height / 2 < 0:
            self.change_y *= -1

        self.center_y += self.change_y
        self.center_x += self.change_x

class Player(arcade.Sprite):

    def update(self):

        self.center_x += self.change_x
        self.center_y += self.change_y

        # Border checks
        if self.center_x - self.width / 2 < 0:
            self.center_x = self.width / 2
            self.change_x = 0
        elif self.center_x + self.width / 2 > WIDTH:
            self.center_x = WIDTH - self.width / 2
            self.change_x = 0

        if self.center_y + self.height / 2 > HEIGHT:
            self.center_y = HEIGHT - self.height / 2
            self.change_y = 0
        elif self.center_y - self.height / 2 < 0:
            self.center_y = self.height / 2
            self.change_y = 0

def bolder_split(bolder,game_info): # Bolder splits into smaller pieces
    # Get info
    bolder.kill()
    x = bolder.center_x
    y = bolder.center_y
    scale = bolder.scale

    # Make new boldes
    for i in range(random.randint(2,5)):

        new_scale = scale * 0.5
        # Check to see if bolder is too small
        if new_scale >= 0.05:
            skin = random.choice(game_info.bolder_skins)
            bolder = Bolder(skin, new_scale, center_x=x,center_y=y)
            bolder.change_x = random.uniform(-5,5)
            bolder.change_y = random.uniform(-5,5)
            game_info.bolder_list.append(bolder)


class Game():
    def __init__(self,key_map,frame_count,game_score,bolder_list,bolder_skins,player,bullet_list,):
        self.key_map = key_map
        self.frame_count = frame_count
        self.game_score = game_score
        self.bolder_list = bolder_list
        self.bolder_skins = bolder_skins
        self.player = player
        self.bullet_list = bullet_list

    def update(self):
        # Increment score and frames
        self.frame_count += 1
        if self.frame_count % 20 == 0:
            self.game_score += 1

        # Bolder creation
        if self.frame_count % 280 == 0:
            x = random.randint(100, WIDTH - 100)
            y = random.randint(100, HEIGHT - 100)
            bolder = Bolder('Image Folder/spaceMeteors_001.png', 0.2, center_x=x, center_y=y)
            bolder.change_x = random.uniform(-5, 5 + 1)
            bolder.change_y = random.uniform(-5, 5 + 1)
            self.bolder_list.append(bolder)

        # Check for movement speeds/directions
        max_speed = 4
        if self.key_map['up pressed'] == True:
            if abs(self.player.change_y + 0.5) < max_speed:
                self.player.change_y += .5
        elif self.key_map['down pressed'] == True:
            if abs(self.player.change_y - 0.5) < max_speed:
                self.player.change_y -= .5

        if self.key_map['right pressed'] == True:
            if abs(self.player.change_x + 0.5) < max_speed:
                self.player.change_x += .5
        elif self.key_map['left pressed'] == True:
            if abs(self.player.change_x - 0.5) < max_speed:
                self.player.change_x -= .5

        self.player.update()

        # Collision between bullet and bolder
        for bullet in self.bullet_list:
            bullet_bolder_collision = arcade.check_for_collision_with_list(bullet, self.bolder_list)
            for bolder in bullet_bolder_collision:
                bullet.kill()
                bolder_split(bolder,self)

        # Collision between player and bolder
        for bolder in self.bolder_list:
            player_bolder_collision = arcade.check_for_collision(self.player, bolder)
            if player_bolder_collision == True:
                return 'Contact'

        self.bullet_list.update()
        self.bolder_list.update()

    def on_draw(self):
        # Score
        arcade.draw_text('Score: {}'.format(self.game_score), WIDTH - 150, 25, arcade.color.WHITE, 22)

        # Player
        self.player.draw()

        # Bullets
        self.bullet_list.draw()

        # Bolders
        self.bolder_list.draw()

    def on_key_press(self,key):
        if key == arcade.key.W:
            self.key_map['up pressed'] = True
        if key == arcade.key.S:
            self.key_map['down pressed'] = True
        if key == arcade.key.A:
            self.key_map['left pressed'] = True
        if key == arcade.key.D:
            self.key_map['right pressed'] = True

    def on_key_release(self,key):
        if key == arcade.key.W:
            self.key_map['up pressed'] = False
        if key == arcade.key.S:
            self.key_map['down pressed'] = False
        if key == arcade.key.A:
            self.key_map['left pressed'] = False
        if key == arcade.key.D:
            self.key_map['right pressed'] = False

    def on_mouse_press(self,x,y):

        # CREATE BULLET
        mouse_x = x
        mouse_y = y

        # Setup trig ratios
        x_diff = mouse_x - self.player.center_x
        y_diff = mouse_y - self.player.center_y
        angle = math.atan2(y_diff, x_diff)
        bullet_angle = math.degrees(angle) - 90

        bullet_speed = 14
        d_x = math.cos(angle) * bullet_speed
        d_y = math.sin(angle) * bullet_speed

        # Finished product
        bullet = Bullet('Image Folder/Bullet.png', 0.6, center_x=self.player.center_x, center_y=self.player.center_y)
        bullet.change_x = d_x
        bullet.change_y = d_y
        bullet.angle = bullet_angle
        self.bullet_list.append(bullet)

    def on_mouse_motion(self,x, y):

        # Gether info
        mouse_x = x
        mouse_y = y

        # Setup trig ratios
        x_diff = mouse_x - self.player.center_x
        y_diff = mouse_y - self.player.center_y
        angle = math.atan2(y_diff, x_diff)
        new_angle = math.degrees(angle) - 90

        self.player.angle = new_angle

class Button():
    def __init__(self, x, y, w, h, default_color, hover_color, current_color,text):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.default_color = default_color
        self.hover_color = hover_color
        self.current_color = current_color
        self.text = text

    def draw(self):
        arcade.draw_rectangle_filled(self.x, self.y, self.w, self.h, self.current_color)
        arcade.draw_text(self.text,self.x,self.y,arcade.color.BLACK,15,anchor_x='center',anchor_y='center')

    def on_hover(self,mouse_x,mouse_y):
        if self.x - self.w / 2 <= mouse_x <= self.x + self.w / 2 and self.y - self.h / 2 <= mouse_y <= self.y + self.h / 2:
            self.current_color = self.hover_color
        else:
            self.current_color = self.default_color

    def on_click(self,mouse_x,mouse_y):
        if self.x - self.w / 2 <= mouse_x <= self.x + self.w / 2 and self.y - self.h / 2 <= mouse_y <= self.y + self.h / 2:
            return True

        return False

class Menu():
    def __init__(self): # Why do we still need __init__
        global instructions_option,game_option,credits_option
        default_color = (240, 63, 63)
        hover_color = (204, 255, 229)
        current_color = default_color
        instructions_option = Button(WIDTH / 2, HEIGHT / 2 + 100,100,35,
                            default_color, hover_color, current_color, 'Instructions')
        game_option = Button(WIDTH / 2, HEIGHT / 2,100,35,
                            default_color, hover_color, current_color, 'Game')
        credits_option = Button(WIDTH / 2, HEIGHT / 2 - 100,100,35,
                            default_color, hover_color, current_color, 'Credits')

    def draw(self):
        instructions_option.draw()
        game_option.draw()
        credits_option.draw()
        arcade.draw_text('Shoot Space', WIDTH / 2,HEIGHT / 2 + 225,arcade.color.BLACK, 45,
                         align='center', anchor_y='center', anchor_x='center')

    def on_hover(self, mouse_x, mouse_y):
        instructions_option.on_hover(mouse_x, mouse_y)
        game_option.on_hover(mouse_x, mouse_y)
        credits_option.on_hover(mouse_x, mouse_y)

    def on_click(self,mouse_x,mouse_y):

        # Is the click registered onto a box?
        if instructions_option.on_click(mouse_x,mouse_y) == True:
            return 'instructions'
        elif game_option.on_click(mouse_x,mouse_y) == True:
            return 'game'
        elif credits_option.on_click(mouse_x, mouse_y) == True:
            return 'credits'

        # None are clicked
        return False

class Instructions():
    def __init__(self):
        default_color = (240, 63, 63)
        hover_color = (204, 255, 229)
        current_color = default_color

        global back_option
        back_option = Button(75, 50, 75, 50, default_color, hover_color, current_color, 'Back')
    def draw(self):

        # Set up instructions txt
        arcade.draw_text('Instructions', WIDTH/2, HEIGHT/2 + 200, arcade.color.BLACK, 35,
                         anchor_x='center', anchor_y='center', align='center')
        arcade.draw_text('Movement \n\n W,A,S,D to move.', WIDTH/2, HEIGHT/2 + 100, arcade.color.ORANGE, 25,
                         anchor_x='center', anchor_y='center', align='center')
        arcade.draw_text('Shooting \n\n Left click to shoot.', WIDTH/2, HEIGHT/2, arcade.color.RED, 25,
                         anchor_x='center', anchor_y='center', align='center')
        arcade.draw_text('Aiming \n\n Cursor to aim.', WIDTH/2, HEIGHT/2 - 100, arcade.color.GRAPE, 25,
                         anchor_x='center', anchor_y='center', align='center')

        # Set up back button
        back_option.draw()

    def on_click(self,mouse_x,mouse_y):

        # Box click checks
        if back_option.on_click(mouse_x,mouse_y) == True:
            return 'back'

        return False

    def on_hover(self, mouse_x, mouse_y):
        back_option.on_hover(mouse_x, mouse_y)

class Exitscreen():
    def __init__(self):
        default_color = (240, 63, 63)
        hover_color = (204, 255, 229)
        current_color = default_color

        global back_option
        back_option = Button(75, 50, 75, 50, default_color, hover_color, current_color, 'Back')

    def draw(self,score):

        # Print exitscreen txt

        arcade.draw_text('Your Died \n\n Your Score: {}'.format(score), WIDTH / 2, HEIGHT / 2, arcade.color.BLACK,40,
                         align='center', anchor_x='center', anchor_y='center')

        # Set up back button
        back_option.draw()

    def on_click(self, mouse_x, mouse_y):

        # Box click checks
        if back_option.on_click(mouse_x, mouse_y) == True:
            return 'back'

        return False

    def on_hover(self, mouse_x, mouse_y):
        back_option.on_hover(mouse_x, mouse_y)

class Credits():
    def __init__(self):
        default_color = (240, 63, 63)
        hover_color = (204, 255, 229)
        current_color = default_color

        global back_option
        back_option = Button(75, 50, 75, 50, default_color, hover_color, current_color, 'Back')

    def draw(self):

        # Set up credits txt
        arcade.draw_text('This game is so far made entirely by Thomas Wu', WIDTH / 2, HEIGHT / 2, arcade.color.BLACK, 22,
                         anchor_y='center', anchor_x='center', align='center')

        # Set up back button
        back_option.draw()

    def on_click(self,mouse_x,mouse_y):

        # Box click checks
        if back_option.on_click(mouse_x,mouse_y) == True:
            return 'back'

        return False

    def on_hover(self, mouse_x, mouse_y):
        back_option.on_hover(mouse_x, mouse_y)

def update(delta_time):
    global exitscreen_bool, game_bool

    if game_bool == True:
        # Check for contact
        if game.update() == 'Contact':
            exitscreen_bool = True
            game_bool = False

def on_draw():
    arcade.start_render()

    if main_menu_bool == True:
        main_menu.draw()

    elif instructions_bool == True:
        instructions.draw()

    elif credits_bool == True:
        credits.draw()

    elif game_bool == True:
        game.on_draw()

    elif exitscreen_bool == True:
        exitscreen.draw(game.game_score)

def on_key_press(key, modifiers):
    if game_bool == True:
        game.on_key_press(key)

def on_key_release(key, modifiers):
    if game_bool == True:
        game.on_key_release(key)

def on_mouse_press(x, y, button, modifiers):
    global main_menu_bool, instructions_bool, game_bool, credits_bool, exitscreen_bool

    if main_menu_bool == True:
        click_result = main_menu.on_click(x,y)
        if click_result != False:
            main_menu_bool = False

            if click_result == 'instructions':
                instructions_bool = True
            elif click_result == 'game':
                game_bool = True
            else:   # Credits box was clicked
                credits_bool = True

    elif instructions_bool == True:
        click_result = instructions.on_click(x, y)
        if click_result != False:

            # Go back to main menu
            instructions_bool = False
            main_menu_bool = True


    elif credits_bool == True:
        click_result = credits.on_click(x, y)

        if click_result != False:

            # Go back to main menu
            credits_bool = False
            main_menu_bool = True

    elif exitscreen_bool == True:
        click_result = exitscreen.on_click(x, y)

        if click_result != False:

            # Go back to main menu
            exitscreen_bool = False
            main_menu_bool = True

    elif game_bool == True:
        game.on_mouse_press(x, y)

def on_mouse_motion(x,y,dx,dy):
    if main_menu_bool == True:
        main_menu.on_hover(x, y)

    elif instructions_bool == True:
        instructions.on_hover(x,y)

    elif credits_bool == True:
        credits.on_hover(x, y)

    elif game_bool == True:
        game.on_mouse_motion(x, y)

    elif exitscreen_bool == True:
        exitscreen.on_hover(x, y)

def setup():
    arcade.open_window(WIDTH, HEIGHT, "EZ CLAP TOO EASY")
    arcade.set_background_color(arcade.color.GREEN_YELLOW)
    arcade.schedule(update, 1/60)

    # Override arcade window methods
    window = arcade.get_window()
    window.on_draw = on_draw
    window.on_key_press = on_key_press
    window.on_key_release = on_key_release
    window.on_mouse_motion = on_mouse_motion
    window.on_mouse_press = on_mouse_press

    global main_menu
    main_menu = Menu()

    global instructions
    instructions = Instructions()

    global credits
    credits = Credits()

    global exitscreen
    exitscreen = Exitscreen()

    global main_menu_bool,instructions_bool, credits_bool,game_bool, exitscreen_bool
    main_menu_bool = True
    instructions_bool = False
    game_bool = False
    credits_bool = False
    exitscreen_bool = False

    # Info about the actual game play

    # Bolders
    bolder_skins = [
        'Image Folder/spaceMeteors_001.png',
        'Image Folder/spaceMeteors_002.png',
        'Image Folder/spaceMeteors_003.png',
        'Image Folder/spaceMeteors_004.png'
    ]
    bolder_list = arcade.SpriteList()

    # Player and player movement
    player = Player('Image Folder/Space_ship.png',0.40,center_x= WIDTH / 2, center_y=HEIGHT / 2)
    player.change_x = 0
    player.change_y = 0
    key_map = {'up pressed':False,'down pressed': False, 'right pressed': False, 'left pressed': False}

    # Bullets
    bullet_list = arcade.SpriteList()

    # Score data
    frame_count = 0
    game_score = 0

    # Initial bolder creation (default bolders in the game)
    for i in range(3):
        skin = random.choice(bolder_skins)
        x = random.randint(100,WIDTH - 100)
        y = random.randint(100, HEIGHT - 100)
        scale = random.uniform(0.15, 0.23)
        bolder = Bolder(skin, scale, center_x = x, center_y = y)
        bolder.change_x = random.uniform(-5,5 + 1)
        bolder.change_y = random.uniform(-5, 5 + 1)
        bolder_list.append(bolder)

    global game
    game = Game(key_map, frame_count, game_score, bolder_list, bolder_skins, player, bullet_list)

    arcade.run()

if __name__ == '__main__':
    setup()
