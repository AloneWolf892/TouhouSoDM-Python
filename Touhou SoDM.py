# Important libraries
import os
import time
import pygame
from pygame import Surface, mouse
from pygame.font import Font
import pygame.locals
from pygame import image as img
from Modules.custom_classes import SpriteIdentifier, Button, Player, Bullet, Coin, Terrain, Wall, Turret, Door, Accesory

os.path.dirname(os.path.abspath(__file__))


pygame.init()
pygame.mixer.init()
pygame.font.init()

window_icon: Surface = img.load("./Media/Images/Shinki-Icon.png")
generic_background: Surface = img.load("./Media/Images/backg1.jpg")

generic_music: str = "./Media/Music/Infinite Being.mp3"
pygame.mixer.music.load(generic_music)
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.25)

# Font for Text
comic_sans_font_28: Font = pygame.font.SysFont("Comic Sans MS", 28)
comic_sans_font_56: Font = pygame.font.SysFont("Comic Sans MS", 56)

# Inicializar variables y asignar valores por defecto
coin_score = 0
health_points = 100
last_time: float = time.time()
buttons_list: list[Button] = []

# Inicializar componentes de video
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.display.set_caption("Touhou - Science of Mad Dreamland")
pygame.display.set_icon(window_icon)
game = pygame.display.set_mode((640, 480))
game_rect = pygame.Rect(0, 0, 640, 480)

# Inicializar reloj del juego
clock = pygame.time.Clock()

# Inicializar partida guardada
save_file = open("./Saves/SaveFile.txt", "r+")
level_1_state = level_2_state = level_3_state = False
levels_state_list = [level_1_state, level_2_state, level_3_state]

non_list_save_file_default = ""
default_save_file = ["Level_1 = Fals\n",
                     "Level_2 = Fals\n", "Level_3 = Fals\n"]
complete_save_file = ["Level_1 = True\n",
                      "Level_2 = True\n", "Level_3 = True\n"]
mouse_position = mouse.get_pos()


def stage_builder(level_layout) -> bool:
    # Player and Enemy sprites
    player_walk_up_animation_sprites = [
        img.load("./Media/Images/RikakoSprites/Rikako-UP2.png"),
        img.load("./Media/Images/RikakoSprites/Rikako-UP.png"),
        img.load("./Media/Images/RikakoSprites/Rikako-UP3.png"),
    ]

    player_walk_down_animation_sprites = [
        img.load("./Media/Images/RikakoSprites/Rikako-DOWN2.png"),
        img.load("./Media/Images/RikakoSprites/Rikako-DOWN.png"),
        img.load("./Media/Images/RikakoSprites/Rikako-DOWN3.png"),
    ]

    player_walk_left_animation_sprites = [
        img.load("./Media/Images/RikakoSprites/Rikako-LEFT2.png"),
        img.load("./Media/Images/RikakoSprites/Rikako-LEFT.png"),
        img.load("./Media/Images/RikakoSprites/Rikako-LEFT3.png"),
    ]

    player_walk_right_animation_sprites = [
        img.load("./Media/Images/RikakoSprites/Rikako-RIGHT2.png"),
        img.load("./Media/Images/RikakoSprites/Rikako-RIGHT.png"),
        img.load("./Media/Images/RikakoSprites/Rikako-RIGHT3.png"),
    ]

    enemy_turret_facing_sprites_type_A = [
        img.load("./Media/Images/PC-89 Sprites/PC98-sprites_47.png"),
        img.load("./Media/Images/PC-89 Sprites/PC98-sprites_11.png"),
        img.load("./Media/Images/PC-89 Sprites/PC98-sprites_23.png"),
        img.load("./Media/Images/PC-89 Sprites/PC98-sprites_35.png"),
    ]

    # World Sprites
    terrain_sprite_type_A = img.load(
        "./Media/Images/ItemSprite/Items_02.png"
    )  # Grammita
    wall_sprite_type_A = img.load("./Media/Images/ItemSprite/Items_501.png")  #
    wall_sprite_type_B = img.load("./Media/Images/ItemSprite/Items_527.png")
    door_sprite_type_A = [
        img.load("./Media/Images/ItemSprite/Items_360.png"),
        img.load("./Media/Images/ItemSprite/Items_368.png"),
    ]
    coin_sprite_type_A = img.load("./Media/Images/ItemSprite/Items_995.png")
    accesory_sprite_type_A = img.load(
        "./Media/Images/ItemSprite/Items_1030.png")

    # Music and Sound effects
    coin_get_sound = pygame.mixer.Sound("./Media/Music/coinGet.ogg")

    player_shoots_sound = pygame.mixer.Sound("./Media/Music/PlayerShoot.ogg")
    player_gets_shooted_sound = pygame.mixer.Sound(
        "./Media/Music/PlayerGetShoot.ogg")
    player_dies_sound = pygame.mixer.Sound(
        "./Media/Music/Touhou Death Sound Pichuun.ogg"
    )
    enemy_dies_sound = pygame.mixer.Sound("./Media/Music/EnemyDeath.ogg")
    enemy_shoots_sound = pygame.mixer.Sound("./Media/Music/EnemyShoot.ogg")

    # Some Variables being initialized

    global coin_score
    global health_points
    global last_time
    # player_stun: bool = False
    health_points = 100
    coin_score = 0

    cooldown_tracker = 0

    # Game beggining
    # terrain_rect = pygame.Rect(32,32,576,416)
    clock = pygame.time.Clock()

    # Objects and lists
    rikako = Player(player_walk_up_animation_sprites, player_walk_down_animation_sprites, player_walk_left_animation_sprites, player_walk_right_animation_sprites)
    wall_list = []
    door_list = []
    terrain_list = []
    coin_list = []
    accesory_list = []
    enemy_turret_list = []
    bullets_shot_by_player = []
    bullets_shot_by_enemy_turret = []

    # Level Layout, P = Player, W = Walls, E = Enemy/Turret, C = Coins

    # Read the Layout and create the elements

    def level_layout_read(level_layout):
        identifier = SpriteIdentifier.NONE

        x_display_coordinates = y_display_coordinates = 0
        for row in level_layout:
            for column in row:
                if (
                    x_display_coordinates >= 32 and y_display_coordinates >= 32 and y_display_coordinates < 448 and x_display_coordinates < 640
                ):
                    match column:
                        case "-":
                            identifier = SpriteIdentifier.TERRAIN
                        case "W":
                            identifier = SpriteIdentifier.WALL
                        case "C":
                            identifier = SpriteIdentifier.COIN
                        case "D":
                            identifier = SpriteIdentifier.DOOR
                        case "A":
                            identifier = SpriteIdentifier.ACCESORY
                        case "T":
                            identifier = SpriteIdentifier.TURRET
                        case "~":
                            identifier = SpriteIdentifier.BLANK
                        case ".":
                            match identifier:
                                case SpriteIdentifier.TERRAIN:
                                    terrain_list.append(
                                        Terrain(
                                            (
                                                x_display_coordinates - 32,
                                                y_display_coordinates,
                                            ),
                                            terrain_sprite_type_A,
                                        )
                                    )
                                    identifier = SpriteIdentifier.NONE
                                case SpriteIdentifier.BLANK:
                                    identifier = SpriteIdentifier.NONE
                        case "a":
                            match identifier:
                                case SpriteIdentifier.WALL:
                                    wall_list.append(
                                        Wall(
                                            (
                                                x_display_coordinates - 32,
                                                y_display_coordinates,
                                            ),
                                            wall_sprite_type_A,
                                        )
                                    )
                                    identifier = SpriteIdentifier.NONE
                                case SpriteIdentifier.COIN:
                                    coin_list.append(
                                        Coin(
                                            (
                                                x_display_coordinates - 32,
                                                y_display_coordinates,
                                            ),
                                            coin_sprite_type_A,
                                        )
                                    )
                                    identifier = SpriteIdentifier.NONE
                                case SpriteIdentifier.DOOR:
                                    door_list.append(
                                        Door(
                                            (
                                                x_display_coordinates - 32,
                                                y_display_coordinates,
                                            ),
                                            door_sprite_type_A[0],
                                        )
                                    )
                                    identifier = SpriteIdentifier.NONE
                                case SpriteIdentifier.ACCESORY:
                                    accesory_list.append(
                                        Accesory(
                                            (
                                                x_display_coordinates - 32,
                                                y_display_coordinates,
                                            ),
                                            accesory_sprite_type_A,
                                        )
                                    )
                                    identifier = SpriteIdentifier.NONE
                        case "b":
                            match identifier:
                                case SpriteIdentifier.WALL:
                                    wall_list.append(
                                        Wall(
                                            (
                                                x_display_coordinates - 32,
                                                y_display_coordinates,
                                            ),
                                            wall_sprite_type_B,
                                        )
                                    )
                                    identifier = SpriteIdentifier.NONE
                                case SpriteIdentifier.DOOR:
                                    door_list.append(
                                        Door(
                                            (
                                                x_display_coordinates - 32,
                                                y_display_coordinates,
                                            ),
                                            door_sprite_type_A[1],
                                        )
                                    )
                                    identifier = SpriteIdentifier.NONE
                        case "u":
                            match identifier:
                                case SpriteIdentifier.TURRET:
                                    enemy_turret_list.append(
                                        Turret(
                                            (
                                                x_display_coordinates - 32,
                                                y_display_coordinates,
                                            ),
                                            "up",
                                            enemy_turret_facing_sprites_type_A,
                                        )
                                    )
                                    identifier = SpriteIdentifier.NONE
                        case "d":
                            match identifier:
                                case SpriteIdentifier.TURRET:
                                    enemy_turret_list.append(
                                        Turret(
                                            (
                                                x_display_coordinates - 32,
                                                y_display_coordinates,
                                            ),
                                            "down",
                                            enemy_turret_facing_sprites_type_A,
                                        )
                                    )
                                    identifier = SpriteIdentifier.NONE
                        case "l":
                            match identifier:
                                case SpriteIdentifier.TURRET:
                                    enemy_turret_list.append(
                                        Turret(
                                            (
                                                x_display_coordinates - 32,
                                                y_display_coordinates,
                                            ),
                                            "left",
                                            enemy_turret_facing_sprites_type_A,
                                        )
                                    )
                                    identifier = SpriteIdentifier.NONE
                        case "r":
                            match identifier:
                                case SpriteIdentifier.TURRET:
                                    enemy_turret_list.append(
                                        Turret(
                                            (
                                                x_display_coordinates - 32,
                                                y_display_coordinates,
                                            ),
                                            "right",
                                            enemy_turret_facing_sprites_type_A,
                                        )
                                    )
                                    identifier = SpriteIdentifier.NONE

                if identifier == SpriteIdentifier.NONE:
                    x_display_coordinates += 32

            y_display_coordinates += 32
            x_display_coordinates = 0

    level_layout_read(level_layout[0])
    level_layout_read(level_layout[1])

    # Time checking for enemy
    def check_time_passed():
        enemy_shoots_sound.set_volume(0.3)
        actual_time = time.time()
        global last_time
        time_has_passed = actual_time > last_time + 1
        if time_has_passed:
            for enemy_turret_object in enemy_turret_list:
                bullets_shot_by_enemy_turret.append(Bullet(
                    (
                        enemy_turret_object.rect.x + enemy_turret_object.rect.width // 2,
                        enemy_turret_object.rect.y + enemy_turret_object.rect.height // 2
                    ),
                    enemy_turret_object.facing_state,
                    "Fairy",
                ))
            enemy_shoots_sound.play()
            last_time = time.time()

    # Display
    def redraw_game_window():
        game.blit(generic_background, (0, 0))

        check_time_passed()

        for terrain_object in terrain_list:
            terrain_object.object_draw(game)

        for wall_object in wall_list:
            wall_object.object_draw(game)

        for door_object in door_list:
            door_object.object_draw(game)

        for coin_object in coin_list:
            coin_object.object_draw(game)

        for accesory_object in accesory_list:
            accesory_object.object_draw(game)

        for enemy_turret_object in enemy_turret_list:
            enemy_turret_object.object_draw(game)

        for bullet_object in bullets_shot_by_player:
            bullet_object.bullet_shots(game)

        for bullet_object in bullets_shot_by_enemy_turret:
            bullet_object.bullet_shots(game)

        rikako.draw(game)

        coin_score_string = str(coin_score)
        health_points_string = str(health_points)

        coin_score_display_text = comic_sans_font_28.render(
            "Coins:" + coin_score_string, True, (0, 0, 0)
        )
        health_points_display_text = comic_sans_font_28.render(
            "Health: " + health_points_string, True, (0, 0, 0)
        )
        lost_display_text_1 = comic_sans_font_56.render(
            "PERDISTE D:", True, (0, 0, 0))
        win_display_text_1 = comic_sans_font_56.render(
            "GANASTE :D", True, (0, 0, 0))

        game.blit(coin_score_display_text, (320, -5))
        game.blit(health_points_display_text, (32, -5))

        if len(enemy_turret_list) == 0 and len(coin_list) == 0:
            game.blit(win_display_text_1, (160, 160))

        if health_points <= 0:
            player_dies_sound.play()
            game.blit(lost_display_text_1, (160, 160))

        pygame.display.flip()

    # Main Loop
    run = True
    while run:
        # FPS
        clock.tick(60)
        # Exit
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False
                pygame.quit()

        # Bullet movement and colliding
        for bullet_object in bullets_shot_by_player:
            for wall_object in wall_list:
                if bullet_object.rect.colliderect(wall_object.rect):
                    bullets_shot_by_player.pop(
                        bullets_shot_by_player.index(bullet_object)
                    )

            for enemy_turret_object in enemy_turret_list:
                if bullet_object.rect.colliderect(enemy_turret_object.rect):
                    enemy_dies_sound.play()
                    bullets_shot_by_player.pop(
                        bullets_shot_by_player.index(bullet_object)
                    )
                    enemy_turret_list.pop(
                        enemy_turret_list.index(enemy_turret_object))

            match bullet_object.move_direction:
                case "up":
                    bullet_object.rect.y -= bullet_object.velocity
                case "down":
                    bullet_object.rect.y += bullet_object.velocity
                case "left":
                    bullet_object.rect.x -= bullet_object.velocity
                case "right":
                    bullet_object.rect.x += bullet_object.velocity

        for bullet_object in bullets_shot_by_enemy_turret:
            for wall_object in wall_list:
                if bullet_object.rect.colliderect(wall_object.rect):
                    bullets_shot_by_enemy_turret.pop(
                        bullets_shot_by_enemy_turret.index(bullet_object)
                    )

            if bullet_object.rect.colliderect(rikako.rect):
                player_gets_shooted_sound.play()
                health_points -= 25
                bullets_shot_by_enemy_turret.pop(
                    bullets_shot_by_enemy_turret.index(bullet_object)
                )

            match bullet_object.move_direction:
                case "up":
                    bullet_object.rect.y -= bullet_object.velocity
                case "down":
                    bullet_object.rect.y += bullet_object.velocity
                case "left":
                    bullet_object.rect.x -= bullet_object.velocity
                case "right":
                    bullet_object.rect.x += bullet_object.velocity

        # if not player_stun:
        detected_key_pressing = pygame.key.get_pressed()

        # Speed Up
        if detected_key_pressing[pygame.K_x]:
            rikako.velocity = 4
        else:
            rikako.velocity = 2

        # Shooting
        cooldown_tracker += clock.get_time()
        if detected_key_pressing[pygame.K_z]:
            player_shoots_sound.set_volume(1)
            if cooldown_tracker > 170:
                cooldown_tracker = 0
                if len(bullets_shot_by_player) <= 10:
                    bullets_shot_by_player.append(
                        Bullet(
                            (
                                rikako.rect.x + rikako.rect.width // 2,
                                rikako.rect.y + rikako.rect.height // 2,
                            ),
                            rikako.facing,
                            "Rikako",
                        )
                    )
                    player_shoots_sound.play()

        collider_list = [wall_list, coin_list, enemy_turret_list]

        # Movement keys
        if detected_key_pressing[pygame.K_UP]:
            rikako.move_detector(0, rikako.velocity * -1, collider_list)
            rikako.facing = "up"
            rikako.standing_state = False

        elif detected_key_pressing[pygame.K_DOWN]:
            rikako.move_detector(0, rikako.velocity, collider_list)
            rikako.facing = "down"
            rikako.standing_state = False

        elif detected_key_pressing[pygame.K_LEFT]:
            rikako.move_detector(rikako.velocity * -1, 0, collider_list)
            rikako.facing = "left"
            rikako.standing_state = False

        elif detected_key_pressing[pygame.K_RIGHT]:
            rikako.move_detector(rikako.velocity, 0, collider_list)
            rikako.facing = "right"
            rikako.standing_state = False

        else:
            rikako.standing_state = True

        if isinstance(rikako.successful_collide, Coin):
            coin_get_sound.play()
            coin_score += 1
            coin_list.remove(rikako.successful_collide)
        elif isinstance(rikako.successful_collide, Turret):
            player_dies_sound.play()
            health_points = 0

        # Keep player inside the screen
        rikako.rect.clamp_ip(game_rect)

        redraw_game_window()

        # Win condition
        if len(enemy_turret_list) == 0 and len(coin_list) == 0:
            time.sleep(2)
            run = False
            return True

        elif health_points <= 0:
            time.sleep(2)
            run = False
            return False


# Wa = Pared de tipo A
# Du = Puerta de tipo A parte de arriba
# Ca = Moneda de tipo A
# Aa = Accesorio de tipo A
# Tu = Enemigo de tipo torreta mirando hacia arriba (up)
level_sample_back_layout = [
    # 1,2,3,4,5,6,7,8,9,A,B,C,D,E,F,G,H,I,J,K
    "-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.",  # 1
    "-.WaWaWaWaWaWaWaWaWaWaWaWaWaWaWaWaWaWa-.",  # 2
    "-.Wa-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.Wa-.",  # 3
    "-.Wa-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.Wa-.",  # 4
    "-.Wa-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.Wa-.",  # 5
    "-.Wa-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.Wa-.",  # 6
    "-.Wa-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.Wa-.",  # 7
    "-.Wa-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.Wa-.",  # 8
    "-.Wa-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.Wa-.",  # 9
    "-.Wa-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.Wa-.",  # A
    "-.Wa-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.Wa-.",  # B
    "-.Wa-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.Wa-.",  # C
    "-.Wa-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.Wa-.",  # D
    "-.WaWaWaWaWaWaWaWaWaWaWaWaWaWaWaWaWaWa-.",  # E
    "-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.",  # F
]
level_sample_middle_layout = []
level_sample_front_layout = [
    # 1,2,3,4,5,6,7,8,9,A,B,C,D,E,F,G,H,I,J,K
    "~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.",  # 1
    "~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.",  # 2
    "~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.",  # 3
    "~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.",  # 4
    "~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.Ca~.~.~.",  # 5
    "~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.",  # 6
    "~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.Aa~.~.",  # 7
    "~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.",  # 8
    "~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.Td~.~.~.",  # 9
    "~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.",  # A
    "~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.",  # B
    "~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.",  # C
    "~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.",  # D
    "~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.",  # E
    "~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.",  # F
]
level_sample_layout = [level_sample_back_layout, level_sample_front_layout]

level_1_back_layout = [
    # 1,2,3,4,5,6,7,8,9,A,B,C,D,E,F,G,H,I,J,K
    "-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.",  # 1
    "-.WaWaWaWaWaWaWaWaWaWaWaWaWaWaWaWaWaWa-.",  # 2
    "-.Wa-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.Wa-.",  # 3
    "-.Wa-.WaWaWaWaWa-.-.-.-.Wa-.-.-.-.-.Wa-.",  # 4
    "-.Wa-.WaWaWaWaWa-.-.-.-.Wa-.-.-.-.-.Wa-.",  # 5
    "-.Wa-.-.-.-.-.Wa-.-.-.-.Wa-.-.-.-.-.Wa-.",  # 6
    "-.WaWaWaWaWa-.Wa-.-.-.-.Wa-.-.-.-.-.Wa-.",  # 7
    "-.Wa-.-.-.Wa-.WaWaWaWaWaWa-.-.-.-.-.Wa-.",  # 8
    "-.Wa-.-.-.Wa-.Wa-.-.-.-.-.-.-.-.-.-.Wa-.",  # 9
    "-.Wa-.-.-.Wa-.Wa-.-.-.-.-.-.-.-.-.-.Wa-.",  # A
    "-.Wa-.-.-.Wa-.Wa-.-.-.-.-.-.-.-.-.-.Wa-.",  # B
    "-.Wa-.-.-.Wa-.Wa-.-.-.-.-.-.-.-.-.-.Wa-.",  # C
    "-.Wa-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.Wa-.",  # D
    "-.WaWaWaWaWaWaWaWaWaWaWaWaWaWaWaWaWaWa-.",  # E
    "-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.",  # F
]
level_1_front_layout = [
    # 1,2,3,4,5,6,7,8,9,A,B,C,D,E,F,G,H,I,J,K
    "~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.",  # 1
    "~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.",  # 2
    "~.~.~.~.~.~.TrCa~.~.~.~.~.~.~.~.~.~.~.~.",  # 3
    "~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.",  # 4
    "~.~.Ca~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.",  # 5
    "~.~.Tr~.~.~.~.~.~.~.~.~.~.TdTdTdTdTd~.~.",  # 6
    "~.~.~.~.~.~.~.~.Tl~.~.Ca~.~.~.~.~.~.~.~.",  # 7
    "~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.",  # 8
    "~.~.~.~.~.~.~.~.CaCa~.~.~.~.~.~.~.~.~.~.",  # 9
    "~.~.~.~.~.~.~.~.CaCa~.~.~.~.~.~.~.~.~.~.",  # A
    "~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.",  # B
    "~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.",  # C
    "~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.",  # D
    "~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.",  # E
    "~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.",  # F
]
level_1_layout = [level_1_back_layout, level_1_front_layout]

level_2_back_layout = [
    # 1,2,3,4,5,6,7,8,9,A,B,C,D,E,F,G,H,I,J,K
    "-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.",  # 1
    "-.WaWaWaWaWaWaWaWaWaWaWaWaWaWaWaWaWaWa-.",  # 2
    "-.Wa-.-.-.-.-.Wa-.-.-.-.Wa-.-.-.-.-.Wa-.",  # 3
    "-.Wa-.-.-.-.-.Wa-.-.-.-.Wa-.-.-.-.-.Wa-.",  # 4
    "-.Wa-.-.-.-.-.Wa-.-.-.-.Wa-.-.-.-.-.Wa-.",  # 5
    "-.Wa-.-.-.-.-.Wa-.-.-.-.Wa-.-.-.-.-.Wa-.",  # 6
    "-.WaWaWa-.-.WaWaWa-.-.WaWaWa-.-.WaWaWa-.",  # 7
    "-.Wa-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.Wa-.",  # 8
    "-.Wa-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.Wa-.",  # 9
    "-.Wa-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.Wa-.",  # A
    "-.Wa-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.Wa-.",  # B
    "-.Wa-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.Wa-.",  # C
    "-.Wa-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.Wa-.",  # D
    "-.WaWaWaWaWaWaWaWaWaWaWaWaWaWaWaWaWaWa-.",  # E
    "-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.",  # F
]
level_2_front_layout = [
    # 1,2,3,4,5,6,7,8,9,A,B,C,D,E,F,G,H,I,J,K
    "~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.",  # 1
    "~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.",  # 2
    "~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.",  # 3
    "~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.",  # 4
    "~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.",  # 5
    "~.~.CaTr~.~.Tl~.~.~.~.~.~.~.~.~.~.~.~.~.",  # 6
    "~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.",  # 7
    "~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.",  # 8
    "~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.",  # 9
    "~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.",  # A
    "~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.",  # B
    "~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.",  # C
    "~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.",  # D
    "~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.",  # E
    "~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.",  # F
]
level_2_layout = [level_2_back_layout, level_2_front_layout]

level_3_back_layout = [
    # 1,2,3,4,5,6,7,8,9,A,B,C,D,E,F,G,H,I,J,K
    "-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.",  # 1
    "-.WaWaWaWaWaWaWaWaWaWaWaWaWaWaWaWaWaWa-.",  # 2
    "-.Wa-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.Wa  ",  # 3
    "-.Wa-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.Wa  ",  # 4
    "-.Wa-.-.Wb-.-.-.-.-.-.-.-.-.-.-.-.-.Wa  ",  # 5
    "-.Wa-.-.Wa-.-.-.-.-.-.-.-.-.-.-.-.-.Wa  ",  # 6
    "-.Wa-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.Wa  ",  # 7
    "-.Wa-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.Wa  ",  # 8
    "-.Wa-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.Wa  ",  # 9
    "-.Wa-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.Wa  ",  # A
    "-.Wa-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.Wa  ",  # B
    "-.Wa-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.Wa  ",  # C
    "-.Wa-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.Wa  ",  # D
    "-.WaWaWaWaWaWaWaWaWaWaWaWaWaWaWaWaWaWa  ",  # E
    "-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.",  # F
]
level_3_front_layout = [
    # 1,2,3,4,5,6,7,8,9,A,B,C,D,E,F,G,H,I,J,K
    "~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.",  # 1
    "~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.",  # 2
    "~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.",  # 3
    "~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.",  # 4
    "~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.Ca~.~.~.",  # 5
    "~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.",  # 6
    "~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.Aa~.~.",  # 7
    "~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.",  # 8
    "~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.Td~.~.~.",  # 9
    "~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.",  # A
    "~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.",  # B
    "~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.",  # C
    "~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.",  # D
    "~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.",  # E
    "~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.",  # F
]
level_3_layout = [level_3_back_layout, level_3_front_layout]

levels_list = [level_1_layout, level_2_layout, level_3_layout]


def check_time_passed():
    actual_time = time.time()
    global last_time
    time_has_passed = actual_time > last_time + 1
    if time_has_passed:
        last_time = time.time()


def redraw_game_window():
    game.blit(generic_background, (0, 0))
    for button in buttons_list:
        button.draw(game, mouse_position, comic_sans_font_28)
    pygame.display.flip()


buttons_list.append(Button(32, 32, 160, 64, (0, 0, 0),
                    (255, 255, 255), "Nivel 1 :D"))
buttons_list.append(Button(32, 128, 160, 64, (0, 0, 0),
                    (255, 255, 255), "Nivel 2 :D"))
buttons_list.append(Button(32, 224, 160, 64, (0, 0, 0),
                    (255, 255, 255), "Nivel 3 :D"))
buttons_list.append(
    Button(320, 320, 220, 64, (0, 0, 0), (255, 255, 255), "Borrar Guardado")
)

run = True
while run:
    # FPS
    clock.tick(30)
    # Exit
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False

    save_file.seek(0)
    save_state = save_file.readlines()

    buttons_list_length = len(buttons_list) - 2
    for buttons_list_index, x in enumerate(buttons_list):
        if (
            buttons_list[buttons_list_index].rect.x < mouse_position[0] and buttons_list[buttons_list_index].rect.y < mouse_position[1] and buttons_list[buttons_list_index].rect.right > mouse_position[0] and buttons_list[buttons_list_index].rect.bottom > mouse_position[1]
        ):
            mouse_click = mouse.get_pressed()
            if mouse_click[0] and buttons_list_length < buttons_list_index:
                save_file.seek(0)
                for save_entry in default_save_file:
                    non_list_save_file_default += save_entry
                save_file.write(non_list_save_file_default)
                save_file.truncate()
                non_list_save_file_default = ""
            elif mouse_click[0] and buttons_list_length >= buttons_list_index:
                if buttons_list_index == 0:
                    levels_state_list[buttons_list_index] = stage_builder(
                        levels_list[buttons_list_index]
                    )
                    time.sleep(0.1)
                else:
                    if (
                        save_state[buttons_list_index - 1] == complete_save_file[buttons_list_index - 1]
                    ):
                        levels_state_list[buttons_list_index] = stage_builder(
                            levels_list[buttons_list_index]
                        )
                        time.sleep(0.1)

    mouse_position = mouse.get_pos()

    for levels_state_list_index, x in enumerate(levels_state_list):
        if levels_state_list[levels_state_list_index]:
            if (save_state[levels_state_list_index] == default_save_file[levels_state_list_index]):
                save_file.seek(levels_state_list_index * 16)
                save_file.write(complete_save_file[levels_state_list_index])
                save_file.seek(0, 2)
                save_file.truncate()
                levels_state_list[levels_state_list_index] = False

    check_time_passed()
    redraw_game_window()

pygame.quit()
