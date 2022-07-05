import pygame
from settings import *

class Player(pygame.sprite.Sprite):

    def __init__(self, pos, groups, obstacle_sprites): #o position é justamente pq iremos ter que encontrar posições/coordenadas para os objetos no nosso jogo
        super().__init__(groups) #utilizamos toda vez que vamos iniciar uma classe "Sprite"
        self.image = pygame.image.load('graphics/player/move/down/0.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

        self.direction = pygame.math.Vector2() #isso nos dá um vetor que vai possuir um x e um y em que, por padrão os dois serão zero e, a partir disso, iremos configurar o nosso programa para utilizarmos o teclado do nosso computador para mudar esses números de x e y e mover nosso personagem
        self.speed = 5 #como o próprio nome já diz, essa variável será a velocidade, em pixels,que meu personagem vai andar 

        self.obstacle_sprites = obstacle_sprites #para tratarmos sobre colisões no jogo, é importante que o personagem saiba identifucar no mapa onde os obstáculos estão, e, para isso, adicionamos o argumento "obstacle_sprites" para a classe


    def input(self): #aqui vamos configurar a entrada do teclado em nosso programa e o que determinada tecla vai fazer
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.direction.y = -1 #aqui, devemos lembrar que o plano cartesiano em python funciona de maneira contrária ao usual, ao menos no eixo y, onde o eixo acima das abscissas (x) é negativo e abaixo é positivo
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0 #aqui, utilizamos esse "else" para zerar o "direction.y", pois, ao pressionarmos qualquer uma das teclas configuradas acima, seu valor vai mudar e o personagem irá se mover na tela, porém, sem uma configuração pré-definida, a partir do momento que soltássemos a tecla, o personagem continuaria seguindo, então para corrigir isso, criamos esse "else" para pararmos o personagem assim que soltarmos a tecla

        if keys[pygame.K_a]:
            self.direction.x = -1 
        elif keys[pygame.K_d]:
            self.direction.x = 1
        else:
            self.direction.x = 0


    def move(self, speed): #essa é a função onde, de fato, o personagem irá se mover, para isso, utilizamos como atributo o "self.speed" que colocamos no código acima
        if self.direction.magnitude() != 0: #ou seja, se o tamanho do nosso vetor "direction" tiver tamanho diferente de 0, será atribuído a ele o tamanho de 1 ao vetor, isso se aplica a casos em que pressionamor duas teclas ao mesmo tempo para mover o personagem, por exemplo, para a direção nordeste, onde o vetor vai ter tamanho superior a 1 e, consequentemente, o personagem se moveria mais rápido do que deveria (tendo em vista que multiplicamos a direção do personagem com a velocidade para conseguirmos movê-lo)
            self.direction = self.direction.normalize()
        
        #abaixo: pegamoss o retângulo do meu personagem (e o divide em eixos x e y) e atribui a ele a soma entre o próprio eixo do retângulo e a multipliação entre a direção (em x e y) ao qual meu personagem vai andar (de acordo com determinada tecla que eu apertar) com a velocidade, em pixels, que atribímos a tal variável
        self.rect.x += self.direction.x * speed
        self.collision('horizontal')
        self.rect.y += self.direction.y * speed
        self.collision('vertical')


    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites: #a cada sprite presente em "obstacle_sprites"
                if sprite.rect.colliderect(self.rect): #basicamente estamos checando se o retângulo do sprite do obstáculo e o sprite do personagem colidiram
                    if self.direction.x > 0: #movendo para a direita
                        self.rect.right = sprite.rect.left #ou seja, quando o personagem está se movendo para a direita e colide com o objeto (geralmente no lado esquerdo do objeto), normalmente esse objeto o sobrepõe, porém, ao utilizarmos esse parâmetro, fazemos com que nosso personagem (que agora está sobreposto pelo objeto) se move para o lado esquerdo do objeto ao qual "colidiu"
                    if self.direction.x < 0: #movendo para a esquerda
                        self.rect.left = sprite.rect.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.y > 0: #moving down
                        self.rect.bottom = sprite.rect.top
                    if self.direction.y < 0: #moving up
                        self.rect.top = sprite.rect.bottom

    def update(self):
        self.input()
        self.move(self.speed)