from image_capture import capture, save
from drone_init import _takeoff, _land
import pygame
import time
import sys

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Drone Control")
pygame.key.stop_text_input()
clock = pygame.time.Clock()

def keyboard():
    for op in pygame.event.get():
        pass

    key = pygame.key.get_pressed()
    if key[pygame.K_a]: #left
        return "a"
    elif key[pygame.K_d]: #right
        return "d"
    elif key[pygame.K_w]: #forward
        return "w"
    elif key[pygame.K_s]: #backward
        return "s"
    elif key[pygame.K_z]: #up
        return "z"
    elif key[pygame.K_x]: #down
        return "x"
    elif key[pygame.K_q]: #left rotate
        return "q"
    elif key[pygame.K_e]: #right rotate
        return "e"

    if key[pygame.K_ESCAPE]:
        _land()
    if key[pygame.K_t]:
        _takeoff()
    if key[pygame.K_p]:
        save()
        time.sleep(0.2)

def update_display():
    screen.fill((0, 0, 0))
    pygame.display.update()
    clock.tick(60)