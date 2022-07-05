from operator import length_hint
from pickle import FALSE, TRUE
from numpy import block
import pygame
import time
import random
from pygame.locals import *

size = 20

class Banana:
    def __init__(self,screen):
        self.image = pygame.image.load("resources/banana.png").convert_alpha()
        self.screen = screen
        self.x = 100
        self.y = 100
    
    def draw(self):
        self.screen.blit(self.image ,(self.x, self.y))
  
    
    def move(self):
        self.x = random.randint(0,49) * size
        self.y = random.randint(2,23) * size


class Snake:
    def __init__(self, screen, length):
        self.length = length
        self.screen = screen
        self.block = pygame.image.load("resources/block.png").convert_alpha()
        self.x = [size]*length
        self.y = [size]*length
        self.direction = 'down'

    def increase_length(self):
        self.length = self.length + 1
        self.x.append(-1)
        self.y.append(-1)


    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'
    
    def draw(self):
        for i in range(self.length):
            self.screen.blit(self.block ,(self.x[i], self.y[i]))
    

    def walk(self):

        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == 'left':
            self.x[0] = self.x[0] - 20
        if self.direction == 'right':
            self.x[0] = self.x[0] + 20
        if self.direction == 'up':
            self.y[0] = self.y[0] - 20
        if self.direction == 'down':
            self.y[0] = self.y[0] + 20
        self.draw()



class Game:
    def __init__(self):
        pygame.init()

        pygame.mixer.init()
        self.play_background_music()

        self.surface = pygame.display.set_mode((1000,500))
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.Banana = Banana(self.surface)
        self.Banana.draw()
    
    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + size:
            if y1 >= y2 and y1 < y2 + size:
                return True
        return False
    
   
    def render_background(self):
        bg = pygame.image.load("resources/Background.png").convert_alpha()
        self.surface.blit(bg, (0,0))
        
    def play(self):

        self.render_background()
        self.snake.walk()
        self.Banana.draw()
        self.display_score()
        
        pygame.display.update()

        #snake colliding with apple

        if self.is_collision(self.snake.x[0], self.snake.y[0], self.Banana.x, self.Banana.y):
            sound = pygame.mixer.Sound("resources/Applesound.wav")
            pygame.mixer.Sound.play(sound)
            self.snake.increase_length()
            self.Banana.move()
        
        #snake colliding with itself

        for i in range(3,self.snake.length ):
            if self.is_collision(self.snake.x[0],self.snake.y[0], self.snake.x[i],self.snake.y[i]):
                sound = pygame.mixer.Sound("resources/Crash.wav")
                pygame.mixer.Sound.play(sound)
                raise 'Game over'
        

    def play_background_music(self):
        pygame.mixer.music.load("resources/Music.mp3")
        pygame.mixer.music.play()
   



    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial',30)
        game_over = font.render(f"Game over. Your final score was {self.snake.length}!", True , (0,0,0))
        self.surface.blit(game_over, (230,180))
        play_again = font.render(f"To play again press Enter. To exit press Escape!", True , (0,0,0))
        self.surface.blit(play_again, (150,240))
        pygame.mixer.music.pause()
        pygame.display.update()

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.Banana = Banana(self.surface)
        
            

    def display_score(self):
        font = pygame.font.SysFont('arial',30)
        score = font.render(f"Score: {self.snake.length}", True , (0,0,0))
        self.surface.blit(score, (400,20))

    

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    
                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:   
                        if  event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()
                elif event.type == QUIT:
                    running = False
            try: 
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            
            time.sleep(0.075)

if __name__  == "__main__":
    game = Game()
    game.run()