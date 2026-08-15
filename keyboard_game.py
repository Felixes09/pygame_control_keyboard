import pygame

pygame.init()
screen=pygame.display.set_mode((800,600))
bg_img = pygame.image.load('background.png').convert()
bg_img = pygame.transform.scale(bg_img,(800,600))



running = True

#设置帧率d
clock = pygame.time.Clock()

#设置平台
class platform(pygame.sprite.Sprite):
    def __init__(self, topleft):
        super().__init__()
        
        
        #这两项是强制的，必须要有
        self.image = pygame.Surface((200,20))#Surface 要大写，不然fill为白色
        self.image.fill('white')
        
        self.rect = self.image.get_rect(topleft = topleft)#?
        
#平台组
platform_group = pygame.sprite.Group()
platform_group.add(platform(topleft=(400,400)))
platform_group.add(platform(topleft=(250,250)))
platform_group.add(platform(topleft=(100,150)))
platform_group.add(platform(topleft=(50,400)))


#设置玩家
class player(pygame.sprite.Sprite):
    def __init__(self, topleft):
        super().__init__()
        #PART 1 the details of the player
        # self.image = pygame.Surface((50,50))
        #PATR 4 CHANGED INTO 100*100
        self.image = pygame.Surface((100,100))

        #PART 1 BUILDED AND PART 4 CANCELED
        #self.image.fill("red")
        self.rect = self.image.get_rect(topleft = topleft)

        # PART 2 MOVE THE PLAYER
        self.g = 1
        self.y_speed = 0
        self.x_speed = 5
       

        #PART 4
        self.run_frame_index = 0
        self.idle_frame_index = 0
        self.anim_timer = 0
        self.anim_speed = 8
        # self.frame_index = 0
        # self.anim_timer = 0
        # self.anim_speed = 8

        #PART 4 LOADING THE PICTURES FOR THE PLAYER
        self.idle = [
            pygame.transform.scale(
                pygame.image.load(f'player/idle/{i:02d}.png'),
                (100, 100)
            )
            for i in range(0, 22)
        ]
        self.image = self.idle[0]


        #将已有的飘带图片镜像翻转
        self.flipped_idle = []
        for image in self.idle:
            flip_img = pygame.transform.flip(image,True,False)
            flip_img.set_colorkey((0,0,0))
            self.flipped_idle.append(flip_img)

        #PART 5 ADDED THE APPATENCE OF RUNNING AND BGM WHEN THE PLAYER TACKING ACTION
        self.run = [
            pygame.transform.scale(
                pygame.image.load(f'player/run/{i}.png'),
                (100, 100)
            )
            for i in range(0, 8)
        ]
        for image in self.run:
            #将图片底色变为透明
            image.set_colorkey((0,0,0))

        #将已有的跑步图片镜像翻转
        self.flipped_run = []
        for image in self.run:
            flip_img = pygame.transform.flip(image,True,False)
            flip_img.set_colorkey((0,0,0))
            #将翻转后的图片加入到flipped_run列表中
            self.flipped_run.append(flip_img)

        #跳跃动画
        self.jump_wav = pygame.mixer.Sound('shoot.wav')
        self.jump = [
            pygame.transform.scale(
                pygame.image.load(f'player/jump/{0}.png')
                ,(100,100)
            )
        ]
        for image in self.jump:
            image.set_colorkey((0,0,0))

        #镜像跳跃动画
        self.filpped_jump = pygame.transform.flip(self.jump[0],True,False)

    #PATR 5 
    #向右行走时的动画循环

    def run_anim(self):
            if self.anim_timer >= self.anim_speed:
                #这个是为了让动画循环播放，%len(self.run)是为了让索引回到0
                self.run_frame_index = (self.run_frame_index + 1) % len(self.run) 
                self.anim_timer = 0
                #self.run存放了所有的跑步图片，self.run_frame_index是索引，self.image是当前显示的图片
            self.image = self.run[self.run_frame_index]


    #向左行走时的动画循环

    def filppedrun_anim(self):
                if self.anim_timer >= self.anim_speed:
                    #这个是为了让动画循环播放，%len(self.run)是为了让索引回到0
                    self.run_frame_index = (self.run_frame_index + 1) % len(self.run) 
                    self.anim_timer = 0
                    #self.run存放了所有的跑步图片，self.run_frame_index是索引，self.image是当前显示的图片
                self.image = self.flipped_run[self.run_frame_index]


    def idel_anim(self):
        if self.anim_timer>=8:
            self.frame_index = (self.idle_frame_index + 1)%len(self.idle)
            self.anim_timer = 0

        self.image = self.idle[self.idle_frame_index]



    def update(self, space_flag, platform_group):
        #PATR 2
        self.y_speed += self.g
        self.rect.bottom += self.y_speed

        
        #PART4
        self.anim_timer += 1

        #part 3 checking ground
        on_ground = self.check_ground(platform_group)
        if on_ground:
            self.y_speed = 0
            self.image = self.idle[0]
        if on_ground and space_flag: #returning self.y_speed to -20 when the player was touch with ground and the space_flag return true
            self.y_speed = -20

#键盘控制 the keyboard control of the player

        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            self.rect.x -= self.x_speed
            #PAGE 5
            self.filppedrun_anim()
            #向右时跳跃
            if space_flag:
                    self.y_speed = -20 #the place in y would move up when the space_flag return true
                    self.jump_wav.play()
                    self.image = self.filpped_jump

        if key[pygame.K_d]:
            self.rect.x += self.x_speed
            #PART 5
            self.run_anim()
            #向左时跳跃
            if space_flag:
                    self.y_speed = -20 #the place in y would move up when the space_flag return true
                    self.jump_wav.play()
                    self.image = self.jump[0]

        if key[pygame.K_f]:
            self.jump_wav.play()
            bullet_group.add(bullet(center=(player_group)))

        if not(key[pygame.K_a] or key[pygame.K_d]):
                if space_flag:
                     self.y_speed = -20
                     self.jump_wav.play()
                     self.image = self.jump[0]
                self.idel_anim()

            

    #cheking for wether the player is on a ground    
    def check_ground(self,platform_group):

        self.rect.y += 60 #strengthing 3 points for checking if the player had touched any platform
        
        hit = pygame.sprite.spritecollide(self,platform_group,False)#这返回一个列表，里面是所有和player碰撞的platform

        self.rect.y -= 60 #shrinking back if the player was touched with any plantform
        if hit:
            if self.y_speed >= 0: #如果玩家是下落的状态才会触发碰撞检测
                self.rect.bottom = hit[0].rect.top#将玩家的底部设置为平台的顶部
                return True
        else:
            return False


                

player_group = pygame.sprite.GroupSingle(player(topleft=(100,100)))#这个是为了让玩家只能有一个，GroupSingle是一个特殊的组，只能有一个精灵

#PART 6 SHOOTING BULLETS
class bullet(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill('red')
        #这个是为了让子弹从玩家的中心位置发射
        # 其中player_group.sprite.rect.centerx是玩家的中心位置的x坐标，player_group.sprite.rect.centery是玩家的中心位置的y坐标
        #子弹速度
        self.x_speed  = 6
        self.y_speed = 0
        self.g = 1


    def update(self):
        #self.y_speed += self.g
        self.rect.x += self.x_speed
        #self.rect.y += self.y_speed
        if self.rect.left > 600:
             self.kill()

bullet_group = pygame.sprite.Group()

    

while running:
    clock.tick(60)

    space_flag = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                space_flag = True #转至125行

        

    screen.blit(bg_img,(0,0))

    #画入平台
    platform_group.draw(screen)
    #画入玩家
    player_group.draw(screen)
    player_group.update(space_flag,platform_group)

    bullet_group.draw(screen)
    bullet_group.update()
    
    #ADDED A FRAME ON PLAYER
    for player in player_group:
        #在玩家周围画一个矩形框
        pygame.draw.rect(screen,  (255, 0, 0), player.rect, width= 1)
        
    pygame.display.flip()
            
        
pygame.quit()
