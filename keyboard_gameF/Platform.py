import pygame
class platform(pygame.sprite.Sprite):
    def __init__(self, topleft):
        super().__init__()
        
        
        #这两项是强制的，必须要有
        self.image = pygame.Surface((200,20))#Surface 要大写，不然fill为白色
        self.image.fill('white')
        
        self.rect = self.image.get_rect(topleft = topleft)#?
