import pygame

from settings import *
import pygame as pg
import random
from player import *
from enemy import *
from star import *
from animations import *
from powerUps import *

font_name = pg.font.match_font('Comic Sans MS')


def draw_text(surf, text, size, x, y, color):
    font = pg.font.Font(font_name, size)
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surf, text_rect)


def draw_bar(surf, x, y, pct, color):
    if pct < 0:
        pct = 0
    bar_height = 25
    bar_len = 200
    fill = (pct / 100) * bar_len
    outline_rect = pg.Rect(x, y, bar_len, bar_height)
    fill_rect = pg.Rect(x, y, fill, bar_height)
    pg.draw.rect(surf, color, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 3)


def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)


def show_gameover_screen():
    screen.blit(background, background_rect)
    draw_text(screen, TITLE, 80, WIDTH / 2, HEIGHT / 4, RED)
    draw_text(screen, "A and D to move, Space to fire", 30, WIDTH/2, HEIGHT/2, WHITE)
    draw_text(screen, "Press any key to play or click the X to close", 20, WIDTH/2, HEIGHT*3/4, BLUE)
    pg.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYUP:
                waiting = False


# Setup pygame
pg.init()
pg.mixer.init()  # Setup sound

# Create game objects
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption(TITLE)
clock = pg.time.Clock()
all_sprites = pg.sprite.Group()
player_group = pg.sprite.Group()
enemy_group = pg.sprite.Group()
bullet_group = pg.sprite.Group()
pow_group = pg.sprite.Group()

# load imgs
background = pg.image.load(os.path.join(img_folder, 'starfield.png')).convert()
background = pg.transform.scale(background, (WIDTH, HEIGHT))
background_rect = background.get_rect()

player_img = pg.image.load(os.path.join(img_folder, 'playerShip1_orange.png')).convert()
player_mini_img = pg.transform.scale(player_img, (25, 20))
player_mini_img.set_colorkey(BLACK)

bullet_img = pg.image.load(os.path.join(img_folder, '10.png')).convert()

meteor_img_list = []
meteor_list = ['meteorBrown_big1.png', 'meteorBrown_med1.png',
               'meteorBrown_small1.png', 'meteorBrown_tiny1.png',
               'meteorBrown_big2.png', 'meteorBrown_med3.png',
               'meteorBrown_small2.png', 'meteorBrown_tiny2.png',
               'meteorBrown_big3.png', 'meteorBrown_big4.png',
               'meteorGrey_big1.png', 'meteorGrey_big2.png',
               'meteorGrey_big3.png', 'meteorGrey_big4.png',
               'meteorGrey_med1.png', 'meteorGrey_med2.png',
               'meteorGrey_small1.png', 'meteorGrey_small2.png',
               'meteorGrey_tiny1.png', 'meteorGrey_tiny2.png'
               ]

for img in meteor_list:
    enemy_img = pg.image.load(os.path.join(img_folder, img)).convert()
    meteor_img_list.append(enemy_img)

exp_anim = {}
exp_anim["lg"] = []
exp_anim["sm"] = []
exp_anim["playerExp"] = []
for i in range(9):
    filename = "regularExplosion0{}.png".format(i)
    img = pg.image.load(os.path.join(img_folder, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pg.transform.scale(img, (75, 75))
    exp_anim["lg"].append(img_lg)
    img_sm = pg.transform.scale(img, (30, 30))
    exp_anim["sm"].append(img_sm)
    filename = "sonicExplosion0{}.png".format(i)
    img = pg.image.load(os.path.join(img_folder, filename)).convert()
    img.set_colorkey(BLACK)
    exp_anim['playerExp'].append(img)

pow_img = {}
pow_img["shield"] = pg.image.load(os.path.join(img_folder, "shield_gold.png")).convert()
pow_img["gun"] = pg.image.load(os.path.join(img_folder, "bolt_gold.png")).convert()

# loading in sound assets
shoot_names = ['laser.wav', 'laser2.wav']
shootsnd = []
for snd in shoot_names:
    shootsnd.append(pg.mixer.Sound(os.path.join(fx_folder, snd)))

exp_names = ['expl3.wav', 'expl6.wav']
expsnd = []
for snd in exp_names:
    expsnd.append(pg.mixer.Sound(os.path.join(fx_folder, snd)))

music = pg.mixer.music.load(os.path.join(music_folder, 'spacemusic.ogg'))
pg.mixer.music.set_volume(0.7)

pow_snd = pg.mixer.Sound(os.path.join(fx_folder, "score.wav"))

score = 0

player = Player(player_img, bullet_img, all_sprites, bullet_group, random.choice(shootsnd))

for i in range(20):
    e = Mob(random.choice(meteor_img_list))
    enemy_group.add(e)
    all_sprites.add(e)

for i in range(20):
    starimage = pg.image.load((os.path.join(img_folder, 'star.png')))
    e = Star(starimage)
    all_sprites.add(e)

all_sprites.add(player)
player_group.add(player)

# Sets running to true to start the game loop
running = True
game_over = True
pg.mixer.music.play(loops=-1)

# Game loop

while running:
    if game_over:
        show_gameover_screen()
        game_over = False
        all_sprites = pg.sprite.Group()
        player_group = pg.sprite.Group()
        enemy_group = pg.sprite.Group()
        bullet_group = pg.sprite.Group()
        pow_group = pg.sprite.Group()
        player = Player(player_img, bullet_img, all_sprites, bullet_group, random.choice(shootsnd))

        for i in range(20):
            e = Mob(random.choice(meteor_img_list))
            enemy_group.add(e)
            all_sprites.add(e)

        for i in range(20):
            starimage = pg.image.load((os.path.join(img_folder, 'star.png')))
            e = Star(starimage)
            all_sprites.add(e)

        all_sprites.add(player)
        player_group.add(player)

    # the loop that runs all the code of the game

    # tick clock
    clock.tick(FPS)
    # process events
    # collision with player and asteroids
    hits = pg.sprite.spritecollide(player, enemy_group, True, pg.sprite.collide_circle)
    if hits:
        for hit in hits:
            if hit.radius >= 30:
                size = "lg"
            else:
                size = "sm"
            all_sprites.add(Explosion(size, exp_anim, hit.rect.center))
            random.choice(expsnd).play()
            player.takeDamage(hit)
            enemy = Mob(random.choice(meteor_img_list))
            enemy_group.add(enemy)
            all_sprites.add(enemy)
            if player.shield <= 0:
                death_exp = Explosion("playerExp", exp_anim, player.rect.center)
                all_sprites.add(death_exp)
                player.die()

    if player.lives == 0 and not death_exp.alive():
        game_over = True
        # play explosion sound
        # damage player
        # destroy asteroids
        # spawn replacement
    # Check for collisions between bullets and asteroids
    hits = pg.sprite.groupcollide(enemy_group, bullet_group, True, True)
    if hits:
        for hit in hits:
            score += int(50 - hit.radius)
            e = Mob(random.choice(meteor_img_list))
            enemy_group.add(e)
            all_sprites.add(e)
            if hit.radius >= 30:
                size = "lg"
            else:
                size = "sm"
            all_sprites.add(Explosion(size, exp_anim, hit.rect.center))
            random.choice(expsnd).play()
            if random.random() > 0.9:
                pow = Pow(hit.rect.center, pow_img)
                all_sprites.add(pow)
                pow_group.add(pow)

    hits = pg.sprite.spritecollide(player, pow_group, True)
    if hits:
        for hit in hits:
            pow_snd.play()
            if hit.type == "shield":
                amount = random.randint(25, 80)
                player.addShield(amount)
            if hit.type == "gun":
                player.gun_up()

    for event in pg.event.get():

        if event.type == pg.QUIT:
            running = False
    # update
    all_sprites.update()
    # Render / Draw
    screen.fill(cfBlue)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)

    draw_bar(screen, 25, 25, player.shield, GREEN)
    draw_text(screen, str(score), 25, WIDTH / 2, 25, WHITE)
    draw_text(screen, "Shield", 20, 130, 22, WHITE)

    # draw_bar(screen, 375, 25, player.fuel, BLUE)
    # draw_text(screen, "Fuel", 20, 475, 22, WHITE)

    draw_lives(screen, WIDTH - 100, 10, player.lives, player_mini_img)

    # This must be the last call in draw
    pg.display.flip()
