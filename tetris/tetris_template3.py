#########################################
# Programmer: Matthew Paulin
# Date: December, 20, 2016
# File Name: tetris_template3.py
# Description: This program is the third game template for our Tetris game.
######################################### next, hold, delay for more mmovement, invisible
#importing the classes file, random, pygame, and time modules
from tetris_classes import *
from random import randint
import pygame
import time
#start pygame
pygame.init()
#set the  width, height and gridsize, and makes a surface
HEIGHT = 600
WIDTH  = 800
GRIDSIZE = HEIGHT//24
screen=pygame.display.set_mode((WIDTH,HEIGHT))
#color
GREY = (192,192,192)

#---------------------------------------#
COLUMNS = 10                            #number of columns
ROWS = 20                               # number of rows
LEFT = 11                                # number of blocks that the left wall is away from the left side of the surface
RIGHT = LEFT + COLUMNS                  # number of blocks that the right wall is away from the left side of the surface
MIDDLE = LEFT + COLUMNS//2               #number of blocks that the middle is away from the left side of the surface
TOP = 3                                 #number of blocks that the top wall is away from the top of the surface
FLOOR = TOP + ROWS                     #number of blocks that the bottom wall is away from the top of the surface


framecount=0#number of frames since the game has started
score = 0 # a player's score
frame=0 # frame number of the gif border
pause=False #pause boolean
string = 'frame' #string that makes it easier to add the gif
images=[] #list of gif frames
#loading all the frames of the gif
for i in range(8):
    images.append(pygame.image.load(string+str(i)+'.png'))
    images[i] = images[i].convert_alpha()
    images[i] = pygame.transform.scale(images[i], (14*GRIDSIZE-10,24*GRIDSIZE))
box=[] #list of gif frames
#loading all the images of the gif again for the smaller boxes for the hold and next shape
for i in range(8):
    box.append(pygame.image.load(string+str(i)+'.png'))
    box[i] = box[i].convert_alpha()
    box[i] = pygame.transform.scale(box[i], (6*GRIDSIZE,5*GRIDSIZE))

#loading pictures
tback=(pygame.image.load('tback.jpg'))
tback = tback.convert_alpha()
tback = pygame.transform.scale(tback, (WIDTH,HEIGHT))
tend=(pygame.image.load('tend.jpg'))
tend = tend.convert_alpha()
tend = pygame.transform.scale(tend, (WIDTH,HEIGHT))
tpause=(pygame.image.load('pause.png'))
tpause = tpause.convert_alpha()
tpause = pygame.transform.scale(tpause, (WIDTH,HEIGHT//2))
#loading sounds
pygame.mixer.music.load('tetris.wav')  #
pygame.mixer.music.set_volume(0.6)      #      #
pauses = pygame.mixer.Sound('pause.wav')   # 
pauses.set_volume(0.7)
clear = pygame.mixer.Sound('shrink.wav')   # 
clear.set_volume(0.5)
wow = pygame.mixer.Sound('bottom.wav')   # 
wow.set_volume(1)

shapeNo = randint(1,7)#shape number
nextNo = randint(1,7)# next shape number
holdNo = -1 #hold shape number
shape = Shape(MIDDLE,TOP,shapeNo) #shape object
nextshape= Shape(RIGHT+5,TOP+4,nextNo)#next shape object
hold=Shape(LEFT-7,TOP+4,abs(holdNo))#hold shape object
shadow = Shape(shape.col,shape.row, shape.clr)#shadow object
#wall objects
ceil = Floor(LEFT-1,2,COLUMNS+2)
floor = Floor(LEFT-1,FLOOR,COLUMNS+2)
walll = Wall(LEFT-1, TOP, ROWS)
wallr = Wall(RIGHT, TOP, ROWS)

obstacles =Obstacles(LEFT, FLOOR)#obstacles object
level=0#level
numrows=0#number of rows cleared
speed=17#speed (starts slow, lower is faster)
#different size fonts
font = pygame.font.SysFont("Ariel Black",50)
font1 = pygame.font.SysFont("Ariel Black",150)
font2 = pygame.font.SysFont("Ariel Black",100)
font3 = pygame.font.SysFont("Ariel Black",70)
#start and restart button coordinates
rx=LEFT*GRIDSIZE+GRIDSIZE
ry=FLOOR*GRIDSIZE-4*GRIDSIZE
rw=9*GRIDSIZE
rh=4*GRIDSIZE

gameover=0#game starts at the start screen
backtoback=False#boolean that checks for back to back tetrises

#---------------------------------------#

#---------------------------------------#
#   functions                           #
#---------------------------------------#
def redraw_screen():
    screen.fill(BLACK)
    draw_grid() #draws a grid on the playing area
    screen.blit(images[frame%8], ((LEFT-2)*GRIDSIZE+5,(TOP-2)*GRIDSIZE)) #draws the gif border
    #draws the two boxes with the gif border
    screen.blit(box[frame%8], ((LEFT-9)*GRIDSIZE,(TOP+1)*GRIDSIZE+GRIDSIZE/2))
    screen.blit(box[frame%8], ((RIGHT+3)*GRIDSIZE,(TOP+1)*GRIDSIZE+GRIDSIZE/2))
    if level<15:
        #draw the obstacles when the level is under 15
        obstacles.draw(screen, GRIDSIZE)
    else:
        if shape.row<5:
            #makes obstacles invisible past a certain point when the level is 15 or over
            obstacles.draw(screen, GRIDSIZE)                      
    nextshape.draw(screen, GRIDSIZE)#draws the next shape
    if holdNo>0:
        #draws the held shape
        hold.draw(screen, GRIDSIZE)
    shadow.sdraw(screen, GRIDSIZE)#draw the shadow
    shape.draw(screen, GRIDSIZE)# draw the shape
    #draw the walls of the playing area
    floor.draw(screen, GRIDSIZE)
    ceil.draw(screen, GRIDSIZE)
    walll.draw(screen, GRIDSIZE)
    wallr.draw(screen, GRIDSIZE)
    #drawing all the text on the screen for score, level, etc.
    text = font.render('SCORE:', 1, (0,255,0))
    text1 = font.render(str(score), 1, (0,255,0))
    text2=font.render('LEVEL:', 1, (0,255,0))
    text3=font.render(str(level), 1, (0,255,0))
    text4=font.render('HOLD', 1, (0,255,0))
    text5=font.render('NEXT', 1, (0,255,0))
    screen.blit(text,(24*GRIDSIZE,17*GRIDSIZE))
    screen.blit(text1,(24*GRIDSIZE,18*GRIDSIZE+10))                                                
    screen.blit(text2,(3*GRIDSIZE,17*GRIDSIZE))
    screen.blit(text3,(3*GRIDSIZE,18*GRIDSIZE+10))
    screen.blit(text4,(3*GRIDSIZE,3*GRIDSIZE+10))
    screen.blit(text5,(25*GRIDSIZE,3*GRIDSIZE+10))
    timer=font.render('Timer: '+str(int((time.time()-startTime)//1)),1, (0,255,0))
    screen.blit(timer,(0,GRIDSIZE+10))
    pygame.display.update()#updates the display
    
def draw_grid():
    """ Draw horisontal and vertical lines on the entire game window.
        Space between the lines is GRIDSIZE.
    """
    for i in range(LEFT*GRIDSIZE,RIGHT*GRIDSIZE,GRIDSIZE):
        pygame.draw.line(screen, (50,50,50), (i,TOP*GRIDSIZE), (i,FLOOR*GRIDSIZE),1)
    for j in range(TOP*GRIDSIZE,FLOOR*GRIDSIZE,GRIDSIZE):
        pygame.draw.line(screen, (50,50,50), (LEFT*GRIDSIZE,j), (RIGHT*GRIDSIZE,j),1)
    
        
#---------------------------------------#
#   main program                        #
#---------------------------------------#    
inPlay = True #start the game                                        
print('press p to pause') #instructions
while inPlay:#while in the game
    framecount+=1#1 is added to the frame counter each frame
    frame+=1#next frame for the gif
    for event in pygame.event.get():
        if event.type == pygame.QUIT:         
            inPlay = False#if the user tries to exit, kill the program
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:#if p is pressed
                if pause:#if the game is paused
                    pause=False#resume
                    pygame.mixer.music.play(loops = -1)#play the music
                else:
                    pygame.mixer.music.stop()#stop the music
                    pauses.play()#play the pause sound
                    pause=True#pause the game
        if pause==False:#while the game is not paused
            if event.type == pygame.KEYDOWN and gameover==1:#while the game is running
                if event.key == pygame.K_UP:#if the up arrow key is pressed, rotate the image
                    #checks for any collisions and corrects them
                    shape.rotateClkwise()
                    shadow.rotateClkwise()
                    if shape.collides(obstacles):
                        shape.rotateCntclkwise()
                        shadow.rotateCntclkwise()
                if event.key == pygame.K_LEFT:#if the left arrow key is pressed
                    #move the shape left, check for collisions, and correct them
                    shape.move_left()
                    shadow.move_left()
                    if shape.collides(obstacles):
                        shape.move_right()
                        shadow.move_right()
                if event.key == pygame.K_RIGHT:#if the right arrow key is pressed
                    #move the shape right, check for collisions and correct them
                    shape.move_right()
                    shadow.move_right()
                    if shape.collides(obstacles):
                        shape.move_left()
                        shadow.move_left()
         
                #check for collisions again and corrects them
                if shape.collides(walll) or shape.collides(wallr):
                    while shape.collides(walll):
                        shape.move_right()
                        shadow.move_right()
                    while shape.collides(wallr):
                        shape.move_left()
                        shadow.move_left()
                if event.key == pygame.K_SPACE:#if spacebar is pressed
                    #drop the shape to the furthest down position it can go
                    while shape.collides(floor) == False and shape.collides(obstacles)==False:
                        shape.move_down()
                if event.key == pygame.K_LSHIFT:#if left shift is pressed
                    if holdNo>0:#if there is already a block held
                        #compares the number of obstacles to the previous number of obstacles to check if hold has already been used once that turn
                        if len(obstacles.blocks) !=numobstacles:
                            #change the shape with the held shape and sets the number of obstacles again
                            shapeNo , holdNo = holdNo, shapeNo
                            shape=Shape(MIDDLE,TOP,shapeNo)
                            hold= Shape(LEFT-7,TOP+4,holdNo)
                            shadow=Shape(shape.col,shape.row, shape.clr)
                            numobstacles=len(obstacles.blocks)
        
                    else:
                        #change the shape with the held shape
                        hold= Shape(LEFT-7,TOP+4,shapeNo)
                        holdNo=shapeNo
                        shapeNo=nextNo
                        shape=Shape(MIDDLE,TOP,shapeNo)
                        nextNo = randint(1,7)
                        nextshape= Shape(RIGHT+5,TOP+4,nextNo)
                        shadow=Shape(shape.col,shape.row, shape.clr)
                        numobstacles=len(obstacles.blocks)
    if gameover==0: #Start screen, draws an image and a start button and moves to the main screen after the user presses start
        screen.blit(tback, (0,0))
        pygame.draw.rect(screen, BLACK, ((rx,ry),(rw,rh)),0)  #rect for the start button
        txtCLR = (255,255,255) #text color
        welcome=font1.render('TETRIS', 1, txtCLR) #Title
        start=font2.render('START', 1, WHITE) #start text
        #displaying font
        screen.blit(start,(LEFT*GRIDSIZE+GRIDSIZE,ry+25))
        screen.blit(welcome,(WIDTH/2-190,100))

        #gets the position of the cursor and if mouse is pressed, sets all variables to their starting values and moves to the main screen
        (mx,my)=pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if mx>=rx and mx<=rx+rw and my>=ry and my<=ry+rh:
                startTime=time.time()
                pygame.mixer.music.play(loops = -1)
                gameover=1
        pygame.display.update() #updates the display
    elif gameover==1:#main game screen
        if pause==False:#while the game is not paused
            keys = pygame.key.get_pressed()
            if keys[pygame.K_DOWN] == True:#if the down arrow key is pressed
                    #move the shape down
                    shape.move_down()
            if framecount%speed==0 and shape.collides(floor)==False and shape.collides(obstacles)==False:
                #move the shape down if it is not colliding and at a certain frame number
                shape.move_down()
            #checks collisions, corrects them
            if shape.collides(floor) or shape.collides(obstacles):
                shape.move_up()
                wow.play()
                if shape.row<=TOP:#ends the game if the shape collides with the top
                    gameover=2
                obstacles.append(shape)#add the shape to the obstacles object
                shapeNo = nextshape.clr#sets shape and shadow to the next shape
                shape=Shape(MIDDLE,TOP,shapeNo)
                nextNo = randint(1,7)#random next shape
                nextshape= Shape(RIGHT+5,TOP+4,nextNo)
                shadow=Shape(shape.col,shape.row, shape.clr)
                fullRows = obstacles.findFullRows(TOP, FLOOR, COLUMNS)    # finds the full rows and removes their blocks from the obstacles 
                
                if len(fullRows)>0:
                    #adds different scores depending on number of lines and back to back tetrises
                    numrows+=len(fullRows)
                    level=(score//500)+1
                    if level<15:
                        speed=17-level
                    else:
                        speed=2
                    if len(fullRows)==4 and backtoback:
                        score+=1200
                    elif len(fullRows)==4:
                        score+=800
                    else:
                        score+=(100*len(fullRows))
                        
                    if len(fullRows)==4:
                        backtoback=True
                    else:
                        backtoback = False
                    clear.play()#play line clear sound effect
                obstacles.removeFullRows(fullRows)#remove full rows
            #resets the shadow
            shadow.col = shape.col
            shadow.row  = shape.row
            shadow.clr = shape.clr
            #move the shadow down while its not colliding
            while shadow.collides(floor)==False and shadow.collides(obstacles)==False:
                shadow.move_down()
            #move the shadow up after it collides with something
            shadow.move_up()
            #call the redraw function to draw all objects and images
            redraw_screen()
            pygame.time.delay(40)#delay
        else:#while the game is paused show the pause image
            screen.blit(tpause, (0,WIDTH//2-(WIDTH//2)//2))
            pygame.display.update()
    elif gameover==2: #end screen, draws an image and a restart button and moves to the main screen after the user presses restart
        screen.blit(tend, (0,0))
        pygame.draw.rect(screen, BLACK, ((rx,ry),(rw,rh)),0)  #rect for the restart button
        txtCLR = (255,255,255) #text color
        #setting every piece of text to be displayed
        welcome=font1.render('GAME', 1, txtCLR) 
        welcome1=font1.render('OVER', 1, txtCLR) 
        start=font3.render('RESTART', 1, WHITE) 
        start1=font2.render('SCORE: '+str(score), 1, (255,255,0)) 
        #displaying font
        screen.blit(start,(LEFT*GRIDSIZE+GRIDSIZE,ry+25))
        screen.blit(start1,(LEFT*GRIDSIZE-2*GRIDSIZE,ry-90))
        screen.blit(welcome,(WIDTH/2-190,100))
        screen.blit(welcome1,(WIDTH/2-110,200))

        #gets the position of the cursor and if mouse is pressed, sets all variables to their starting values and moves to the main screen
        (mx,my)=pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if mx>=rx and mx<=rx+rw and my>=ry and my<=ry+rh:
                shapeNo = randint(1,7)
                nextNo = randint(1,7)
                holdNo = -1
                shape = Shape(MIDDLE,TOP,shapeNo)
                nextshape= Shape(RIGHT+5,TOP+4,nextNo)
                hold=Shape(LEFT-7,TOP+4,abs(holdNo))
                shadow = Shape(shape.col,shape.row, shape.clr)
                ceil = Floor(LEFT-1,2,COLUMNS+2)
                floor = Floor(LEFT-1,FLOOR,COLUMNS+2)
                walll = Wall(LEFT-1, TOP, ROWS)
                wallr = Wall(RIGHT, TOP, ROWS)
                obstacles =Obstacles(LEFT, FLOOR)
                level=1
                numrows=0
                speed=17
                backtoback=False
                startTime=time.time()
                framecount=0
                score = 0
                frame=0
                gameover=1               
        pygame.display.update() #updates the display
pygame.quit()#quit
    
    
