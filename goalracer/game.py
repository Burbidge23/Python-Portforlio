from settings import *
import sys
from os import path
import pygame as pg
from sprites import *
from tilemap import *

class Game():

    def __init__(self):
        self.playing = True
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.load_data()
        self.create_game_objects()
        pg.key.set_repeat(500, 100)
        self.game_loop()

    def draw_text(self, surf, text, size, x, y, color):
        font = pg.font.Font(font_name, size)
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect()
        text_rect.midtop = (x, y)
        surf.blit(text_surf, text_rect)

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'imgs')
        self.map = Map(path.join(game_folder, 'map2.txt'))
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert()
        self.player_img = pg.transform.scale(self.player_img, (35, 35))
        self.p2_img = pg.image.load(path.join(img_folder, P2IMG)).convert()
        self.p2_img.set_colorkey(WHITE)
        self.p2_img = pg.transform.scale(self.p2_img, (35, 35))
        self.mob_img = pg.image.load(path.join(img_folder, MOB_IMG)).convert_alpha()
        self.bullet_img = pg.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()

        # sounds
        assets_folder = path.join(game_folder, 'assets')
        snd_folder = path.join(assets_folder, 'audio')
        fx_folder = path.join(snd_folder, 'fx')
        music_folder = path.join(snd_folder, 'music')
        self.bumpsnd = pg.mixer.Sound(path.join(fx_folder, 'bump.ogg'))
        self.scoresnd = pg.mixer.Sound(path.join(fx_folder, 'score.ogg'))
        self.music = pg.mixer.music.load(path.join(music_folder, 'music.ogg'))
        pg.mixer.music.set_volume(0.1)
        pg.mixer.music.play(-1)
        self.bumpsnd.set_volume(0.5)

    def create_game_objects(self):
        # creating game objects
        self.all_sprites = pg.sprite.Group()
        self.player_group = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.balls = pg.sprite.Group()
        self.goals = pg.sprite.Group()
        # self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()

        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'r':
                    Goal(self, col, row, 'r')
                if tile == 'l':
                    Goal(self, col, row, 'l')
                if tile == 'P':
                    self.player = Player(self, col, row, 0, 1, self.player_img)
                if tile == '2':
                    self.player2 = Player(self, col, row, 180, 2, self.p2_img)
                if tile == 'B':
                    self.ball = Ball(self, col, row)
            self.camera = Camera(self.map.width, self.map.height)
            self.draw_debug = False

    def check_events(self):
        # Check Events
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                self.playing = False
            if event.type == pg.KEYUP:
                pass
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_h:
                    self.draw_debug = not self.draw_debug
        for goal in self.goals:
            hits = pg.sprite.spritecollide(goal, self.balls, True)
            if hits:
                if goal.side == 'r':
                    self.ball = Ball(self, 17, 7)
                    self.player.score += 1
                    self.player.pos = PLAYER1START * TILESIZE
                    self.player2.pos = PLAYER2START * TILESIZE
                    self.player.boost = 100
                    self.player2.boost = 100
                    self.player.rot = 0
                    self.player2.rot = 180
                    self.scoresnd.play()
                if goal.side == 'l':
                    self.ball = Ball(self, 17, 7)
                    self.player2.score += 1
                    self.player.pos = PLAYER1START * TILESIZE
                    self.player2.pos = PLAYER2START * TILESIZE
                    self.player.boost = 100
                    self.player2.boost = 100
                    self.player.rot = 0
                    self.player2.rot = 180
                    self.scoresnd.play()

    def update(self):
        # update
        self.all_sprites.update()
        self.camera.update(self.ball)
        hits = pg.sprite.groupcollide(self.player_group, self.balls, False, False)
        if hits:
            for hit in hits:
                self.bumpsnd.play()
                self.ball.bump(hit)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, BLUE, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, BLUE, (0, y), (WIDTH, y))

    def draw(self):
        # Draw
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.screen.fill(BROWN)
        # self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        for sprite in self.player_group:
            if self.draw_debug:
                pg.draw.rect(self.screen, BLUE, self.camera.apply_rect(sprite.hit_rect), 1)
        for sprite in self.balls:
            if self.draw_debug:
                pg.draw.rect(self.screen, BLUE, self.camera.apply_rect(sprite.hit_rect), 1)
        self.draw_text(self.screen, 'score 1: ' + str(self.player.score), 45, 200, 40, BLACK)
        self.draw_text(self.screen, 'score 2: ' + str(self.player2.score), 45, 850, 40, BLACK)
        # pg.draw.rect(self.screen, WHITE, self.player.hit_rect, 2)
        pg.display.flip()

    def game_loop(self):
        # game loop

        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.check_events()
            self.update()
            self.draw()
            # Tick
            self.clock.tick(FPS)

