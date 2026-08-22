import pygame
from Bullet import bullet
import os 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


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

        #设置动画循环参数
        self.walk_frame_index = 0 #它表示当前正在显示第几张跑步图片
        self.anime_timer = 0 #这是动画计时器。通常在 update 方法中不断增加
        self.anim_speed = 8  


        #载入右行走动画
        self.walkR = []
        for i in range(11):
            image = pygame.image.load(
                os.path.join(BASE_DIR,'Goblin','walkingR',f'{i:02d}.png')
            )

            image = pygame.transform.scale(image,(100,100))

            self.walkR.append(image)

        #载入左行走动画(右行走镜像)
        self.walkL = []
        for image in self.walkR:
            fliped_img = pygame.transform.flip(image,True,False)
            self.walkL.append(fliped_img)


    #右行走动画循环函数
    def walkR_anim(self):
        if self.anime_timer >= self.anim_speed:
            self.walk_frame_index = (self.walk_frame_index +1 ) % len(self.walkR)
            self.anime_timer = 0
        self.image = self.walkR[self.walk_frame_index]

    def walkL_anim(self):
        if self.anime_timer >= self.anim_speed:
            self.walk_frame_index = (self.walk_frame_index + 1)%len(self.walkL)
            self.anime_timer = 0
        self.image = self.walkL[self.walk_frame_index]


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
            
        if self.health <= 0:
            self.kill()

    def update(self):
        self.rect.x += self.x_speed

        self.anime_timer += 1
        if self.rect.right >= 800 or self.rect.left <= 400 :
            self.x_speed = -self.x_speed
        if self.x_speed >= 0:
            self.walkR_anim()
        if self.x_speed < 0:
            self.walkL_anim()