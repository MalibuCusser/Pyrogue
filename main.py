__author__ = 'Malibu'
import pygame
from creeps import Wall, Player
from pygame.locals import *
from pyrogue import Pyrogue

def main():
    """ Main function for the game. """
    pygame.init()
    # Set the width and height of the screen [width,height]
    size = [1728, 960]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("My Game")
    pygame.mouse.set_visible(False)
    #Loop until the user clicks the close button.
    done = False
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    game = Pyrogue(size, screen)
    game.display_background(screen)

    # -------- Main Program Loop -----------
    while not done and not game.game_over:
        done = game.process_events()
        game.run_logic()
        game.display_frame(screen)
        clock.tick(30)
    # Close the window and quit.
    # If you forget this line, the program will 'hang'
    # on exit if running from IDLE.
    pygame.quit()

if __name__ == "__main__":
    main()