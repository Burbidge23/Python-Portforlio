from settings import *
import pygame as pg
from game_object import *
from player import *
from enemy import *


class Game():

    def __init__(self):
        self.playing = True
        self.level = 1
        self.load_sound()
        self.create_game_objects()
        self.reset_level()

    def load_sound(self):
        pg.mixer.music.set_volume(0.5)
        pg.mixer.music.load("assets/audio/music/MattOglseby - 2.ogg")
        self.walk_sound = pg.mixer.Sound("assets/audio/fx/walk.wav")
        self.die_sound = pg.mixer.Sound("assets/audio/fx/dying.wav")
        self.score_sound = pg.mixer.Sound("assets/audio/fx/score.wav")

    def create_game_objects(self):
        # creating game objects
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.background = Game_object(0, 0, WIDTH, HEIGHT, "assets/imgs/bgimgs/background.png")
        self.player = Player(player_start_x, player_start_y, player_w,
                             player_h, player_img_path, player_speed)
        self.coin = Game_object(coin_x, coin_y, coin_w, coin_h, coin_path)

    def reset_level(self):
        self.level += .25
        speed = 5 + self.level * 5

        starting_pos = HEIGHT - 200
        self.enemies = []
        for i in range(int(self.level//1)):
            enemy = Enemy(enemy_start_x, starting_pos, enemy_w,
                          enemy_h, enemy_img_path, speed)
            self.enemies.append(enemy)
            starting_pos -= 200

    def check_events(self):
        # Check Events
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                self.playing = False
            if event.type == pg.KEYUP:
                if event.key == pg.K_1:
                    self.screen.fill(RED)
                elif event.key == pg.K_2:
                    self.screen.fill(BLUE)
                else:
                    self.screen.fill(CF_BLUE)
                if event.key == pg.K_w:
                    self.walk_sound.stop()
                    self.player.move_stop()
                if event.key == pg.K_s:
                    self.walk_sound.stop()
                    self.player.move_stop()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_w:
                    self.walk_sound.play(loops=-1)
                    self.player.move_up()
                elif event.key == pg.K_s:
                    self.walk_sound.play(loops=-1)
                    self.player.move_down()

    def update(self):
        # update
        self.player.move()
        for enemy in self.enemies:
            enemy.move()

        # Check collision between player and enemy
        for enemy in self.enemies:
            if self.detect_collisions(self.player,enemy):
                self.walk_sound.stop()
                self.die_sound.play()
                print("You got hit by a log")
                self.player.die()
                if self.player.lives <=0:
                    self.playing = False

        # Check collisions between player and coin
        if self.detect_collisions(self.player,self.coin):
            self.score_sound.play()
            print("You win!")
            self.player.score_up(1)
            self.player.reset()
            self.reset_level()

    def draw(self):
        # Draw
        self.screen.blit(self.background.img, (self.background.x, self.background.y))
        self.screen.blit(self.coin.img, (self.coin.x, self.coin.y))
        self.screen.blit(self.player.img, (self.player.x, self.player.y))
        for enemy in self.enemies:
            self.screen.blit(enemy.img, (enemy.x, enemy.y))

        self.draw_text(self.screen, "Lives: " + str(self.player.lives), "impact", 25, 250, 15, WHITE)
        self.draw_text(self.screen, "Score: " + str(self.player.score), "impact", 25, WIDTH - 250, 15, WHITE)





        pg.display.update()

    def game_loop(self):
        pg.mixer.music.play(loops=-1)
        # game loop

        while self.playing:
            self.check_events()
            self.update()
            self.draw()
            # Tick
            self.clock.tick(FPS)

    def detect_collisions(self,obj1,obj2):
        if obj1.y > (obj2.y + obj2.h):
            return False
        elif (obj1.y +obj1.h) < obj2.y:
            return False
        if obj1.x > (obj2.x + obj2.w):
            return False
        elif (obj1.x +obj1.w) < obj2.x:
            return False


        return True

    def draw_text(self, surf, text, font, size, x, y, color):
        try:
            font_name = pg.font.match_font(font)
        except:
            font_name = pg.font.match_font("arial")
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surf.blit(text_surface, text_rect)

    def start_screen(self):
        self.screen.fill(CF_BLUE)
        enemyimg = Enemy(WIDTH / 2 - 40, HEIGHT / 2, 80, 80, enemy_img_path, 0)
        self.screen.blit(enemyimg.img, (enemyimg.x, enemyimg.y))
        self.draw_text(self.screen, TITLE, "impact", 50, WIDTH / 2, HEIGHT / 2 - 50, RED)
        self.draw_text(self.screen, "Use W and S to maneuver past the logs to get the gold coin!",
                       "impact", 25, WIDTH / 2, HEIGHT / 2 + 100, RED)
        self.draw_text(self.screen, "Press any key to begin!", "impact", 25,
                       WIDTH / 2, HEIGHT / 2 + 150, GREEN)
        self.draw_text(self.screen, "By Chris Burbidge", "impact", 25,
                       WIDTH / 2, HEIGHT / 2 + 200, GREEN)

        pg.display.flip()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.KEYUP:
                    waiting = False

    def end_screen(self):
        self.draw_text(self.screen, "GAME OVER", "impact", 50, WIDTH / 2, HEIGHT / 2 - 50, RED)
        self.draw_text(self.screen, "Press Enter to play again",
                       "impact", 25, WIDTH / 2, HEIGHT / 2 + 100, RED)
        self.draw_text(self.screen, "Or press esc to Quit", "impact", 25,
                       WIDTH / 2, HEIGHT / 2 + 150, GREEN)
        pg.display.flip()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.KEYUP:
                    if event.key == pg.K_RETURN:
                        waiting = False
                        self.playing = True
                        self.level = 1
                        self.player.replay()
                    if event.key == pg.K_ESCAPE:
                        return False

        return True

