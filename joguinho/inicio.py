import pygame
import os
import random

largura_da_tela = 500
ultura_da_tela = 800

#aqui sao as imagens do joguinho
imagens_dos_canos = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
imagen_do_chao = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
imagens_de_fundo = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))
imagen_do_passaro = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png')))
]

pygame.font.init()
fonte_de_pontos = pygame.font.SysFont('arial', 50)

class Passaro:
    """esse objeto é a animacao do passaro"""
    imgs = imagen_do_passaro
    rotacao = 25
    velocidade = 20
    tenpo_de_animacao = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagen_da_imagen = 0
        self.imagen = self.imgs[0]
    
    # culculando o pulo do passarinho
    def pular(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y

    #dando limites para o passarinho
    def mover(self):
    # calculando o deslocamento
        self.tempo += 1
        deslocamento = 1.5 * (self.tempo**2) + self.velocidade * self.tempo  #(S=so+vot+ta**2/2)
    # retingindo o deslocamento
        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2

        self.y += deslocamento
    # o angulo do passaro
        if deslocamento < 0 or self.y < (self.altura + 50):
            if self.angulo < self.rotacao:
                self.angulo = self.rotacao
        else:
            if self.angulo > -90:
                self.angulo -= self.velocidade

    #desenhando o passarinho
    def desenha(self, tela):
    #qual imagen inicial usar
        self.contagen_da_imagen += 1 

        if self.contagen_da_imagen < self.tenpo_de_animacao:
            self.imagen = self.imgs[0]
        elif self.contagen_da_imagen < self.tenpo_de_animacao*2:
            self.imagen = self.imgs[1]
        elif self.contagen_da_imagen < self.tenpo_de_animacao*3:
            self.imagen = self.imgs[3]
        elif self.contagen_da_imagen < self.tenpo_de_animacao*4:
            self.imagen = self.imgs[1]
        if self.contagen_da_imagen >= self.tenpo_de_animacao*4 + 1:
            self.imagen = self.imgs[0]
            self.contagen_da_imagen = 0

    #qual o a imagen usar quando o passaro estiver caindo
        if self.angulo <= -80:
            self.imagen = self.imgs[1]
            self.contagen_da_imagen = self.tenpo_de_animacao*2

    # desenhar a imagen
        imagem_rotacionada = pygame.transform.rotate(self.imagen, self.angulo)
        pos_centro_imagem = self.imagen.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagem_rotacionada.get_rect(center=pos_centro_imagem)
        tela.blit(imagem_rotacionada, retangulo.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.imagen)

class Canos:
    """nesce objeto vou distanciar os canos"""

    deslocamento = 200
    velocidade = 5

    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.topo = 0
        self.base = 0
        self.cano_topo = pygame.transform.flip(imagens_dos_canos, False, True)
        self.cano_base = imagens_dos_canos
        self.passou = False
        self.definir_altura()
    
    def definir_altura(self):
        """definindo altura do cano do topo e da base"""
        self.altura = random.randrange(50, 450)
        self.pos_topo = self.altura - self.cano_topo.get_height()
        self.pos_base = self. altura + self.deslocamento

    def mover(self): 
        self.x -= self.velocidade

    def desenhar(self, tela):
        tela.blit(self.cano_topo, (self.x, self.pos_topo))
        tela.blit(self.cano_base, (self.x, self.pos_base))

    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.cano_topo)
        base_mask = pygame.mask.from_surface(self.cano_base)

        dislocamento_do_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        dislocamento_da_base = (self.x - passaro.x, self.pos_base - round(passaro.y))

        topo_ponto = passaro_mask.overlap(topo_mask, dislocamento_do_topo)
        base_ponto = passaro_mask.overlap(base_mask, dislocamento_da_base)

        if base_ponto or topo_ponto:
            return True
        else:
            return False

class Chao:
    velocidade = 5
    largura_do_chao = imagen_do_chao.get_width()
    imagen = imagen_do_chao

    def __init__(self, y):
        self.y = y 
        self.x0 = 0
        self.x1 = self.largura

    def mover(self):
        self.x0 -= self.velocidade
        self.x1 -= self.velocidade

        if self.x0 + self.largura < 0:
            self.x0 = self.largura
        if self.x1 + self.largura < 0:
            self.x1 = self.largura 

    def desenhar(self, tela):
        tela.blit(self.imagen, (self.x0, self.y))
        tela.blit(self.imagen, (self.x1, self.y))

    #desenhando o jogo/ desenhando tela

def desenhar_tela(tela, passaros, canos, chao, pontos):
    tela.blit(imagens_de_fundo, (0, 0))
    for passaro in passaros:
        passaro.desenhar(tela)
    for cano in canos:
        cano.desenhar(tela)

    texto = fonte_de_pontos.render(f"Pontuação: {pontos}", 1, (255, 255, 255))
    tela.blit(texto, (largura_da_tela - 10 - texto.get_width(), 10))
    chao.desenhar(tela)
    pygame.display.update()

def main():
    passaros = [passaros(230, 250)]
    chao = chao(730)
    canos = [canos(700)]
    tela = pygame.display.set_mode({largura_da_tela, ultura_da_tela})
    ponto = 0
    relogio = pygame.time.Clock()

    rodando = True
    while rodando:
        relogio.tick(30)

        #interacao do jogo
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando.QUIT()
                quit()
            if evento.key == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    for passaros in passaros:
                        passaros.pular()

        for passaros in passaros: 
            passaros.mover()
        chao.mover()

        add_cano = False
        for cano in canos: 
            for i, passaros in enumerate(passaros):
                if cano.colidir(passaros):
                    passaros.pop()
                if not cano.passou and passaros.x > canos.x:
                    cano.passou = True
                    add_cano = True
                cano.mover()
                if cano.x + canos.cano_topo.get_width() < 0:
                    cano.append(canos)

        if add_cano: 
            ponto += 1
            canos.append((cano(600)))
        for canos in canos:
            canos.remove(cano)
        
        for passaro in enumerate(passaro):
            if (passaro.y + passaro.imagen.get_heigth()) > 730 or passaro.y < 0:
                passaros.pop()
        
         # mover as coisas
        for passaro in passaros:
            passaro.mover()
        chao.mover()

        adicionar_cano = False
        remover_canos = []
        for cano in canos:
            for i, passaro in enumerate(passaros):
                if cano.colidir(passaro):
                    passaros.pop(i)
                if not cano.passou and passaro.x > cano.x:
                    cano.passou = True
                    adicionar_cano = True
            cano.mover()
            if cano.x + cano.CANO_TOPO.get_width() < 0:
                remover_canos.append(cano)

        if adicionar_cano:
            pontos += 1
            canos.append(cano(600))
        for cano in remover_canos:
            canos.remove(cano)

        for i, passaro in enumerate(passaros):
            if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0:
                passaros.pop(i)

        desenhar_tela(tela, passaros, canos, chao, ponto)


if __name__ == "main":
    main()