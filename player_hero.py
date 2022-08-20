import pygame
from hero_images import *



class Player_hero(pygame.sprite.Sprite):
    
    current_hero = 0
    
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.keystate = pygame.key.get_pressed()
        
        # boy sprites
        self.boy_run_sp = run_list
        self.boy_jump_sp = jump_list
        self.boy_laying_sp = laying_list

        # girl sprites
        self.girl_run_sp = girl_run
        self.girl_jump_sp = girl_jump
        self.girl_laying_sp = girl_laying

        # current hero 
        self.sprites = run_list
        self.sp_jump = jump_list
        self.sp_laying = laying_list
            
        # run sprites
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect(midbottom = (pos_x, pos_y), width=45)
        
        # jump sprites
        self.cur_jump_sp = 0
        self.jump_img = self.sp_jump[self.cur_jump_sp]
        
        # laying sprites
        self.cur_laying_sp = 0
        self.laying_img = self.sp_jump[self.cur_laying_sp]
        
        # score setup
        self.score = 0
        self.score_status = True
        
        # game set
        self.life = 3
        self.life_status = True
        
        self.jump_status = True
        self.jump_top = False
        self.jump_bot = False
        
        self.run_status = False
        
        # hero dead sprites 
        self.dead_girl = dead_girl
        self.dead_boy = dead_boy
        
        # sound 
        self.hit_music = pygame.mixer.Sound('audio/hit.wav')
        
        
    def update(self,speed):
        
        if self.run_status:
            self.laing_on_floor(speed)
            
        elif not self.jump_status:
            self.jump_sp(speed)
            
        else:
            self.run(speed)
    
    def run(self, speed):
        self.current_sprite += speed
        if int(self.current_sprite) >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]
    
    def jump_sp(self, speed):
        
        if self.jump_top:
            # check hero pos
            if self.rect.top >= 130:
                self.rect.top -= 6
                # jump top sprites
                self.cur_jump_sp += speed
                
                if int(self.cur_jump_sp) >= len(self.sp_jump) - 4:
                    self.cur_jump_sp = 6
                self.image = self.sp_jump[int(self.cur_jump_sp)]
                
            else:
                self.jump_top = False
                self.jump_bot = True
                
        if self.jump_bot:
            
            # check hero pos
            if self.rect.bottom <= 345:
                self.rect.bottom += 6
                # jump bottom sprites
                self.cur_jump_sp += speed
                
                if int(self.cur_jump_sp) >= len(self.sp_jump) - 1:
                    self.cur_jump_sp = 9
                self.image = self.sp_jump[int(self.cur_jump_sp)]
                
            else:
                self.jump_bot = False
                self.jump_status = True
                self.rect.bottom = 345
                self.cur_jump_sp = 0
                
    def laing_on_floor(self, speed):
        self.cur_laying_sp += speed
        
        if int(self.cur_laying_sp) >= len(self.sp_laying):
            self.cur_laying_sp = 0
            
        self.image = self.sp_laying[int(self.cur_laying_sp)]
        
        self.rect.bottom = 360
        self.jump_top = False
        self.jump_bot = False
        
    def collision_and_score(self, enemy):
        if self.life_status:
            # score
            if enemy.rect.left <= -100 and self.score_status:
                self.score += 1
                
            # collision
            if self.rect.colliderect(enemy.rect):
                pygame.mixer.Sound.play(self.hit_music)
                enemy.hit_status = True
                
                if enemy.enemy_skin_ready:
                    enemy.current_sprite = 0
                    
                self.life_status = False
                self.score_status = False
                
        if enemy.rect.left <= -100 and not self.life_status:
            self.life_status = True
            self.score_status = True
            self.life -= 1

    def choose_hero(self):
        
        if self.__class__.current_hero:
            self.sprites = self.girl_run_sp
            self.sp_jump = self.girl_jump_sp
            self.sp_laying = self.girl_laying_sp
            
        if not self.__class__.current_hero:
            self.sprites = self.boy_run_sp
            self.sp_jump = self.boy_jump_sp
            self.sp_laying = self.boy_laying_sp
    

        
