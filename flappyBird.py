import pygame,sys,random
from pygame.locals import*

pygame.init()
pygame.display.set_caption("Flappi Burd")

FPS = 60
FramePerSec = pygame.time.Clock()

displayScreen = pygame.display.set_mode((960, 720))

fontScore = pygame.font.SysFont("couriernew", 30, True)                                                     #Fonts for scores
scoreText = fontScore.render("Score = ", False, (255,0,0))
highScoreText = fontScore.render("High Score = ", False, (255,0,0))

fontText_major = pygame.font.SysFont("castellar", 60, True)                                                 #Font for below written texts
Text_home_major = fontText_major.render("Flappi Burd", False, (255,255,255))
Text_highScore_major = fontText_major.render("New High Score!!", False, (255,255,255))
Text_retry_major = fontText_major.render("Try Again!!", False, (255,255,255))

fontText_minor = pygame.font.SysFont("castellar", 40, True)                                                 #Font for enter to start
Text_minor = fontText_minor.render("Press Enter to start", False, (255,255,255))


background = pygame.image.load("images/background.png")                                                     #Load background image
background_sized = pygame.transform.scale(background, (2082, 720))                                          #Scaling it to fit the screen
background_x = 0
background_velocity = 2;

bird_up = pygame.image.load("images/bird_up.png")                                                           #Loading bird with wings up and scaling
bird_up_sized = pygame.transform.scale(bird_up, (60, 50))
bird_down = pygame.image.load("images/bird_down.png")                                                       #Loading bird with wings down and scaling
bird_down_sized = pygame.transform.scale(bird_down, (60, 50))

pipe_down = pygame.image.load("images/pipe.png")                                                            #Loading image of pipe, flipping it and scaling both
pipe_down_sized = pygame.transform.scale(pipe_down, (100, 400))
pipe_up = pygame.transform.flip(pipe_down, False, True)
pipe_up_sized = pygame.transform.scale(pipe_up, (100, 400))
pipe_pair = pygame.sprite.Group()


class Bird(pygame.sprite.Sprite): 
    key = 0                                                                                                  #position of bird. 0 for down, 1 for up
    x = 230                                                                                                  #spawn position
    y = 300                 
    y_velocity = -5
    gravity = 0.15
    bird_sized = bird_down_sized
    score = 0
    score_value = fontScore.render(str(score), False, (255,0,0))                                            #Rendering score 
    highScore = 0
    high_Score_value = fontScore.render(str(highScore), False, (255,0,0))
    firstTime = True                                                                                        #To ensure New game screen while playing firt time
    
    def __init__(self, x=230, y=300):                                                                       #Constructor
        super().__init__()
        self.x = x
        self.y = y
        self.rect = bird_up_sized.get_rect()
        self.rect.topleft = (self.x,self.y)
    

    def display(self):                                                                                      #Updating position of bird by applying velocity and gravity, and dispalying it
        self.y += self.y_velocity
        self.y_velocity += self.gravity
        displayScreen.blit(self.bird_sized, (self.x, self.y)) 


    def switch(self):                                                                                       #Switching position of bird every 0.3 second
        if self.bird_sized == bird_up_sized:
            self.bird_sized = bird_down_sized
        else:
            self.bird_sized = bird_up_sized
    
    def reset(self):                                                                                        #Resetting all parameteres every time brd crashes 
        self.key = 0
        self.x = 230
        self.y = 300
        self.y_velocity = -5
        self.bird_sized = bird_down_sized
        self.score = 0


class Pipe(pygame.sprite.Sprite):
    offset = 200                                                                                            #Window for bird to pass through
    x = 960                                                                                                 #Spawn position of new pipe, ie, extreme righ tof screen

    def __init__(self, pipe_middle):                                                                        #Constructor
        super().__init__()
        self.offset = 200
        self.pos = pipe_middle
        self.pipe_up_sized = pipe_up_sized
        self.pipe_down_sized = pipe_down_sized
    
    def display_pipe_pair(self, pos):                                                                       #Updating position of pipes and displaying it 
        self.x -= 5

        displayScreen.blit(pipe_up_sized, (self.x, -400 + pos-(self.offset/2)))
        displayScreen.blit(pipe_down_sized, (self.x, pos + (self.offset/2)))


def updateBackground_x(background_x):
    if background_x < -1030:                                                                                #Moving background image leftwards in a loop
        background_x = 0
    else:
        background_x -= background_velocity
    return background_x


def gameLoop(background_x, pipeList):
    while True:                                                                                             #Game loop
        bird.firstTime = False                                                                              #Diff between menu screen and game loop

        background_x = updateBackground_x(background_x);                                                            
        displayScreen.blit(background_sized, (background_x,0))                                              #Blitting background

        if bird.y < 0 - 5 or bird.y > 720 - 50 + 5:                                                         #To ensure bird stays in scnreen
            menuScreen(0)

        for pipes in pipeList:                                                                              #updating position of all pipes to move them leftwards
            if pipes.x > -100:
                pipes.display_pipe_pair(pipes.pos)
        for pipes in pipeList:                                                                              #Deleting pipes which go out of screen
            if pipes.x < -100:
                pipeList.remove(pipes)
        for pipes in pipeList:                                                                              #Detecting collision of bird and pipe
            if pipes.x > 135 and pipes.x < 285:
                if bird.y > pipes.pos + 100 - 50 + 5 or bird.y < pipes.pos - 100 - 5:
                    menuScreen(0)

        for pipes in pipeList:                                                                              #If pipe crosses bird, incerement score
            if pipes.x == 125:
                bird.score += 1

        bird.display()
        displayScreen.blit(highScoreText, (5,5))                                                            #Displaying scores
        bird.high_Score_value = fontScore.render(str(bird.highScore), False, (255,0,0))
        displayScreen.blit(bird.high_Score_value, (236,5))
        displayScreen.blit(scoreText, (5,40))
        bird.score_value = fontScore.render(str(bird.score), False, (255,0,0))
        displayScreen.blit(bird.score_value, (147,40))
        
        for event in pygame.event.get():                                                                    #To exit game
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == birdSwitch:                                                                    #Catching event timer loop for bird switch 
                bird.switch()

            if event.type == pipeSpawn:                                                                     #Catching event timer loop for pipe spawn
                pipe_middle = random.randint(320,500)
                pipeList.append(Pipe(pipe_middle))


            pressed = pygame.key.get_pressed()
            if pressed[K_ESCAPE]:                                                                           #Quitting game by escape key
                pygame.quit()
                sys.exit()
            
            if pressed[K_SPACE] or pressed[K_UP]:                                                           #Play the game by space or up arrow
                bird.y_velocity = -4

        pygame.display.update()                                                                             #Update screen
        FramePerSec.tick(FPS)                                                                               #Set FPS


def menuScreen(background_x):
    while(True):                                                                                            #Menu screen loop
        displayScreen.blit(background_sized, (background_x,0))

        if bird.firstTime == True:                                                                          #Accessing without having gone to game loop
            displayScreen.blit(Text_home_major, (240,200))
        elif bird.firstTime == False:                                                                       #Displaying messages
            if bird.score > bird.highScore:
                displayScreen.blit(Text_highScore_major, (140,200))
            else:
                displayScreen.blit(Text_retry_major, (240,200))

        displayScreen.blit(bird_down_sized, (230,300))                                                      #Spawning bird
        
        if bird.score > bird.highScore:                                                                     #Updating and diplaying highscore
            bird.high_Score_value = fontScore.render(str(bird.score), False, (255,0,0))
        displayScreen.blit(highScoreText, (5,5))
        displayScreen.blit(bird.high_Score_value, (236,5))
        displayScreen.blit(Text_minor, (200, 400))

        for event in pygame.event.get():                                                                    #To exit game
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            pressed = pygame.key.get_pressed()
            if pressed[K_ESCAPE]:                                                                           #Quitting game by escape key
                pygame.quit()
                sys.exit()
            
            if pressed[K_RETURN] or pressed[K_SPACE]:                                                       #Starting the game by space or enter
                if bird.score > bird.highScore:
                    bird.highScore = bird.score
                pipeList.clear()                                                                            #Emptying list or pipes
                bird.reset()                                                                                #Resetting bird's variables

                gameLoop(background_x, pipeList)                                                            #Calling the game loop

        pygame.display.update()                                                                             #Update screen
        FramePerSec.tick(FPS)                                                                               #Set FPS


bird = Bird()                                                                                               #Object of bird
pipeList = []                                                                                               #Storing all pipes on scnreen in a list


birdSwitch = pygame.USEREVENT + 1                                                                           #Switching bird position every 0.3 second
pygame.time.set_timer(birdSwitch, 300)

pipeSpawn = pygame.USEREVENT + 2                                                                           #Spawning new pipe every 1.6 second
pygame.time.set_timer(pipeSpawn, 1600)

menuScreen(background_x)                                                                                    #Calling the menu screen, starting the game
