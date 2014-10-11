__author__ = 'Malibu'
import pygame
from creeps import *
from pygame.locals import *
import random

TILE_SIZE = 32
DIRECT_DICT = {pygame.K_LEFT : (-1, 0),
pygame.K_RIGHT : ( 1, 0),
pygame.K_UP : ( 0,-1),
pygame.K_DOWN : ( 0, 1)}

class Pyrogue(object):
    def __init__(self, screen_size, screen):
        l = Level((54,30))
        self.all_sprites_group = pygame.sprite.Group()
        self.creep_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.wall_sprites_group = pygame.sprite.Group()

        self.wall_sprites_group.add(l.get_wall())
        self.background_surface = self.generate_background(screen_size)
        #self.generate_walls(screen_size, [TILE_SIZE, TILE_SIZE])
        self.player = Player(((screen_size[0]/2)-TILE_SIZE/2, (screen_size[1]/2)-TILE_SIZE/2), "Knight.png")
        self.player_group.add(self.player)
        self.all_sprites_group.add(self.player)
        self.creep_group.add(self.generate_creep((112, 112)))
        self.all_sprites_group.add(self.creep_group)
        self.text_sprites_group = pygame.sprite.Group()
        self.all_sprites_group.add(self.text_sprites_group)
        self.all_sprites_group.add(self.wall_sprites_group)
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
            if event.type == KEYDOWN: self.player.speed = TILE_SIZE
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

    # def generate_walls(self, screen_bounds, wall_size):
    #     for x in range(0, screen_bounds[0], wall_size[0]):
    #         new_wall = Wall()
    #         new_wall.rect.x = x
    #         new_wall.rect.y = 0
    #         self.wall_sprites_group.add(new_wall)
    #         self.all_sprites_group.add(new_wall)
    #         new_wall = Wall()
    #         new_wall.rect.x = x
    #         new_wall.rect.y = screen_bounds[1]-wall_size[1]
    #         self.wall_sprites_group.add(new_wall)
    #         self.all_sprites_group.add(new_wall)
    #     for y in range(0, screen_bounds[1], wall_size[1]):
    #         new_wall = Wall()
    #         new_wall.rect.x = 0
    #         new_wall.rect.y = y
    #         self.wall_sprites_group.add(new_wall)
    #         self.all_sprites_group.add(new_wall)
    #         new_wall = Wall()
    #         new_wall.rect.x = screen_bounds[0]-wall_size[0]
    #         new_wall.rect.y = y
    #         self.wall_sprites_group.add(new_wall)
    #         self.all_sprites_group.add(new_wall)

    def generate_creep(self, position):
        new_creep = Creep(position, "Knight.png")
        return new_creep

class Level(object):

    def __init__(self, size):
        self.rooms = []
        self.size = size
        x,y = size
        rx, ry = self.room_size = (18, 15)
        self.num_rooms = (x * y) // (rx * ry)
        for i in range (self.num_rooms):
            self.rooms.append(self.generate_room())

    def draw(self):
        pass

    def get_wall(self):
        walls = pygame.sprite.Group()
        room_size_x, room_size_y = self.room_size
        lev_size_x, lev_size_y = self.size
        rooms_across = lev_size_x//room_size_x
        rooms_down = lev_size_y // room_size_y
        for i in range(0,rooms_down):
            for j in range(0,rooms_across):
                walls.add(self.draw_room(self.rooms[(i*rooms_across)+j], (j*room_size_x, i * room_size_y)))
        # for r in range(0,6):
        #     walls.add(self.draw_room(self.rooms[r], (r*room_size_x,0)))
        # for r in range(6, 12):
        #     walls.add(self.draw_room(self.rooms[r], ((r-6)*room_size_x, room_size_y)))
        return walls

    def generate_room(self):
        room_size_x, room_size_y = self.room_size
        room = [[0 for i in range(room_size_x)] for j in range(room_size_y)]
        start_index = (room_size_x // 2, room_size_y // 2)
        i = room_size_x * room_size_y // 1.3
        in_corner = False
        while i > 0 and not in_corner:
            x,y = start_index
            valid_moves = [(0,1), (0,-1), (1,0), (-1,0)]
            possible_moves = []
            for m in valid_moves:
                mx, my = m
                if (y + my) >=1 and (y + my) < room_size_x-1 and (x + mx) >= 1 and (x + mx) < room_size_y-1:
                    if room[x + mx][y + my] == 0:
                        possible_moves.append(m)
            if possible_moves:
                next_move = random.choice(possible_moves)
                nx,ny = next_move
                room[x+nx][y+ny] = 1
                start_index = (x+nx,y+ny)
            else: in_corner = True
        return room


    def draw_room(self, room, top_left):
        new_room = pygame.sprite.Group()
        top_left_x, top_left_y = top_left
        for i in range(len(room)):
            for j in range(len(room[i])):
                if room[i][j] == 0:
                    new_wall = Wall()
                    new_wall.rect.x = (top_left_x * 32) + (j * 32)
                    new_wall.rect.y = (top_left_y * 32) + (i * 32)
                    new_room.add(new_wall)
        return new_room


