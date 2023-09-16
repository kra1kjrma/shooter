import pygame
import random
import time

WIDTH = 800
HEIGHT = 800
SIZE = (WIDTH,HEIGHT)
FPS = 60
score = 0
pygame.font.init()
font1 = pygame.font.Font(None, 36)
lost = 0
game_over = False


window = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Space Invaders")
background = pygame.transform.scale(
    pygame.image.load("galaxy.jpg"),
    SIZE
)

clock = pygame.time.Clock()

pygame.font.init()

pygame.mixer.init()
pygame.mixer.music.load("space.ogg")
pygame.mixer.music.play()

bullets = pygame.sprite.Group()
fire_sound = pygame.mixer.Sound("fire.ogg")


class GameSprite(pygame.sprite.Sprite):
    def __init__(self, filename, x,y, size, speed):
        super().__init__()
        self.image  = pygame.transform.scale(
            pygame.image.load(filename), size
        )

        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y
        
        self.speed = speed
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed

        if keys_pressed[pygame.K_RIGHT] and self.rect.x < WIDTH-70:
            self.rect.x += self.speed
        
        if keys_pressed[pygame.K_UP]:
            self.rect.y -= self.speed

        if keys_pressed[pygame.K_DOWN] and self.rect.y < HEIGHT-70:
            self.rect.y += self.speed
        
        if self.rect.y < 0: 
            self.rect.x = random.randint(0,800)
            self.rect.y = random.randint(0,800)

    def fire(self):
        bullet = Bullet("bullet.png", player.rect.x+23, player.rect.y, (5,15), 4)
        bullets.add(bullet)
        fire_sound.play()


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > HEIGHT: 
            self.rect.x = random.randint(0, 800)
            self.rect.y = 0
            global lost
            lost = lost + 1

enemies = pygame.sprite.Group()
enemies_num = 5

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed

        if self.rect.y < 0:
            self.kill()

for i in range(enemies_num):
    enemy = Enemy("ufo.png", WIDTH/2, 0, (70,70), random.randint(1,5))
    enemies.add(enemy)

player = Player("rocket.png", WIDTH/2, HEIGHT-70, (50,70), 5)



while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.fire()

    window.blit(background, (0,0))
    player.reset()
    player.update()
    enemies.update()
    enemies.draw(window)
    bullets.update()
    bullets.draw(window)

    text_scored = font1.render("Вбито:" + str(score), True, (255,255,255))
    window.blit(text_scored, (0,0))

    killed_enemies = pygame.sprite.groupcollide(
        enemies, bullets, True, True
    )
    for ke in killed_enemies:
        score += 1
        new_enemy = Enemy("ufo.png", random.randint(0,WIDTH), 0, (70,70), random.randint(1,5))
        enemies.add(new_enemy)
    
    if score == 100 or pygame.sprite.spritecollide(player, enemies, True):
        game_over = True

    pygame.display.update()
    clock.tick(60)