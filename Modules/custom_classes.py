from enum import Enum
import pygame


class SpriteIdentifier(Enum):
    NONE = 0
    TERRAIN = 1
    WALL = 2
    COIN = 3
    DOOR = 4
    ACCESORY = 5
    TURRET = 6
    BLANK = 7


class ColliderReturn(Enum):
    WALL = 1
    COIN = 2
    TURRET = 3


class Button(object):
    def __init__(self, x, y, width, height, color1, color2, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.color1 = color1
        self.color2 = color2
        self.text = text

    def draw(self, game, mousePos, comic_sans_font_28):
        if self.rect.x < mousePos[0] and self.rect.y < mousePos[1] and self.rect.right > mousePos[0] and self.rect.bottom > mousePos[1]:
            self.show = comic_sans_font_28.render(self.text, True, self.color2)
            game.fill(self.color1, self.rect)
            game.blit(self.show, self.rect)
        else:
            self.show = comic_sans_font_28.render(self.text, True, self.color1)
            game.fill(self.color2, self.rect)
            game.blit(self.show, self.rect)


class Wall(object):
    # Initiate and creating the walls list
    def __init__(self, display_coordinates, object_sprite):
        self.rect = pygame.Rect(
            display_coordinates[0], display_coordinates[1], 28, 28)
        self.sprite = object_sprite

    def object_draw(self, game):
        game.blit(self.sprite, (self.rect.x, self.rect.y))


class Terrain(object):
    def __init__(self, display_coordinates, object_sprite):
        self.rect = pygame.Rect(
            display_coordinates[0], display_coordinates[1], 28, 28)
        self.sprite = object_sprite

    def object_draw(self, game):
        game.blit(self.sprite, (self.rect.x, self.rect.y))


class Coin(object):
    # Initiate and create the coins list
    def __init__(self, display_coordinates, object_sprite):
        self.rect = pygame.Rect(
            display_coordinates[0], display_coordinates[1], 28, 28)
        self.sprite = object_sprite

    def object_draw(self, game):
        game.blit(self.sprite, (self.rect.x, self.rect.y))


class Bullet(object):
    # Initiate the bullets, detect the shooter and add them to the list
    def __init__(self, display_coordinates, shooter_facing_state, shooters_identity):
        self.velocity = 5
        self.move_direction = shooter_facing_state
        self.bullet_radius = 5
        self.rect = pygame.Rect(
            display_coordinates[0], display_coordinates[1], 5, 5)

        match shooters_identity:
            case "Rikako":
                self.bullet_color = (255, 0, 255)

            case "Fairy":
                self.bullet_color = (0, 255, 0)

        # Display the bullets
    def bullet_shots(self, game):
        pygame.draw.circle(game, self.bullet_color, (self.rect.x, self.rect.y), self.bullet_radius, self.rect.width)


class Turret(object):
    # Initiate and create the Turrets/Enemy list
    def __init__(self, display_coordinates, facing_state, object_sprites):
        self.rect = pygame.Rect(
            display_coordinates[0], display_coordinates[1], 28, 28)
        self.facing_state = facing_state
        self.sprite = object_sprites

    def object_draw(self, game):
        match self.facing_state:
            case "up":
                game.blit(self.sprite[0], (self.rect.x, self.rect.y))
            case "down":
                game.blit(self.sprite[1], (self.rect.x, self.rect.y))
            case "left":
                game.blit(self.sprite[2], (self.rect.x, self.rect.y))
            case "right":
                game.blit(self.sprite[3], (self.rect.x, self.rect.y))


class Door(object):
    def __init__(self, display_coordinates, object_sprite):
        self.rect = pygame.Rect(
            display_coordinates[0], display_coordinates[1], 28, 28)
        self.sprite = object_sprite

    def object_draw(self, game):
        game.blit(self.sprite, (self.rect.x, self.rect.y))


class Accesory(object):
    def __init__(self, display_coordinates, object_sprite):
        self.rect = pygame.Rect(
            display_coordinates[0], display_coordinates[1], 28, 28)
        self.sprite = object_sprite

    def object_draw(self, game):
        game.blit(self.sprite, (self.rect.x, self.rect.y))


class Player(object):
    # Initiate the player
    def __init__(self, animation_up_sprites, animation_down_sprites, animation_left_sprites, animation_right_sprites):
        self.rect = pygame.Rect(96, 224, 32, 32)
        self.walk_animation_count = 0
        self.standing_state = True
        self.facing = "down"
        self.velocity = 2
        self.successful_collide = 0
        self.animation_up_sprites = animation_up_sprites
        self.animation_down_sprites = animation_down_sprites
        self.animation_left_sprites = animation_left_sprites
        self.animation_right_sprites = animation_right_sprites

    # Detect key pressing for movement
    def move_detector(self, difference_in_x, difference_in_y, collider_list):
        if difference_in_x != 0:
            self.move_in_axis(difference_in_x, 0, collider_list)
        if difference_in_y != 0:
            self.move_in_axis(0, difference_in_y, collider_list)

    # Make the player move and detect collides
    def move_in_axis(self, difference_in_x, difference_in_y, collider_list):
        self.successful_collide = 1
        self.rect.x += difference_in_x
        self.rect.y += difference_in_y
        for wall_object in collider_list[0]:
            if self.rect.colliderect(wall_object.rect):
                if difference_in_x > 0:
                    self.rect.right = wall_object.rect.left
                if difference_in_x < 0:
                    self.rect.left = wall_object.rect.right
                if difference_in_y > 0:
                    self.rect.bottom = wall_object.rect.top
                if difference_in_y < 0:
                    self.rect.top = wall_object.rect.bottom

        for coin_object in collider_list[1]:
            if self.rect.colliderect(coin_object.rect):
                self.successful_collide = coin_object

        for enemy_turret_object in collider_list[2]:
            if self.rect.colliderect(enemy_turret_object.rect):
                self.successful_collide = enemy_turret_object

    # Display the player
    def draw(self, game):
        self.animation_state = 0
        if self.walk_animation_count >= 6:
            self.walk_animation_count = 0

        match self.walk_animation_count:
            case 0 | 1:
                self.animation_state = 0
            case 2 | 3:
                self.animation_state = 1
            case 4 | 5:
                self.animation_state = 2
        if self.standing_state:
            match self.facing:
                case "up":
                    game.blit(
                        self.animation_up_sprites[1],
                        (self.rect.x, self.rect.y),
                    )
                case "down":
                    game.blit(
                        self.animation_down_sprites[1],
                        (self.rect.x, self.rect.y),
                    )
                case "left":
                    game.blit(
                        self.animation_left_sprites[1],
                        (self.rect.x, self.rect.y),
                    )
                case "right":
                    game.blit(
                        self.animation_right_sprites[1],
                        (self.rect.x, self.rect.y),
                    )

        else:
            match self.facing:
                case "up":
                    game.blit(
                        self.animation_up_sprites[self.animation_state],
                        (self.rect.x, self.rect.y),
                    )
                    self.walk_animation_count += 1
                case "down":
                    game.blit(
                        self.animation_down_sprites[
                            self.animation_state
                        ],
                        (self.rect.x, self.rect.y),
                    )
                    self.walk_animation_count += 1
                case "left":
                    game.blit(
                        self.animation_left_sprites[
                            self.animation_state
                        ],
                        (self.rect.x, self.rect.y),
                    )
                    self.walk_animation_count += 1
                case "right":
                    game.blit(
                        self.animation_right_sprites[
                            self.animation_state
                        ],
                        (self.rect.x, self.rect.y),
                    )
                    self.walk_animation_count += 1
