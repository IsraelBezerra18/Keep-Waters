import os, pygame, numpy as np
from PIL import Image

imageLoad = pygame.image.load
audioLoad = pygame.mixer.Sound

def resize(image: pygame.Surface, proporcoes: pygame.math.Vector2):
    proporcaoW, proporcaoH = proporcoes.x, proporcoes.y
    if proporcaoW != 1 or proporcaoH != 1:
        originalW = image.get_width(); originalH = image.get_height()
        newW = int(originalW * proporcaoW); newH = int(originalH * proporcaoH)
        imageBytes = pygame.image.tostring(image, 'RGBA')
        pilImage = Image.frombytes('RGBA', (originalW, originalH), imageBytes)
        newImage = pilImage.resize((newW, newH), Image.BILINEAR)
        newImageBytes = newImage.tobytes()
        return pygame.image.fromstring(newImageBytes, newImage.size, 'RGBA').convert_alpha()
    return image.convert_alpha()


def loadImage(diretorio: str, proporcoes, type='dict', argumento=0, transform=False, notLoad=False):
    def dicionario():
        if argumento and transform:
            return {
                root.split('\\' if '\\' in root else '/')[-1]:
                np.array([resize(transform(imageLoad(os.path.join(root, sprite)), argumento), proporcoes)
                for sprite in images]) for root, _, images in os.walk(diretorio) if images and not 
                root.split('\\' if '\\' in root else '/')[-1] == notLoad
            }
        return {
            root.split('\\' if '\\' in root else '/')[-1]:
            np.array([resize(imageLoad(os.path.join(root, sprite)), proporcoes)
            for sprite in images]) for root, _, images in os.walk(diretorio) if images and not
            root.split('\\' if '\\' in root else '/')[-1] == notLoad
        }

    def lista():
        if argumento and transform:
            return np.array([resize(transform(imageLoad(os.path.join(diretorio, sprite)), argumento), proporcoes)
                                for sprite in os.listdir(diretorio)])
        return np.array([resize(imageLoad(os.path.join(diretorio, sprite)), proporcoes)
                            for sprite in os.listdir(diretorio)])
    match type:
        case 'dict':
            return dicionario()
        case 'list':
            return lista()


def loadAudio(diretorio: str, retorno='list', notLoad=False):
    def dicionario():
        return {
            root.split('\\' if '\\' in root else '/')[-1]:
            [audioLoad(os.path.join(root, audio)) 
            for audio in audios] for root, _, audios in os.walk(diretorio) if audios and not
            root.split('\\' if '\\' in root else '/')[-1] == notLoad
        }

    def lista():
        return [audioLoad(os.path.join(diretorio, audio))
                        for audio in os.listdir(diretorio)]
    match retorno:
        case 'dict':
            return dicionario()
        case 'list':
            return lista()
