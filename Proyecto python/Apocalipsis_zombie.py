from pygame import *
from random import randint

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)

        # cada objeto debe almacenar una propiedad image
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        # cada objeto debe almacenar la propiedad rect en la cual está inscrito
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    # método que dibuja al personaje en la ventana
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# clase del jugador principal
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 600:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < 400:
            self.rect.y += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -10)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(80, win_width - 80)
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

class DeadlyPoint(sprite.Sprite):
    def __init__(self, player_x, player_y, radius):
        sprite.Sprite.__init__(self)
        self.image = Surface((radius*2, radius*2), SRCALPHA)
        draw.circle(self.image, (255, 255, 255), (radius, radius), radius)
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

def reset_game():
    global score, lost, finish, player, monsters, bullets, deadly_points
    score = 0
    lost = 0
    finish = False
    player = Player("Jugador.png", 5, win_height - 100, 80, 100, 10)
    monsters.empty()
    for i in range(1, 6):
        monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 60, 40, randint(1, 5))
        monsters.add(monster)
    bullets.empty()
    deadly_points.empty()
    for i in range(5):
        deadly_point = DeadlyPoint(randint(80, win_width - 80), randint(80, win_height - 80), 10)
        deadly_points.add(deadly_point)

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Apocalipsis")

img_back = "Apocalipsis fondo.jpg"
img_enemy = "Enemigo.png"
img_bullet = "Bala.png"

score = 0
lost = 0
max_lost = 50
goal = 50

background = transform.scale(image.load(img_back), (win_width, win_height))

FPS = 60
clock = time.Clock()

finish = False
run = True

mixer.init()
mixer.music.load("Adrenalina.ogg")
mixer.music.play()
fire_sound = mixer.Sound("Disparo.ogg")

player = Player("Jugador.png", 5, win_height - 100, 80, 100, 10)

font.init()
font2 = font.SysFont("Arial", 36)

font1 = font.SysFont("Arial", 70)
texto_para_ganador = font1.render("GANASTE!!!!", True, (0, 255, 0))
texto_para_perdedor = font1.render("PERDISTE!!!!", True, (255, 0, 0))

reset_button_font = font.SysFont("Arial", 50)
reset_button_text = reset_button_font.render("Reiniciar", True, (255, 255, 255))
reset_button_rect = reset_button_text.get_rect(center=(win_width // 2, win_height // 2 + 100))

monsters = sprite.Group()

for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 60, 40, randint(1, 5))
    monsters.add(monster)

bullets = sprite.Group()

deadly_points = sprite.Group()
for i in range(5):
    deadly_point = DeadlyPoint(randint(80, win_width - 80), randint(80, win_height - 80), 10)
    deadly_points.add(deadly_point)

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()
                fire_sound.play()
        elif e.type == MOUSEBUTTONDOWN:
            if reset_button_rect.collidepoint(e.pos):
                reset_game()

    if not finish:
        window.blit(background, (0, 0))

        text = font2.render("Puntaje: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Fallados: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        player.update()
        player.reset()

        monsters.update()
        monsters.draw(window)

        bullets.update()
        bullets.draw(window)

        deadly_points.draw(window)

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 90, 60, randint(1, 5))
            monsters.add(monster)

        if sprite.spritecollide(player, monsters, False) or sprite.spritecollide(player, deadly_points, False) or lost >= max_lost:
            finish = True
            window.blit(texto_para_perdedor, (200, 200))
            window.blit(reset_button_text, reset_button_rect.topleft)

        if score >= goal:
            finish = True
            window.blit(texto_para_ganador, (200, 200))
            window.blit(reset_button_text, reset_button_rect.topleft)

        display.update()
    clock.tick(FPS)