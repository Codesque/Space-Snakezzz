


import pygame    
import random  
from pygame import mixer 
import snakeGame
from snakeGame import execute



DEF_WIDTH = 900 
DEF_HEIGHT = 700  
PIXEL = 50
SNAKE_COLOR = (120,0,210)  
BLACK_BLUE = (10,0,20)  
LIGHT_BLUE = (120 , 120 , 255)
YELLOW = (255,255,0) 
WHITE = (255,255,255)  
PINK = (120,0,225)
COUNT = 0 

class Stars(pygame.sprite.Sprite): 

    def __init__(self , length , color , width = DEF_WIDTH , height = DEF_HEIGHT) -> None:
        super().__init__() 
        self.image = pygame.Surface([length , length]) 
        self.image.fill(color)  
        self.rect = self.image.get_rect()  
        self.rect.centerx = random.randint(0 , width - PIXEL)  
        self.rect.centery = random.randint(0 , height - PIXEL) 
        self.width , self.height = width , height   

        

        self.vx = 1 * random.choice([-1,-1,-1,1,1,1,1,1,1,1])
        self.vy = 0.3
        
        pygame.draw.rect(self.image , WHITE , self.rect)  
        pygame.display.update(self.rect)


    def movement(self): 

        self.rect.centerx += self.vx  
        self.rect.centery += self.vy 

        if self.rect.centerx < PIXEL : 
            self.rect.centerx =  self.width - PIXEL

        elif self.rect.centerx > self.width: 
            self.rect.centerx = PIXEL 

        if self.rect.centery < 0 : 
            self.rect.centery = self.height - PIXEL 

        elif self.rect.centery + PIXEL  > self.height : 
            self.rect.centery = PIXEL   




class SnakeGUI : 

    def __init__(self , width = DEF_WIDTH , height = DEF_HEIGHT ): 
        self.width , self.height = width , height   
        pygame.init() 
        self.screen = pygame.display.set_mode((self.width , self.height))  
        pygame.display.set_caption("Space Snakezzzzz")
        self.screen.fill(BLACK_BLUE)   


        self.all_sprites_list = pygame.sprite.Group()  


        self.play_but , self.options_but , self.exit_but = YELLOW , YELLOW , YELLOW
        self.PLAY = pygame.USEREVENT + 1 
        self.OPTIONS = pygame.USEREVENT + 2 
        self.EXIT = pygame.USEREVENT + 3    
        self.SELECT_MUSİC = pygame.USEREVENT + 4  
        self.select_cooldown = False 

        mixer.init() 

        mixer.Channel(0).play(mixer.Sound("snakeGame/sounds/bg_music.mp3") , -1)  # this is a preview but it fits with the game 
        mixer.Channel(1) # Button select sound
        


        stars = []
        for i in range(50): 

            if i % 6 != 0 :
                stars.append(Stars(5 , WHITE , self.width , self.height))  
            else :  
                stars.append(Stars(5 , LIGHT_BLUE , self.width , self.height))



        self.all_sprites_list.add(stars)
        self.running = True  

    def events(self): 
        global COUNT
        for e in pygame.event.get(): 
            
            if e.type == self.SELECT_MUSİC : 
                pass # There was a major bug in sounds , because of that , I deleted this part 
                

            if e.type == pygame.QUIT or e.type == self.EXIT : 
                self.running = False 
                raise SystemExit   

            if e.type == self.PLAY :   

                mixer.Channel(0).stop() 
                mixer.Channel(1).stop() 
                execute(self.screen) 

            if e.type == self.OPTIONS: 
                pass  

            

    


    def stars(self):

        for star in self.all_sprites_list.sprites() : 
            star.movement() 
        self.all_sprites_list.draw(self.screen)  
        self.all_sprites_list.update()  
        





    def buttons(self , mouse_pos : tuple ,  play_but = None , options_but = None , exit_but = None ): 
        

        
        but_w , but_h = self.width//5 , self.height//10  
         
        
        x , y = (self.width - but_w )//2 , (self.height - but_h)//2   
        play_but = pygame.draw.rect(self.screen , self.play_but  ,pygame.Rect(x , y , but_w , but_h) )   
        
        y += self.height//5 
        options_but = pygame.draw.rect(self.screen , self.options_but ,pygame.Rect(x , y , but_w , but_h ))  

        y += self.height//5
        exit_but = pygame.draw.rect(self.screen , self.exit_but , pygame.Rect(x , y , but_w , but_h) ) 

        return play_but , options_but , exit_but 

    def fonts(self , play_but : pygame.Rect , options_but : pygame.Rect , exit_but : pygame.Rect): 
        pygame.font.get_fonts()  
        
        font_play = pygame.font.SysFont("Corbel" , play_but.width//4 ) 
        text_play = font_play.render("PLAY" , False ,(255,255,255)) 
        self.screen.blit(text_play , (play_but.centerx - play_but.width//2 , play_but.centery - play_but.height//4))  

        font_options = pygame.font.SysFont("Corbel" , play_but.width//4 )
        text_options = font_options.render("OPTIONS" , False ,(255,255,255)) 
        self.screen.blit(text_options , (options_but.centerx - play_but.width//2 , options_but.centery - options_but.height//4)) 

        font_exit = pygame.font.SysFont("Corbel" , play_but.width//4)
        text_exit = font_exit.render("EXIT" , False ,(255,255,255)) 
        self.screen.blit(text_exit , (exit_but.centerx - play_but.width//2 , exit_but.centery - exit_but.height//4))         
      

    def applyEvents(self): 
        mouse_pos = pygame.mouse.get_pos() 
        mouse_press = pygame.mouse.get_pressed()
        
        self.screen.fill(BLACK_BLUE)
        self.stars()
        play , options , exit = self.buttons(mouse_pos)  
        self.fonts(play , options , exit)   

        if play.collidepoint(mouse_pos):  
            self.play_but = PINK    
            if mouse_press[0]: 
                pygame.event.post( pygame.event.Event(self.PLAY) )  
        else : 
            self.play_but = YELLOW  
        
        if options.collidepoint(mouse_pos): 
            self.options_but = PINK    
            if mouse_press[0]: 
                pygame.event.post( pygame.event.Event(self.OPTIONS) )   
                 
        else : 
            self.options_but = YELLOW   

        if exit.collidepoint(mouse_pos): 
            self.exit_but = PINK    
            if mouse_press[0]:
                pygame.event.post( pygame.event.Event(self.EXIT) ) 

        else :
            self.exit_but = YELLOW  
        pygame.display.update()
        




if __name__ == "__main__": 
    menu = SnakeGUI() 
    while menu.running : 
        menu.events() 
        menu.applyEvents() 

          




