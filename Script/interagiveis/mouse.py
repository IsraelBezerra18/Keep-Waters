import pygame

class Image(pygame.sprite.Sprite):
    def __init__(self, diretorio) -> None:
        super().__init__()
        self.image = pygame.image.load(diretorio).convert_alpha()
        self.rect = pygame.Rect(0, 0, 1, 1)
        self.posMap = pygame.math.Vector2(0, 0)
    
    def set_posMap(self, pos: tuple):
        self.posMap.x = pos[0]
        self.posMap.y = pos[1]

class Mouse:
    def __init__(self, diretorio, clock):
        self.timer = clock.createTimer(manage=False)
        self.image = Image(diretorio)
        self.cursor = pygame.cursors.Cursor((0, 0), self.image.image)
        pygame.mouse.set_cursor(self.cursor)
        self.botaoL = False
        self.botaoR = False
    
    def click(self, limitClick=0.15):
        self.timer.countdown(limitClick)
        mouse_click = pygame.mouse.get_pressed()
        self.botaoL = False
        self.botaoR = False
        
        if True in mouse_click:
            if self.timer.finished:
                self.timer.restart()
                self.botaoL = mouse_click[0]
                self.botaoR = mouse_click[2]

    def collideImg(self, grupo):
        return pygame.sprite.spritecollide(self.image, grupo, dokill=False, 
                                          collided=pygame.sprite.collide_mask)

    def collideRect(self, rect):
        return self.image.rect.colliderect(rect)
    
    def collideObj(self, grupo):
        objcollide = self.collideImg(grupo)
        if objcollide: return self.collideRect(objcollide[0])
        return False
        
    def collideId(self, grupo):
        collision = self.collideImg(grupo)
        if collision: return (collision[0].id, collision[0].estado)
        else: return False
        
    def update(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.image.rect.x = mouse_x
        self.image.rect.y = mouse_y
        