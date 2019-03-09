import pygame
import random
import numpy as np
import os

class game:
    def __init__(self):
        self.w             = 1500
        self.h             = 900
        self.WHITE         = (0,0,0)
        self.time          = 0
        self.pygame_init()
        self.block         = block()
    
    def pygame_init(self):
        # config
        pygame.init()
        pygame.display.set_caption('Unifox-Tetris')
        
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0)
        
        # image config
        self.pad           = pygame.display.set_mode((self.w, self.h), pygame.NOFRAME)
        self.clock         = pygame.time.Clock() 
        self.bg            = pygame.image.load('image/map1-2.png')
        self.title         = pygame.image.load('image/first_start_on.png')
        self.pad.fill(self.WHITE)
        
        self.page = 0
    
    def draw_bg(self):
        self.pad.blit(self.bg, (0,0))
    
    def draw_title(self):
        self.pad.blit(self.title, (0,0))

    def system(self):
        gamedone = False
        systemdone = False
        while not systemdone:
            while self.page == 0 and not gamedone:
                for event in pygame.event.get(): # User did something
                    if event.type == pygame.QUIT or event.type == pygame.K_q: # If user clicked close
                        gamedone=True # Flag that we are done so we exit this loop
                        systemdone=True
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.page=1
                            self.block = block()
                            self.block.init_variable()
                self.render()
           
            while self.page==1 and not gamedone:
                for event in pygame.event.get(): # User did something
                    if event.type == pygame.QUIT: # If user clicked close
                        gamedone=True # Flag that we are done so we exit this loop
                        systemdone = True
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_a:
                            self.block.spin(True)
                        if event.key == pygame.K_d:
                            self.block.spin(False)
                        if event.key == pygame.K_LEFT:
                            if self.block.left() and self.block.block_collision_left():
                                self.block.x-=1
                        if event.key == pygame.K_RIGHT:
                            if self.block.right() and self.block.block_collision_right():
                                self.block.x+=1
                        if event.key == pygame.K_DOWN:
                            if not self.block.collision() and not self.block.block_collision_down():
                                self.block.y+=1
                            else:
                                self.time = self.block.level-1
                        if event.key == pygame.K_SPACE:
                            while not self.block.collision() and not self.block.block_collision_down():
                                self.block.y+=1
                            self.time = self.block.level-1
                self.render()
                self.next()

            while self.page==2 and not gamedone:
                for event in pygame.event.get(): # User did something
                    if event.type == pygame.QUIT or event.type == pygame.K_q: # If user clicked close
                        gamedone=True # Flag that we are done so we exit this loop
                        systemdone=True
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.page = 0
                self.render()
    
    def next(self):
        if self.time % self.block.level == self.block.level-1:
            if self.block.collision() or self.block.block_collision_down():
                if self.block.gameover() == True:
                    self.page = 2
                    pass
                self.block.merge()
                self.block.init_variable()
                self.block.delete_line()
            else:
                self.block.y+=1
        self.time+=1

    def render(self):
        if self.page == 0:
            self.draw_title()
        
        elif self.page == 1:
            self.draw_bg()
            self.block.draw_block_shape(self.pad)
            self.block.draw_block_map(self.pad)
        else:
            self.draw_bg()
        pygame.display.update()
                       
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
             [[0,1,0],
             [0,1,0],
             [0,1,1]],

             [[0,0,0],
             [1,1,1],
             [1,0,0]],

             [[1,1,0],
             [0,1,0],
             [0,1,0]],

             [[0,0,1],
             [1,1,1],
             [0,0,0]],
             ],
             [
            [[0,1,0],
             [0,1,0],
             [1,1,0]],
             
            [[1,0,0],
             [1,1,1],
             [0,0,0]],

            [[0,1,1],
             [0,1,0],
             [0,1,0]],

            [[0,0,0],
             [1,1,1],
             [0,0,1]],
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
            [[0,1,0,0],
             [0,1,0,0],
             [0,1,0,0],
             [0,1,0,0]],

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
             [0,0,0,0]]
          ]
        ]
        self.rotate= 0
        self.x    = 0
        self.y    = 0
        self.maptop_x      = 450
        self.maptop_y      = -60
        self.max_height    = 9
        self.max_width     = 6
        self.min_width     = 0
        self.n    = 0
        self.map = np.zeros((self.max_height,self.max_width))
        self.level = 70
        self.step = 0
        self.bag = []
        self._set_bag()
        
        self.I_block       = pygame.image.load('image/I_block.png')
        self.J_block       = pygame.image.load('image/J_block.png')
        self.L_block       = pygame.image.load('image/L_block.png')
        self.O_block       = pygame.image.load('image/O_block.png')
        self.S_block       = pygame.image.load('image/S_block.png')
        self.T_block       = pygame.image.load('image/T_block.png')
        self.Z_block       = pygame.image.load('image/Z_block.png')
        
    def _set_bag(self):
        bag_order = np.arange(0,7)
        for i in range(3):
            np.random.shuffle(bag_order)
            self.bag = np.append(self.bag, bag_order)
    
    def collision(self):
        tel = int(self.bag[(self.step)%21])
        ac  = self.rotate % 4
        length = len(self.telomino[tel][ac])
        for i in range(length):
            for j in range(length):
                if self.telomino[tel][ac][i][j] == 1:
                    if self.y + i + 1 == self.max_height:
                        return True
        return False        
    
    def spin(self, direction): # True = Left
        dr = -1 if direction == True else 1
        tel = int(self.bag[(self.step)%21])
        ac  = (self.rotate + dr) % 4
        length = len(self.telomino[tel][ac])
        
        dx = [0, -1, 1, 0, -1, 1, 0, -1, 1]
        dy = [0, 0, 0, -1, -1, -1, 1, 1, 1]

        for k in range(9):
            spintmp = True
            for i in range(length):
                for j in range(length):
                    if self.telomino[tel][ac][i][j] == 1:
                        if self.y+i+dy[k] < self.max_height and self.x+j+dx[k] < self.max_width and self.y+i+dy[k] >=0 and self.x+j+dx[k] >=0:
                            if self.map[self.y+i+dy[k]][self.x+j+dx[k]] > 0: 
                                spintmp = False
                        else:
                            spintmp = False
            if spintmp == True:
                self.y += dy[k]
                self.x += dx[k]
                self.rotate += dr
                break

    def gameover(self):
        tel = int(self.bag[(self.step)%21])
        ac  = self.rotate % 4
        length = len(self.telomino[tel][ac])
        for i in range(length):
            for j in range(length):
                if self.telomino[tel][ac][i][j] == 1:
                    if self.y+i >= self.max_height or self.y+i <0:
                        return True
        return False

    def merge(self):
        tel = int(self.bag[(self.step)%21])
        ac  = self.rotate % 4
        length = len(self.telomino[tel][ac])
        for i in range(length):
            for j in range(length):
                if self.telomino[tel][ac][i][j] == 1:
                    if self.y+i < self.max_height and self.x+j < self.max_width and self.y+i >=0 and self.x+j >=0:
                        self.map[self.y+i][self.x+j] = 1+tel
   
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
        isTetris = self.check_tetris()
        for i in range(self.max_height):
            if isTetris[i] == True:
                self.shift_map(i)

    def shift_map(self,num):
        for i in range(num,1,-1):
            for j in range(self.max_width):
                self.map[i][j]  = self.map[i-1][j]
        for j in range(self.max_width):
            self.map[0][j] = 0

    def draw_block(self,pad,num,x,y):
        if num == 0:
            pad.blit(self.I_block,(x,y))
        if num == 1:
            pad.blit(self.J_block,(x,y))
        if num == 2:
            pad.blit(self.L_block,(x,y))
        if num == 3:
            pad.blit(self.O_block,(x,y))
        if num == 4:
            pad.blit(self.S_block,(x,y))
        if num == 5:
            pad.blit(self.T_block,(x,y))
        if num == 6:
            pad.blit(self.Z_block,(x,y))
            
    def init_variable(self):
        self.x=2
        self.y=-2
        self.step+=1

    def draw_block_shape(self,pad):
        tel = int(self.bag[(self.step)%21])
        ac  = self.rotate%4
        length = len(self.telomino[tel][ac])
        for i in range(length):
            for j in range(length):
                if self.telomino[tel][ac][i][j] == 1:
                    self.draw_block(pad,tel,self.maptop_x+(self.x+j)*100, self.maptop_y+(self.y+i)*100)

    def draw_block_map(self,pad):
        for i in range(self.max_height):
            for j in range(self.max_width):
                if self.map[i][j] > 0:  
                    self.draw_block(pad, self.map[i][j]-1, self.maptop_x+j*100, self.maptop_y+i*100)

    def right(self):
        max_w = 0
        tel = int(self.bag[(self.step)%21])
        ac  = self.rotate%4
        length = len(self.telomino[tel][ac])
        for i in range(length):
            for j in range(length):
                if self.telomino[tel][ac][i][j]==1:
                    max_w = max(max_w, j)
        if max_w+self.x == self.max_width - 1:
            return False
        else:
            return True 
            
    def left(self):
        min_w = 5
        tel = int(self.bag[(self.step)%21])
        ac  = self.rotate%4
        length = len(self.telomino[tel][ac])
        for i in range(length):
            for j in range(length):
                if self.telomino[tel][ac][i][j]==1:
                    min_w=min(min_w,j)
        if min_w+self.x == self.min_width:
            return False
        else:
            return True 

    def block_collision_right(self):
        tel = int(self.bag[(self.step)%21])
        ac  = self.rotate%4
        length = len(self.telomino[tel][ac])
        for i in range(length):
            for j in range(length):
                if self.y+i < self.max_height and self.x+j+1 < self.max_width and self.y+i>= 0 and self.x+j+1 >=0:
                    if self.telomino[tel][ac][i][j] == 1 and self.map[self.y+i][self.x+1+j] > 0:
                        return False
        return True

    def block_collision_left(self):
        tel = int(self.bag[(self.step)%21])
        ac  = self.rotate%4
        length = len(self.telomino[tel][ac])
        for i in range(length):
            for j in range(length):
                if self.x+j-1 < self.max_width and self.y+i < self.max_height and self.x+j-1 >= 0 and self.y+i >=0 :
                    if self.telomino[tel][ac][i][j] == 1 and self.map[self.y+i][self.x-1+j] > 0:
                        return False
        return True
        
    def block_collision_down(self):
        tel = int(self.bag[(self.step)%21])
        ac  = self.rotate%4
        length = len(self.telomino[tel][ac])
        for i in range(length):
            for j in range(length):
                if self.x+j < self.max_width and self.y+1+i < self.max_height and self.x+j >= 0 and self.y+1+i >= 0:
                    if self.telomino[tel][ac][i][j] == 1 and self.map[self.y+1+i][self.x+j] > 0:
                        return True
        return False

if __name__ == "__main__":
    env = game()
    env.system()
