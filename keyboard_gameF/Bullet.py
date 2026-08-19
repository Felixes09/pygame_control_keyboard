import pygame

#PART 6 SHOOTING BULLETS
class bullet(pygame.sprite.Sprite):
    def __init__(self, center,x_speed):
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill('red')

        self.rect = self.image.get_rect()
        self.rect.center = center

        #这个是为了让子弹从玩家的中心位置发射
        # 其中player_group.sprite.rect.centerx是玩家的中心位置的x坐标，player_group.sprite.rect.centery是玩家的中心位置的y坐标
        #子弹速度
        self.x_speed  = x_speed
        self.y_speed = 0
        self.g = 1


    def update(self):
        self.y_speed += self.g
        self.rect.x += self.x_speed
        #self.rect.y += self.y_speed
        if self.rect.left > 800:
             self.kill()