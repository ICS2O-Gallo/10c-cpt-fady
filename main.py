import arcade
import math
import random

WIDTH = 900
HEIGHT = 550


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

        #Border checks
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

def bolder_split(bolder):# Bolder splits into smaller pieces
    # Get info
    bolder.kill()
    x = bolder.center_x
    y = bolder.center_y
    scale = bolder.scale

    #Make new boldes
    for i in range(random.randint(2,5)):

        new_scale = scale * 0.5
        #Check to see if bolder is too small
        if new_scale >= 0.05:
            skin = random.choice(bolder_skins)
            bolder = Bolder(skin, new_scale, center_x=x,center_y=y)
            bolder.change_x = random.uniform(-5,5)
            bolder.change_y = random.uniform(-5,5)
            bolder_list.append(bolder)

def setup():
    arcade.open_window(WIDTH, HEIGHT, "Fart Blart The Far Dart")
    arcade.set_background_color(arcade.color.GREEN_YELLOW)
    arcade.schedule(update, 1/80)

    # Frame count
    global frame_count
    frame_count = 0

    # Bolder list
    global bolder_list, bolder_skins
    bolder_skins = [
        'Image Folder/spaceMeteors_001.png',
        'Image Folder/spaceMeteors_002.png',
        'Image Folder/spaceMeteors_003.png',
        'Image Folder/spaceMeteors_004.png'
    ]

    bolder_list = arcade.SpriteList()

    # Initial bolder creation
    for i in range(3):
        skin = random.choice(bolder_skins)
        x = random.randint(100,WIDTH - 100)
        y = random.randint(100, HEIGHT - 100)
        scale = random.uniform(0.15, 0.23)
        bolder = Bolder(skin, scale, center_x = x, center_y = y)
        bolder.change_x = random.uniform(-5,5 + 1)
        bolder.change_y = random.uniform(-5, 5 + 1)
        bolder_list.append(bolder)

    # Player
    global player
    player = Player('Image Folder/Space_ship.png',0.5, center_x= WIDTH / 2, center_y=HEIGHT / 2)
    player.change_x = 0
    player.change_y = 0

    # Movements
    global key_map
    key_map = {'up pressed':False,'down pressed': False, 'right pressed': False, 'left pressed': False}

    # Bullets
    global bullet_list
    bullet_list = arcade.SpriteList()

    # Override arcade window methods
    window = arcade.get_window()
    window.on_draw = on_draw
    window.on_key_press = on_key_press
    window.on_key_release = on_key_release
    window.on_mouse_press = on_mouse_press
    window.on_mouse_motion = on_mouse_motion

    arcade.run()

def update(delta_time):
    global frame_count, game_score
    frame_count += 1
    game_score = frame_count // 20

    if frame_count % 240 == 0:
        x = random.randint(100,WIDTH - 100)
        y = random.randint(100, HEIGHT - 100)
        bolder = Bolder('Image Folder/spaceMeteors_001.png',0.2, center_x=x, center_y=y)
        bolder.change_x = random.uniform(-5,5 + 1)
        bolder.change_y = random.uniform(-5, 5 + 1)
        bolder_list.append(bolder)

    #Check for movement speeds/directions

    max_speed = 4
    if key_map['up pressed'] == True:
        if abs(player.change_y + 0.3) < max_speed:
            player.change_y += .5
    elif key_map['down pressed'] == True:
        if abs(player.change_y - 0.3) < max_speed:
            player.change_y -= .5

    if key_map['right pressed'] == True:
        if abs(player.change_x + 0.3) < max_speed:
            player.change_x += .5
    elif key_map['left pressed'] == True:
        if abs(player.change_x - 0.3) < max_speed:
            player.change_x -= .5

    player.update()

    #Collision between bullet and bolder
    for bullet in bullet_list:
        bullet_bolder_collision = arcade.check_for_collision_with_list(bullet,bolder_list)
        for bolder in bullet_bolder_collision:
            bullet.kill()
            bolder_split(bolder)

    # Collision between player and bolder
    for bolder in bolder_list:
        player_bolder_collision = arcade.check_for_collision(player, bolder)
        if player_bolder_collision == True:
            print('CONTACT')
            #arcade.pause(5)

    bullet_list.update()
    bolder_list.update()

def on_draw():
    arcade.start_render()

    # Score
    arcade.draw_text('Score: {}'.format(game_score),WIDTH - 150, 25,arcade.color.WHITE,22)

    # Player
    player.draw()

    # Bullets
    bullet_list.draw()

    # Bolders
    bolder_list.draw()

def on_key_press(key, modifiers):
    if key == arcade.key.W:
        key_map['up pressed'] = True
    if key == arcade.key.S:
        key_map['down pressed'] = True
    if key == arcade.key.A:
        key_map['left pressed'] = True
    if key == arcade.key.D:
        key_map['right pressed'] = True

def on_key_release(key, modifiers):
    if key == arcade.key.W:
        key_map['up pressed'] = False
    if key == arcade.key.S:
        key_map['down pressed'] = False
    if key == arcade.key.A:
        key_map['left pressed'] = False
    if key == arcade.key.D:
        key_map['right pressed'] = False

def on_mouse_press(x, y, button, modifiers):

    # CREATE BULLET
    mouse_x = x
    mouse_y = y

        # Setup trig ratios
    x_diff = mouse_x - player.center_x
    y_diff = mouse_y - player.center_y
    angle = math.atan2(y_diff,x_diff)
    bullet_angle = math.degrees(angle) - 90

    bullet_speed = 14
    d_x = math.cos(angle) * bullet_speed
    d_y = math.sin(angle) * bullet_speed

        # Finished product
    bullet = Bullet('Image Folder/Bullet.png',0.6, center_x = player.center_x,center_y = player.center_y)
    bullet.change_x = d_x
    bullet.change_y = d_y
    bullet.angle = bullet_angle
    bullet_list.append(bullet)

def on_mouse_motion(x,y,dx,dy):

    #Gether info
    mouse_x = x
    mouse_y = y

        # Setup trig ratios
    x_diff = mouse_x - player.center_x
    y_diff = mouse_y - player.center_y
    angle = math.atan2(y_diff,x_diff)
    new_angle = math.degrees(angle) - 90

    player.angle = new_angle

if __name__ == '__main__':
    setup()
