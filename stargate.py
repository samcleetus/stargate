from math import floor
import pygame
from pygame.locals import *
import time
from pygame import mixer
import pickle
from os import X_OK, path
import random
from button import Button
from var import *
from rain import Rain, rainfall_main

pygame.init()
pygame.key.set_repeat(500, 30)
clock = pygame.time.Clock()
score_clock = pygame.time.Clock()
fps = 50

SCREEN_WIDTH = 550
SCREEN_HEIGHT = 800

icon = pygame.image.load("./images/cat_right.png")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Stargate - by Sam Cleetus')
pygame.display.set_icon(icon)


#defs
def reset():
    global jump_count
    global move_complete

    player.alive = True
    jump_count = 0
    move_complete = False

def draw_bg():
    height = bg_img.get_height()
    for y in range(5):
        screen.blit(bg_img, (0, (y * height)))

def draw_floor(player):
    if jump_count == 0:
        floor = pygame.draw.rect(screen, grey, pygame.Rect(0, 770, 550, 30))
        if floor.colliderect(player.rect):
            if player.rect.bottom > 770:
                player.rect.bottom = 770

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#classes
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, char):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char = char
        self.image = pygame.image.load("./images/cat_right.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False

    def update(self):
        global jump_ok
        global jump_count
        global death
        global main_menu
        global play_game
        screen_scroll = 0
        col_thresh = 20

        dx = 0
        dy = 0

        #get key presses
        key = pygame.key.get_pressed()

        #jumping
        if key[pygame.K_w] and jump_ok == True:
            self.vel_y = -25
            self.jumped = True
            jump_count += 1
            jump_ok = False

        #if key[pygame.K_w] == False:
            #self.jumped = False
    

        #moving sideways and such
        if key[pygame.K_a]:
            dx -= 5
            if self.char == 1:
                self.image = pygame.image.load("./images/cat_left.png")
            if self.char == 2:
                self.image = pygame.image.load("./images/cat_left_white.png")

        if key[pygame.K_d]:
            dx += 5
            if self.char == 1:
                self.image = pygame.image.load("./images/cat_right.png")
            if self.char == 2:
                self.image = pygame.image.load("./images/cat_right_white.png")

        #add gravity
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        #collision
        if jump_count != 0:
            for platform in platform_group:
                #collision in x direction
                if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                #collision in y direction
                if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    #check if below platform
                    if abs((self.rect.top + dy) - platform.rect.bottom) < col_thresh:
                        self.vel_y = 0
                        dy = platform.rect.bottom - self.rect.top

                    #check if above platform
                    elif abs((self.rect.bottom + dy) - platform.rect.top) < col_thresh:
                        self.rect.bottom = platform.rect.top
                        dy = 0
                        jump_ok = True

                    #move sideways with the platform
                    self.rect.x += platform.move_direction



        #update player coordinates
        self.rect.x += dx
        self.rect.y += dy

        #update scroll
        if self.rect.top < SCROLL_THRESH:
            self.rect.y -= dy
            screen_scroll = -dy


        #draw player
        screen.blit(self.image, self.rect)

        return screen_scroll, death


    def move_unto_screen(self):
        move_complete = False
        dx = 0
        if self.rect.left < 100:
            dx += 3
            self.rect.x += dx
        if self.rect.left >= 100:
            move_complete = True

        return move_complete


    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    #def update(self):
        #self.rect.move_ip(-self.speed, 0)
        #if self.rect.right < 0:
            #self.kill()


    def draw(self):
        self.rect.y += screen_scroll
        screen.blit(self.image, self.rect)

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = grass_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100)
        self.rect.y = random.randint(0, 800)
        #self.rect.x = x
        #self.rect.y = y
        self.speed = random.randint(1, 4)
        self.move_counter = 0
        self.move_direction = -self.speed
        #self.move_x = move_x
        #self.move_y = move_y

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

    def draw(self):
        self.rect.y += screen_scroll
        screen.blit(self.image, self.rect)


player = Player(-70, 790, char)
#cloud = Cloud(SCREEN_HEIGHT, SCREEN_WIDTH)
#cloud_group.add(cloud)
platform = Platform(200, 400)
platform_group.add(platform)

#cutom event to add more clouds
#EVENT_ADD_CLOUD = pygame.USEREVENT + 1; pygame.time.set_timer(EVENT_ADD_CLOUD, 200)
EVENT_ADD_PLATFORM = pygame.USEREVENT + 1; pygame.time.set_timer(EVENT_ADD_PLATFORM, 1000)


run = True
while run:
    clock.tick(fps)

    #background
    if bg_num == 1:
        bg_img = night_img
    elif bg_num == 2:
        bg_img = sky_img
    elif bg_num == 3:
        bg_img = snowy_img

    #main menu
    if main_menu == True and player_dead == False:
        screen.blit(main_bg, (0, 0))
        screen.blit(stars_img, (0, 0))
        draw_text('STARGATE', font, white, 95, 100)

        screen.blit(moon_img, (20, 20))
        if easter_egg_btn.draw(screen):
            easter_egg = True
        #screen.blit(cat_img, (223, 64))
        screen.blit(white_cat, (400, 610))

        if start_btn.draw(screen):
            main_menu = False
            play_game = True
        if change_char_btn.draw(screen):
            choose_character = True
            main_menu = False
        if change_bg_btn.draw(screen):
            choose_background = True
            main_menu = False

        #exit button
        if exit_btn.draw(screen):
            exit = True

    #the exit screen
    if exit == True:
        screen.fill(maroon)
        draw_text("Are you sure you want to leave?", font2, white, 70, 170)
        screen.blit(sad_cat, (205, 240))

        if yes_btn.draw(screen):
            run = False
        if no_btn.draw(screen):
            exit = False
            main_menu = True

    #choosing a background
    if choose_background == True:
        screen.fill(maroon)
        draw_text("Choose a background", font2, white, 135, 110)

        #background buttons
        if night_btn.draw(screen):
            bg_num = 1
        if sky_btn.draw(screen):
            bg_num = 2
        if snowy_btn.draw(screen):
            bg_num = 3
        if bg_num == 1:
            draw_text("Night background selected!", font2, white, 90, 350)
        elif bg_num == 2:
            draw_text("Daytime background selected!", font2, white, 75, 350)
        elif bg_num == 3:
            draw_text("Snowy background selected!", font2, white, 90, 350)

        if back_btn.draw(screen):
            main_menu = True
            choose_background = False

    #choosing a character
    if choose_character == True:
        main_menu = False
        screen.fill(maroon)
        draw_text("It's super easy:", font2, white, 180, 170)
        draw_text("click on the cat you want", font2, white, 110, 210)

        if black_cat_btn.draw(screen):
            player.char = 1
            current_char = 1
            player.image = pygame.image.load("./images/cat_right.png")
            main_menu == True
            choose_character == False
            play_game = False

        if white_cat_btn.draw(screen):
            player.char = 2
            current_char = 2
            player.image = pygame.image.load("./images/cat_right_white.png")
            main_menu == True
            choose_character == False
            play_game = False

        if player.char == 1:
            draw_text("Black cat selected!", font2, white, 152, 500)
        elif player.char == 2:
            draw_text("White cat selected!", font2, white, 152, 500)

        with open('character.dat', 'wb') as file:
            pickle.dump(char, file)

        if back_btn.draw(screen):
            main_menu = True
            choose_character = False

    #the easter egg
    if easter_egg == True:
        screen.fill(maroon)
        egg_found = True

        draw_text("You found the Easter Egg!", font2, white, 105, 100)
        draw_text("When your at the second minute", font3, white, 120, 250)
        draw_text("walk off of the right of the screen. . .", font3, white, 110, 295)

        if back_btn.draw(screen):
            main_menu = True
            easter_egg = False

    #DOWN HERE IS
    #the actual fucking game
    if player.alive == True and main_menu == False:
        if play_game == True:
            #get time for score
            if milliseconds > 1000:
                seconds += 1
                milliseconds -= 1000
            if seconds > 60:
                minutes += 1
                seconds -= 60

            #drawing what needs to be drawn
            draw_bg()
            screen.blit(moon_img, (20, 20))

            for platform in platform_group:
                platform.update()
                platform.draw()

            #showing the time on the screen
            draw_text(f'Time:', font3, white, SCREEN_WIDTH - 120, 10)
            if seconds < 10:
                timelabel = font3.render("{}:0{}".format(minutes, seconds), 1, white)
                screen.blit(timelabel, (SCREEN_WIDTH - 55, 10))
            else:
                timelabel = font3.render("{}:{}".format(minutes, seconds), 1, white)
                screen.blit(timelabel, (SCREEN_WIDTH - 55, 10))

            #back button
            if jump_count == 0 and player.alive == True:
                if back_btn.draw(screen):
                    main_menu = True
                    play_game = False
                    milliseconds = 0
                    seconds = 0
                    minutes = 0

            #drawing the floor
            draw_floor(player)
            if move_complete == False:
                move_complete = player.move_unto_screen()

            screen_scroll, death = player.update()

            #some collision checks
            if player.rect.top > SCREEN_HEIGHT:
                player.alive = False
            if player.rect.left < 0:
                player.rect.left = 0
            if player.rect.left > SCREEN_WIDTH:
                player.alive = False 
            if player.rect.left > SCREEN_WIDTH and minutes == 2 and egg_found == True:
                war_rob = True
                play_game = False

    #The in-game easter egg
    if war_rob == True:
        screen.fill(maroon)

        draw_text('CONGRATULATIONS!', font4, white, 17, 30)
        draw_text('You found the hidden treasure:', font2, white, 67, 95)

    #player death
    elif player.alive == False:
        player_dead = True
        if bg_num == 3:
            draw_text('YOU LOSE', font, maroon, 100, 200)
        else:
            draw_text('YOU LOSE', font, white, 100, 200)

        if redo_btn.draw(screen):
            player = Player(-70, 790, char)
            player.alive = True
            player_dead = False
            move_complete = False
            jump_count = 0
            jump_ok = True
            milliseconds = 0
            seconds = 0
            minutes = 0
            if current_char == 1:
                player.image = pygame.image.load("./images/cat_right.png")
                player.char = 1
            elif current_char == 2:
                player.image = pygame.image.load("./images/cat_right_white.png")
                player.char = 2

    #exiting out control
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == EVENT_ADD_PLATFORM and play_game == True and main_menu == False:  # Add a new cloud
            #if player.alive == True: # Only add new enemies if the Game is still in play (Player not Dead)
            new_platform = Platform(SCREEN_HEIGHT, SCREEN_WIDTH)
            platform_group.add(new_platform)


    milliseconds += score_clock.tick_busy_loop(60)
    pygame.display.update()