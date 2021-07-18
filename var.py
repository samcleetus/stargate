# These are all of the variables and button instances for Stargate

import pygame
from button import Button
pygame.init()

#images
img = pygame.image.load("./images/night_sky.png")
night_img = pygame.transform.scale(img, (550, 800))
night_img_btn = pygame.transform.scale(img, (69, 58))
img = pygame.image.load("./images/snowy.png")
snowy_img = pygame.transform.scale(img, (550, 800))
snowy_img_btn = pygame.transform.scale(img, (69, 58))
img = pygame.image.load("./images/sky.png")
sky_img = pygame.transform.scale(img, (550, 800))
sky_img_btn = pygame.transform.scale(img, (69, 58))
exit_btn = pygame.image.load("./images/exit_btn.png")
start_btn = pygame.image.load("./images/start_btn.png")
cat_img = pygame.image.load("./images/cat_right.png")
white_cat_img = pygame.image.load("./images/cat_right_white.png")
white_cat = pygame.image.load("./images/cat_left_white.png")
moon_img = pygame.image.load("./images/moon.png")
change_btn = pygame.image.load("./images/change_btn.png")
change_bg_btn = pygame.image.load("./images/change_bg_btn.png")
back_btn = pygame.image.load("./images/back_btn.png")
no_btn = pygame.image.load("./images/no_btn.png")
yes_btn = pygame.image.load("./images/yes_btn.png")
redo_btn = pygame.image.load("./images/redo_btn.png")
img = pygame.image.load("./images/stars.png")
stars_img = pygame.transform.scale(img, (550, 267))
img = pygame.image.load("./images/sad_cat.png")
sad_cat = pygame.transform.scale(img, (190, 205))
platform_img = pygame.image.load("./images/platform.png")
grass_img = pygame.image.load("./images/grass.png")
rain_on_btn = pygame.image.load("./images/rain_on.png")
rain_off_btn = pygame.image.load("./images/rain_off.png")
img = pygame.image.load("./images/bg.png")
main_bg = pygame.transform.scale(img, (550, 800))

#variables
minutes = 0
seconds = 0
milliseconds = 0
jump_ok = True
crimson = (117, 1, 1)
bg_num = 1
play_game = False
main_menu = True
easter_egg = False
choose_character = False
choose_background = False
war_rob = False
exit = False
death = False
egg_found = False
move_complete = False
player_dead = False
char = 1
current_char = 1
weather = 1
current_weather = 1
blue = (0, 0, 255)
white = (255, 255, 255)
maroon = (66, 40, 53)
grey = (104, 104, 105)
jump_count = 0
bg = (118, 163, 204)
screen_scroll = 0
bg_scroll = 0
SCROLL_THRESH = 150
font = pygame.font.SysFont('Bauhaus 93', 100)
font2 = pygame.font.SysFont('Bauhaus 93', 40)
font3 = pygame.font.SysFont('Bauhaus 93', 30)
font4 = pygame.font.SysFont('Bauhaus 93', 70)


#groups
platform_group = pygame.sprite.Group()

#all the fucking buttons
start_btn = Button(35, 350, start_btn, 1)
exit_btn = Button(300, 350, exit_btn, 1)
no_btn = Button(305, 500, no_btn, 1)
yes_btn = Button(135, 500, yes_btn, 1)
change_char_btn = Button(45, 650, change_btn, 1)
change_bg_btn = Button(280, 650, change_bg_btn, 1)
black_cat_btn = Button(110, 300, cat_img, 3)
white_cat_btn = Button(320, 300, white_cat_img, 3)
back_btn = Button(20, 20, back_btn, 1)
sky_btn = Button(50, 200, sky_img_btn, 2)
night_btn = Button(212, 200, night_img_btn, 2)
snowy_btn = Button(370, 200, snowy_img_btn, 2)
easter_egg_btn = Button(223, 64, cat_img, 1)
redo_btn = Button(165, 300, redo_btn, 1)

#Rain buttons
rain_on = Button(212, 500, rain_on_btn, 1)
rain_off = Button(350, 500, rain_off_btn, 1)