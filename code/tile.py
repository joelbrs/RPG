import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups): #o position é justamente pq iremos ter que encontrar posições/coordenadas para os objetos no nosso jogo
        super().__init__(groups) #utilizamos toda vez que vamos iniciar uma classe "Sprite"
        self.image = pygame.image.load('tilemap/rock.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect(topleft = pos)