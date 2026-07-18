import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))

bg_img = pygame.image.load('background.png').convert()
bg_img = pygame.transform.scale(bg_img, (800, 600))
running = True

clock = pygame.time.Clock()


class Bullet(pygame.sprite.Sprite):

    def __init__(self, center):
        super().__init__()
        self.image = pygame.Surface((12, 12))
        self.image.fill('red')
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.x_speed = 4

    def update(self):
        self.rect.x += self.x_speed
        if self.rect.x > 800:
            self.kill()


bullet_group = pygame.sprite.Group()

class Platform(pygame.sprite.Sprite):
    def __init__(self, topleft):
        super().__init__()
        self.image = pygame.Surface((200, 20))
        self.image.fill('white')
        self.rect = self.image.get_rect(topleft = topleft)

platform_group = pygame.sprite.Group() 
platform_group.add(Platform(topleft=(400, 400)))
platform_group.add(Platform(topleft=(100, 400)))
platform_group.add(Platform(topleft=(100, 150)))

class Player(pygame.sprite.Sprite):
    def __init__(self, topleft):
        super().__init__()
        
        self.idle = [
            pygame.transform.scale(
                pygame.image.load(f'player/idle/{i:02d}.png'), (100, 100))
            for i in range(0, 22)
        ]

        self.run = [
            pygame.transform.scale(
                pygame.image.load(f'player/run/{i}.png'), (100, 100))
            for i in range(0, 8)
        ]
        for image in self.run:
            image.set_colorkey((0, 0, 0))
        self.jump_wav = pygame.mixer.Sound('shoot.wav')
        self.image = self.idle[0]
        # self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(topleft = topleft)
        self.g = 1
        self.y_speed = 1
        self.x_speed = 5

        self.run_frame_index = 0
        self.idle_frame_index = 0
        self.anim_timer = 0
        self.anim_speed = 8

    def run_anim(self):
        if self.anim_timer >= self.anim_speed:
            self.run_frame_index = (self.run_frame_index + 1) % len(self.run)
            self.anim_timer = 0
        self.image = self.run[self.run_frame_index]
    
    def idel_anim(self):
        if self.anim_timer >= self.anim_speed:
            self.idle_frame_index = (self.idle_frame_index + 1) % len(self.idle)
            self.anim_timer = 0
        self.image = self.idle[self.idle_frame_index]

    def check_ground(self, platform_group):

        self.rect.y += 3
        hit = pygame.sprite.spritecollide(self, platform_group, False)
        self.rect.y -= 3
        if hit:
            self.rect.bottom = hit[0].rect.top
            return True
        return False
    
    def update(self, space_flag, platform_group):
        
        self.anim_timer += 1
        # if self.anim_timer >= self.anim_speed:
        #     self.frame_index = (self.frame_index + 1) % len(self.idle)
        #     self.anim_timer = 0
        # self.image = self.idle[self.frame_index]

        self.y_speed += self.g
        self.rect.bottom += self.y_speed
        key = pygame.key.get_pressed()        
        if key[pygame.K_a]:
            self.rect.right -= self.x_speed
            self.run_anim()

        if key[pygame.K_d]:
            self.rect.right += self.x_speed
            self.run_anim()
        
        if key[pygame.K_c]:
            bullet_group.add(Bullet(center=self.rect.center))

        if not(key[pygame.K_a] or key[pygame.K_d]):
            # self.image = self.idle[self.frame_index]
            self.idel_anim()

        on_ground = self.check_ground(platform_group)

        if on_ground:
            self.y_speed = 0
        
        if on_ground and space_flag:

            self.y_speed = -20
            self.jump_wav.play()
            
        
        
        # if space_flag:
        #     self.y_speed = -20

        # if self.check_ground(platform_group):
        #     self.y_speed = 0
        #     self.g = 0





player_group = pygame.sprite.GroupSingle(Player(topleft=(100, 100)))

while running:
    clock.tick(60)
    space_flag = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                space_flag = True
    
    screen.blit(bg_img, (0, 0)) 

    player_group.update(space_flag, platform_group)

    for player in player_group:
        pygame.draw.rect(screen,  (255, 0, 0), player.rect, width= 10)

    bullet_group.update()


    platform_group.draw(screen)
    player_group.draw(screen)
    bullet_group.draw(screen)
    

    pygame.display.flip()

pygame.quit()