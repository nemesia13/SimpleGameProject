import pygame
import sqlite3

import Player #import player class
import Obstacle #import obstacle class
from sys import exit
from random import choice
import os #provides functions to interact with evironment variables

#specifies that the working dir is the same as the script dir, stops errors from happening outside VSCode
os.chdir(os.path.dirname(os.path.abspath(__file__)))

## METHODS##    
#method for loading images
def image_load(image):
    return pygame.image.load(image).convert_alpha() #has to be convert_aplha() for transparent in png to be trasnparent in game

#method for display text on screen
def displayText(text, size, x, y):
    #import font
    font = pygame.font.Font('font/plain-old-handwriting-font/PlainOldHandwriting-Gn2A.ttf',int(size)) #font_type,font_size
    surface= font.render(text,False,(255,255,255)) #displayed text, "True" if you want to smooth out the text,color(rgb)        
    rectangle = surface.get_rect(center=(x,y)) #rectangle created based on text
    screen.blit(surface, rectangle) #display surface on screen

#create rectangle using an image
def createAndDisplayRectangle(img_path,x,y):
    surface = image_load(img_path)
    rectangle = surface.get_rect(topleft=(x,y))
    screen.blit(surface,rectangle)
    return rectangle #returns the created rectangle

def moveBuildings():
    #moves the background buildings, resets to y=1600 when the bottom has reached the top
    for building in building_rectangles:
        if building.bottom < -1: building.top = 1600
        building.top -=0.8 #building moves upwards

def movePipes():
    #waterpipes movement, resets to 0 when top has reached lower then 799
    for pipe in pipe_rectangles: 
        if pipe.top > 799: pipe.bottom = 0
        pipe.top += 0.8 #pipes move downwards

#method that determines what happens when two sprites collide, or a sprite and a sprite group
#gets a group of obstacles as parameter
def spritesCollision(obstacle_group):
    #if True: the obstacle would be deleted everytime the player touches one, don't want that to happen here
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False): #needs (sprite, group, boolean), reutrns a list
        #when a collison happens delete all sprites in the obstacle group
        obstacle_group.empty()
        #local scope to global scope using return statement
        #returns a boolean that determines the games activity in the main code
        return False
    else:
        return True

#method for displaying and calculating the game score
def displayScore():
    current_time = int(pygame.time.get_ticks()/1000) -start_time #int to avoid float numbers, /1000 so it's in seconds not ms
    displayText(f'Score: {current_time}',60,200,50)

    return current_time #so it can be accessed outside the function

#adds a new score and player to the DB table named highscore
def addScore(name,score):
    #connects to a sqlite3 DB named "oppari_game.db"
    connection = sqlite3.connect("oppari_game.db")
    cursor = connection.cursor() #send SQL commands to DB with cursor

    cursor.execute("SELECT COUNT(*) FROM highscore") #counts how many rows the table has
    result = cursor.fetchone() #fetches one of results
    row_count = result[0] #amount of rows
    id = row_count+1

    newPlayer = (id,name,score)

    sql = ''' INSERT INTO highscore (id,name,score)
              VALUES(?,?,?) '''
    cursor.execute(sql,newPlayer)#add new data into table
    connection.commit() #commit changes to DB
    connection.close() #close connection to DB

#displays top3 highsocres from the DB table "highscore"
def displayHighscore():
    connection = sqlite3.connect("oppari_game.db")
    cursor = connection.cursor()

    #selects both name and score from highscore table, table is sorted in descending order by score
    cursor.execute("SELECT name FROM highscore ORDER BY score DESC")
    names = cursor.fetchall() #fetch all results
    cursor.execute("SELECT score FROM highscore ORDER BY score DESC")
    scores = cursor.fetchall()
    connection.close()#close connection with database

    i = 0
    for (name,score) in zip(names,scores): #iterates through multiple lists at once
        displayText(str(name[0]+"................."+str(score[0])),25,190,650+i)
        i+=22
        if i== 66: break #gets the top 3 scores, with space between scores counted in

#returns the img_path based on what character the player uses
def getGameOverImg(type):
    connection = sqlite3.connect("oppari_game.db")
    cursor = connection.cursor()

    cursor.execute("SELECT img_path FROM "+str(type)+" WHERE description== 'game_over' ")
    result = cursor.fetchone()
    connection.close()
    return str(result[0]) #returns imag_path 

#initializ pygame,necessery for running pygame
pygame.init()
screen= pygame.display.set_mode((400,800)) #create game window
pygame.display.set_caption('Oppari_game') #changes the caption seen up in the tab text
clock = pygame.time.Clock() #decides the games max fps
start_time = 0 #needed for current_time to get zeroed
score = 0
playerName = "" #empty name
characterType="" #no choice yet
selectMenu = False
arrow_placement= 180 #default middle

#import images for game background
building_surface = image_load('graphics/windows_01.png')
building_surface2 = image_load('graphics/windows_02.png')
building_surface3 = image_load('graphics/windows_03.png')
pipes_surface = image_load('graphics/pipes_01.png')

building_surfaces = [building_surface,building_surface2, building_surface3] #list for all the building surfaces

#create rectangles to be same size as the given surface
building_rectangle = building_surface.get_rect(topleft=(0,0))
building_rectangle2 = building_surface2.get_rect(topleft=(0,800))
building_rectangle3 = building_surface3.get_rect(topleft=(0,1600))
pipe_rectangle = pipes_surface.get_rect(topleft=(0,0))
pipe_rectangle2 = pipes_surface.get_rect(topleft=(0,800))

#lists for different rectangles
building_rectangles = [building_rectangle,building_rectangle2,building_rectangle3]
pipe_rectangles = [pipe_rectangle,pipe_rectangle2]

#OBSTACLE
#initialize object_group, Group() is used for several sprites
obstacle_group = pygame.sprite.Group()

#Obstacle Timer
obstacle_easy_timer = pygame.USEREVENT+1 #use +1 to define a userevent
obstacle_medium_timer = pygame.USEREVENT+2 #increase the userevent when adding new ones
obstacle_hard_timer = pygame.USEREVENT+3
pygame.time.set_timer(obstacle_easy_timer,2000) #speed of obstacles showing up
pygame.time.set_timer(obstacle_medium_timer,1500) #speed of obstacles showing up
pygame.time.set_timer(obstacle_hard_timer,1000) #speed of obstacles showing up

#game is not active at the start
game_active = False

while True:
    #gets the events in pygame
    for event in pygame.event.get():
        #the games display does nothing before you quit the game, display can be seen "forever"
        if event.type == pygame.QUIT:
            pygame.quit()
            exit() #exit while loop
        
        #decides how the player moves, using left and right keyboard arrows
        if event.type == pygame.KEYDOWN and game_active==True: #checks if a key has been pushed down
            if  event.key == pygame.K_a or event.key == pygame.K_LEFT and playerPosition > 1: #checks if the pushed key is the same as here
                playerPosition = playerPosition - 1
            if  event.key == pygame.K_d or event.key == pygame.K_RIGHT and playerPosition < 3:
                playerPosition = playerPosition + 1

            main_player = Player.Player(characterType,playerPosition) #creates a player using the sprite class, needs type and placement for player
            main_player.add(player) #adds player to the "player" sprite group
            fallDirection = playerPosition+3 #change fallDirection based on player position, always a playerPosition+3 higher

        #controls the user input for a player name
        if event.type == pygame.KEYDOWN and game_active==False:
            if event.key != pygame.K_SPACE:#the game moves forward when SPACE is pressed
                if event.key == pygame.K_BACKSPACE:
                    playerName = playerName[:-1] #use range to erase the last character
                else:
                    playerName += event.unicode #gunicode= gets the value of the key that was pressed


        #method that blocks specfic events from queueing up, user can't use keyboards
        def keysBlocked():
            pygame.event.set_blocked([pygame.KEYDOWN, pygame.KEYUP])
        #method that allows specfic events to queue up, user can use keyboards
        def keysAllowed():
            pygame.event.set_allowed([pygame.KEYDOWN, pygame.KEYUP])

        if game_active: #this way the game won't create obstacles when the game is not running
            #obstacles will increase in showing up when the score gets higher
            if event.type == obstacle_easy_timer and score <= 50:
                #choice= let's pick a random item from a list, add more of one if you want it to occur more
                obstacle_group.add(Obstacle.Obstacle(characterType,choice(['obstacle_1','obstacle_2','obstacle_3']))) #obstacle sprite needs a type
            elif event.type == obstacle_medium_timer and 100 >= score > 50:
                obstacle_group.add(Obstacle.Obstacle(characterType,choice(['obstacle_1','obstacle_2','obstacle_3']))) 
            elif event.type == obstacle_hard_timer and score > 100:
                obstacle_group.add(Obstacle.Obstacle(characterType,choice(['obstacle_1','obstacle_2','obstacle_3'])))

        else: 
            #KEYUP here so we can use KEYDOWN in the other one wihtout messing the game up
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE and playerName != "" and selectMenu==False: #start game by pressing "space" when there is a player name
                selectMenu = True #shows selectMenu screen

            if event.type == pygame.KEYDOWN and selectMenu==True: #when selectScreen shows
                #controls the arrow rectangle that selects the character
                if event.key == pygame.K_LEFT and arrow_placement > 100:
                    arrow_placement -= 140
                if event.key == pygame.K_RIGHT and arrow_placement < 300:
                    arrow_placement += 140
                if event.key == pygame.K_b: #takes the game back to beginning screen
                    selectMenu=False

                if event.key == pygame.K_SPACE: #checks if the mouse button has been pressed down
                    if clownChoice_rectangle.colliderect(arrow_rectangle): #checks if arrow rect collides with a character choice rect
                        characterType = "clownPlayer" #changes the characterType based on users choice
                        game_active = True #game becomes active
                    elif suitChoice_rectangle.colliderect(arrow_rectangle):
                        characterType = "suitPlayer"
                        game_active = True
                    elif bunnyChoice_rectangle.colliderect(arrow_rectangle):
                        characterType = "bunnyPlayer"
                        game_active = True

                    playerPosition = 2 #player position, default position being middle
                    #uses the Player class sprite, but isn't a sprite itself
                    main_player = Player.Player(characterType,playerPosition) #specify that Player class has been imported, with default player choosen
                    player = pygame.sprite.GroupSingle() #initialize a sprite group, GroupSingle is used for one sprite
                    main_player.add(player) #add the created player into the created group
                    #what direction the character falls too, default fallDirection being middle:
                    fallDirection = playerPosition+3 
                
                    selectMenu= False #selectMenu closes  
                    start_time = int(pygame.time.get_ticks()/1000) #gets the time for how long pygame HAS been running
            
            #start a new round after game over
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and score !=0:
                game_active = True
                start_time = int(pygame.time.get_ticks()/1000)
            #get back to beginning screen after game over
            if event.type == pygame.KEYDOWN and event.key == pygame.K_b and score !=0:
                playerName = playerName[:-1] #erases the "b" that comes behind the name when you go back
                score = 0
 

    #THE ACTUAL GAME RUNNING
    if game_active:
        
        #shows the buidling surfaces on screen
        for surface,rectangle in zip(building_surfaces,building_rectangles):
            screen.blit(surface,rectangle)
        moveBuildings() #buildings movement

        #show pipe surfaces on screen
        for rectangle in pipe_rectangles:
            screen.blit(pipes_surface,rectangle) #pip rectangles use the same surface
        movePipes() #pipes movement

        #draws the player sprite on screen, uses sprite group
        player.draw(screen)  
        player.update() #updates player sprite

        obstacle_group.draw(screen) #draws the obstacle sprites
        obstacle_group.update() #updates the obstacle sprites

        score = displayScore() #gets current_time from method
        
        #COLLISIONS
        #when a collision happens
        if spritesCollision(obstacle_group) == False:
                keysBlocked() #block keys from working when player has been hit
                #create a new main_player for the group player, name the Player so it's easier to call back to it
                main_player = Player.Player(characterType,fallDirection)
                main_player.add(player)
                addScore(playerName,score) #add the score and player name to DB

        #when player character falls down and hits 900 on y-axis the game will end
        if main_player.rect.y > 900:
            game_active=False
            keysAllowed() #call function to allow keys to work again
            #default player start position being middle, and fallDirection being middle
            main_player = Player.Player(characterType,2)
            main_player.add(player)
            fallDirection = 5                    
 
    else:

        #Start screen, select screen or Game over screen
        #Start screen
        if score == 0 and selectMenu==False:
            #show start screen and text
            screen.fill((0,0,0))
            #screen.blit(start_screen,start_screen_rectangle)
            displayText('Oppari Game',60,200,100)
            displayText('Please type your name:',35,200,300)
            #playerName shows up on screen whilst typeing
            displayText(f'{playerName}',30,200,350)
            displayText('.........................................................',30,190,360)
            createAndDisplayRectangle('graphics/leftArrow.png',40,293) #decorative arrows
            createAndDisplayRectangle('graphics/rightArrow.png',310,293)
            
            displayText('Press SPACE To Continue',40,200,490)
            #only needs to display rectangles, not used anywhere else
            createAndDisplayRectangle('graphics/leftArrow.png',15,480)
            createAndDisplayRectangle('graphics/rightArrow.png',355,480)
            createAndDisplayRectangle('graphics/cube.png',0,580) #decoration
            displayText('Highscores:',40,200,590)
            createAndDisplayRectangle('graphics/leftArrow.png',85,580)
            createAndDisplayRectangle('graphics/rightArrow.png',255,580)
            displayHighscore()
            
        #Select menu screen
        elif score==0 and selectMenu==True:
            screen.fill((0,0,0))

            displayText('Choose a character!',60,200,150)
            displayText('Use arrow keys to change character',25,200,185)
            displayText('Press SPACE to start game',40,200,560)
            displayText('Press B to go back', 25,80,760)

            #create and display rectangles for character choices
            clownChoice_rectangle = createAndDisplayRectangle('graphics/clownPlayer_choice.png',10,200)
            suitChoice_rectangle = createAndDisplayRectangle('graphics/suitPlayer_choice.png',140,200)
            bunnyChoice_rectangle = createAndDisplayRectangle('graphics/bunnyPlayer_choice.png',270,200)
            #create and display rectangles for arrows
            arrow_rectangle = createAndDisplayRectangle('graphics/pointerArrow.png',arrow_placement,400)
            back_arrow_rectangle = createAndDisplayRectangle('graphics/backArrow.png',10,700)
            

        else: 
            #show game over screen and text:
            #code needs to be down enough so all the elements have time to change in the above code
            game_over_rectangle = createAndDisplayRectangle(getGameOverImg(characterType),0,0)

            displayText('Game Over',60,200,110)
            displayText(f'Your score: {score}',40,200,200)
            displayText('Press SPACE to play again',40,200,630)
            displayText('Press B to get to the Beginning',25,200,690)        


    #updates the screen that is on display
    pygame.display.update()
    clock.tick(60) #max fps(frames by second) is 60