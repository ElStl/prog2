import pygame
from pygame import font
from sprites import *
from config import *
import sys

class Game:
    def __init__(self):
        pygame.init()
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.display = pygame.Surface((WIN_WIDTH, WIN_HIGHT))
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HIGHT))
        self.font_name = '8-BIT WONDER.TTF'
        self.font = pygame.font.Font(self.font_name, TILESIZE)
        self.clock = pygame.time.Clock()
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.curr_menu = self.main_menu

        self.character_spritesheet = Spritesheet("../img/character.png")
        self.terrain_spritesheet = Spritesheet("../img/terrain.png")
        self.enemy_spritesheet = Spritesheet("../img/enemy.png")
        self.attack_spritesheet = Spritesheet("../img/attack.png")
        self.go_background = pygame.image.load("../img/black.png")
        self.bush = SpritesheetToHor("../img/terrain_new.png")
        self.coin = SpritesheetToHor("../img/coin.png")

    def createTilemap(self):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == "B":
                    Block(self, j, i)
                if column == "E":
                    Enemy(self, j, i)
                if column == "W":
                    Water(self, j, i)
                if column == "C":
                    WallVer(self, j, i)
                if column == "K":
                    WallHor(self, j, i)
                if column == "O":
                    Coin(self, j, i)
                if column == "P":
                    self.player = Player(self, j, i)

    def new(self):
        #új játék
        self.playing = True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()

        self.createTilemap()

    def events(self):
        # game loop events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.player.facing == "up":
                        Attack(self, self.player.rect.x, self.player.rect.y - TILESIZE)
                    if self.player.facing == "down":
                        Attack(self, self.player.rect.x, self.player.rect.y + TILESIZE)
                    if self.player.facing == "left":
                        Attack(self, self.player.rect.x - TILESIZE, self.player.rect.y)
                    if self.player.facing == "right":
                        Attack(self, self.player.rect.x + TILESIZE, self.player.rect.y)

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface, text_rect)

    def update(self):
        # game loop updates
        self.all_sprites.update()

    def draw(self):
        # game loop draw
        self.screen.fill(THEGREEN)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        # dest = (100, 100)
        # self.screen.blit(self.map_img, dest)
        pygame.display.update()

    def main(self):
        # game loop
        while self.playing:
            self.events()
            self.display.fill(BLACK)
            self.screen.blit(self.display, (0,0))
            self.update()
            self.draw()
            self.reset_keys()

    def game_over(self):
        gameover = self.font.render("Game Over", True, WHITE)
        gameover_rect = gameover.get_rect(center=(WIN_WIDTH/2, WIN_HIGHT/2 - 20))
        text = self.font.render("Press enter to restart", True, WHITE)
        text_rect = text.get_rect(center=(WIN_WIDTH/2, WIN_HIGHT/2 + 20))
        self.state = "Start"
        # restart_button = Button(WIN_WIDTH/2, WIN_HIGHT/2, WIN_WIDTH, WIN_HIGHT, WHITE, BLACK, " ", TILESIZE)
        
        for sprite in self.all_sprites:
            sprite.kill()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.new()
                        self.main()

            self.screen.blit(self.go_background, (0,0))
            self.screen.blit(text, text_rect)
            self.screen.blit(gameover, gameover_rect)
            self.clock.tick(FPS)
            pygame.display.update()

class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = WIN_WIDTH / 2, WIN_HIGHT / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 100

    def draw_cursor(self):
        self.game.draw_text('*', 15, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.game.screen.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()

class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 50
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 70
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.events()
            self.check_input()
            self.game.display.fill(BLACK)
            self.game.draw_text('Main Menu', 20, WIN_WIDTH / 2, WIN_HIGHT / 2 - 20)
            self.game.draw_text("Start Game", 20, self.startx, self.starty)
            self.game.draw_text("Options", 20, self.optionsx, self.optionsy)
            self.game.draw_text("Credits", 20, self.creditsx, self.creditsy)
            self.draw_cursor()
            self.blit_screen()


    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
        elif self.game.UP_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Start':
                self.game.playing = True
            if self.state == 'Options':
                self.game.curr_menu = self.game.options
            if self.state == 'Credits':
                self.game.curr_menu = self.game.credits
            self.run_display = False

class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Volume'
        self.volx, self.voly = self.mid_w, self.mid_h + 20
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 40
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.events()
            self.check_input()
            self.game.display.fill((0, 0, 0))
            self.game.draw_text('Options', 20, WIN_WIDTH / 2, WIN_HIGHT / 2 - 30)
            self.game.draw_text("Volume", 15, self.volx, self.voly)
            self.game.draw_text("Controls", 15, self.controlsx, self.controlsy)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.UP_KEY or self.game.DOWN_KEY:
            if self.state == 'Volume':
                self.state = 'Controls'
                self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy)
            elif self.state == 'Controls':
                self.state = 'Volume'
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)

class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Credits', 20, WIN_WIDTH / 2, WIN_HIGHT / 2 - 20)
            self.game.draw_text('Made by me', 15, WIN_WIDTH / 2, WIN_HIGHT / 2 + 10)
            self.blit_screen()

g = Game()
g.new()
while g.running:
    g.curr_menu.display_menu()
    g.main()
    g.game_over()
    g.yourewinner()


pygame.quit()
sys.exit()




