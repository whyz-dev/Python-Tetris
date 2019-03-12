import pygame
import random
import numpy as np
import os

class game:
    def __init__(self):
        self.w             = 1200
        self.h             = 720
        self.WHITE         = (255,255,255,255)
        self.BLACK         = (0,0,0,0)
        self.time          = 0
        self.block         = block()
        self.selection     = 0
        self.score         = 0
        self.tetris_cnt    = 0
        self.pygame_init()
    
    def pygame_init(self):
        # config
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()
        pygame.display.set_caption('Unifox-Tetris')
        
        # image config
        self.pad           = pygame.display.set_mode((self.w, self.h))
        self.clock         = pygame.time.Clock() 
        self.bg_img        = pygame.image.load('image/map1-2.png')

        self.title_on      = pygame.image.load('image/first_all_on.png')
        self.title_off     = pygame.image.load('image/first_all_off.png')

        self.title0_img    = pygame.image.load('image/first_start_on.png').convert_alpha()
        self.title1_img    = pygame.image.load('image/first_score_on.png')
        self.title2_img    = pygame.image.load('image/first_exit_on.png')
        self.logo_img      = pygame.image.load('image/logo.png')

        self.start_snd     = pygame.mixer.Sound('sound/start.wav')
        self.gameover_snd  = pygame.mixer.Sound('sound/gameover.wav')
        self.level_up_high_snd  = pygame.mixer.Sound('sound/levelup_high.wav')
        self.level_up_low_snd  = pygame.mixer.Sound('sound/levelup_low.wav')
        self.delete_snd    = pygame.mixer.Sound('sound/delete.wav')
        self.hui_snd       = pygame.mixer.Sound('sound/Start effect.wav')
        
        self.hold_snd      = pygame.mixer.Sound('sound/hold.wav')
        self.move_snd      = pygame.mixer.Sound('sound/move.wav')
        self.rotation_snd  = pygame.mixer.Sound('sound/rotation.wav')
        self.collision_snd = pygame.mixer.Sound('sound/collision.wav')
        self.select_snd    = pygame.mixer.Sound('sound/select.wav')

        self.pad.fill(self.WHITE)
        
        self.music_list = ['sound/Tetris first page.mp3','sound/Tetris Theme.mp3']  
        self.page = 0

    def draw_bg(self):
        self.pad.blit(self.bg_img, (0,0))
    
    def draw_title(self,num):
        if num == 0:
            self.pad.blit(self.title0_img, (0,0))
        elif num == 1:
            self.pad.blit(self.title1_img, (0,0))
        else:
            self.pad.blit(self.title2_img, (0,0))

    def intro(self):
        self.pad.fill(self.WHITE)
        
        for i in range(60):
            
            pygame.event.get()
            self.pad.blit(self.title_off,(0,0))
            pygame.display.update()

        self.play_start()
        for i in range(50):
            pygame.event.get()
            if ((i+6) // 8) % 2 == 0:
                self.pad.blit(self.title_on,(0,0))
            else:
                self.pad.blit(self.title_off,(0,0))
            pygame.display.update()
        
        for i in range(30):
            pygame.event.get()
            self.pad.blit(self.title_on,(0,0))
            pygame.display.update()
            
    def play_select(self):
        self.select_snd.play()
        
    def play_start(self):
        self.start_snd.play()

    def play_collision(self):
        self.collision_snd.play()

    def play_level_up_low(self):
        self.level_up_low_snd.play()
    
    def play_level_up_high(self):
        self.level_up_high_snd.play()
    
    def play_gameover(self):
        self.gameover_snd.play()

    def play_delete(self):
        self.delete_snd.play()

    def play_rotate(self):
        self.rotation_snd.play()

    def play_move(self):
        self.move_snd.set_volume(0.9)
        self.move_snd.play()

    def play_hold(self):
        self.hold_snd.play()

    def set_music(self, music):
        pygame.mixer.music.load(music)
        pygame.mixer.music.set_volume(10)
        
    def play_song(self):
        # pygame.mixer.music.play(-1)
        pass
    def stop_song(self):
        pygame.mixer.music.stop()

    def system(self):
        gamedone = False
        systemdone = False
        self.intro()
        while not systemdone:
            self.set_music(self.music_list[self.page])
            self.play_song()
            while self.page == 0 and not gamedone:
                for event in pygame.event.get(): 
                    if event.type == pygame.QUIT: 
                        gamedone=True 
                        systemdone=True
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            if self.selection == 0:
                                self.page=1
                                self.set_music(self.music_list[self.page])
                                self.play_song()
                                self.init_game()
                            elif self.selection == 1:
                                pass
                            else:
                                gamedone=True 
                                systemdone=True
                        if event.key == pygame.K_DOWN:
                            if self.selection < 2:
                                self.selection +=1
                                self.play_collision()
                        if event.key == pygame.K_UP:
                            if self.selection > 0:
                                self.selection -=1
                                self.play_collision()
                        if event.key == pygame.K_q:
                            gamedone=True 
                            systemdone=True
                self.render()
           
            while self.page==1 and not gamedone:
                for event in pygame.event.get(): 
                    if event.type == pygame.QUIT: 
                        gamedone=True 
                        systemdone = True
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            gamedone=True 
                            systemdone=True
                        if event.key  == pygame.K_c:
                            if self.block.hold_pushed == False:
                                self.play_hold()
                            self.block.hold_block()
                        if event.key == pygame.K_a:
                            self.block.spin(True)
                            self.play_rotate()
                        if event.key == pygame.K_d:
                            self.block.spin(False)
                            self.play_rotate()
                        if event.key == pygame.K_LEFT:
                            if self.block.left() and self.block.block_collision_left():
                                self.play_move()
                                self.block.x-=1
                        if event.key == pygame.K_RIGHT:
                            if self.block.right() and self.block.block_collision_right():
                                self.play_move()
                                self.block.x+=1
                        if event.key == pygame.K_DOWN:
                            if not self.block.collision() and not self.block.block_collision_down():
                                self.play_move()
                                self.block.y+=1
                                self.time=0
                                self.score+=10
                            else:
                                self.time = self.block.level-1
                                self.play_select()
                        if event.key == pygame.K_SPACE:
                            while not self.block.collision() and not self.block.block_collision_down():
                                self.block.y+=1
                                self.score+=10
                            self.time = self.block.level-1
                            self.play_select()
                self.render()
                self.next()

            while self.page==2 and not gamedone:
                for event in pygame.event.get(): 
                    if event.type == pygame.QUIT: 
                        gamedone=True 
                        systemdone=True
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            gamedone=True 
                            systemdone=True
                        if event.key == pygame.K_SPACE:
                            self.page = 0
                            self.play_collision()
                self.render()
    
    def init_game(self):
        self.block = block()
        self.tetris_cnt = 0
        self.score = 0
        self.step = 0
        self.block.init_variable()

    def next(self):
        self.block.level_up(self.tetris_cnt)

        if self.time % self.block.level == self.block.level-1:
            if self.block.collision() or self.block.block_collision_down():
                if self.block.gameover() == True:
                    self.page = 2
                    self.stop_song()
                    self.play_gameover()
                    pass
                self.block.merge()
                self.block.init_variable()
                deleted_line = self.block.delete_line()
                if deleted_line > 0:
                    self.play_delete()
                self.tetris_cnt += deleted_line
                self.score += deleted_line * deleted_line * 10
            else:
                self.block.y+=1
        self.time+=1

    def draw_score(self):
        font = pygame.font.Font("font/font.ttf", 60)
        text = font.render(str(self.score), True, self.WHITE)
        textRect = text.get_rect()
        textRect.center = (165,420)
        
        self.pad.blit(text,textRect)
        
        text = font.render(str((self.tetris_cnt+3)//3), True, self.WHITE)
        textRect = text.get_rect()
        textRect.center = (180,520)
        self.pad.blit(text,textRect)

    def render(self):
        if self.page == 0:
            self.draw_title(self.selection)
        
        elif self.page == 1:
            self.draw_bg()
            self.block.draw_block_shape(self.pad)
            self.block.draw_block_map(self.pad)
            self.block.draw_next_block(self.pad)
            if self.block.ishold:
                self.block.draw_hold_block(self.pad)
            self.draw_score()
        else:
            self.draw_bg()
        pygame.display.update()
        self.clock.tick(60)
                       
class block:
    def __init__(self):
        self.telomino =[
            [
             [[0,0,0],
             [1,1,1],
             [0,1,0]],

             [[0,1,0], 
             [1,1,0],
             [0,1,0]],
             
             [[0,1,0],
             [1,1,1],
             [0,0,0]],
             
             [[0,1,0],
             [0,1,1],
             [0,1,0]]
            ],
            [
             [[0,0,0],
             [1,1,0],
             [0,1,1]],

             [[0,1,0],
             [1,1,0],
             [1,0,0]],
             
             [[1,1,0],
             [0,1,1],
             [0,0,0]],

             [[0,0,1],
             [0,1,1],
             [0,1,0]]
            ],

            [
             [[0,0,0],
             [0,1,1],
             [1,1,0]],

            [[1,0,0],
             [1,1,0],
             [0,1,0]],

            [[0,1,1],
             [1,1,0],
             [0,0,0]],

            [[0,1,0],
             [0,1,1],
             [0,0,1]]
            ],
            [

             [[0,0,0],
             [1,1,1],
             [1,0,0]],

             [[1,1,0],
             [0,1,0],
             [0,1,0]],

             [[0,0,1],
             [1,1,1],
             [0,0,0]],
             
             [[0,1,0],
             [0,1,0],
             [0,1,1]],
             ],
             [
             
            [[1,0,0],
             [1,1,1],
             [0,0,0]],

            [[0,1,1],
             [0,1,0],
             [0,1,0]],

            [[0,0,0],
             [1,1,1],
             [0,0,1]],
             
            [[0,1,0],
             [0,1,0],
             [1,1,0]],
             ],
            [
            [[1,1,],
             [1,1,]],
            [[1,1,],
             [1,1,]],
            [[1,1,],
             [1,1,]],
             [[1,1,],
             [1,1,]],
          ],
          [

            [[0,0,0,0],
             [1,1,1,1],
             [0,0,0,0],
             [0,0,0,0]],

            [[0,0,1,0],
             [0,0,1,0],
             [0,0,1,0],
             [0,0,1,0]],

            [[0,0,0,0],
             [0,0,0,0],
             [1,1,1,1],
             [0,0,0,0]],
             
            [[0,1,0,0],
             [0,1,0,0],
             [0,1,0,0],
             [0,1,0,0]],
          ]
        ]
        self.rotate= 0
        self.x    = 0
        self.y    = 0
        self.nexttop_x      = 1020
        self.nexttop_y      = 100
        
        self.holdtop_x      = 160
        self.holdtop_y      = 200

        self.maptop_x      = 360
        self.maptop_y      = 32
        self.max_height    = 8
        self.max_width     = 6
        self.min_width     = 0
        self.n    = 0
        self.map = np.zeros((self.max_height,self.max_width))
        self.level = 70
        self.step = 0
        self.hold = 0
        self.tel  = 0
        self.hold_pushed = False
        self.ishold = False
        self.bag = []
        self._set_bag()
        
        pygame.display.init()

        self.I_block       = pygame.image.load('image/I_block.png')
        self.J_block       = pygame.image.load('image/J_block.png')
        self.L_block       = pygame.image.load('image/L_block.png')
        self.O_block       = pygame.image.load('image/O_block.png')
        self.S_block       = pygame.image.load('image/S_block.png')
        self.T_block       = pygame.image.load('image/T_block.png')
        self.Z_block       = pygame.image.load('image/Z_block.png')
        
        self.I_blockm       = pygame.image.load('image/N_I.png')
        self.J_blockm       = pygame.image.load('image/N_J.png')
        self.L_blockm       = pygame.image.load('image/N_L.png')
        self.O_blockm       = pygame.image.load('image/N_O.png')
        self.S_blockm       = pygame.image.load('image/N_S.png')
        self.T_blockm       = pygame.image.load('image/N_T.png')
        self.Z_blockm       = pygame.image.load('image/N_Z.png')
        
    def _set_bag(self):
        bag_order = np.arange(0,7)
        for i in range(3):
            np.random.shuffle(bag_order)
            self.bag = np.append(self.bag, bag_order)
    
    def collision(self):
        
        ac  = self.rotate % 4
        length = len(self.telomino[self.tel][ac])
        for i in range(length):
            for j in range(length):
                if self.telomino[self.tel][ac][i][j] == 1:
                    if self.y + i + 1 == self.max_height:
                        return True
        return False        
    
    def set_tel(self):
        self.tel = int(self.bag[(self.step)%21])
        print(self.step, self.tel)

    def hold_block(self):
        if not self.hold_pushed:
            self.hold_pushed = True
            if self.ishold:
                tmp = self.tel
                self.tel = self.hold
                self.hold = tmp
                
                length = len(self.telomino[self.tel][0])

                
                self.x= self.max_width//2 - length//2
                self.y=-2
                self.rotate = 0

            else:
                self.hold = self.tel
                self.ishold = True
                self.init_variable()
                self.set_tel()
            
                
    def spin(self, direction): # True = Left
        dr = -1 if direction == True else 1
        
        ac  = (self.rotate + dr) % 4
        length = len(self.telomino[self.tel][ac])
        
        dx = [0, 1, -1, 2]
        dy = [0, 1, -1]

        for ddy in dy:
            for ddx in dx:
                spintmp = True
                for i in range(length):
                    for j in range(length):
                        if self.telomino[self.tel][ac][i][j] == 1:
                            if self.y+i+ddy < self.max_height and self.x+j+ddx < self.max_width  and self.x+j+ddx >=0:
                                if self.map[self.y+i+ddy][self.x+j+ddx] > 0: 
                                    spintmp = False
                            else:
                                spintmp = False
                if spintmp == True:
                    self.y += ddy
                    self.x += ddx
                    self.rotate += dr
                    return None

    def level_up(self,cnt):
        cal_tmp = max(2, 60 - (cnt + 3) // 3 * 3)
        if self.level != cal_tmp:
            self.level = cal_tmp

    def gameover(self):
        
        ac  = self.rotate % 4
        length = len(self.telomino[self.tel][ac])
        for i in range(length):
            for j in range(length):
                if self.telomino[self.tel][ac][i][j] == 1:
                    if self.y+i < 0:
                        return True
        return False

    def merge(self):
        
        ac  = self.rotate % 4
        length = len(self.telomino[self.tel][ac])
        for i in range(length):
            for j in range(length):
                if self.telomino[self.tel][ac][i][j] == 1:
                    if self.y+i < self.max_height and self.x+j < self.max_width and self.y+i >=0 and self.x+j >=0:
                        self.map[self.y+i][self.x+j] = 1+self.tel
   
    def check_tetris(self):
        isTetris = np.zeros(self.max_height)
        for i in range(self.max_height):
            tmp = True
            for j in range(self.max_width):
                if self.map[i][j] == 0: 
                    tmp = False
            isTetris[i] = tmp
        return isTetris

    def delete_line(self):
        cnt=0
        isTetris = self.check_tetris()
        for i in range(self.max_height):
            if isTetris[i] == True:
                self.shift_map(i)
                cnt+=1
        return cnt

    def shift_map(self,num):
        for i in range(num,0,-1):
            for j in range(self.max_width):
                self.map[i][j]  = self.map[i-1][j]
        for j in range(self.max_width):
            self.map[0][j] = 0

    def draw_block(self,pad,num,x,y):
        if num == 0:
            pad.blit(self.T_block,(x,y))
        if num == 1:
            pad.blit(self.Z_block,(x,y))
        if num == 2:
            pad.blit(self.S_block,(x,y))
        if num == 3:
            pad.blit(self.L_block,(x,y))
        if num == 4:
            pad.blit(self.J_block,(x,y))
        if num == 5:
            pad.blit(self.O_block,(x,y))
        if num == 6:
            pad.blit(self.I_block,(x,y))
            
    def init_variable(self):        
        ac  = self.rotate % 4
        length = len(self.telomino[self.tel][ac])

        self.x= self.max_width//2 - length//2
        self.y=-2
        self.step+=1
        self.rotate = 0
        self.hold_pushed = False

        self.set_tel()
        
    def draw_block_shape(self,pad):
        ac  = self.rotate%4
        length = len(self.telomino[self.tel][ac])
        for i in range(length):
            for j in range(length):
                if self.telomino[self.tel][ac][i][j] == 1:
                    self.draw_block(pad,self.tel,self.maptop_x+(self.x+j)*80, self.maptop_y+(self.y+i)*80)

    def draw_block_map(self,pad):
        for i in range(self.max_height):
            for j in range(self.max_width):
                if self.map[i][j] > 0:  
                    self.draw_block(pad, self.map[i][j]-1, self.maptop_x+j*80, self.maptop_y+i*80)

    def draw_next_block(self,pad):
        for k in range(self.step+1, self.step+4):
            tel = int(self.bag[(k)%21])
            ac  = 0
            length = len(self.telomino[tel][ac])
            if tel == 6:
                self.draw_mini_block(pad,tel,self.nexttop_x-75, self.nexttop_y+(k-self.step-1)*150)
            else: 
                self.draw_mini_block(pad,tel,self.nexttop_x-60, self.nexttop_y+(k-self.step-1)*150)
    
    def draw_mini_block(self,pad,num,x,y):
        if num == 0:
            pad.blit(self.T_blockm,(x,y))
        if num == 1:
            pad.blit(self.Z_blockm,(x,y))
        if num == 2:
            pad.blit(self.S_blockm,(x,y))
        if num == 3:
            pad.blit(self.L_blockm,(x,y))
        if num == 4:
            pad.blit(self.J_blockm,(x,y))
        if num == 5:
            pad.blit(self.O_blockm,(x,y))
        if num == 6:
            pad.blit(self.I_blockm,(x,y))

    def draw_hold_block(self,pad):
        tel = self.hold
        ac  = 0
        length = len(self.telomino[tel][ac])
        if tel == 6:
            self.draw_mini_block(pad,tel,self.holdtop_x - 75, self.holdtop_y-60)
        else:
            self.draw_mini_block(pad,tel,self.holdtop_x - 60, self.holdtop_y-60)
            
    def right(self):
        max_w = 0
        
        ac  = self.rotate%4
        length = len(self.telomino[self.tel][ac])
        for i in range(length):
            for j in range(length):
                if self.telomino[self.tel][ac][i][j]==1:
                    max_w = max(max_w, j)
        if max_w+self.x == self.max_width - 1:
            return False
        else:
            return True 
            
    def left(self):
        min_w = 5
        
        ac  = self.rotate%4
        length = len(self.telomino[self.tel][ac])
        for i in range(length):
            for j in range(length):
                if self.telomino[self.tel][ac][i][j]==1:
                    min_w=min(min_w,j)
        if min_w+self.x == self.min_width:
            return False
        else:
            return True 

    def block_collision_right(self):
        
        ac  = self.rotate%4
        length = len(self.telomino[self.tel][ac])
        for i in range(length):
            for j in range(length):
                if self.y+i < self.max_height and self.x+j+1 < self.max_width and self.y+i>= 0 and self.x+j+1 >=0:
                    if self.telomino[self.tel][ac][i][j] == 1 and self.map[self.y+i][self.x+1+j] > 0:
                        return False
        return True

    def block_collision_left(self):
        
        ac  = self.rotate%4
        length = len(self.telomino[self.tel][ac])
        for i in range(length):
            for j in range(length):
                if self.x+j-1 < self.max_width and self.y+i < self.max_height and self.x+j-1 >= 0 and self.y+i >=0 :
                    if self.telomino[self.tel][ac][i][j] == 1 and self.map[self.y+i][self.x-1+j] > 0:
                        return False
        return True
        
    def block_collision_down(self):
        
        ac  = self.rotate%4
        length = len(self.telomino[self.tel][ac])
        for i in range(length):
            for j in range(length):
                if self.x+j < self.max_width and self.y+1+i < self.max_height and self.x+j >= 0 and self.y+1+i >= 0:
                    if self.telomino[self.tel][ac][i][j] == 1 and self.map[self.y+1+i][self.x+j] > 0:
                        return True
        return False

if __name__ == "__main__":
    env = game()
    env.system()
