import pygame, numpy as np

loadFont = pygame.font.Font
font1 = 'Data/Fontes/Retroville NC.ttf'
font2 = 'Data/Fontes/slkscre.ttf'

class TextManager:
    '''Cria e gerencia a exibição de textos na tela'''
    def __init__(self, proporcoes) -> None:
        self.font = np.array([font1, font2])
        self.textArray = np.array([])
        self.proporcoes = proporcoes
    
    def blit(self, display):
        for obj in self.textArray:
            if isinstance(obj, np.ndarray):
                for value in obj:
                    if value.exibir: display.blit(value.image, value.rect)
            else:
                if obj.exibir: display.blit(obj.image, obj.rect)

    @property
    def size(self): 
        return self.textArray.size

    def ajustsize(self, obj_ref):
        texto = obj_ref.texto
        size = int(obj_ref.rect.width * 0.8)
        if not texto.rect.width <= size:
            while texto.rect.width > size:
                texto.size -= 1
                texto.load = loadFont(texto.font, texto.size)
                texto.image = texto.load.render(texto.text, False, texto.color)
                texto.rect = texto.image.get_rect(center=obj_ref.rect.center)
                if not texto.size: break
    
    def remove(self, text):
        texts = np.array([texto.text for texto in self.textArray])
        self.textArray = np.delete(self.textArray, np.where(texts == text)[0][0])

    def createText(self, text: str, size: int, pos: tuple, color=(202, 218, 234), font_id=0, manager=True):
        texto = self.Text(text, self.font[font_id], int(size * self.proporcoes.x), pos, color)
        if manager: self.textArray = np.append(self.textArray, texto)
        return texto

    def createLine(self, text: str, sizeText: int, pos: tuple, sizeLimite=500,
                   color=(202, 218, 234), font_id=0, manager=True):
        linhas = []; texto = text.split(' '); linha = ''
        fonte = loadFont(self.font[font_id], sizeText)
        limite = sizeLimite; contador = 0
        
        def gerarlinha():
            if not linhas: linhas.append(self.Text(linha, self.font[font_id], sizeText, pos, color))
            else:
                linha_ante = linhas[-1]
                posicao = (linha_ante.rect.centerx, linha_ante.rect.centery + linha_ante.rect.height)
                obj_text = self.Text(linha, self.font[font_id], sizeText, posicao, color)
                obj_text.rect.x = linha_ante.rect.x
                linhas.append(obj_text)
        
        while contador < len(texto):
            new_palavra = f' {texto[contador]}'
            frase = fonte.render(linha + new_palavra, False, color)
            rect = frase.get_rect(); sizeFrase = rect.width
            if sizeFrase >= limite:
                linha = linha[1:]
                gerarlinha(); linha = ''
            else: linha += new_palavra; contador += 1
        if linha:
            linha = linha[1:]
            gerarlinha()
        if manager: self.textArray = np.append(self.textArray, np.array(linhas))
        return np.array(linhas)
            
    def escrever(self):...

    class Text:
        def __init__(self, text, font, size, pos, color) -> None:
            self.exibir = True
            self.text = text; self.size = size; self.color = color
            self.font = font; self.pos = pos
            self.load = loadFont(self.font, self.size)
            self.alpha = 255
            self.speed = 20

            self.reference = self.load.render(self.text, False, self.color)
            self.image = self.reference.copy()
            self.rect = self.image.get_rect(center=self.pos)
        
        @staticmethod
        def modifyColor(tomAtual, tomDestino, velocidade):
            if tomAtual > tomDestino:
                return tomAtual - velocidade
            elif tomAtual < tomDestino:
                return tomAtual + velocidade
            return tomAtual
        
        @property
        def visible(self):
            if self.alpha == 255: return True
            return False
        
        def set_alpha(self, alpha: int):
            self.image = self.reference.copy()
            self.image.set_alpha(alpha)
            self.rect = self.image.get_rect(center=self.pos)
            self.alpha = alpha

        def set_text(self, new_text: str):
            self.text = new_text
            self.reference = self.load.render(self.text, False, self.color)
            self.image = self.reference.copy()
            self.image.set_alpha(self.alpha)
            self.rect = self.image.get_rect(center=self.pos)
        
        def set_color(self, new_color: tuple[int, int, int], delta=False, animation=False, speed=False):
            if self.color != new_color:
                if delta and animation:
                    velocidade = speed * delta if speed else self.speed * delta
                    r = self.modifyColor(self.color[0], new_color[0], velocidade)
                    g = self.modifyColor(self.color[1], new_color[1], velocidade)
                    b = self.modifyColor(self.color[2], new_color[2], velocidade)
                    self.image = self.load.render(self.text, False, (int(r), int(g), int(b)))
                    if int(r) == new_color[0] and int(g) == new_color[1] and int(b) == new_color[2]:
                        self.color = new_color
                else:
                    self.color = new_color
                    self.image = self.load.render(self.text, False, self.color)

        def enterAlpha(self, delta, speed=False):
            velocidade = speed * delta if speed else self.speed * delta
            if self.alpha < 255:
                self.image = self.reference.copy()
                self.alpha += velocidade
            else: self.alpha = 255
            self.image.set_alpha(self.alpha)
        
        def closeAlpha(self, delta, speed=False):
            velocidade = speed * delta if speed else self.speed * delta
            if self.alpha > 0:
                self.image = self.reference.copy()
                self.alpha -= velocidade
            else: self.alpha = 0
            self.image.set_alpha(self.alpha)
