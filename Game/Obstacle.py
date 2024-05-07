import pygame
import sqlite3
from random import randint

#method for loading images
def image_load(image):
    return pygame.image.load(image).convert_alpha() 

#get the used obstacles image path by connecting to DB
def obstacleType(character,type):
    connection = sqlite3.connect("oppari_game.db")
    #send SQL commands to DB with cursor
    cursor = connection.cursor()

    cursor.execute("SELECT img_path FROM obstacles WHERE character=='"+character+"' AND type=='"+type+"'")
    result = cursor.fetchone() #fetches one row with the above criteria
    img_path = result[0] #returns the values as plain text, no extra [] around it
    connection.close()
    return img_path

#create Obstacle class, which is type: Sprite
class Obstacle(pygame.sprite.Sprite):
    def __init__(self,character,type): #needs a type since there is more then one obstacle, needs player character type too
        super().__init__() #initilizie sprite class in this class

        #different types of obstacles below
        if type == 'obstacle_1':
            obstacle_011 = image_load(obstacleType(character,'type_011'))
            obstacle_012 = image_load(obstacleType(character,'type_012'))
            self.frames = [obstacle_011,obstacle_012] #adds the image to the frames list
            x_position = 10 #obstacles position on the x-axis

        if type == 'obstacle_2':
            obstacle_021 = image_load(obstacleType(character,'type_021'))
            obstacle_022= image_load(obstacleType(character,'type_022'))
            self.frames = [obstacle_021,obstacle_022]
            x_position = 150

        if type == 'obstacle_3':
            obstacle_031 = image_load(obstacleType(character,'type_031'))
            obstacle_032 = image_load(obstacleType(character,'type_032'))
            self.frames = [obstacle_031,obstacle_032]
            x_position = 300

        self.animation_index = 0 #tells what picture will be used form the frames-list
        #image and rect always needed, can't have a sprite without them
        self.image = self.frames[self.animation_index]
        #randomize the y_position for the obstacles
        self.rect = self.image.get_rect(bottomleft=(x_position,randint(-300,-90)))

    #decides which image of the obstacle will be shown
    def animation_state(self):
        self.animation_index += 0.06 #increases the animation_index, works as animation speed
        #when length of self.frames is bigger then animation_index, the index will be set back to 0
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    #method to kill the sprite obstacle
    def destroy(self):
        #destroys obstacle when it has hit 900 on the y-axis
        if self.rect.y >= 900:
            self.kill()

    #method that can be accessed outside the class
    def update(self):
        self.rect.y += 6 #moves the obstacle downwards
        self.animation_state()
        self.destroy()


