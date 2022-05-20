from settings import *
import os
import pygame as pg
from game_object import *
from player import *
from enemy import *

class Game():
    def __init__(self):
        self.playing = True
        self.create_game_objects()
        self.sound_create()
        self.game_over = True

        self.game_loop()


    def draw_bar(self, surf, x, y, pct, color):
        if pct < 0:
            pct = 0
        bar_height = 25
        bar_len = 200
        fill = (pct / 100) * bar_len
        outline_rect = pg.Rect(x, y, bar_len, bar_height)
        fill_rect = pg.Rect(x, y, fill, bar_height)
        pg.draw.rect(surf, color, fill_rect)
        pg.draw.rect(surf, BLACK, outline_rect, 3)

    def draw_text(self, surf, text, size, x, y, color):
        self.font_name = pg.font.match_font('Comic Sans MS')
        font = pg.font.Font(self.font_name, size)
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect()
        text_rect.midtop = (x, y)
        surf.blit(text_surf, text_rect)

    def sound_create(self):
        music = pg.mixer.music.load("assets/audio/music/fight_looped.wav")
        pg.mixer.music.set_volume(0.7)
        pg.mixer.music.play(loops=-1)
        self.shootsnd = pg.mixer.Sound("assets/audio/fx/laser.wav")
        self.explosionsnd = pg.mixer.Sound("assets/audio/fx/expl3.wav")

    def create_game_objects(self):
        # creating game objects
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.player_sprites = pg.sprite.Group()
        self.enemy_sprites = pg.sprite.Group()
        self.enemy_bullet_group = pg.sprite.Group()
        self.player_bullet_group = pg.sprite.Group()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.background = Game_object(0, 0, WIDTH, HEIGHT)
        self.bullet_img = pg.image.load("assets/imgs/sprites/enemy/10.png")
        self.player_img = pg.image.load("assets/imgs/sprites/player/16.png").convert()
        self.player = Player(self.player_img, self.bullet_img, self)
        self.all_sprites.add(self.player)
        self.player_sprites.add(self.player)
        self.enemy_img = pg.image.load("assets/imgs/sprites/enemy/6.png")
        for i in range(0, 5):
            self.enemy_i = Enemy(self, self.enemy_img)
            self.enemy_sprites.add(self.enemy_i)


    def check_events(self):
        # Check Events
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                quit()
                self.playing = False
            if event.type == pg.KEYUP:
                pass

        hits = pg.sprite.spritecollide(self.player, self.enemy_bullet_group, True)
        if hits:
            for hit in hits:
                self.player.hit()

        hits = pg.sprite.groupcollide(self.enemy_sprites, self.player_bullet_group, True, True)
        if hits:
            self.explosionsnd.play()
            self.enemy = Enemy(self, self.enemy_img)
            self.enemy_sprites.add(self.enemy)
            self.player.regen()
            self.score += 1
            if self.score % 10 == 0 and len(self.enemy_sprites) < 25:
                self.enemy = Enemy(self, self.enemy_img)
                self.enemy_sprites.add(self.enemy)
                


    def update(self):
        # update
        if self.game_over:
            self.show_game_over()
            self.create_game_objects()
            self.game_over = False
        self.player_sprites.update()
        self.enemy_sprites.update()
        self.enemy_bullet_group.update()
        self.player_bullet_group.update()
        if not self.player.alive:
            self.game_over = True

    def show_game_over(self):
        self.screen.blit(self.background.img, (self.background.x, self.background.y))
        self.draw_text(self.screen, TITLE, 80, WIDTH / 2, HEIGHT / 4, BLUE)
        self.draw_text(self.screen, "WASD to move and Space to fire", 30, WIDTH / 2, HEIGHT / 2, BLACK)
        self.draw_text(self.screen, "Press any key to play or click the X to close", 20, WIDTH / 2, HEIGHT * 3 / 4, BLACK)
        pg.display.flip()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    quit()
                    pg.quit()
                if event.type == pg.KEYUP:
                    waiting = False

    def draw(self):
        # Draw
        self.screen.blit(self.background.img, (self.background.x, self.background.y))
        self.all_sprites.draw(self.screen)
        self.draw_bar(self.screen, 25, 25, self.player.health, RED)
        self.draw_text(self.screen, str(self.score), 25, WIDTH / 2, 25, BLACK)
        self.draw_text(self.screen, "Ammo: " + str(self.player.ammo), 25, WIDTH * .75, 25, BLACK)

        pg.display.update()

    def game_loop(self):
        # game loop
        while self.playing:
            # Tick
            self.dt = self.clock.tick(FPS) / 1000.0
            self.clock.tick(FPS)
            self.check_events()
            self.update()
            self.draw()


