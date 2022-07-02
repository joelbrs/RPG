import pygame
from settings import *
from tile import Tile
from player import Player

class Level:
    def __init__(self):
        
        #get the display surface
        self.display_surface = pygame.display.get_surface()

        #sprite group setup:
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()

        #sprite setup:
        self.create_map()

    def create_map(self):
        for row_index, row in enumerate(WORLD_MAP): #para cada "linha" do "WORLD_MAP", vamos precisar do index de cada uma, já que podemos perceber brevemente que esta é um vetor, para isso, utilizamos a função "enumerate"
            for col_index, col in enumerate(row): #cada loop desses existe para que possamos calcular e encontrar os eixos x e y do "WORLD_MAP", possibilitando fazer as adições necessárias no mapa sem tantos problemas
                x = col_index * TILESIZE #a posição x do mapa é igual à linha multiplicado pelo "TILESIZE" de settings
                y = row_index * TILESIZE

                if col == 'x':
                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites])
                if col == 'p':
                    Player((x, y), [self.visible_sprites], self.obstacle_sprites) #ou seja, colocamos o personagem dentro do grupo das sprites visíveis e estamos atribuindo a ele o grupo dos obstáculos para fim das colisões 

    def run(self):
        #update and draw the game
        self.visible_sprites.draw(self.display_surface)
        self.visible_sprites.update()

