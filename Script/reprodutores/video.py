from moviepy.editor import VideoFileClip
import pygame, numpy as np
from Script.interagiveis.button import BotaoAtivar, BotaoFrame, BotaoIcon
from Script.reprodutores.audio import Audio


class ReprodutorVideo:
    '''Reprodutor de vídeos'''
    def __init__(self, sprites, mouse, clock, GroupArray) -> None:
        self.video = None
        self.mouse = mouse
        self.sprites = sprites
        
        self.allGroups = GroupArray
        self.frames = self.allGroups.createGroup(priority=0)
        self.botoes = self.allGroups.createGroup(priority=1)
        self.list_frame = []

        self.clock = clock
        self.pausar = False
        self.loop = False
        self.cutscene = False

        self.size = None
        self.index = 0
        self.fps = 0
    
    def gerar_frame(self, pos):
        size = int((self.video.size[0])/self.quantFrame)
        img_inicio = np.array([])
        for img in self.sprites['inicio']:
            img_inicio = np.append(img_inicio, pygame.transform.smoothscale(img, (size, 12)))
        img_centro = np.array([])
        for img in self.sprites['centro']:
            img_centro = np.append(img_centro, pygame.transform.smoothscale(img, (size, 12)))
        img_fim = np.array([])
        for img in self.sprites['fim']:
            img_fim = np.append(img_fim, pygame.transform.smoothscale(img, (size, 12)))

        for contador in range(self.quantFrame):
            if contador == 0:
                botao_frame = BotaoFrame(img_inicio, '', pos)
            else:
                reference = img_centro
                if contador == self.quantFrame-1:
                    reference = img_fim
                frame_anterior = self.frames.sprites()[contador-1]
                botao_frame = BotaoFrame(reference, '', (-40, -40))
                botao_frame.rect.left = frame_anterior.rect.right
                botao_frame.rect.centery = frame_anterior.rect.centery
            botao_frame.id = contador
            self.frames.add(botao_frame)

    def gerar_botoes(self):
        primeiro_frame = self.frames.sprites()[0]
        ultimo_frame = self.frames.sprites()[-1]
        pos_botao_acao = (primeiro_frame.rect.left-20, primeiro_frame.rect.centery)
        pos_botao_loop = (ultimo_frame.rect.right+20, primeiro_frame.rect.centery)

        if not self.botoes:
            self.botao_play = BotaoIcon(self.sprites['botao_play'], audio='', position=pos_botao_acao)
            self.botao_pause = BotaoIcon(self.sprites['botao_pause'], audio='', position=pos_botao_acao)
            self.botao_circle = BotaoIcon(self.sprites['botao_player'], audio='', position=primeiro_frame.rect.center)
            self.botao_loop = BotaoAtivar(self.sprites['botao_loop'], audio='', position=pos_botao_loop)
            self.botao_acao = self.botao_play
            self.botoes.add(self.botao_circle, self.botao_loop)
        else:
            self.botao_play.rect.center = pos_botao_acao
            self.botao_pause.rect.center = pos_botao_acao
            self.botao_circle.rect.center = primeiro_frame.rect.center
            self.botao_loop.rect.center = pos_botao_loop

    def execute_painel(self, display):
        display.blit(self.botao_acao.image, self.botao_acao.rect)
        self.allGroups.draw(display)
        self.frames.update(self.mouse.botao_esquerdo, self.index)
        self.update_botoes()
    
    def update_botoes(self):
        if not self.cutscene:
            self.botao_acao = self.botao_pause
            if self.pausar:
                self.botao_acao = self.botao_play
            
            if self.botao_acao.estado:
                self.pausar = False if self.pausar else True
            self.loop = self.botao_loop.estado

            colisao = self.mouse.collide(self.frames)
            if colisao:
                self.botao_circle.estado = True
                if colisao[1]:
                    self.index = colisao[0]
            else:
                self.botao_circle.estado = False
            self.botao_circle.rect.center = self.frames.sprites()[int(self.index)].rect.center
            self.botao_circle.update(False)
            self.botao_acao.update(self.mouse.botao_esquerdo)
            self.botao_pause.update(self.mouse.botao_esquerdo)
            self.botao_loop.update(self.mouse.botao_esquerdo)

    def reproduzir(self, display):
        if not self.video.finished:
            if self.index >= self.quantFrame-1:
                self.index = 0
                if not self.loop:
                    self.pausar = True
                if self.cutscene:
                    self.video.finished = True
            if not self.cutscene:
                self.execute_painel(display)
            display.blit(self.list_frame[int(self.index)], self.video.rect)

            if not self.pausar:
                velocidade = self.clock.delta(get_speed=self.fps)
                self.index += velocidade if velocidade < 1 else 0
        
    def adicionar_video(self, video, cutscene=False):
        self.frames.remove(self.frames)
        self.video = video
        self.quantFrame = len(video.frames)
        self.size = video.size
        self.fps = video.fps
        self.cutscene = cutscene
        self.list_frame = video.frames
        if not self.cutscene:
            self.video.rect.center = video.pos
            self.pausar = True
            self.gerar_frame((video.rect.left + 75, video.rect.bottom + 15))
            self.gerar_botoes()
            self.botao_loop.estado = True
        self.index = 0

class Video:
    def __init__(self, diretorio, size, pos) -> None:
        self.finished = False
        self.video = VideoFileClip(diretorio)
        self.pos = pos
        self.fps = self.video.fps
        self.size = size
        self.frames = np.array([])
        self.imagens = np.array([pygame.surfarray.make_surface(self.video.get_frame(time)).convert_alpha() 
                        for time in np.arange(0, self.video.duration, 1/self.fps)])
        self.quantImagem = len(np.arange(0, self.video.duration, 1/self.fps))
        
        fun = pygame.transform
        for imagem in range(self.quantImagem):
            imagem = fun.smoothscale(fun.flip(fun.rotate(self.imagens[imagem], 270), True, False), self.size)
            self.frames = np.append(self.frames, imagem)
        self.rect = self.frames[0].get_rect(topleft=self.pos)
    
    def close(self, condiction):
        if condiction:
            self.finished = True
