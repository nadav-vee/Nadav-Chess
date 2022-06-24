from client import main_screen
import pygame


def main():
    pygame.init()
    pygame.font.init()
    cl = main_screen()
    cl.start()

main()