import pygame
import sys
import time
import os
import csv
import random

# Define a variable to keep track of the music state
music_enabled = True

# Initialize the pygame mixer
pygame.mixer.init()

# Load the sound file (adjust the path accordingly)
music_on_sound = pygame.mixer.Sound("audio/music.mp3")


def play_music_on_sound():
    music_on_sound.play()


def stop_music():
    pygame.mixer.stop()


class OptionPopup:
    def __init__(self, screen):
        self.screen = screen
        self.music_enabled = True
        self.popup_rect = pygame.Rect(340, 50, 600, 300)
        self.music_button_rect = pygame.Rect(
            self.popup_rect.x + 100, self.popup_rect.y + 175, 80, 70)
        self.icon_x_rect = pygame.Rect(self.popup_rect.x + self.popup_rect.width // 2 - 37,
                                       self.popup_rect.y + self.popup_rect.height - 60, 75, 75)

    def show(self):
        original_content = self.screen.copy()

        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))

        popup_image = pygame.image.load("img/popup_papan.png")
        popup_image = pygame.transform.scale(popup_image, (575, 608))

        icon_x = pygame.image.load("img/icons/icon_cancel.png")
        icon_x = pygame.transform.scale(icon_x, (75, 75))

        rowdies_font = pygame.font.Font("font/Rowdies-Bold.ttf", 36)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.popup_rect.collidepoint(event.pos):
                        if self.music_button_rect.collidepoint(event.pos):
                            self.music_enabled = not self.music_enabled
                            if self.music_enabled:
                                print("Music ON")
                                play_music_on_sound()
                            else:
                                print("Music OFF")
                                stop_music()
                        if self.icon_x_rect.collidepoint(event.pos):
                            print("Cancel button clicked!")
                            return
                        if not self.popup_rect.collidepoint(event.pos):
                            return

            # Draw the original content
            self.screen.blit(original_content, (0, 0))

            self.screen.blit(overlay, (0, 0))
            self.screen.blit(popup_image, self.popup_rect)

            music_icon_path = "img/icons/icon_music_on.png" if self.music_enabled else "img/icons/icon_music_off.png"
            music_icon = pygame.image.load(music_icon_path)
            music_icon = pygame.transform.scale(music_icon, (80, 70))
            self.screen.blit(music_icon, (self.popup_rect.x +
                             100, self.popup_rect.y + 175))

            music_text = "Music ON" if self.music_enabled else "Music OFF"
            text_surface = rowdies_font.render(
                music_text, True, (255, 255, 255))
            self.screen.blit(
                text_surface, (self.popup_rect.x + 185, self.popup_rect.y + 190))

            self.screen.blit(icon_x, self.icon_x_rect)

            pygame.display.update()


class CreditPopup:
    def __init__(self, screen):
        self.screen = screen
        self.popup_rect = pygame.Rect(340, 50, 600, 300)
        self.icon_x_rect = pygame.Rect(self.popup_rect.x + self.popup_rect.width // 2 - 37,
                                       self.popup_rect.y + self.popup_rect.height + 180, 75, 75)

    def show(self):
        original_content = self.screen.copy()

        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))

        credit_image = pygame.image.load("img/popup_credit.png")
        credit_image = pygame.transform.scale(credit_image, (575, 670))

        icon_x = pygame.image.load("img/icons/icon_cancel.png")
        icon_x = pygame.transform.scale(icon_x, (75, 75))

        # Font for the credit text
        credit_title_font = pygame.font.Font("font/Rowdies-Bold.ttf", 30)
        credit_info_font = pygame.font.Font(
            "font/Rowdies-Regular.ttf", 20)  # Use None for the default font

        # Information to display
        credit_info = [
            {"position": "PRODUCER", "name": "Fifit Syafaaty"},
            {"position": "QUALITY ASSURANCE TESTER",
                "name": "Muvidha Fatmawati Putri"},
            {"position": "DEVELOPER", "name": "Rizqi Cahya Angelita"},
            {"position": "WRITER", "name": "Dwi Ramadhaniasari"},
            {"position": "GAME DESIGNER", "name": "Alvin Noor Hidayah"}
        ]

        # Set the spacing between title and info
        spacing = 30

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.popup_rect.collidepoint(event.pos):
                        if self.icon_x_rect.collidepoint(event.pos):
                            print("Cancel button clicked!")
                            return
                        # Add other button click handling logic here if needed
                    elif not self.popup_rect.collidepoint(event.pos):
                        return

            # Draw the original content
            self.screen.blit(original_content, (0, 0))

            self.screen.blit(overlay, (0, 0))
            self.screen.blit(credit_image, self.popup_rect)

            # Draw the "Cancel" button
            self.screen.blit(icon_x, self.icon_x_rect)

            # Draw credit information
            credit_title_surface = credit_title_font.render(
                "CURRENT TEAM", True, (255, 255, 255))
            credit_title_rect = credit_title_surface.get_rect(
                center=(self.popup_rect.centerx, self.popup_rect.y + 150))
            self.screen.blit(credit_title_surface, credit_title_rect)

            credit_y = credit_title_rect.bottom + spacing
            for info in credit_info:
                position_surface = credit_info_font.render(
                    info["position"], True, (255, 255, 255))
                position_rect = position_surface.get_rect(
                    center=(self.popup_rect.centerx, credit_y))
                self.screen.blit(position_surface, position_rect)
                credit_y += 25

                name_surface = credit_info_font.render(
                    info["name"], True, (255, 255, 255))
                name_rect = name_surface.get_rect(
                    center=(self.popup_rect.centerx, credit_y))
                self.screen.blit(name_surface, name_rect)
                credit_y += 35  # Adjust the spacing between position and name

            pygame.display.update()


class NPC(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.images = [pygame.transform.scale(pygame.image.load(
            f'img/npc/greeting/0_Citizen_Greeting_0 ({i}).png'), (300, 300)) for i in range(1, 30)]
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.topleft = (25, 400)  # Ganti posisi sesuai kebutuhan
        self.greeting_timer = pygame.time.get_ticks()
        self.greeting_interval = 50  # Ganti interval sesuai kebutuhan

        # Tambahkan properti popup_image
        self.popup_image = pygame.transform.scale(
            pygame.image.load('img/popup_talking.png'), (365, 100))
        self.popup_rect = self.popup_image.get_rect()
        # Sesuaikan posisi popup di atas NPC
        self.popup_rect.topleft = (self.rect.x - 20, self.rect.y - 100)
        self.popup_text = "Ayo taklukan tantangan!"

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.greeting_timer > self.greeting_interval:
            self.greeting_timer = now
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]

    def draw_popup(self, screen):
        # Gambar popup di atas NPC
        screen.blit(self.popup_image, self.popup_rect)

        # Tambahkan teks pada popup
        # Sesuaikan jenis font dan ukuran teks sesuai kebutuhan
        font_popup = pygame.font.Font("font/PressStart2P-Regular.ttf", 14)
        text_surface = font_popup.render(self.popup_text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.popup_rect.center)
        screen.blit(text_surface, text_rect.topleft)


class Popup:
    def __init__(self, screen, message, position):
        self.screen = screen
        self.message = message
        self.position = position
        self.font = pygame.font.Font("font/Rowdies-Bold.ttf", 24)
        self.popup_surface = pygame.Surface((500, 50), pygame.SRCALPHA)
        self.popup_rect = self.popup_surface.get_rect(topleft=position)
        self.time_displayed = 0
        self.show_duration = 2000  # Display time in milliseconds

    def draw(self):
        pygame.draw.rect(self.popup_surface,
                         (255, 255, 255, 200), (0, 0, 500, 50))
        text = self.font.render(self.message, True, (0, 0, 0))
        self.popup_surface.blit(text, (10, 10))
        self.screen.blit(self.popup_surface, self.position)

    def update(self, dt):
        self.time_displayed += dt
        if self.time_displayed >= self.show_duration:
            return True  # Signal that the notification should be removed
        return False


class Component:
    def __init__(self, image_path, position, size):
        self.image_path = image_path
        self.image = pygame.image.load(image_path)
        self.size = size
        self.image = pygame.transform.scale(self.image, size)
        self.position = position
        self.rect = self.image.get_rect(topleft=position)
        self.dragging = False

    def draw(self, screen):
        screen.blit(self.image, self.position)

    def update_position(self, new_position):
        self.position = new_position
        self.rect.topleft = new_position


def is_filled(box, components):
    for component in components:
        if box.colliderect(component.rect):
            return True
    return False


def game_level1_page(screen):
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 700

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # set framerate
    clock = pygame.time.Clock()
    FPS = 60

    # define game variables
    GRAVITY = 0.75
    SCROLL_THRESH = 200
    ROWS = 17
    COLS = 150
    TILE_SIZE = SCREEN_HEIGHT // ROWS
    TILE_TYPES = 27
    screen_scroll = 0
    bg_scroll = 0
    level = 1

    # define player action variables
    moving_left = False
    moving_right = False
    shoot = False

    jump_fx = pygame.mixer.Sound('audio/jump.wav')
    jump_fx.set_volume(0.05)
    shot_fx = pygame.mixer.Sound('audio/shot.wav')
    shot_fx.set_volume(0.05)

    # load images
    icon_star = pygame.transform.scale(
        pygame.image.load('img/icons/icon_star.png'), (50, 50))
    star_position = (495, 5)
    icon_life = pygame.transform.scale(
        pygame.image.load('img/icons/icon_life.png'), (55, 70))
    life_position = (10, 10)

    # background
    office1_img = pygame.image.load(
        'img/Background/office1.png').convert_alpha()
    office2_img = pygame.image.load(
        'img/Background/office2.png').convert_alpha()
    office3_img = pygame.image.load(
        'img/Background/office3.png').convert_alpha()
    sky_img = pygame.image.load('img/Background/sky.png').convert_alpha()
    # store tiles in a list
    img_list = []
    for x in range(TILE_TYPES):
        img = pygame.image.load(f'img/Tile/{x}.png')
        img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        img_list.append(img)
    # bullet
    bullet_img = pygame.image.load('img/icons/bullet.png').convert_alpha()
    # pick up boxes
    health_img = pygame.image.load('img/icons/health.png').convert_alpha()
    heatsink_img = pygame.image.load('img/icons/heatsink.png').convert_alpha()
    ram_img = pygame.image.load('img/icons/ram.png').convert_alpha()
    cpu_img = pygame.image.load('img/icons/cpu.png').convert_alpha()
    fan_img = pygame.image.load('img/icons/fan.png').convert_alpha()
    hdd_img = pygame.image.load('img/icons/hdd.png').convert_alpha()
    psu_img = pygame.image.load('img/icons/psu.png').convert_alpha()
    thermal_img = pygame.image.load('img/icons/thermal.png').convert_alpha()
    book_img = pygame.image.load('img/icons/book.png').convert_alpha()
    item_boxes = {
        'Health': health_img,
        'heatsink': heatsink_img,
        'ram': ram_img,
        'cpu': cpu_img,
        'fan': fan_img,
        'hdd': hdd_img,
        'psu': psu_img,
        'thermal paste': thermal_img,
        'book': book_img
    }

    # define colours
    BG = (144, 201, 120)
    BLACK = (0, 0, 0)

    # define font
    font = pygame.font.SysFont('font/Rowdies-Regular.ttf', 30)

    def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))

    def draw_bg():
        screen.fill(BG)
        width = sky_img.get_width()
        for x in range(5):
            screen.blit(sky_img, ((x * width) - bg_scroll * 0.5, 0))
            screen.blit(office3_img, ((x * width) - bg_scroll * 0.6,
                        SCREEN_HEIGHT - office3_img.get_height() - 200))
            screen.blit(office2_img, ((x * width) - bg_scroll * 0.8,
                        SCREEN_HEIGHT - office2_img.get_height() - 75))
            screen.blit(office1_img, ((x * width) - bg_scroll * 0.7,
                        SCREEN_HEIGHT - office1_img.get_height() - 15))

    def draw_components(player):
        global heatsink_found, ram_found
        draw_text('Komponen PC: ', font, BLACK, 10, 80)

        component_spacing = 40  # Adjust the spacing between components
        component_offset = 70

        for component, count in player.components.items():
            if count > 0:  # Check if the player has obtained the component
                for _ in range(count):
                    screen.blit(item_boxes[component],
                                (90 + component_offset, 70))
                    component_offset += component_spacing

    def reset_level():
        enemy_group.empty()
        bullet_group.empty()
        item_group.empty()
        decoration_group.empty()
        water_group.empty()
        exit_group.empty()

        # create empty tile list
        data = []
        for row in range(ROWS):
            r = [-1] * COLS
            data.append(r)

        return data

    # Add these lines to load the pause icon image
    pause_img = pygame.transform.scale(
        pygame.image.load('img/icons/icon_pause.png'), (70, 55))
    pause_position = (1135, 5)
    paused = False
    resume_button = pygame.transform.scale(
        pygame.image.load('img/btn_resume.png'), (200, 80))
    home_button = pygame.transform.scale(
        pygame.image.load('img/btn_home.png'), (200, 80))
    resume_button_rect = resume_button.get_rect(center=(600, 300))
    home_button_rect = home_button.get_rect(center=(600, 400))

    # Add this class to handle the pause pop-up
    class PausePopup:
        def __init__(self):
            self.image = pygame.image.load(
                'img/popup_pause.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (575, 608))
            self.rect = self.image.get_rect()
            self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        def draw(self):
            screen.blit(self.image, self.rect.topleft)
            # Draw resume and home buttons
            screen.blit(resume_button, resume_button_rect)
            screen.blit(home_button, home_button_rect)

    class Soldier(pygame.sprite.Sprite):
        def __init__(self, char_type, x, y, scale, speed, *components):
            pygame.sprite.Sprite.__init__(self)
            self.alive = True
            self.char_type = char_type
            self.speed = speed
            self.shoot_cooldown = 0
            component_names = ['heatsink', 'ram', 'fan',
                               'thermal paste', 'hdd', 'cpu', 'psu', 'book']
            self.components = {name: 0 for name in component_names}
            self.health = 3
            self.max_health = self.health
            self.direction = 1
            self.vel_y = 0
            self.jump = False
            self.in_air = True
            self.flip = False
            self.animation_list = []
            self.frame_index = 0
            self.action = 0
            self.update_time = pygame.time.get_ticks()
            # ai specific variables
            self.move_counter = 0
            self.vision = pygame.Rect(0, 0, 150, 20)
            self.idling = False
            self.idling_counter = 0
            self.score = 0  # Add a score attribute
            self.scored = False  # Add this line

            # load all images for the players
            animation_types = ['Idle', 'Run', 'Jump', 'Death', 'Shoot']
            for animation in animation_types:
                # reset temporary list of images
                temp_list = []
                # count number of files in the folder
                num_of_frames = len(os.listdir(
                    f'img/{self.char_type}/{animation}'))
                for i in range(num_of_frames):
                    img = pygame.image.load(
                        f'img/{self.char_type}/{animation}/{i}.png').convert_alpha()
                    img = pygame.transform.scale(
                        img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                    temp_list.append(img)
                self.animation_list.append(temp_list)

            self.image = self.animation_list[self.action][self.frame_index]
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)
            self.width = self.image.get_width()
            self.height = self.image.get_height()

        def update(self):
            self.update_animation()
            self.check_alive()
            # update cooldown
            if self.shoot_cooldown > 0:
                self.shoot_cooldown -= 1

        def move(self, moving_left, moving_right):
            # reset movement variables
            screen_scroll = 0
            dx = 0
            dy = 0

            # assign movement variables if moving left or right
            if moving_left:
                dx = -self.speed
                self.flip = True
                self.direction = -1
            if moving_right:
                dx = self.speed
                self.flip = False
                self.direction = 1

            # jump
            if self.jump == True and self.in_air == False:
                self.vel_y = -18
                self.jump = False
                self.in_air = True

            # apply gravity
            self.vel_y += GRAVITY
            if self.vel_y > 20:
                self.vel_y
            dy += self.vel_y

            # check for collision
            for tile in world.obstacle_list:
                # check collision in the x direction
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                    # if the ai has hit a wall then make it turn around
                    if self.char_type == 'enemy':
                        self.direction *= -1
                        self.move_counter = 0
                # check for collision in the y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    # check if below the ground, i.e. jumping
                    if self.vel_y < 0:
                        self.vel_y = 0
                        dy = tile[1].bottom - self.rect.top
                    # check if above the ground, i.e. falling
                    elif self.vel_y >= 0:
                        self.vel_y = 0
                        self.in_air = False
                        dy = tile[1].top - self.rect.bottom

            # check for collision with water
            if pygame.sprite.spritecollide(self, water_group, False):
                self.health = 0

            # check for collision with exit
            level_complete = False
            if pygame.sprite.spritecollide(self, exit_group, False):
                level_complete = True

            # check if fallen off the map
            if self.rect.bottom > SCREEN_HEIGHT:
                self.health = 0

            # check if going off the edges of the screen
            if self.char_type == 'player':
                if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
                    dx = 0

            # update rectangle position
            self.rect.x += dx
            self.rect.y += dy

            # update scroll based on player position
            if self.char_type == 'player':
                if (self.rect.right > SCREEN_WIDTH - SCROLL_THRESH and bg_scroll < (world.level_length * TILE_SIZE) - SCREEN_WIDTH)\
                        or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
                    self.rect.x -= dx
                    screen_scroll = -dx

            return screen_scroll, level_complete

        def shoot(self):
            if self.shoot_cooldown == 0:
                self.shoot_cooldown = 20
                bullet = Bullet(self.rect.centerx + (
                    0.65 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
                bullet_group.add(bullet)
                shot_fx.play()

        def ai(self):
            if self.alive and player.alive:
                if self.idling == False and random.randint(1, 200) == 1:
                    self.update_action(0)  # 0: idle
                    self.idling = True
                    self.idling_counter = 50
                # check if the ai in near the player
                if self.vision.colliderect(player.rect):
                    # stop running and face the player
                    self.update_action(4)  # 4: shoot
                    # shoot
                    self.shoot()
                else:
                    if self.idling == False:
                        if self.direction == 1:
                            ai_moving_right = True
                        else:
                            ai_moving_right = False
                        ai_moving_left = not ai_moving_right
                        self.move(ai_moving_left, ai_moving_right)
                        self.update_action(1)  # 1: run
                        self.move_counter += 1
                        # update ai vision as the enemy moves
                        self.vision.center = (
                            self.rect.centerx + 75 * self.direction, self.rect.centery)

                        if self.move_counter > TILE_SIZE:
                            self.direction *= -1
                            self.move_counter *= -1
                    else:
                        self.idling_counter -= 1
                        if self.idling_counter <= 0:
                            self.idling = False

            # scroll
            self.rect.x += screen_scroll

        def update_animation(self):
            # update animation
            ANIMATION_COOLDOWN = 100
            # update image depending on current frame
            self.image = self.animation_list[self.action][self.frame_index]
            # check if enough time has passed since the last update
            if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
                self.update_time = pygame.time.get_ticks()
                self.frame_index += 1
            # if the animation has run out the reset back to the start
            if self.frame_index >= len(self.animation_list[self.action]):
                if self.action == 3:
                    self.frame_index = len(
                        self.animation_list[self.action]) - 1
                else:
                    self.frame_index = 0

        def update_action(self, new_action):
            # check if the new action is different to the previous one
            if new_action != self.action:
                self.action = new_action
                # update the animation settings
                self.frame_index = 0
                self.update_time = pygame.time.get_ticks()

        def check_alive(self):
            if self.health <= 0:
                self.health = 0
                self.speed = 0
                self.alive = False
                self.update_action(3)
                if not self.scored:
                    player.score += 15
                    self.scored = True

        def draw(self):
            screen.blit(pygame.transform.flip(
                self.image, self.flip, False), self.rect)

            screen.blit(icon_star, star_position)
            font = pygame.font.Font("font/Rowdies-Regular.ttf", 32)
            score_text = font.render(f"Score: {player.score}", True, (0, 0, 0))
            screen.blit(score_text, (555, 10))

    class World():
        def __init__(self):
            self.obstacle_list = []

        def process_data(self, data):
            self.level_length = len(data[0])
            # iterate through each value in level data file
            for y, row in enumerate(data):
                for x, tile in enumerate(row):
                    if tile >= 0:
                        img = img_list[tile]
                        img_rect = img.get_rect()
                        img_rect.x = x * TILE_SIZE
                        img_rect.y = y * TILE_SIZE
                        tile_data = (img, img_rect)
                        if tile >= 0 and tile <= 8:
                            self.obstacle_list.append(tile_data)
                        elif tile >= 9 and tile <= 10:
                            water = Water(img, x * TILE_SIZE, y * TILE_SIZE)
                            water_group.add(water)
                        elif tile >= 11 and tile <= 14:
                            decoration = Decoration(
                                img, x * TILE_SIZE, y * TILE_SIZE)
                            decoration_group.add(decoration)
                        elif tile == 15:  # create player
                            player = Soldier(
                                'player', x * TILE_SIZE, y * TILE_SIZE, 1.65, 5, 20, 5, 0, 0, 0, 0, 0, 0)
                            health_bar = HealthBar(
                                10, 10, player.health, player.health)
                        elif tile == 16:  # create enemies
                            enemy = Soldier(
                                'enemy', x * TILE_SIZE, y * TILE_SIZE, 1.65, 2, 20, 0, 0, 0, 0, 0, 0, 0)
                            enemy_group.add(enemy)
                        elif tile == 17:  # create heatsink box
                            item_box = ItemBox(
                                'heatsink', x * TILE_SIZE, y * TILE_SIZE)
                            item_group.add(item_box)
                        elif tile == 18:  # create ram box
                            item_box = ItemBox(
                                'ram', x * TILE_SIZE, y * TILE_SIZE)
                            item_group.add(item_box)
                        elif tile == 19:  # create health box
                            item_box = ItemBox(
                                'fan', x * TILE_SIZE, y * TILE_SIZE)
                            item_group.add(item_box)
                        elif tile == 20:  # create health box
                            item_box = ItemBox(
                                'thermal paste', x * TILE_SIZE, y * TILE_SIZE)
                            item_group.add(item_box)
                        elif tile == 21:  # create health box
                            item_box = ItemBox(
                                'hdd', x * TILE_SIZE, y * TILE_SIZE)
                            item_group.add(item_box)
                        elif tile == 22:  # create health box
                            item_box = ItemBox(
                                'cpu', x * TILE_SIZE, y * TILE_SIZE)
                            item_group.add(item_box)
                        elif tile == 23:  # create health box
                            item_box = ItemBox(
                                'psu', x * TILE_SIZE, y * TILE_SIZE)
                            item_group.add(item_box)
                        elif tile == 24:  # create health box
                            item_box = ItemBox(
                                'Health', x * TILE_SIZE, y * TILE_SIZE)
                            item_group.add(item_box)
                        elif tile == 25:  # create health box
                            item_box = ItemBox(
                                'book', x * TILE_SIZE, y * TILE_SIZE)
                            item_group.add(item_box)
                        elif tile == 26:  # create exit
                            exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
                            exit_group.add(exit)

            return player, health_bar

        def draw(self):
            for tile in self.obstacle_list:
                tile[1][0] += screen_scroll
                screen.blit(tile[0], tile[1])

    class Decoration(pygame.sprite.Sprite):
        def __init__(self, img, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = img
            self.rect = self.image.get_rect()
            self.rect.midtop = (x + TILE_SIZE // 2, y +
                                (TILE_SIZE - self.image.get_height()))

        def update(self):
            self.rect.x += screen_scroll

    class Water(pygame.sprite.Sprite):
        def __init__(self, img, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = img
            self.rect = self.image.get_rect()
            self.rect.midtop = (x + TILE_SIZE // 2, y +
                                (TILE_SIZE - self.image.get_height()))

        def update(self):
            self.rect.x += screen_scroll

    class Exit(pygame.sprite.Sprite):
        def __init__(self, img, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = img
            self.rect = self.image.get_rect()
            self.rect.midtop = (x + TILE_SIZE // 2, y +
                                (TILE_SIZE - self.image.get_height()))

        def update(self):
            self.rect.x += screen_scroll

    class ItemBox(pygame.sprite.Sprite):
        def __init__(self, item_type, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.item_type = item_type
            self.image = item_boxes[self.item_type]
            self.rect = self.image.get_rect()
            self.rect.midtop = (x + TILE_SIZE // 2, y +
                                (TILE_SIZE - self.image.get_height()))

        def update(self):
            # Scroll
            self.rect.x += screen_scroll

            # Check if the player has picked up the box
            if pygame.sprite.collide_rect(self, player):
                # Check what kind of box it was
                if self.item_type == 'Health':
                    player.health = min(player.health + 1, player.max_health)
                else:
                    # Increment the player's score for other items
                    player.score += 20

                    # Handle other item effects if needed
                    if self.item_type in player.components:
                        player.components[self.item_type] += 1

                    # Show pop-up when the player collects a component
                    self.show_popup()

                # Delete the item box
                self.kill()

        def show_popup(self):
            if self.item_type == 'book':
                book_popup_image = pygame.image.load('img/popup_buku.png')
                next_button_image = pygame.image.load(
                    'img/btn_next.png')  # Replace with the actual path
                next_button_image = pygame.transform.scale(
                    next_button_image, (50, 60))  # Resize the button image
                title = "Apa Itu Merakit PC?"
                paragraph = [
                    "Merakit PC adalah proses menyusun komponen-komponen ",
                    "perangkat keras (hardware) yang diperlukan untuk",
                    "membentuk sebuah komputer pribadi (PC). Kegiatan merakit ",
                    "berarti meletakkan komponen-komponen penyusun komputer",
                    "pada posisi masing-masing sehingga dapat beroperasi."
                ]
                book_popup = BookPopup(
                    screen, book_popup_image, next_button_image, (600, 400), title, paragraph)
                book_popup_duration = 5000  # in milliseconds

                start_time = pygame.time.get_ticks()
                clock = pygame.time.Clock()

                while pygame.time.get_ticks() - start_time < book_popup_duration:
                    book_popup.draw()
                    pygame.display.update()
                    clock.tick(60)
            else:
                # Default pop-up behavior
                message = f"You've collected {self.item_type}!"
                popup = Popup(screen, message, (SCREEN_WIDTH //
                              2 - 250, SCREEN_HEIGHT // 2 - 25))
                popup_duration = 2000  # in milliseconds

                start_time = pygame.time.get_ticks()
                clock = pygame.time.Clock()

                while pygame.time.get_ticks() - start_time < popup_duration:
                    popup.draw()
                    pygame.display.update()
                    clock.tick(60)

    class BookPopup:
        def __init__(self, screen, book_popup_image, button_image, position, title, paragraph):
            self.image = book_popup_image
            self.button_image = button_image
            self.rect = self.image.get_rect()
            self.rect.center = position
            self.title_font = pygame.font.Font("font/Rowdies-Bold.ttf", 40)
            self.paragraph_font = pygame.font.Font(
                "font/Rowdies-Regular.ttf", 24)
            self.title = title
            self.paragraph = paragraph
            self.button_rect = None

        def draw(self):
            screen.blit(self.image, self.rect.topleft)

            title_surface = self.title_font.render(
                self.title, True, (255, 255, 255))
            title_rect = title_surface.get_rect(
                center=(self.rect.centerx, self.rect.top + 170))
            screen.blit(title_surface, title_rect)

            # Render each line of the paragraph separately
            line_height = 30  # Adjust as needed
            current_y = self.rect.top + 270

            for line in self.paragraph:
                paragraph_surface = self.paragraph_font.render(
                    line, True, (255, 255, 255))
                paragraph_rect = paragraph_surface.get_rect(
                    center=(self.rect.centerx, current_y))
                screen.blit(paragraph_surface, paragraph_rect)
                current_y += line_height

            # Draw the "Next" button on top of the book popup image
            self.button_rect = screen.blit(
                self.button_image, (self.rect.centerx + 370, current_y + 100))

    class HealthBar():
        def __init__(self, x, y, health, max_health):
            self.x = x
            self.y = y
            self.health = health
            self.max_health = max_health

        def draw(self, health):
            # update with new health
            self.health = health

            screen.blit(icon_life, (10, 10))
            # Display remaining lives as icons
            for i in range(health):
                screen.blit(
                    icon_life, (life_position[0] + i * 60, life_position[1]))

    class Bullet(pygame.sprite.Sprite):
        def __init__(self, x, y, direction):
            pygame.sprite.Sprite.__init__(self)
            self.speed = 10
            self.image = bullet_img
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)
            self.direction = direction

        def update(self):
            # move bullet
            self.rect.x += (self.direction * self.speed) + screen_scroll
            # check if bullet has gone off screen
            if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
                self.kill()
            # check for collision with level
            for tile in world.obstacle_list:
                if tile[1].colliderect(self.rect):
                    self.kill()

            # check collision with characters
            if pygame.sprite.spritecollide(player, bullet_group, False):
                if player.alive:
                    player.health -= 1
                    self.kill()

            for enemy in enemy_group:
                if pygame.sprite.spritecollide(enemy, bullet_group, False):
                    if enemy.alive:
                        enemy.health -= 1
                        self.kill()

    class ScreenFade():
        def __init__(self, direction, colour, speed):
            self.direction = direction
            self.colour = colour
            self.speed = speed
            self.fade_counter = 0

        def fade(self):
            fade_complete = False
            self.fade_counter += self.speed
            if self.direction == 1:  # whole screen fade
                pygame.draw.rect(
                    screen, self.colour, (0 - self.fade_counter, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT))
                pygame.draw.rect(screen, self.colour, (SCREEN_WIDTH //
                                 2 + self.fade_counter, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
                pygame.draw.rect(
                    screen, self.colour, (0, 0 - self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
                pygame.draw.rect(screen, self.colour, (0, SCREEN_HEIGHT //
                                 2 + self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT))
            if self.direction == 2:  # vertical screen fade down
                pygame.draw.rect(screen, self.colour,
                                 (0, 0, SCREEN_WIDTH, 0 + self.fade_counter))
            if self.fade_counter >= SCREEN_WIDTH:
                fade_complete = True

            return fade_complete

    # create sprite groups
    enemy_group = pygame.sprite.Group()
    bullet_group = pygame.sprite.Group()
    item_group = pygame.sprite.Group()
    decoration_group = pygame.sprite.Group()
    water_group = pygame.sprite.Group()
    exit_group = pygame.sprite.Group()

    # create empty tile list
    world_data = []
    for row in range(ROWS):
        r = [-1] * COLS
        world_data.append(r)

    # Load level data and create world
    with open(f'level{level}_data.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for x, row in enumerate(reader):
            for y, tile in enumerate(row):
                world_data[x][y] = int(tile)

    world = World()
    player, health_bar = world.process_data(world_data)

    # Create a PausePopup instance
    pause_popup = PausePopup()
    is_paused = False

    run = True
    while run:
        clock.tick(FPS)

        # Update background
        draw_bg()

        # Draw world map
        world.draw()

        # Show player health
        health_bar.draw(player.health)

        # # Draw obtained components
        # draw_components(player)

        player.update()
        player.draw()

        for enemy in enemy_group:
            enemy.ai()
            enemy.update()
            enemy.draw()

        # Update and draw groups
        bullet_group.update()
        item_group.update()
        decoration_group.update()
        water_group.update()
        exit_group.update()
        bullet_group.draw(screen)
        item_group.draw(screen)
        decoration_group.draw(screen)
        water_group.draw(screen)
        exit_group.draw(screen)

        # Draw the pause icon
        screen.blit(pause_img, pause_position)

        # Check for game events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Toggle pause
                is_paused = not is_paused
                if resume_button_rect.collidepoint(event.pos):
                    paused = False
                elif home_button_rect.collidepoint(event.pos):
                    # Restart the game and go back to the main menu
                    stop_music()  # Stop music when back is clicked
                    main()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    moving_left = True
                if event.key == pygame.K_d:
                    moving_right = True
                if event.key == pygame.K_SPACE:
                    shoot = True
                if event.key == pygame.K_w and player.alive:
                    player.jump = True
                    jump_fx.play()
                if event.key == pygame.K_ESCAPE:
                    run = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    moving_left = False
                if event.key == pygame.K_d:
                    moving_right = False
                if event.key == pygame.K_SPACE:
                    shoot = False

        if not is_paused:
            if player.alive:
                # shoot bullets
                if shoot:
                    player.shoot()

                if player.in_air:
                    player.update_action(2)  # 2: jump
                elif moving_left or moving_right:
                    player.update_action(1)  # 1: run
                elif shoot:
                    player.update_action(4)
                else:
                    player.update_action(0)  # 0: idle
                screen_scroll, level_complete = player.move(
                    moving_left, moving_right)
                bg_scroll -= screen_scroll
                # Check if player has completed the level
                if level_complete:
                    show_completion_page(screen, player.score, level=1)
            else:
                screen_scroll = 0
                game_over_page(screen, player.score, level=1)
        else:
            # Draw the pause pop-up
            pause_popup.draw()

        draw_components(player)

        pygame.display.update()

    pygame.quit()


def draw_highlight_boxes(screen, highlight_boxes):
    for box in highlight_boxes:
        pygame.draw.rect(screen, (0, 255, 0), box, 2)


def game_level2_page(screen):
    print("Game Level 2 Page")

    bg2 = pygame.image.load('img/bg/bg2.png')
    bg2 = pygame.transform.scale(bg2, (1200, 700))

    overlay = pygame.Surface((1200, 700), pygame.SRCALPHA)
    overlay.fill((255, 255, 255, 128))

    npc = NPC()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(npc)

    navy_box = pygame.image.load('img/bg/bg_navy.png')
    navy_box = pygame.transform.scale(navy_box, (800, 600))

    title_font = pygame.font.Font("font/Rowdies-Bold.ttf", 40)
    title_text = title_font.render("Misi: Merakit PC", True, (255, 255, 255))

    icon_life = pygame.transform.scale(
        pygame.image.load('img/icons/icon_life.png'), (55, 70))
    icon_star = pygame.transform.scale(
        pygame.image.load('img/icons/icon_star.png'), (55, 55))
    icon_pause = pygame.transform.scale(
        pygame.image.load('img/icons/icon_pause.png'), (80, 70))
    # icon_settings = pygame.transform.scale(pygame.image.load('img/icons/icon_settings.png'), (78, 67))

    life_position = (10, 10)
    star_position = (485, 15)
    pause_position = (1100, 5)
    # settings_position = (1045, 8)
# Load the motherboard image (adjust the path accordingly)
    motherboard = pygame.image.load('img/pc/casing.png')
    motherboard = pygame.transform.scale(motherboard, (450, 475))

    # Highlight boxes for correct placement
    highlight_boxes = {
        "psu": pygame.Rect(735, 235, 200, 75),
        "hdd": pygame.Rect(975, 375, 150, 75),
        "cpu": pygame.Rect(800, 355, 75, 100),
        "thermal_paste": pygame.Rect(800, 355, 75, 100),
        "heatsink": pygame.Rect(800, 355, 75, 100),
        "ram": pygame.Rect(880, 355, 75, 100),
        "fan": pygame.Rect(655, 345, 75, 100),
    }

    # Score and life initialization
    score = 0
    max_lives = 3
    lives = max_lives

    components = [
        Component("img/pc/psu.png", (400, 175), (150, 50)),
        Component("img/pc/cpu.png", (400, 325), (75, 100)),
        Component("img/pc/hdd.png", (400, 250), (150, 50)),
        Component("img/pc/ram.png", (575, 175), (75, 100)),
        Component("img/pc/thermal_paste.png", (400, 450), (75, 100)),
        Component("img/pc/fan.png", (500, 325), (75, 100)),
        Component("img/pc/heatsink.png", (500, 450), (75, 100)),
    ]

    popups = []

    # Time-related variables
    start_time = pygame.time.get_ticks()
    countdown_time = 90000  # 90 seconds in milliseconds

    icon_pause_rect = icon_pause.get_rect(topleft=pause_position)
    paused = False
    resume_button = pygame.transform.scale(
        pygame.image.load('img/btn_resume.png'), (200, 80))
    home_button = pygame.transform.scale(
        pygame.image.load('img/btn_home.png'), (200, 80))
    resume_button_rect = resume_button.get_rect(center=(600, 300))
    home_button_rect = home_button.get_rect(center=(600, 400))

    paused_popup_bg = pygame.image.load(
        'img/popup_pause.png')  # Adjust the path accordingly
    paused_popup_bg = pygame.transform.scale(paused_popup_bg, (575, 608))
    paused_popup_rect = paused_popup_bg.get_rect(center=(600, 375))

    while True:
        dt = pygame.time.Clock().tick(60)
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - start_time

        if not paused:
            remaining_time = max(0, countdown_time - elapsed_time)
            seconds_remaining = remaining_time // 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not paused:
                    for component in components:
                        if component.rect.collidepoint(event.pos):
                            component.dragging = True

                    if icon_pause_rect.collidepoint(event.pos):
                        paused = True
                        pause_time = current_time

                elif paused:
                    if resume_button_rect.collidepoint(event.pos):
                        paused = False
                        start_time += current_time - pause_time
                    elif home_button_rect.collidepoint(event.pos):
                        # Restart the game and go back to the main menu
                        stop_music()  # Stop music when back is clicked
                        main()

            elif event.type == pygame.MOUSEBUTTONUP:
                if not paused:
                    for component in components:
                        if component.dragging:
                            component.dragging = False
                            placed_correctly = False

                            # Check if the component is placed within the correct highlight box
                            for component_type, box in highlight_boxes.items():
                                if box.colliderect(component.rect):
                                    if component_type == "cpu" and component.image_path.endswith("cpu.png"):
                                        # For CPU, it should be placed in the CPU box
                                        score += 10
                                        message = f"Correct Placement! Score: +10 ({component_type})"
                                        popups.append(
                                            Popup(screen, message, (15, 120)))
                                        placed_correctly = True
                                        break  # Break out of the loop if placed correctly in a highlight box
                                    elif component_type != "cpu" and component.image_path.split("/")[-1].split(".")[0] == component_type:
                                        # For other components, they should not be placed in the CPU box
                                        score += 10
                                        message = f"Correct Placement! Score: +10 ({component_type})"
                                        popups.append(
                                            Popup(screen, message, (15, 120)))
                                        placed_correctly = True
                                        break  # Break out of the loop if placed correctly in a highlight box

                            if not placed_correctly:
                                lives -= 1
                                if score > 0:
                                    score -= 5
                                message = f"Wrong Placement! Lives Remaining: {lives}"
                                popups.append(
                                    Popup(screen, message, (15, 120)))
                                if lives == 0 or seconds_remaining == 0:  # Check if time is up
                                    game_over_page(screen, score, level=2)

        # Update component positions when dragging
        for component in components:
            if component.dragging:
                component.update_position(pygame.mouse.get_pos())

        screen.blit(bg2, (0, 0))
        screen.blit(overlay, (0, 0))
        screen.blit(navy_box, (385, 75))
        screen.blit(title_text, (650, 100))
        screen.blit(motherboard, (700, 200))  # Draw the motherboard

        # Draw the highlight boxes
        draw_highlight_boxes(screen, highlight_boxes.values())

        for component in components:
            component.draw(screen)

        all_sprites.update()
        all_sprites.draw(screen)

        screen.blit(icon_life, life_position)
        # Display remaining lives as icons
        for i in range(lives):
            screen.blit(
                icon_life, (life_position[0] + i * 60, life_position[1]))

        # Gambar popup di atas NPC
        npc.draw_popup(screen)

        # Display countdown timer
        font_timer = pygame.font.Font("font/Rowdies-Bold.ttf", 28)
        timer_text = font_timer.render(
            f"Time: {seconds_remaining}s", True, (241, 28, 12))
        screen.blit(timer_text, (10, 80))  # Adjust the position as needed

        screen.blit(icon_star, star_position)

        font = pygame.font.Font("font/Rowdies-Bold.ttf", 32)
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (550, 25))

        screen.blit(icon_pause, pause_position)
        # screen.blit(icon_settings, settings_position)

        if paused:
            # Draw the paused popup background
            screen.blit(paused_popup_bg, paused_popup_rect.topleft)
            # Draw resume and home buttons
            screen.blit(resume_button, resume_button_rect)
            screen.blit(home_button, home_button_rect)

        for popup in popups:
            popup.draw()
            if popup.update(dt):
                # Remove the notification when its time is up
                popups.remove(popup)

        pygame.display.update()

        if not paused and seconds_remaining == 0:
            game_over_page(screen, score, level=2)

        # Check if the player has successfully assembled the PC
        if score == len(components) * 10 and all(is_filled(box, components) for box in highlight_boxes.values()):
            show_completion_page(screen, score, level=2)
            break
        elif score == 65 and lives <= 2 and all(is_filled(box, components) for box in highlight_boxes.values()):
            show_completion_page(screen, score, level=2)
            break
        elif score == 60 and lives <= 2 and all(is_filled(box, components) for box in highlight_boxes.values()):
            show_completion_page(screen, score, level=2)
            break
        elif seconds_remaining == 0:
            game_over_page(screen, score, level=2)


def show_completion_page(screen, score, level):
    print("Completion Page")

    bg_completion = pygame.image.load('img/bg/bg_complete.png')
    bg_completion = pygame.transform.scale(bg_completion, (1200, 700))

    button_continue = pygame.image.load('img/btn_continue.png')
    button_replay = pygame.image.load('img/btn_replay.png')
    button_back = pygame.image.load('img/btn_back.png')
    icon_star = pygame.transform.scale(
        pygame.image.load('img/icons/icon_star.png'), (70, 70))

    # Increase button sizes
    button_size = (200, 80)  # Adjust the size as needed
    button_continue = pygame.transform.scale(button_continue, button_size)
    button_replay = pygame.transform.scale(button_replay, button_size)
    button_back = pygame.transform.scale(button_back, button_size)

    button_continue_rect = button_continue.get_rect(center=(600, 400))
    button_replay_rect = button_replay.get_rect(center=(600, 500))
    button_back_rect = button_back.get_rect(center=(600, 600))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_continue_rect.collidepoint(event.pos):
                    if level == 1:
                        game_level2_page(screen)
                    elif level == 2:
                        level_selection_page(screen)
                elif button_replay_rect.collidepoint(event.pos):
                    # Restart the game at the corresponding level
                    if level == 1:
                        game_level1_page(screen)
                    elif level == 2:
                        game_level2_page(screen)
                elif button_back_rect.collidepoint(event.pos):
                    # Handle "Back" button click (you can add your logic here)
                    stop_music()  # Stop music when back is clicked
                    main()

        screen.blit(bg_completion, (0, 0))
        screen.blit(button_continue, button_continue_rect)
        screen.blit(button_replay, button_replay_rect)
        screen.blit(button_back, button_back_rect)

        # Display the score and icon
        font = pygame.font.Font("font/Rowdies-Bold.ttf", 32)
        score_text = font.render(f"SCORE {score}", True, (244, 181, 53))
        score_rect = score_text.get_rect(center=(620, 325))
        screen.blit(score_text, score_rect)

        # Draw the star icon next to the score
        screen.blit(icon_star, (score_rect.left - 100,
                    score_rect.centery - icon_star.get_height() // 2))
        pygame.display.update()


def game_over_page(screen, score, level):
    print("Game Over Page")

    bg_game_over = pygame.image.load('img/bg/bg_gameover.png')
    bg_game_over = pygame.transform.scale(bg_game_over, (1200, 700))

    button_yes = pygame.image.load('img/btn_yes.png')
    button_back = pygame.image.load('img/btn_back.png')
    icon_star = pygame.transform.scale(
        pygame.image.load('img/icons/icon_star.png'), (70, 70))

    # Increase button sizes
    button_size = (250, 80)  # Adjust the size as needed
    button_yes = pygame.transform.scale(button_yes, button_size)
    button_back = pygame.transform.scale(button_back, button_size)

    button_yes_rect = button_yes.get_rect(center=(600, 500))
    button_back_rect = button_back.get_rect(center=(600, 600))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_yes_rect.collidepoint(event.pos):
                    # Restart the game at the corresponding level
                    if level == 1:
                        game_level1_page(screen)
                    elif level == 2:
                        game_level2_page(screen)
                elif button_back_rect.collidepoint(event.pos):
                    # Go back to the main menu
                    stop_music()  # Stop music when back is clicked
                    main()

        screen.blit(bg_game_over, (0, 0))

        # Display the score and icon
        font = pygame.font.Font("font/Rowdies-Bold.ttf", 32)
        score_text = font.render(f"SCORE {score}", True, (244, 181, 53))
        score_rect = score_text.get_rect(center=(620, 325))
        screen.blit(score_text, score_rect)

        # Draw the star icon next to the score
        screen.blit(icon_star, (score_rect.left - 100,
                    score_rect.centery - icon_star.get_height() // 2))

        screen.blit(button_yes, button_yes_rect)
        screen.blit(button_back, button_back_rect)
        pygame.display.update()


def level_selection_page(screen):
    # Sesuaikan path gambar dengan kebutuhan
    bg_selection = pygame.image.load('img/bg/bg3.png')
    bg_selection = pygame.transform.scale(bg_selection, (1200, 700))
    overlay = pygame.Surface((1200, 700), pygame.SRCALPHA)
    overlay.fill((255, 255, 255, 128))

    # Sesuaikan path gambar dengan kebutuhan
    button_level1 = pygame.image.load('img/btn_level1.png')
    # Sesuaikan path gambar dengan kebutuhan
    button_level2 = pygame.image.load('img/btn_level2.png')
    # Sesuaikan path gambar dengan kebutuhan
    button_kunci = pygame.image.load('img/btn_kunci.png')
    icon_home = pygame.transform.scale(
        pygame.image.load('img/icons/icon_home.png'), (80, 70))
    icon_settings = pygame.transform.scale(
        pygame.image.load('img/icons/icon_settings.png'), (80, 65))

    home_position = (1050, 5)
    settings_position = (1120, 11)

    # Tambahkan tulisan judul "Level"
    font_level = pygame.font.Font("font/PressStart2P-Regular.ttf", 50)
    level_text = font_level.render("LEVEL", True, (9, 41, 115))
    # Sesuaikan posisi tulisan judul "Level" sesuai kebutuhan
    level_rect = level_text.get_rect(center=(615, 150))

    # Increase button sizes
    button_size = (185, 235)  # Sesuaikan ukuran tombol sesuai kebutuhan
    button_level1 = pygame.transform.scale(button_level1, button_size)
    button_level2 = pygame.transform.scale(button_level2, button_size)
    button_kunci = pygame.transform.scale(button_kunci, button_size)

    button_level1_rect = button_level1.get_rect(center=(280, 385))
    button_level2_rect = button_level2.get_rect(center=(625, 385))
    button_kunci_rect = button_kunci.get_rect(center=(955, 385))

    option_popup = OptionPopup(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:

                if button_level1_rect.collidepoint(event.pos):
                    print("Level 1 button clicked!")
                    game_level1_page(screen)
                elif button_level2_rect.collidepoint(event.pos):
                    print("Level 2 button clicked!")
                    game_level2_page(screen)
                elif icon_home.get_rect(topleft=home_position).collidepoint(event.pos):
                    print("Home icon clicked!")
                    main()
                elif icon_settings.get_rect(topleft=settings_position).collidepoint(event.pos):
                    print("Settings icon clicked!")
                    option_popup.show()

        screen.blit(bg_selection, (0, 0))
        screen.blit(overlay, (0, 0))
        screen.blit(icon_home, home_position)
        screen.blit(icon_settings, settings_position)

        # Gambar tulisan judul "Level"
        screen.blit(level_text, level_rect)

        screen.blit(button_level1, button_level1_rect)
        screen.blit(button_level2, button_level2_rect)
        screen.blit(button_kunci, button_kunci_rect)

        pygame.display.update()


def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((1200, 700))
    pygame.display.set_caption('CyberQuest : Perjalanan Digital')

    # Play music when the program starts
    play_music_on_sound()

    option_popup = OptionPopup(screen)
    credit_popup = CreditPopup(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                start_button = pygame.Rect(500, 300, 200, 170)
                option_button = pygame.Rect(500, 400, 200, 170)
                credit_button = pygame.Rect(500, 500, 200, 170)
                exit_button = pygame.Rect(500, 600, 200, 170)

                if exit_button.collidepoint(event.pos):
                    print("Quit button clicked!")
                    pygame.quit()
                    sys.exit()
                elif credit_button.collidepoint(event.pos):
                    # Handle "Credit" button click reaction
                    print("Credit button clicked!")
                    credit_popup.show()  # Display the credit popup
                elif option_button.collidepoint(event.pos):
                    option_popup.show()
                elif start_button.collidepoint(event.pos):
                    print("Start button clicked!")
                    level_selection_page(screen)

        screen.fill((0, 0, 0))
        bg = pygame.image.load('img/bg/bg1.png')
        screen.blit(bg, (0, 0))

        judul_image = pygame.image.load("img/judul.png")
        judul_image_size = (500, 200)
        judul_image = pygame.transform.scale(judul_image, judul_image_size)
        screen.blit(judul_image, (375, 75))

        start_image = pygame.image.load("img/btn_start.png")
        option_image = pygame.image.load("img/btn_option.png")
        credit_image = pygame.image.load("img/btn_credit.png")
        quit_image = pygame.image.load("img/btn_quit.png")
        DEFAULT_IMAGE_SIZE = (250, 80)
        start_image = pygame.transform.scale(start_image, DEFAULT_IMAGE_SIZE)
        option_image = pygame.transform.scale(option_image, DEFAULT_IMAGE_SIZE)
        credit_image = pygame.transform.scale(credit_image, DEFAULT_IMAGE_SIZE)
        quit_image = pygame.transform.scale(quit_image, DEFAULT_IMAGE_SIZE)

        start_button = pygame.Rect(500, 300, 200, 170)
        option_button = pygame.Rect(500, 400, 200, 170)
        credit_button = pygame.Rect(500, 500, 200, 170)
        exit_button = pygame.Rect(500, 600, 200, 170)

        screen.blit(start_image, start_button)
        screen.blit(option_image, option_button)
        screen.blit(credit_image, credit_button)
        screen.blit(quit_image, exit_button)
        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()
