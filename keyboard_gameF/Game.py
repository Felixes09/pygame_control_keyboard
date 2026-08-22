import os
import pygame
from Platform import platform
from Player import player
from Enemy import Enemy
#from Bullet import bullet

#找到Player.py 文件所在的文件夹
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#platform_image_path = os.path.join(BASE_DIR,'background.png')

pygame.init()
screen = pygame.display.set_mode((800, 600))

background_images = [
    pygame.image.load(os.path.join(BASE_DIR,'backgrounds','sky.png')).convert_alpha(),
    pygame.image.load(os.path.join(BASE_DIR,'backgrounds','mountain.png')).convert_alpha(),
    pygame.image.load(os.path.join(BASE_DIR,'backgrounds','mountains.png')).convert_alpha(),
    pygame.image.load(os.path.join(BASE_DIR,'backgrounds','forest.png')).convert_alpha(),
    pygame.image.load(os.path.join(BASE_DIR,'backgrounds','trees.png')).convert_alpha(),
]

background_images = [
    pygame.transform.scale(image,(800,600))
    for image in background_images

]
 
#bg_img = pygame.image.load(platform_image_path).convert()
#bg_img = pygame.transform.scale(bg_img,(800,600))



running = True

#设置帧率d
clock = pygame.time.Clock()

#平台组
platform_group = pygame.sprite.Group()
platform_group.add(platform(topleft=(400,400),plat_length=400))
platform_group.add(platform(topleft=(250,250)))
platform_group.add(platform(topleft=(100,150)))
platform_group.add(platform(topleft=(50,400)))

#子弹组
bullet_group = pygame.sprite.Group()

#检测子弹与敌人的碰撞
'''def check_bullet_enemy_collision():
    pygame.sprite.groupcollide(
        bullet_group,
        enemy_group,
        True,
        True
    )'''

#创建玩家组，并创建一个玩家player,其中bulet_group是为了在该玩家组Player.py 中的 player里面传入子弹组
player_group = pygame.sprite.GroupSingle(player((100,100),bullet_group))#这个是为了让玩家只能有一个，GroupSingle是一个特殊的组，只能有一个精灵

#创建敌人组，并创建一个enemy
enemy_group = pygame.sprite.GroupSingle(Enemy((400,300),bullet_group,x_speed=2,y_speed = 0))

while running:
    clock.tick(60)

    space_flag = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                space_flag = True 

    for image in background_images:
        screen.blit(image,(0,0))

    #画入平台
    platform_group.draw(screen)
    #画入玩家
    player_group.draw(screen)
    player_group.update(space_flag,platform_group)

    bullet_group.draw(screen)
    bullet_group.update()

    #画入敌人
    enemy_group.draw(screen)
    enemy_group.update()

    #在主循环中调动子弹与敌人碰撞函数
    #check_bullet_enemy_collision()
    for enemy in enemy_group:
        enemy.check_attack_bullet(bullet_group)
    
    #ADDED A FRAME ON PLAYER
    for player in player_group:
        #在玩家周围画一个矩形框
        pygame.draw.rect(screen,  (255, 0, 0), player.rect, width= 1)
        
    pygame.display.flip()
            
        
pygame.quit()
