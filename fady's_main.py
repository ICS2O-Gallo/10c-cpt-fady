import random
import sys
from typing import Any
import arcade
from arcade import ShapeElementList
import random
import math

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

    # Make new bolders
    for i in range(random.randint(2, 5)):

        new_scale = scale * 0.5
        # Check to see if bolder is too small
        if new_scale >= 0.05:
            skin = random.choice(game_info.bolder_skins)
            bolder = Bolder(skin, new_scale, center_x=x,center_y=y)
            bolder.change_x = random.uniform(-5,5)
            bolder.change_y = random.uniform(-5,5)
            game_info.bolder_list.append(bolder)


class Game():
    def __init__(self, key_map, frame_count, game_score, bolder_list, bolder_skins, player, bullet_list):
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

WIDTH = 840
HEIGHT = 580
current_screen = "menu"

ball: ShapeElementList[Any]

ball_x_positions = []
ball_y_positions = []

for _ in range(100):
  x = random.randrange(0, WIDTH)
  y = random.randrange(HEIGHT, HEIGHT * 2)

  ball_x_positions.append(x)
  ball_y_positions.append(y)

BTN_X = 0
BTN_Y = 1
BTN_WIDTH = 2
BTN_HEIGHT = 3
BTN_IS_CLICKED = 4
BTN_COLOR = 5
BTN_CLICKED_COLOR = 6

button1 = [200, 200, 300, 50, False, arcade.color.BLUE, arcade.color.GREEN]
button2 = [200, 100, 300, 50, False, arcade.color.BLUE, arcade.color.GREEN]
button3 = [200, 0, 300, 50, False, arcade.color.BLUE, arcade.color.GREEN]
button4 = [200, 300, 300, 50, False, arcade.color.BLUE, arcade.color.GREEN]

def setup():
    arcade.open_window(WIDTH, HEIGHT, "Lazer Quest")
    arcade.set_background_color(arcade.color.GREEN_YELLOW)
    arcade.schedule(update, 1 / 60)

    window = arcade.get_window()
    window.on_draw = on_draw
    window.on_key_press = on_key_press
    window.on_key_release = on_key_release
    window.on_mouse_press = on_mouse_press
    window.on_mouse_release = on_mouse_release
    window.on_mouse_motion = on_mouse_motion


    # Info about the actual gameplay

    # Player and player movement
    player = Player('Image Folder/Space_ship.png', 0.40, center_x=WIDTH / 2, center_y=HEIGHT / 2)
    player.change_x = 0
    player.change_y = 0
    key_map = {'up pressed': False, 'down pressed': False, 'right pressed': False, 'left pressed': False}

    # Bolders
    bolder_skins = [
        'Image Folder/spaceMeteors_001.png',
        'Image Folder/spaceMeteors_002.png',
        'Image Folder/spaceMeteors_003.png',
        'Image Folder/spaceMeteors_004.png'
    ]

    bolder_list = arcade.SpriteList()

    # Initial bolder creation (default bolders in the game)
    for i in range(3):
        skin = random.choice(bolder_skins)

        # Set up bolder position (Make sure not to spawn on player)
        x_range = [[100, int(WIDTH / 2 - player.width)], [int(WIDTH / 2 + player.width), WIDTH - 100]]
        y_range = [[100, int(HEIGHT / 2 - player.height)],
                   [int(HEIGHT / 2 + player.height), HEIGHT - 100]]
        x = random.randint(*random.choice(x_range))
        y = random.randint(*random.choice(y_range))
        scale = random.uniform(0.15, 0.23)
        bolder = Bolder(skin, scale, center_x=x, center_y=y)
        bolder.change_x = random.uniform(-5, 5 + 1)
        bolder.change_y = random.uniform(-5, 5 + 1)
        bolder_list.append(bolder)

    # Bullets
    bullet_list = arcade.SpriteList()

    # Score data
    frame_count = 0
    game_score = 0

    global game
    game = Game(key_map, frame_count, game_score, bolder_list, bolder_skins, player, bullet_list)

    arcade.run()


def update(delta_time):
  for index in range(len(ball_y_positions)):
      ball_y_positions[index] -= 5

      if ball_y_positions[index] < 0:
          ball_y_positions[index] = 480
          ball_y_positions[index] = random.randrange(HEIGHT, HEIGHT + 50)
          ball_x_positions[index] = random.randrange(0, WIDTH)

  if current_screen == 'play':
    game.update()

def on_mouse_motion(x,y,dx,dy):
    if current_screen == 'play':
        game.on_mouse_motion(x,y)

def on_draw():
  arcade.start_render()
  # Draw in here...

  for x, y in zip(ball_x_positions, ball_y_positions):
      arcade.draw_circle_filled(x, y, 5, arcade.color.COOL_GREY)

  if current_screen == "menu":
      draw_button(button1)
      draw_button(button2)
      draw_button(button3)
      draw_button(button4)

      arcade.draw_text("Play", 300, 305, arcade.color.BLACK, 35)
      arcade.draw_text("Instructions", 240, 205, arcade.color.BLACK, 35)
      arcade.draw_text("Credits", 285, 105, arcade.color.BLACK, 35)
      arcade.draw_text("Exit", 310, 5, arcade.color.BLACK, 35)
      arcade.draw_text('press esc to exit different screens', 10, 10, arcade.color.BLACK, 10)

  if current_screen == "menu":
      arcade.set_background_color(arcade.color.GREEN_YELLOW)
      arcade.draw_text("Main Menu", WIDTH / 3, HEIGHT / 1.2, arcade.color.BLACK, 48)

  elif current_screen == "play":
      arcade.set_background_color(arcade.color.GREEN_YELLOW)
      game.on_draw()

  elif current_screen == "instructions":
      arcade.set_background_color(arcade.color.GREEN_YELLOW)
      arcade.draw_text("Instructions", WIDTH / 3, HEIGHT / 1.2, arcade.color.BLACK, 48)
      arcade.draw_text("You are a spaceship rider surrounded by deadly rocks floating acrosss space. Dodge, shoot, don't let", WIDTH / 40, HEIGHT / 1.5, arcade.color.BLACK)
      arcade.draw_text('your vessel be destroyed while also slowly progressing your way onto a highscore', WIDTH / 40, HEIGHT /1.6, arcade.color.BLACK)

  elif current_screen == "credit":
      arcade.set_background_color(arcade.color.GREEN_YELLOW)
      arcade.draw_text("Credits", WIDTH / 3, HEIGHT / 1.2, arcade.color.BLACK, 48)
      arcade.draw_text("Game coding has been created by Thomas", WIDTH / 40, HEIGHT / 1.5, arcade.color.BLACK, 20)
      arcade.draw_text("Buttons, different screens and all menu screens were coded by Fady", WIDTH / 40, HEIGHT / 1.8, arcade.color.BLACK, 18)

def on_key_press(key, modifiers):
    global current_screen

    if current_screen == 'play':
        game.on_key_press(key)

    if key == arcade.key.ESCAPE:
        current_screen = "menu"


def on_key_release(key, modifiers):
    if current_screen == 'play':
        game.on_key_release(key)


def on_mouse_press(x, y, button, modifiers):

  if current_screen == 'play':
    game.on_mouse_press(x,y)

  # Check if click happened on button1

  if mouse_hover(x, y, button1):
      button1[BTN_IS_CLICKED] = True

  if mouse_hover(x, y, button2):
      button2[BTN_IS_CLICKED] = True

  if mouse_hover(x, y, button3):
      button3[BTN_IS_CLICKED] = True

  if mouse_hover(x, y, button4):
      button4[BTN_IS_CLICKED] = True


def on_mouse_release(x, y, button, modifiers):

  global current_screen

  global instructions

  button1[BTN_IS_CLICKED] = False
  button2[BTN_IS_CLICKED] = False
  button3[BTN_IS_CLICKED] = False
  button4[BTN_IS_CLICKED] = False

  if button4[BTN_IS_CLICKED] == False and mouse_hover(x, y, button4) == True and current_screen == "menu":
      current_screen = "play"

  if button3[BTN_IS_CLICKED] == False and mouse_hover(x, y, button3) == True and current_screen == "menu":
      sys.exit()

  if button1[BTN_IS_CLICKED] == False and mouse_hover(x, y, button1) == True and current_screen == "menu":
      current_screen = "instructions"

  if button2[BTN_IS_CLICKED] == False and mouse_hover(x, y, button2) == True and current_screen == "menu":
      current_screen = "credit"


def mouse_hover(x, y, button) -> bool:

  if (x > button[BTN_X] and x < button[BTN_X] + button[BTN_WIDTH] and
          y > button[BTN_Y] and y < button[BTN_Y] + button[BTN_HEIGHT]):
      return True
  else:
      return False


def draw_button(button):

  if button[BTN_IS_CLICKED]:
      color = button[BTN_CLICKED_COLOR]
  else:
      color = button[BTN_COLOR]

  # Draw button1
  arcade.draw_xywh_rectangle_filled(button[BTN_X],
                                    button[BTN_Y],
                                    button[BTN_WIDTH],
                                    button[BTN_HEIGHT],
                                    color)


if __name__ == '__main__':
  setup()
