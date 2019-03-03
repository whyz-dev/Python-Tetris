import pygame


class game:
    def __init__(self):
        self.w             = 1200
        self.h             = 900
        self.WHITE         = (255,255,255)
        self.pygame_init()
    
    def pygame_init(self):
        # config
        pygame.init()
        pygame.display.set_caption('Unifox-Tetris')

        # image config
        self.pad           = pygame.display.set_mode((self.w, self.h))
        self.pad.fill(self.WHITE)
        self.clock         = pygame.time.Clock() 
        self.bg            = pygame.image.load('image/bg.png')
        self.draw_bg(0,0)
        self.render()
    
    def draw_bg(self,x,y):
        self.pad.blit(self.bg, (x, y))

    def render(self):
        done = False
        while not done:
            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    done=True # Flag that we are done so we exit this loop
            pygame.display.update()
            pygame.event.get()
    


        