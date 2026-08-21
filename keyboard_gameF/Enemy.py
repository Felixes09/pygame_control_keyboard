import pygame
from Bullet import bullet

class Enemy(pygame.sprite.Sprite):
    def __init__(self, position,bullet_group,y_speed,x_speed = 2,):#Python 不允许没有默认值的参数放在有默认值的参数后面
        super().__init__()
        self.image = pygame.Surface((100,100))
        self.image.fill("blue")
        self.rect = self.image.get_rect(topleft=position)
        self.x_speed = x_speed
        self.y_speed = y_speed
        bullet = bullet_group
        self.health = 60


    #子弹与敌人碰撞检测函数

    def check_attack_bullet(self,bullet):
        hit_bullet = pygame.sprite.spritecollide(
            self,
            bullet,
            True
        )

        if hit_bullet:
            # pygame.sprite.spritecollide() 会返回一个列表，表内存储所有撞到敌人的子弹
            self.health -= len(hit_bullet)
            self.image.fill('blue')

        if self.health <= 40:
            self.image.fill('green')

        if self.health <= 20:
            self.image.fill('red')
             
        if self.health <= 0:
            self.kill()

    def update(self):
        self.rect.x += self.x_speed
        if self.rect.right >= 800 or self.rect.left <= 400 :
            self.x_speed = -self.x_speed