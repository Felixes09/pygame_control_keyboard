import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))

bg_img = pygame.image.load('background.png').convert()
bg_img = pygame.transform.scale(bg_img, (800, 600))
running = True

clock = pygame.time.Clock()

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
        self.image = pygame.Surface((50, 50))
        self.image.fill('red')
        self.rect = self.image.get_rect(topleft = topleft)
        self.g = 1
        self.y_speed = 1
        self.x_speed = 5

    def check_ground(self, platform_group):

        self.rect.y += 3
        hit = pygame.sprite.spritecollide(self, platform_group, False)
        self.rect.y -= 3
        if hit:
            self.rect.bottom = hit[0].rect.top
            return True
        return False
        



    def update(self, space_flag, platform_group):
        self.y_speed += self.g
        self.rect.bottom += self.y_speed
        key = pygame.key.get_pressed()        
        if key[pygame.K_a]:
            self.rect.right -= self.x_speed

        if key[pygame.K_d]:
            self.rect.right += self.x_speed

        on_ground = self.check_ground(platform_group)

        if on_ground:
            self.y_speed = 0
        
        if on_ground and space_flag:
            self.y_speed = -20
            
        
        
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

    platform_group.draw(screen)
    player_group.draw(screen)
    

    pygame.display.flip()

pygame.quit()