__author__ = 'Malibu'
import pygame
from creeps import *
from pygame.locals import *


DIRECT_DICT = {pygame.K_LEFT : (-1, 0),
pygame.K_RIGHT : ( 1, 0),
pygame.K_UP : ( 0,-1),
pygame.K_DOWN : ( 0, 1)}

class Pyrogue(object):
    def __init__(self, screen_size, screen):
        self.all_sprites_group = pygame.sprite.Group()
        self.creep_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.wall_sprites_group = pygame.sprite.Group()
        self.background_surface = self.generate_background(screen_size)
        self.generate_walls(screen_size, [32,32])
        self.player = Player(((screen_size[0]/2)-16, (screen_size[1]/2)-16), "Knight.png")
        self.player_group.add(self.player)
        self.all_sprites_group.add(self.player)
        self.creep_group.add(self.generate_creep((112, 112)))
        self.all_sprites_group.add(self.creep_group)
        self.text_sprites_group = pygame.sprite.Group()
        self.all_sprites_group.add(self.text_sprites_group)
        self.combat = Combat()
        self.player.game = self
        self.keys = pygame.key.get_pressed();
        pygame.key.set_repeat(50, 100)
        self.game_over = False

    def process_events(self):
        # for event in pygame.event.get():
        #     self.keys = pygame.key.get_pressed()
        #     if event.type == pygame.QUIT or self.keys[pygame.K_ESCAPE]:
        #         return True
        # return False

        for event in pygame.event.get():
            if event.type == QUIT: return True
            if not hasattr(event, 'key'): continue
            if event.type == KEYDOWN: self.player.speed = 32
            if event.key == K_RIGHT: self.player.set_direction((1,0))
            elif event.key == K_LEFT: self.player.set_direction((-1,0))
            elif event.key == K_UP: self.player.set_direction((0,-1))
            elif event.key == K_DOWN: self.player.set_direction((0,1))
        return False

    def run_logic(self):
        self.all_sprites_group.update(*self.keys)
        if self.player.dead():
            self.game_over = True;


    def display_frame(self, screen):
        self.all_sprites_group.clear(screen, self.background_surface)
        self.all_sprites_group.draw(screen)
        pygame.display.flip()


    def generate_background(self, size):
        background_tile = pygame.image.load("DK_GY_FLOOR.png").convert()
        tile_size = background_tile.get_size()
        background_surface = pygame.Surface(size)
        for x in range(0, size[0], tile_size[0]):
            for y in range(0, size[1], tile_size[1]):
                background_surface.blit(background_tile, [x,y])
        return background_surface

    def display_background(self, screen):
        screen.blit(self.background_surface, [0,0])

    def generate_walls(self, screen_bounds, wall_size):
        for x in range(0, screen_bounds[0], wall_size[0]):
            new_wall = Wall()
            new_wall.rect.x = x
            new_wall.rect.y = 0
            self.wall_sprites_group.add(new_wall)
            self.all_sprites_group.add(new_wall)
            new_wall = Wall()
            new_wall.rect.x = x
            new_wall.rect.y = screen_bounds[1]-wall_size[1]
            self.wall_sprites_group.add(new_wall)
            self.all_sprites_group.add(new_wall)
        for y in range(0, screen_bounds[1], wall_size[1]):
            new_wall = Wall()
            new_wall.rect.x = 0
            new_wall.rect.y = y
            self.wall_sprites_group.add(new_wall)
            self.all_sprites_group.add(new_wall)
            new_wall = Wall()
            new_wall.rect.x = screen_bounds[0]-wall_size[0]
            new_wall.rect.y = y
            self.wall_sprites_group.add(new_wall)
            self.all_sprites_group.add(new_wall)

    def generate_creep(self, position):
        new_creep = Creep(position, "Knight.png")
        return new_creep

