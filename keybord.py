import pygame



pygame.init()
screen = pygame.display.set_mode((800,600))
bg_img = pygame.image.load('background.png',).convert()
bg_img = pygame.transform.scale(bg_img,(800,600))

running=True

clock= pygame.time.Clock()

class Plantform(pygame.sprite.Sprite):
    def __init__(self, topleft):
        super().__init__()
        #这两项是强制的

        self.image = pygame.Surface((200,20))
        self.image.fill ('white')
        self.rect = self.image.get_rect(topleft= topleft)

Plantform_group = pygame.sprite.Group()
Plantform_group.add(Plantform(topleft=(400,400)))
Plantform_group.add(Plantform(topleft=(100,400)))
Plantform_group.add(Plantform(topleft=(100,150)))




class Player(pygame.sprite.Sprite):
    def __init__(self, topleft):
        super().__init__()
        #这两项是强制的

        self.image = pygame.Surface((50, 50))
        self.image.fill('red')
        self.rect = self.image.get_rect(topleft = topleft)
        self.g= 1
        self.y_speed = 1


    def update(self,space_flag):

        self.y_speed += self.g
        self.rect.bottom += self.y_speed
        key=pygame.key.get_pressed()#返回的是列表
        
        if key[pygame.K_a]:
         
         self.rect.right -=2

        if key[pygame.K_d]:
         
         self.rect.right +=2

        if space_flag:
          
          self.y_speed = -20

    



Player_group = pygame.sprite.GroupSingle(Player(topleft= (100,100)))


while running:
    clock.tick(20)
    space_flag=False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type==pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                space_flag = True


    screen.blit(bg_img,(0,0))

    
    Player_group.update(space_flag=space_flag)
    Player_group.draw(screen)
    Plantform_group.draw(screen)

    pygame.display.flip()

pygame.quit()