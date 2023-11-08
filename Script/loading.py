import pygame, random, numpy as np, pyautogui
from Script.grid import *
from Script.reprodutores.video import Video, ReprodutorVideo
from Script.elementos_mapa.map import Map
from Script.menus.menu_principal import PrincipalInterface
from Script.gerenciadores.clock import Clock
from Script.elementos_mapa.player import Player
from Script.interagiveis.mouse import Mouse
from Script.gerenciadores.groups import PriorityArray, GroupSingle
from Script.icones.pdp import Pdp
from Script.icones.icon import Icon
from Script.gerenciadores.text import TextManager
from Script.elementos_mapa.residuo import ResiduoInMap
from Script.loadFile import loadImage
from Script.save import Save
from Script.interagiveis.keyboard import Keyboard
from Script.elementos_mapa.lixeira import Lixeiras
from Script.gerenciadores.message import MessageManager
from Script.gerenciadores.box import BoxInfo
from Script.blur import Blur
from Script.menus.pause import Pause
from Script.gerenciadores.algorithm import VisionField
from Script.elementos_mapa.structure import Structures
from Script.gerenciadores.bot import Bot

mouse = 'Data/Cursor.png'
icon_video = 'Data/Imagens/botoes/botao_video'
video_logo = 'Data/Video/logo_turma.mp4'
sprites_player = 'Data/Imagens/personagens/player_masculino'
sprites_pdp = 'Data/Imagens/icones/pdp'
sprites_residuo = 'Data/Imagens/residuos'
sprites_inventory = 'Data/Imagens/interfaces/inventory'
sprites_hub = 'Data/Imagens/interfaces/hub'
sprites_lixeira = 'Data/Imagens/lixeiras'
icone_bag = 'Data/Imagens/icones/bag'
icone_apagar = 'Data/Imagens/icones/apagar'
icone_mensagem = 'Data/Imagens/icones/message'
sprites_mensagem = 'Data/Imagens/interfaces/message'
sprites_box = 'Data/Imagens/interfaces/exibicao/box'
sprites_botao = 'Data/Imagens/botoes'
icone_life = 'Data/Imagens/icones/life'
sprites_pause = 'Data/Imagens/interfaces/pause'
sprites_struturas = 'Data/Imagens/interfaces/estrutura'

# _____ Inicialização _____ #
saves = Save()
config = saves.config
largura, altura = pyautogui.size()
if config['resolucao_tela'] == 'automático':
    config['resolucao_tela'] = (largura, altura)

# ~~ Pygame
pygame.init()
pygame.mixer.init()

display = pygame.display.set_mode(config['resolucao_tela'])
pygame.display.set_caption('Keep Waters')

# ~~ Proporção
proporcoes = pygame.math.Vector2(config['resolucao_tela'][0] / 1280, config['resolucao_tela'][1] / 720)

# ~~ Vídeo
icon_video = loadImage(icon_video, proporcoes)
# video_logo = Video(video_logo, size=size_tela, pos=(0, 0))

# _____ Menu Inicial _____ #

# _____ Jogo _____ #

# ~~ Imagem
sprites_player = loadImage(sprites_player, proporcoes)
sprites_pdp = loadImage(sprites_pdp, proporcoes)
sprites_residuo = loadImage(sprites_residuo, proporcoes)
sprites_inventory = loadImage(sprites_inventory, proporcoes, notLoad='acoes_slot')
sprites_inventory['acoes_slot'] = loadImage('Data/Imagens/interfaces/inventory/slot/acoes_slot', proporcoes,
                                            type='list', argumento=(35, 35), transform=pygame.transform.smoothscale)
sprites_inventory['icone_bag'] = loadImage(icone_bag, proporcoes, type='list')
sprites_hub = loadImage(sprites_hub, proporcoes)
sprites_lixeira = loadImage(sprites_lixeira, proporcoes)
sprites_mensagem = loadImage(sprites_mensagem, proporcoes)
sprites_mensagem['icones'] = np.array([loadImage(icone_mensagem, proporcoes, type='list')[0], 
                                       loadImage(icone_apagar, proporcoes, type='list')[0]])
sprites_box = loadImage(sprites_box, proporcoes)
sprites_botao = loadImage(sprites_botao, proporcoes)
sprites_life = loadImage(icone_life, proporcoes)
sprites_pause = loadImage(sprites_pause, proporcoes)
sprites_struturas = loadImage(sprites_struturas, proporcoes)

# _____ Game Over _____ #
