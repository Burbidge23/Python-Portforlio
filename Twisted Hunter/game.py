from settings import *
import pygame as pg
from sprites import *
from animations import *


class Game():

    def __init__(self):
        super(Game, self).__init__()
        self.playing = True
        self.start_screen = True
        self.game_over = False
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        pg.display.set_caption(TITLE)
        self.start_screen_music = pg.mixer.music.load(os.path.join(music_folder, 'music.wav'))
        self.background = pg.image.load(os.path.join(background_folder, 'background.png')).convert()
        self.background = pg.transform.scale(self.background, (WIDTH, HEIGHT))
        self.background_rect = self.background.get_rect()
        self.walk_anim = []
        for i in range(2):
            filename = "walking-{}.png".format(i)
            img = pg.image.load(os.path.join(objects_folder, filename))
            img = pg.transform.scale(img, (100, 100))
            self.walk_anim.append(img)
        self.jump_anim = []
        for i in range(2):
            filename = "jump{}.png".format(i)
            img = pg.image.load(os.path.join(objects_folder, filename))
            img = pg.transform.scale(img, (100, 100))
            self.jump_anim.append(img)
        self.allsprites = pg.sprite.Group()
        self.mousesprites = pg.sprite.Group()
        self.enemysprites = pg.sprite.Group()
        self.dogsprite = pg.sprite.Group()
        self.dogwinsprite = pg.sprite.Group()
        x, y = pg.mouse.get_pos()
        self.crosshair_img = pg.image.load(os.path.join(player_folder, 'crosshair.png'))
        self.mouse_sprite = MouseSprite(x, y, self)

        self.game_loop()

    def draw_text(self, surf, text, size, x, y, color):
        font = pg.font.Font(font_name, size)
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect()
        text_rect.midtop = (x, y)
        surf.blit(text_surf, text_rect)

    def draw_bar(self, surf, x, y, pct, color):
        if pct < 0:
            pct = 0
        bar_height = 25
        bar_len = 200
        fill = (pct / 100) * bar_len
        outline_rect = pg.Rect(x, y, bar_len, bar_height)
        fill_rect = pg.Rect(x, y, fill, bar_height)
        pg.draw.rect(surf, color, fill_rect)
        pg.draw.rect(surf, WHITE, outline_rect, 3)

    def draw_lives(self, surf, x, y, lives, img):
        for i in range(lives):
            img_rect = img.get_rect()
            img_rect.x = x + 30 * i
            img_rect.y = y
            surf.blit(img, img_rect)

    def create_game_objects(self):
        # creating game objects
        pg.mouse.set_visible(0)
        self.round1 = True
        self.score = 0
        self.load_imgs()
        self.load_sounds()
        self.ammo = 3
        self.total_ducks = 10
        self.hit_ducks = 0
        self.missed_ducks = 0
        self.allsprites = pg.sprite.Group()
        self.mousesprites = pg.sprite.Group()
        self.enemysprites = pg.sprite.Group()
        self.dogsprite = pg.sprite.Group()
        self.dogwinsprite = pg.sprite.Group()


        # self.enemy = Player(self)
        self.enemy = Enemy(self, self.enemy_img)
        x, y = pg.mouse.get_pos()
        self.crosshair_img = pg.image.load(os.path.join(player_folder, 'crosshair.png'))
        self.mouse_sprite = MouseSprite(x, y, self)




    def load_sounds(self):
        self.shootsnd = pg.mixer.Sound(os.path.join(audio_folder, 'shootsnd.wav'))
        self.diedogsnd = pg.mixer.Sound(os.path.join(audio_folder, 'diedog.wav'))
        self.scoresnd = pg.mixer.Sound(os.path.join(audio_folder, 'score.wav'))
        self.endsnd = pg.mixer.Sound(os.path.join(audio_folder, 'endsound.wav'))
        self.failsnd = pg.mixer.Sound(os.path.join(audio_folder, 'failsnd.wav'))
        self.start_screen_music = pg.mixer.music.load(os.path.join(music_folder, 'music.wav'))

    def load_imgs(self):
        self.background_nosky = pg.image.load(os.path.join(background_folder, 'backgroundnosky.png'))
        self.background_nosky = pg.transform.scale(self.background_nosky, (WIDTH, HEIGHT))
        self.background_nosky.set_colorkey(BLACK)
        self.background_nosky_rect = self.background_nosky.get_rect()
        self.enemy_img = pg.image.load(os.path.join(enemy_folder, 'enemy1.png')).convert()
        self.enemy_img.set_colorkey(WHITE)


        self.dead_duckimg = pg.image.load(os.path.join(enemy_folder, 'deadenemy.png')).convert()
        self.dead_duckimg.set_colorkey(WHITE)
        self.fall_anim = []
        for i in range(2):
            filename = "falling{}.png".format(i)
            img = pg.image.load(os.path.join(enemy_folder, filename)).convert()
            img.set_colorkey(WHITE)
            img = pg.transform.scale(img, (50, 50))
            self.fall_anim.append(img)
        self.enemy_anim = []
        for i in range(3):
            filename = "enemy{}.png".format(i)
            img = pg.image.load(os.path.join(enemy_folder, filename)).convert()
            img.set_colorkey(WHITE)
            img = pg.transform.scale(img, (50, 50))
            self.enemy_anim.append(img)
        self.dog_lose_anim = []
        for i in range(2):
            filename = "laugh{}.png".format(i)
            img = pg.image.load(os.path.join(objects_folder, filename))
            img = pg.transform.scale(img, (50, 50))
            self.dog_lose_anim.append(img)
        self.dog_win_img = pg.image.load(os.path.join(objects_folder, 'duckgrab.png'))
        self.dead_dog = pg.image.load(os.path.join(objects_folder, 'deaddog.png'))


    def check_events(self):
        # Check Events
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                self.playing = False
            if event.type == pg.MOUSEMOTION:
                self.mouse_sprite.update()
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.ammo > 0:
                        self.shootsnd.play()
                        self.ammo -= 1
                        hits = pg.sprite.spritecollide(self.mouse_sprite, self.enemysprites, False)
                        if hits:
                            if not hits[0].hit_peak:
                                    self.score += 500
                                    self.scoresnd.play()
                                    self.ammo = 3
                                    self.hit_ducks += 1
                                    fall_anim = Falling( self.fall_anim, hits[0].rect.center, self)
                                    self.allsprites.add(fall_anim)
                                    hits[0].kill()
                                    self.enemy = Enemy(self, self.enemy_img)

                elif event.button == 3:
                    print("right")

    def show_gameover_screen(self):
        pg.mixer.music.play(-1)
        if self.missed_ducks > 3:
            self.enddog = EndDog(self, True)
        else:
            self.enddog = EndDog(self)
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            self.screen.blit(self.background, self.background_rect)
            self.dogwinsprite.draw(self.screen)
            self.allsprites.update()
            self.screen.blit(self.background_nosky, self.background_nosky_rect)
            self.draw_text(self.screen, TITLE, 80, WIDTH / 2, HEIGHT / 4, BLACK)
            self.draw_text(self.screen, 'YOU SCORED:' + str(self.score), 30, WIDTH / 2, HEIGHT / 2, BLACK)
            self.draw_text(self.screen, 'YOU HIT ' + str(self.hit_ducks) + ' OUT OF ' + str(self.total_ducks), 20,
                           WIDTH / 2, HEIGHT * 7 / 8, BLACK)
            self.draw_text(self.screen, "Right click to play again", 20, WIDTH / 2, HEIGHT * 15 / 16, BLACK)
            self.mousesprites.draw(self.screen)
            pg.display.flip()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.ammo > 0:
                            self.shootsnd.play()
                            self.ammo -= 1
                            hits = pg.sprite.spritecollide(self.mouse_sprite, self.dogwinsprite, False)
                            if hits:
                                    self.scoresnd.play()
                                    self.ammo = 3
                                    self.diedogsnd.play()
                                    self.deaddog = DeadDog(self, hits[0].rect.centerx, hits[0].rect.centery)
                                    hits[0].kill()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 3:
                        waiting = False
    def show_start_screen(self):
        pg.mixer.music.play(-1)
        self.dog = Dogintro(self)
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            self.allsprites.update()
            self.screen.blit(self.background, self.background_rect)
            self.draw_text(self.screen, TITLE, 80, WIDTH / 2, HEIGHT / 4, BLACK)
            self.draw_text(self.screen, 'Shoot the ducks to score!', 30, WIDTH / 2, HEIGHT / 2, BLACK)
            self.draw_text(self.screen, 'Left click to shoot!', 20, WIDTH / 2, HEIGHT * 3 / 4, BLACK)
            self.draw_text(self.screen, "Shoot to start", 20, WIDTH / 2, HEIGHT * 7 / 8, BLACK)
            self.allsprites.draw(self.screen)
            self.mousesprites.draw(self.screen)
            pg.display.update()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    waiting = False
                    pg.mixer.music.set_volume(0.5)

    def update(self):
        # update
        if self.game_over:
            self.show_gameover_screen()
            self.game_over = False
            self.create_game_objects()
        if self.start_screen:
            self.show_start_screen()
            self.start_screen = False
            self.create_game_objects()

        self.allsprites.update()
        if self.ammo <= 0:
            self.enemy.missed()
            self.failsnd.play()
            self.missed_ducks += 1
        if self.hit_ducks + self.missed_ducks == self.total_ducks:
            self.endsnd.play()
            self.game_over = True

    def draw(self):
        # Draw
        self.screen.blit(self.background, self.background_rect)
        self.allsprites.draw(self.screen)
        self.screen.blit(self.background_nosky, self.background_nosky_rect)
        self.dogsprite.draw(self.screen)
        self.draw_text(self.screen, str(self.score), 50, WIDTH - 100, HEIGHT - 140, WHITE)
        self.draw_text(self.screen, 'SCORE', 50, WIDTH - 100, HEIGHT - 90, WHITE)
        self.mousesprites.draw(self.screen)
        self.draw_text(self.screen, 'ammo: ' + str(self.ammo), 50, 100, HEIGHT - 90, WHITE)
        pg.display.update()

    def game_loop(self):
        # game loop

        while self.playing:
            self.check_events()
            self.update()
            self.draw()
            # Tick
            self.clock.tick(FPS)

