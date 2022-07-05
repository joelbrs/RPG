import pygame
from settings import *
from support import import_folder

class Player(pygame.sprite.Sprite):

    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack): #o position é justamente pq iremos ter que encontrar posições/coordenadas para os objetos no nosso jogo
        super().__init__(groups) #utilizamos toda vez que vamos iniciar uma classe "Sprite"
        self.image = pygame.image.load('graphics/player/down_idle/idle_down.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, -26)

        #graphics 
        self.import_player_assets()
        self.status = 'down'
        self.frame_index = 0
        self.animation_speed = 0.15
 
        #movement
        self.direction = pygame.math.Vector2() #isso nos dá um vetor que vai possuir um x e um y em que, por padrão os dois serão zero e, a partir disso, iremos configurar o nosso programa para utilizarmos o teclado do nosso computador para mudar esses números de x e y e mover nosso personagem
        self.speed = 3 #como o próprio nome já diz, essa variável será a velocidade, em pixels,que meu personagem vai andar 
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None

        self.obstacle_sprites = obstacle_sprites #para tratarmos sobre colisões no jogo, é importante que o personagem saiba identifucar no mapa onde os obstáculos estão, e, para isso, adicionamos o argumento "obstacle_sprites" para a classe

        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]


    def import_player_assets(self):
        character_path = 'graphics/player/'
        self.animations = {
            'up': [],
            'down': [],
            'left': [],
            'right': [],
            'right_idle': [],
            'left_idle': [],
            'up_idle': [],
            'down_idle': [],
            'right_attack': [],
            'left_attack': [],
            'up_attack': [],
            'down_attack': [],

        }

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def input(self): #aqui vamos configurar a entrada do teclado em nosso programa e o que determinada tecla vai fazer
        keys = pygame.key.get_pressed()

        #move
        if keys[pygame.K_w]:
            self.direction.y = -1 #aqui, devemos lembrar que o plano cartesiano em python funciona de maneira contrária ao usual, ao menos no eixo y, onde o eixo acima das abscissas (x) é negativo e abaixo é positivo
            self.status = 'up'       
        elif keys[pygame.K_s]:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0 #aqui, utilizamos esse "else" para zerar o "direction.y", pois, ao pressionarmos qualquer uma das teclas configuradas acima, seu valor vai mudar e o personagem irá se mover na tela, porém, sem uma configuração pré-definida, a partir do momento que soltássemos a tecla, o personagem continuaria seguindo, então para corrigir isso, criamos esse "else" para pararmos o personagem assim que soltarmos a tecla

        if keys[pygame.K_a]:
            self.direction.x = -1
            self.status = 'left' 
        elif keys[pygame.K_d]:
            self.direction.x = 1
            self.status = 'right'
        else:
            self.direction.x = 0
        
        #attack
        if keys[pygame.K_SPACE] and not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            self.create_attack()

    def get_status(self):

        #idle
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'

        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0  
            if not 'atack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = self.status

        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')

    def move(self, speed): #essa é a função onde, de fato, o personagem irá se mover, para isso, utilizamos como atributo o "self.speed" que colocamos no código acima
        if self.direction.magnitude() != 0: #ou seja, se o tamanho do nosso vetor "direction" tiver tamanho diferente de 0, será atribuído a ele o tamanho de 1 ao vetor, isso se aplica a casos em que pressionamor duas teclas ao mesmo tempo para mover o personagem, por exemplo, para a direção nordeste, onde o vetor vai ter tamanho superior a 1 e, consequentemente, o personagem se moveria mais rápido do que deveria (tendo em vista que multiplicamos a direção do personagem com a velocidade para conseguirmos movê-lo)
            self.direction = self.direction.normalize()
        
        #abaixo: pegamoss o retângulo do meu personagem (e o divide em eixos x e y) e atribui a ele a soma entre o próprio eixo do retângulo e a multipliação entre a direção (em x e y) ao qual meu personagem vai andar (de acordo com determinada tecla que eu apertar) com a velocidade, em pixels, que atribímos a tal variável
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center


    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites: #a cada sprite presente em "obstacle_sprites"
                if sprite.hitbox.colliderect(self.hitbox): #basicamente estamos checando se o retângulo do sprite do obstáculo e o sprite do personagem colidiram
                    if self.direction.x > 0: #movendo para a direita
                        self.hitbox.right = sprite.hitbox.left #ou seja, quando o personagem está se movendo para a direita e colide com o objeto (geralmente no lado esquerdo do objeto), normalmente esse objeto o sobrepõe, porém, ao utilizarmos esse parâmetro, fazemos com que nosso personagem (que agora está sobreposto pelo objeto) se move para o lado esquerdo do objeto ao qual "colidiu"
                    if self.direction.x < 0: #movendo para a esquerda
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0: #moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0: #moving up
                        self.hitbox.top = sprite.hitbox.bottom

    def couldowns(self):
        self.current_time = pygame.time.get_ticks()

        if self.attacking:
            if self.current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                self.destroy_attack()

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

    def update(self):
        self.input()
        self.couldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)