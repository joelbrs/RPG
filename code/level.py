import pygame
from settings import *
from tile import Tile
from player import Player

class Level:
    def __init__(self):

        #sprite group setup:
        self.visible_sprites = YSortCameraGroup()
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
                    self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites) #ou seja, colocamos o personagem dentro do grupo das sprites visíveis e estamos atribuindo a ele o grupo dos obstáculos para fim das colisões 

    def run(self):
        #update and draw the game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()


class YSortCameraGroup(pygame.sprite.Group): #ou seja, a câmera do jogo seráordenada de acordo com a coordenada y
    def __init__(self):

        #general setup:
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
    

    def custom_draw(self, player):

        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)


