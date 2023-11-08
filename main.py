from Script.loading import *

class KeepWaters:
    def __init__(self) -> None:
        self.init = True

        # ~~ Inicialização Pygame
        pygame.init()
        self.display = display
        self.rect = self.display.get_rect()
        self.time = pygame.time.Clock()
        self.clock = Clock()

        # ~~ Inputs
        self.mouse = Mouse(mouse, self.clock)
        self.keyboard = Keyboard()

        # ~~ Gerenciadores
        self.allGroupsMap = PriorityArray()
        self.allgroupPause = PriorityArray()
        self.allTextMap = TextManager(proporcoes)
        self.textPause = TextManager(proporcoes)
        self.allMessages = MessageManager(sprites_mensagem, self.allTextMap)
        self.allBoxInfo = BoxInfo(sprites_box, self.mouse, proporcoes)

        # ~~ Classes principais
        self.reprodutor = ReprodutorVideo(icon_video, self.mouse, Clock(), PriorityArray())
        self.blur = Blur(self.display)
        
        # ~~ Menu principal
        self.menu_inicial = PrincipalInterface(interface, size_block=64, ArrayGroup=PriorityArray(), proporcoes=proporcoes)
        
        # ~~ Jogo
        posFPS = (int(self.rect.right - 40 * proporcoes.x), int(self.rect.top + 20 * proporcoes.y))
        self.fps = self.allTextMap.createText(str(int(self.time.get_fps())), 20, posFPS, (0, 0, 0))
        self.player = self.allGroupsMap.createGroupSingle(priority=2)
        self.mapa = self.allGroupsMap.createGroupSingle(priority=0)
        self.pdp = Pdp(sprites_pdp, self.clock, self.allTextMap, proporcoes)
        self.structures = Structures(sprites_struturas, self.mapa, self.allGroupsMap, proporcoes)

        # ~~ Pause
        self.groupPause = self.allgroupPause.createGroupSingle(priority=0)
        self.pause = Pause(sprites_pause, self.rect.center, self.allgroupPause, self.clock, 'abrir', self.groupPause)

        # ~~ Game Over

    def loading(self):
        self.menu_inicial.loading(list_bottom_keys)
        self.allBoxInfo.createBoxSolid((self.rect.left+5, self.rect.top+5), reference='topleft')
        self.lixeiras = Lixeiras(self.mapa, sprites_lixeira, self.allGroupsMap, proporcoes)
        self.player.add(Player(sprites_player, proporcoes, self.rect.center, self.allGroupsMap, self.allMessages, 'parado'))
        self.mapa.add(Map(self.player.sprite, self.display, proporcoes))
        self.mapa.sprite.loading()
        self.residuoMap = ResiduoInMap(sprites_residuo, self.mapa.sprite, self.allGroupsMap, proporcoes)
        self.lixeiras.loading()

        self.structures.createStructure(None, 'estrutura upgrade')

        self.objPlayer = self.player.sprite
        self.objMapa = self.mapa.sprite

        self.objPlayer.loading(sprites_life, self.mouse, self.clock)
        self.objPlayer.loadingInventory(sprites_inventory, sprites_hub)

        self.pause.loading(proporcoes, self.display, self.blur, self.textPause)
        self.pause.loadingButton(sprites_botao)

        # ~~~~~~~~ Área de Testes fora da repetição ~~~~~~~~ #
        self.menu_inicial.init = False
        # self.timerTest = self.clock.createTimer()

        self.ia = VisionField(self.objMapa, 500, 50, proporcoes)
        self.ia.loadingGrid((1000, 2000))
        self.teste = Bot((1000, 2300))
        self.destFinal = (800, 1900)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

    def events(self):
        self.keyboard.evento = None
        self.keyboard.resizable = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.init = False
            if event.type == pygame.KEYDOWN:
                self.keyboard.evento = event.key
                if self.keyboard.event(pygame.K_F11):
                    if config['resolucao_tela'] != (largura, altura) and proporcoes.y >= 1:
                        pygame.display.toggle_fullscreen()

    def run(self):
        while self.init:
            # ~~ FPS
            self.time.tick(config['limite_fps'])
            self.fps.set_text(str(int(self.time.get_fps())))

            # ~~ Mouse
            self.mouse.update()
            self.mouse.click()
            self.mouse.image.set_posMap(self.objMapa.get_posMap(self.mouse.image.rect))

            # ~~ Eventos
            self.events()

            # ~~~~~~~~ Área de Testes na repetição ~~~~~~~~ #
            if self.mouse.botaoL and self.keyboard.key(pygame.K_LSHIFT):
                self.residuoMap.createResiduoAreia(self.mouse.image.posMap)

            # self.timerTest.countdown(10, format=60)
            # if self.keyboard.event(pygame.K_t):
            #     iconeTeste = Icon(loadImage(icone_apagar, proporcoes, 'list')[0], (-20, -20))
            #     self.allBoxInfo.createBoxAnimation(iconeTeste, self.timerTest, audio=False)
            
            # if self.keyboard.event(pygame.K_g):
            #     self.objPlayer.life.cure(100)

            # if self.keyboard.event(pygame.K_p):
            #     self.objPlayer.life.damage(25)

            # if self.keyboard.event(pygame.K_t):
            #     self.blur.apply(pygame.display.get_surface().copy(), desfoque=2)
            
            # if self.keyboard.event(pygame.K_r):
            #     self.blur.remove()

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

            # ~~ Logo

            # ~~ Delta
            self.delta = self.clock.delta()
            
            # ~~ Menu inicial
            botao = self.mouse.collideId(self.menu_inicial.buttons)
            inputs = self.menu_inicial.inputs(botao)
            self.init = inputs if inputs is not None else self.init
            self.menu_inicial.run(self.mouse, self.delta)

            # ~~ Jogo
            if not self.menu_inicial.init:
                # ~~ Ativação do Pause
                if not self.objPlayer.objBag.open:
                    if self.keyboard.event(pygame.K_ESCAPE):
                        if not self.pause.animation: self.pause.pausar()

                if not self.pause.paused and not self.blur.active:
                    # ~~~~~~~~~~~ #
                    self.ia.fieldUpdate(self.player)
                    if self.mouse.botaoR and self.keyboard.key(pygame.K_LSHIFT):
                        self.destFinal = self.mouse.image.posMap.xy
                    testePos = self.ia.createPath(self.teste.posCurrent, self.destFinal)
                    self.teste.set_path(testePos)
                    self.teste.move(self.delta)
                    # ~~~~~~~~~~~ #

                    # ~~ Descarte
                    perimetroDescarte = self.lixeiras.descarte()
                    if perimetroDescarte:
                        if self.objPlayer.objBag.open and self.mouse.botaoL:
                            self.objPlayer.objBag.descartar(perimetroDescarte, self.pdp)
                        else: self.objPlayer.hub.descartar(perimetroDescarte, self.objPlayer, self.pdp, self.keyboard)

                    # ~~ Atualizações
                    self.allGroupsMap.draw(self.display)

                    # ~~~~~~~~~~~ #
                    self.ia.draw_perim(self.display)
                    self.ia.draw_path(self.display, self.teste, testePos)
                    self.teste.draw(self.display, self.objMapa)
                    # ~~~~~~~~~~~ #

                    self.mapa.update()
                    self.structures.update(self.keyboard)
                    self.lixeiras.update(self.delta)
                    self.allBoxInfo.update(self.display, self.delta)
                    self.player.update(mapa=self.mapa.sprite, keyboard=self.keyboard, delta=self.delta)
                    self.residuoMap.update(self.keyboard, self.delta)
                    self.pdp.update(self.objMapa, self.delta)
                    self.allMessages.update(self.delta, self.display, proporcoes)

            self.allTextMap.blit(self.display)
            self.blur.update(self.delta)

            # ~~ Execução do Pause
            if self.pause.paused:
                self.clock.config_all_timers('pausar')
                self.allMessages.clock.config_all_timers('pausar')

                self.allgroupPause.draw(self.display)
                self.pause.update(self.delta)
                self.textPause.blit(self.display)
                match self.pause.updateButton(self.delta, self.mouse):
                    case ('Continuar', True): self.pause.pausar()
                    case ('Sair do jogo', True): self.init = False
            elif self.clock.pause:
                self.clock.config_all_timers('despausar')
                self.allMessages.clock.config_all_timers('despausar')
            pygame.display.update()

keep_waters = KeepWaters()
keep_waters.loading()
keep_waters.run()
