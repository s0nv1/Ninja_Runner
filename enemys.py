import pygame
import random 
from enemys_images import *

# sprites idle
dict_enemys = {0:shred_list,
                1:samurai_list,
                2:sam_heavy_list,
                3:orel_fly,
                4:vorona_fly,
                5:ptica_fly,
                }
# sprites hit
dict_hit_enemys = {0: shred_hit,
                    1: samurai_hit,
                    2: sam_heavy_hit,
                    }


class Enemy(pygame.sprite.Sprite):
    
    def __init__(self, pos_x, pos_y, speed):
        super().__init__()

        # position sprites
        self.pos_x = pos_x
        self.pos_y = pos_y
        
        # enemys sprites img
        self.sprites = dict_enemys
        self.sprites_hit = dict_hit_enemys
        
        # random enemy 
        self.cur_skin = random.randint(0, len(dict_enemys) - len(dict_enemys) // 2 - 1)
        self.current_sprite = 0
        
        # rect image
        self.image = self.sprites[self.cur_skin][self.current_sprite]
        self.rect = self.image.get_rect(bottomleft = (pos_x, pos_y),width=50)

        # speed 
        self.speed = speed
        
        # hit status
        self.hit_status = False
        self.hit_count = 0
        
        # fly or mili status 
        self.enemy_skin_ready = False
        
    def enemy_random(self):
        
        self.cur_skin = random.randint(0 , len(dict_enemys) - 1)
        
        if self.cur_skin > 2:
            self.pos_y, width = 290, 30
            self.enemy_skin_ready = False
        else:
            self.pos_y, width = 345, 30
            self.enemy_skin_ready = True
            
        self.current_sprite = 0
        self.image = self.sprites[self.cur_skin][int(self.current_sprite)]
        self.rect = self.image.get_rect(midbottom = (900, self.pos_y),width=width)

    
    def update(self, speed):
        
        if self.hit_status:
            self.hit_hero(speed)
        else:
            self.run(speed)
            
    def hit_hero(self, speed):

        if self.rect.left > -100:
            self.rect.left -= self.speed
            self.hit_count += speed + 0.15
            self.current_sprite += speed
            
            if int(self.current_sprite) >= len(self.sprites[self.cur_skin]):
                self.current_sprite = 0
                
            if int(self.hit_count) >= len(self.sprites_hit[0]):
                self.hit_count = 0
                self.hit_status = False
            
            # check if enemy has sprites for hit
            self.check_hit = self.sprites_hit.get(self.cur_skin, False)
            
            if not self.check_hit:
                self.image = self.sprites[self.cur_skin][int(self.current_sprite)]
            else:
                self.image = self.sprites_hit[self.cur_skin][int(self.hit_count)]
                
        else:
            self.rect.left = 900
            self.enemy_random()

    def run(self, speed):
        
        if self.rect.left > -100:
            self.rect.left -= self.speed
            # enemy sprites
            self.current_sprite += speed
            
            if int(self.current_sprite) >= len(self.sprites[self.cur_skin]):
                self.current_sprite = 0
            self.image = self.sprites[self.cur_skin][int(self.current_sprite)]
            
        else:
            self.rect.left = 900
            self.enemy_random()
