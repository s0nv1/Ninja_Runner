import pygame, sys
import random
from settings import *
from player_hero import Player_hero
from enemys import *
from hero_images import dead_boy, dead_girl
from hero_moving_bg import *
from screen_bg_img import *
from highscore import HighScoreTable


pygame.init()

screen_bg = [(darkmain, dark_main_ground),
            (sand_bg, sand_bg_ground),
            (darkforest, darkfor_ground),
            (bg_img_sc, bg_img_sc_ground),
            ]
            
            
class Game:
    
    def __init__(self):

        # general setup
        self.screen = pygame.display.set_mode((WEIGHT, HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Ninja Runner')
        
        # screen count
        self.screen_count = 0
        self.screen_bg = screen_bg[self.screen_count][0]
        self.ground_bg = screen_bg[self.screen_count][1]
        self.start_button = pygame.image.load('graphics/bg/start.png').convert_alpha()
        
        # boy and girl bg imgs
        self.boy_bg_img = pygame.image.load('graphics/bg/boy_bg.png').convert_alpha()
        self.girl_bg_img = pygame.image.load('graphics/bg/girl_bg.png').convert_alpha()
        
        # arrow main screen
        self.arrow_up = pygame.image.load('graphics/bg/arrow/arrow_up.png').convert_alpha()
        self.arrow_down = pygame.image.load('graphics/bg/arrow/arrow_down.png').convert_alpha()
        self.arrow_left = pygame.image.load('graphics/bg/arrow/arrow_left.png').convert_alpha()
        self.arrow_right = pygame.image.load('graphics/bg/arrow/arrow_right.png').convert_alpha()
        
        self.arrow_r_status = False
        self.arrow_l_status = False
        
        self.press_enter_status = False
        
        # score surface
        self.score_surf = pygame.font.Font('fontdir/ChunkFivePrint.otf', 50)
        # hero life
        self.image_life = pygame.image.load('graphics/ninja/Kunai.png').convert_alpha()
        
        # text render
        self.main_window = self.score_surf.render('Press Enter', False, 'Black')
        self.end_text = self.score_surf.render('Game over', False, 'Black')
        
        # end game image
        self.end_press_enter = pygame.image.load('graphics/bg/end_game/pr_enter_to_ress.png').convert_alpha()
        
        # game speed
        self.speed = 5
        self.speed_status = False
        self.sprite_speed = 0.25
        self.cur_sp_dead = 0
        # for bg screen
        self.pos_x = 0
        self.pos_x_sec = 800
        
        # current hero for screen bg
        self.cur_hero = 0
        self.cur_sp_hero = boy_moving_bg
        self.sp_bg_speed = 0
        self.animation_status = False
        
        # hero and enemy surface
        self.player = Player_hero(70,345)
        self.enemys = Enemy(900, 345, self.speed)
        self.sec_enemys = Enemy(1350, 345, self.speed)
        self.score_table = HighScoreTable()
        self.score_table.create_game_table()
        self.lis_table = []
        
        # Creating the sprites and group
        self.moving_sprites = pygame.sprite.Group()
        self.moving_sprites.add(self.enemys)
        self.moving_sprites.add(self.sec_enemys)
        self.moving_sprites.add(self.player)
        
        # hero dead sprites 
        self.dead_girl = dead_girl
        self.dead_boy = dead_boy
        
        # game music
        pygame.mixer.music.load('audio/bg.mp3')
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)
        self.jump_music = pygame.mixer.Sound('audio/jump.wav')
        
    def main_window_game(self):
        
        while True:
            # bg, boy, girl, enemy surfaces blit
            self.screen.blit(self.screen_bg, (0,0))
            
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.KEYDOWN:
                    # choose hero
                    if event.key == pygame.K_LEFT:
                        self.cur_hero = 0
                        Player_hero.current_hero = self.cur_hero
                        self.player.choose_hero()
                        self.animation_status = True
                        self.arrow_r_status = True
                        self.arrow_l_status = False
                    
                    if event.key == pygame.K_RIGHT:
                        self.cur_hero = 1
                        Player_hero.current_hero = self.cur_hero
                        self.player.choose_hero()
                        self.animation_status = True
                        self.arrow_r_status = False
                        self.arrow_l_status = True
                    
                    # change bg image
                    if event.key == pygame.K_UP:
                        self.screen_bg_change('up')
                    
                    if event.key == pygame.K_DOWN:
                        self.screen_bg_change('down')
                        
                    # enter to start game 
                    if self.press_enter_status:
                        self.start_but_status = True
                        if event.key == pygame.K_RETURN:
                            return None
                        
                    # quit
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
            
            # animation pick hero
            if self.animation_status:
                self.animation_hero_bg()
            else:
                self.screen.blit(self.girl_bg_img, (430, 0))
                self.screen.blit(self.boy_bg_img, (30, 20))
                
            self.show_current_player()
            
            # show 'start' button or arrows
            if self.press_enter_status:
                self.screen.blit(self.start_button, (302, 300))
            else:
                self.screen.blit(self.arrow_left, (350, 300))
                self.screen.blit(self.arrow_right, (400, 300))
            
            # arrow for "bg"
            self.screen.blit(self.arrow_up, (375, 150))
            self.screen.blit(self.arrow_down, (375, 200))
            
            pygame.display.update()
            self.clock.tick(FPS)
            
    def play_game(self):
        
        while True:
            # game score
            self.screen.blit(self.screen_bg, (0,0))
            self.game_speed()
            self.speed_ground()
            self.score_rect = self.score_surf.render(f'Score: {self.player.score}', 
                                                    False,
                                                    'Black')
            self.screen.blit(self.score_rect, (20, 20))
            self.show_life_point()
            # check hit box
            # pygame.draw.rect(self.screen, 'Red', self.player.rect, width=1)
            # pygame.draw.rect(self.screen, 'Red', self.enemys.rect, width=1)
            # pygame.draw.rect(self.screen, 'Red', self.sec_enemys.rect, width=1)
            
            for event in pygame.event.get():
                # quit()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    # jump 
                    if self.player.jump_status:
                        if event.key == pygame.K_UP:
                            pygame.mixer.Sound.play(self.jump_music)
                            self.player.jump_top = True
                            self.player.jump_status = False
                    # sitting
                    if event.key == pygame.K_DOWN:
                        self.player.run_status = True
                    # quit
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                        
                # sitting end
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        self.player.jump_status = True
                        self.player.run_status = False
                        self.player.rect.bottom = 345
            
            self.moving_sprites.draw(self.screen)
            self.moving_sprites.update(self.sprite_speed)
            self.player.collision_and_score(self.enemys)
            self.player.collision_and_score(self.sec_enemys)
            
            if self.player.life == 0:
                return None
                
            # def setup
            pygame.display.flip()
            self.clock.tick(FPS)
            
    def end_game(self):
        
        name_input = False
        name_text = ''
        text = self.score_surf.render('Write your name: ', False, 'Black')
        self.score_rect = self.score_surf.render(f'Score: {self.player.score}', 
                                                    False,
                                                    'Black')
        self.record_table = pygame.font.Font('fontdir/ChunkFivePrint.otf', 30)
        press_enter = self.record_table.render('Press Enter', False, 'Black')
        
        Name = self.record_table.render('Name', False, "Black")
        Score = self.record_table.render('Score', False, "Black")
        
        while True:
            # bg
            self.screen.blit(self.screen_bg, (0,0))
            self.dead_hero()
            for event in pygame.event.get():
                # quit
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    # quit
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                        
                    # check len(name)
                    if len(name_text) < 11 and event.key != pygame.K_RETURN:
                        name_text += event.unicode
                    
                    # del letter in name
                    if event.key == pygame.K_BACKSPACE:
                        name_text = name_text[:len(name_text) - 2]
                        
                    # save name, score in sql_talbe
                    if len(name_text) > 3 and not name_input:
                        if event.key == pygame.K_RETURN:
                            name_input = True
                            self.score_table.update_table(name_text, self.player.score)
                            self.lis_table = self.score_table.show_top_10_hero()
                            
                    # restart the game 
                    if name_input:
                        if event.key == pygame.K_SPACE:
                            return True

            # blit score, text, name, enter
            if not name_input:
                self.screen.blit(self.score_rect, (20, 20))
                self.screen.blit(text, (200, 100))
                nick_name = self.score_surf.render(name_text, False, 'Black')
                self.screen.blit(nick_name, (270, 150))
                
                if len(name_text) > 3:
                    self.screen.blit(press_enter, (330, 210))
            
            # blit table score and image
            if self.lis_table:
                self.show_record_table(Name, Score)
            
            pygame.display.update()
            self.clock.tick(FPS)
    
    # game window
    def speed_ground(self):
        self.pos_x -= self.speed
        self.pos_x_sec -= self.speed
        
        if -801 < self.pos_x < 0:
            self.screen.blit(self.ground_bg, (self.pos_x, 340))
            self.screen.blit(self.ground_bg, (self.pos_x_sec, 340))
        else:
            self.pos_x = 0
            self.pos_x_sec = 800
            
    # game window
    def show_life_point(self):
        wh_life = ((745, 15), (700, 15), (655, 15))
        for i in range(0, self.player.life):
            self.screen.blit(self.image_life, wh_life[i])
    
    # game window
    def game_speed(self):
        if self.player.score % 20 == 0:
            if self.speed_status:
                self.speed += 1
                self.enemys.speed += 1
                self.sec_enemys.speed += 1
                self.speed_status = False
        else:
            self.speed_status = True
    
    # menu window
    def animation_hero_bg(self):
        self.sp_bg_speed += self.sprite_speed + 0.1
        # check speed for index image
        if int(self.sp_bg_speed) > len(self.player.sprites) - 1:
            self.sp_bg_speed = 0
            self.animation_status = False
        if self.cur_hero:
            self.screen.blit(girl_moving_bg[int(self.sp_bg_speed)], (430, 0))
            self.screen.blit(self.boy_bg_img, (30, 20))
        else:
            self.screen.blit(boy_moving_bg[int(self.sp_bg_speed)], (30, 20))
            self.screen.blit(self.girl_bg_img, (430, 0))
    
    # manu window
    def show_current_player(self):
        
        if self.arrow_l_status:
            self.screen.blit(self.arrow_up, (640, 350))
            self.arrow_r_status = False
            self.press_enter_status = True
        if self.arrow_r_status:
            self.screen.blit(self.arrow_up, (110, 350))
            self.arrow_l_status = False
            self.press_enter_status = True
    
    # manu window
    def screen_bg_change(self, sumbol):
        num = self.screen_count
        
        if sumbol == "up":
            self.screen_count = num + 1 if num + 1 < len(screen_bg) else 0
        else:
            self.screen_count = num - 1 if num - 1 >= 0 else len(screen_bg) - 1
            
        self.screen_bg = screen_bg[self.screen_count][0]
        self.ground_bg = screen_bg[self.screen_count][1]
    
    # end game, record table
    def show_record_table(self, Name, Score):
        pos_x, pos_y = 50, 40
        pos_x_score = 350
        
        # title name and score
        self.screen.blit(Name, (50, 10))
        self.screen.blit(Score, (330, 10))
        
        # end game
        self.screen.blit(self.end_press_enter, (450, 100))
        for name, score in self.lis_table:
            
            name = self.record_table.render(f"{name}", False, 'Black')
            score = self.record_table.render(f'{score}', False, 'Black')
                
            self.screen.blit(name, (pos_x, pos_y))
            self.screen.blit(score, (pos_x_score, pos_y))
            
            pos_y += 30

    def dead_hero(self):
        self.cur_sp_dead += self.sprite_speed
        if self.cur_sp_dead > len(self.dead_girl):
            self.cur_sp_dead = 9
        if self.player.current_hero:
            self.screen.blit(self.dead_girl[int(self.cur_sp_dead) - 1], (70, 285))
        else:
            self.screen.blit(self.dead_boy[int(self.cur_sp_dead) - 1], (70, 285))


if __name__ == '__main__':
    while True:
        game = Game()
        game.main_window_game()
        game.play_game()
        if not game.end_game():
            break
