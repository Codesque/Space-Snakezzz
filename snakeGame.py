import pygame  
import random 
import time 
from pygame import mixer



RED = (120,0,0) 
YELLOW = (255,255,0)  
LIGHT_BLUE = (100 , 100 , 255) 
MOSTLY_DARK_BLUE = (10,0,20) 
WHITE = (255,255,255)
PIXEL = 50


class SnakeGame : 
    
    def __init__(self , window : pygame.Surface ,   width = 900 , height = 700,  velocity = 10 ) -> None:
        
        pygame.init()    

        w , h = window.get_width() , window.get_height()
        self.w , self.h = w , h  
        self.screen = window  

        
        mixer.init() 
        mixer.Channel(0).play(mixer.Sound("snakeGame/sounds/bg_music.mp3") , -1) 
        self.muted = False 
        self.fps = pygame.time.Clock()  
        self.v = velocity
        self.snake_pos = [100 , 50]  
        self.snake_head_r = pygame.Rect(self.snake_pos[0] , self.snake_pos[1] , 15 , 15)
        self.snake_body = [ [100,50] , 
                            [90,50]  ,
                            [80,50]  ,
                            [70,50]  ]  

        

        self.fruit_pos = [ random.randrange(PIXEL , (self.w//10) * 10 - 2 * PIXEL) , 
                            random.randrange(PIXEL , (self.h//10) * 10 - 2 * PIXEL )  ]  

        self.fruit_r = pygame.Rect(self.fruit_pos[0] , self.fruit_pos[1] , 10 , 10)

        self.fruit_spawn = True 
        self.direction = "RIGHT" 
        self.change2 = "RIGHT" 
        self.score = 0 
        self.running = True   


    def showScore(self , color , font , size , window : pygame.Surface): 
        score_font = pygame.font.SysFont(font , size) 
        score_surface = score_font.render(f"Score : {self.score}" , False , color)  
        score_rect = score_surface.get_rect()  
        window.blit(score_surface , score_rect)   


    def gameOver(self , window : pygame.Surface): 

        go_font = pygame.font.SysFont("Corbel" , 100 ) 

        go_surface = go_font.render("GAME OVER" , False , RED ) 
        go_rect = go_surface.get_rect() 

        go_rect.midtop = (self.w//2 , self.h//4) 
        window.blit(go_surface , go_rect)  

        fs_surface = go_font.render(f"Your Final Score is {self.score}" , False , WHITE) 
        fs_rect = fs_surface.get_rect() 

        fs_rect.midtop = (self.w//2 , 3 *self.h//4) 
        window.blit(fs_surface , fs_rect)
        pygame.display.flip() 

        time.sleep(2)  
        self.running = False



    def events(self): 

        for e in pygame.event.get(): 

            if e.type == pygame.QUIT : 
                raise SystemExit 

                
            if e.type == pygame.KEYDOWN:    
                if e.key == pygame.K_UP: 
                    self.change2 = "UP" 

                if e.key == pygame.K_DOWN: 
                    self.change2 = "DOWN" 

                if e.key == pygame.K_LEFT : 
                    self.change2 = "LEFT" 

                if e.key == pygame.K_RIGHT: 
                    self.change2 = "RIGHT"   

                if e.key == pygame.K_p: 
                    if not self.muted : 
                        mixer.Channel(0).pause() 
                        self.muted = True  
                    else : 
                        mixer.Channel(0).unpause() 
                        self.muted = False 


    def applyMovement(self): 

        
        if self.change2 == "UP" and self.direction != "DOWN":  
            self.direction = "UP" 

        if self.change2 == "DOWN" and self.direction != "UP": 
            self.direction = "DOWN" 

        if self.change2 == "LEFT" and self.direction != "RIGHT": 
            self.direction = "LEFT"  

        if self.change2 == "RIGHT" and self.direction != "LEFT": 
            self.direction = "RIGHT" 


        if self.direction == "UP": 
            self.snake_pos[1] -= self.v 

        if self.direction == "DOWN": 
            self.snake_pos[1] += self.v 

        if self.direction == "LEFT": 
            self.snake_pos[0] -= self.v  

        if self.direction == "RIGHT": 
            self.snake_pos[0] += self.v 


    def apply_bodyGrowingMechanism(self): 
        self.snake_body.insert(0 , list(self.snake_pos)) 
        if self.fruit_r.collidepoint(self.snake_pos[0] , self.snake_pos[1]):  
            self.score += 10 
            self.fruit_spawn = False   

        else : 
            self.snake_body.pop() 

        if not self.fruit_spawn : 
            self.fruit_r.centerx = random.randrange(PIXEL , (self.w//10) * 10 - 2 *PIXEL  )  
            self.fruit_r.centery = random.randrange( PIXEL , (self.h//10) * 10  - 2 *PIXEL )
    

    def apply_overBorder(self): 

        if self.snake_pos[0] < PIXEL : 
            self.snake_pos[0] = self.w - PIXEL 

        if self.snake_pos[0] > self.w - PIXEL : 
            self.snake_pos[0] = PIXEL 

        if self.snake_pos[1] < PIXEL: 
            self.snake_pos[1] = self.h - PIXEL 

        if self.snake_pos[1] > self.h - PIXEL : 
            self.snake_pos[1] = PIXEL  


    def apply_eatingYourself(self , window): 
        for block in self.snake_body[1:] : 

            if self.snake_pos[0] == block[0] and self.snake_pos[1] == block[1] : 
                self.gameOver(window)
    
    
    
    def apply_animation(self , window : pygame.Surface): 

        self.fruit_spawn = True   
        window.fill(MOSTLY_DARK_BLUE) 

        
        for pos in self.snake_body[:]:  
            pygame.draw.rect(window , YELLOW , pygame.Rect(pos[0] , pos[1] , 10 , 10)) 

        pygame.draw.rect(window , LIGHT_BLUE , self.fruit_r)   


    def applyEvents(self , window : pygame.Surface): 
        self.applyMovement() 
        self.apply_bodyGrowingMechanism() 
        self.apply_animation(window) 
        self.apply_overBorder() 
        self.apply_eatingYourself(window) 
        self.showScore(WHITE,"Corbel",20,window) 
        pygame.display.update() 
        self.fps.tick(self.v)


def execute(window ): 
        game = SnakeGame(window) 
        while game.running : 
            game.events() 
            game.applyEvents(window) 

"""
if __name__ == "__main__": 
    pygame.init() 
    screen = pygame.display.set_mode((900,700)) 
    execute(screen) 
"""

