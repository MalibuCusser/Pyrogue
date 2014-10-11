__author__ = 'Malibu'
import pygame
import random

BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)
BLUE = (0,0,255)

DIRECT_DICT = {pygame.K_LEFT : (-1, 0),
pygame.K_RIGHT : ( 1, 0),
pygame.K_UP : ( 0,-1),
pygame.K_DOWN : ( 0, 1)}



class Creep(pygame.sprite.Sprite):
    def __init__(self, position, sprite_map):
        pygame.sprite.Sprite.__init__(self)
        self.position = position
        self.image = pygame.image.load(sprite_map).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        self.hit_points = 20
        self.attack = 4
        self.defense = 0
        self.game = None
        self.direction = (0, -1)

    def dead(self):
        return self.hit_points <=0

    def update(self, *args):
        if self.dead(): self.kill()

    def set_direction(self, direction):
        if self.direction == direction:
            return
        prev_direction = self.direction
        px, py = prev_direction
        cx, cy = direction
        tuple_add = tuple(map(sum, zip(prev_direction, direction)))
        rotate = 0
        if tuple_add == (0,0): rotate = 180
        else:
            if px == 0:
                if py == -1:
                    if cx == -1: rotate = 90
                    if cx == 1: rotate = -90
                else:
                    if cx == -1: rotate = -90
                    if cx == 1: rotate = 90
            else:
                if px == -1:
                    if cy == -1: rotate = -90
                    if cy == 1: rotate = 90
                else:
                    if cy == -1: rotate = 90
                    if cy == 1: rotate = -90
        self.image = pygame.transform.rotate(self.image, rotate)
        self.direction = direction

class Player(Creep):

    def __init__(self, position, sprite_map):
        Creep.__init__(self, position, sprite_map)
        self.speed = 0
        self.direction = (0, -1)


    def update(self, *args):
        self.prev_position = self.position
        self.move()
        self.speed = 0
        self.get_collisions()


    def move(self):
        x,y = self.position
        x += self.speed * self.direction[0]
        y += self.speed * self.direction[1]
        self.position = (x,y)
        self.rect = self.image.get_rect()
        self.rect.center = self.position


    def get_collisions(self):
        #if pygame.sprite.spritecollideany(self, self.game.wall_sprites_group):
            #self.position = self.prev_position
        combat = Combat()
        battles = pygame.sprite.spritecollide(self, self.game.creep_group, False)
        for b in battles:
            self.game.text_sprites_group.add(
                combat.battle(self, b)
            )
        self.game.all_sprites_group.add(self.game.text_sprites_group)
        if battles: self.position = self.prev_position
        self.rect.center = self.position



    def set_direction(self, direction):
        if self.direction == direction:
            return
        prev_direction = self.direction
        px, py = prev_direction
        cx, cy = direction
        tuple_add = tuple(map(sum, zip(prev_direction, direction)))
        rotate = 0
        if tuple_add == (0,0): rotate = 180
        else:
            if px == 0:
                if py == -1:
                    if cx == -1: rotate = 90
                    if cx == 1: rotate = -90
                else:
                    if cx == -1: rotate = -90
                    if cx == 1: rotate = 90
            else:
                if px == -1:
                    if cy == -1: rotate = -90
                    if cy == 1: rotate = 90
                else:
                    if cy == -1: rotate = 90
                    if cy == 1: rotate = -90
        self.image = pygame.transform.rotate(self.image, rotate)
        self.direction = direction



class Wall(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        large_image = pygame.image.load("LT_GY_WALL.png").convert()
        self.image = pygame.Surface([32,32]).convert()
        self.image.blit(large_image, (0,0), (0,0,32,32))
        self.rect = self.image.get_rect()

class CombatText(pygame.sprite.Sprite):

    def __init__(self, initial_position, text):
        pygame.sprite.Sprite.__init__(self)
        self.position = initial_position
        self.text = text
        self.font = pygame.font.SysFont('Tahoma', 18)
        self.image = self.font.render(self.text, True, (173,3,3))
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        self.fade = 30

    def update(self, *args):
        x,y = self.position
        y -=1
        self.position = (x,y)
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        self.fade -= 1
        if self.fade == 0:
            self.kill()


class Combat(object):

    def battle(self, creep1, creep2):
        dx = (creep1.prev_position[0] - creep2.position[0])/32
        dy = (creep1.prev_position[1] - creep2.position[1])/32
        creep2.set_direction((dx,dy))
        combat_text = pygame.sprite.Group()
        creep1_attack = Die(creep1.attack).roll()
        combat_text.add(CombatText(creep1.prev_position,str(creep1_attack)))
        creep2_attack = Die(creep2.attack).roll()
        combat_text.add(CombatText(creep2.position,str(creep2_attack)))
        creep1.hit_points -= creep2_attack
        creep2.hit_points -= creep1_attack
        return combat_text


class Die(object):
    def __init__(self, sides):
        self.sides = sides

    def roll(self):
        return random.randint(1, self.sides)