import pygame, time
from Script.gerenciadores.groups import Group

class Clock:
    def __init__(self) -> None:
        self.group_timer = Group()

        # ~~ Delta time
        self.fps_padrao = 60
        self.prev_time = time.time()
        self.dt = 0

        # ~~ Pause clock
        self.pause = False
    
    def delta(self, get_speed=0):
        now = time.time(); self.dt = 0
        diferenca = now - self.prev_time
        if diferenca < 0.15:
            self.dt = diferenca*self.fps_padrao if not get_speed else diferenca*get_speed
        self.prev_time = now
        return self.dt

    def createTimer(self, manage=True):
        if manage:
            return self.Timer(self.group_timer)
        return self.Timer()
    
    def removeTimer(self, timer) -> None:
        self.group_timer.remove(timer)

    def config_all_timers(self, config: str) -> None:
        """Esta função aceita como parametro apenas as strings 'pausar' para pausar
        TODOS os cronometros e 'despausar' para despausar TODOS os cronometros."""
        match config:
            case 'pausar':
                action = True
            case 'despausar':
                action = False
        if action != self.pause:
            for timer in self.group_timer:
                timer.pause = action
            self.pause = action
        elif self.pause:
            for timer in self.group_timer:
                timer.countdown(timer.register)

    # ~~ Classe Cronometro
    class Timer(pygame.sprite.Sprite):
        def __init__(self, *group) -> None:
            super().__init__(group)
            
            self.finished = False # indica se a contagem chegou a 0
            self.pause = False # bool para pausar o tempo (True para pausar)
            
            self.time_initial = time.time() # Registra o tempo inicial
            self.time_record = 0 # Registra o tempo que passou (progressiva) ou o tempo que falta (regressiva)

            # ~~ Atributos para ajustar o tempo ~~ #
            self.time_pause = 0 # Armazena o valor do time_record no momento do pause
            self.adjustment = 0 # Armazena o módulo do intervalo entre o tempo atual e o momento de pause
            self.register = 0
        
        def restart(self):
            self.finished = False
            self.time_initial = time.time()
            self.time_record = 0
            self.time_pause = 0
            self.adjustment = 0

        def progressive(self) -> None:
            if self.pause:
                if not self.time_pause:
                    self.time_pause = self.time_record
                self.adjustment = abs(self.time_record - self.time_pause)
            else:
                if self.adjustment:
                    self.time_initial += self.adjustment
                    self.time_pause = 0
                    self.adjustment = 0
            self.time_record = time.time() - self.time_initial

        def countdown(self, time: float, format=0) -> None:
            if not self.pause:
                time = float(time)
                time = int(time)*format + int(str(time)[str(time).index('.')+1:]) if format else time
                self.register = time
            self.progressive()
            self.time_record = time - self.time_record
            if self.time_record <= 0 and not self.pause:
                self.finished = True
        
        # ~~ Função de exibição de tempo
        def get_score(self, format_min_sec=True, casas_decimais=0):
            time_reference = (0 if self.time_record < 0 and not self.pause else self.time_record 
                              if not self.pause else self.time_pause)
            verificacao = time_reference/60
            if verificacao >= 1 and format_min_sec:
                restante = time_reference - int(verificacao)*60
                return f'{int(verificacao)}:'+(f'{(restante):.{casas_decimais}f}'.zfill(casas_decimais + 3)
                                                 if casas_decimais else str(int(restante))).zfill(2)
            return ((f'{time_reference:.{casas_decimais}f}') if casas_decimais
                    and not time_reference == 0 else str(int(time_reference)))
