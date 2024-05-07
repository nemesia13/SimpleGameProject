import pygame
import sqlite3

#method for loading images
def image_load(image):
    return pygame.image.load(image).convert_alpha()

#get players position image path from a DB
def playerPlacement(type,placement):
    connection = sqlite3.connect("oppari_game.db")
    #send SQL commands to DB with cursor
    cursor = connection.cursor()

    cursor.execute("SELECT img_path FROM "+type+" WHERE description=='"+placement+"'")
    result = cursor.fetchone() #fetches one row with the above criteria
    img_path = result[0] #returns the values as plain text, no extra [] around it
    connection.close()
    return img_path

#create a Player class that's the Sprite type
class Player(pygame.sprite.Sprite):
    def __init__(self,type, placement): #player needs specified a character type and player placement
        super().__init__() #initilizie sprite class in this class
        
        self.gravity = 0  #gravity for player, avoids player seeming like it floats when it falls
        self.animation_speed = 0.05 #default "speed" for animation

        #different types of player climbing and placements on the x-axis
        if placement == 1:
            climbLeft01 = image_load(playerPlacement(type,"climb_left01"))
            climbLeft02 = image_load(playerPlacement(type,"climb_left02"))
            self.frames = [climbLeft01,climbLeft02] #image will be added to the frames-list
            x_position = 4 #position on the x-axis
        elif placement == 2:
            climbMiddle01 = image_load(playerPlacement(type,"climb_middle01"))
            climbMiddle02 = image_load(playerPlacement(type,"climb_middle02"))
            self.frames = [climbMiddle01,climbMiddle02]
            x_position = 135
        elif placement == 3:
            climbRight01 = image_load(playerPlacement(type,"climb_right01"))
            climbRight02 = image_load(playerPlacement(type,"climb_right02"))
            self.frames = [climbRight01,climbRight02]
            x_position = 260

    #different placements for the fall direction
        elif placement == 4:
            fallLeft01 = image_load(playerPlacement(type,"fall_left01"))
            fallLeft02 = image_load(playerPlacement(type,"fall_left02"))
            self.frames = [fallLeft01,fallLeft02]
            x_position = 0
            self.gravity += 6 #increase the gravity when hit and causes characther to fall
            self.animation_speed = 0.15 #changes the speed the animation changes the pictures with
        elif placement == 5:
            fallMiddle01 = image_load(playerPlacement(type,"fall_right01"))
            fallMiddle02 = image_load(playerPlacement(type,"fall_right02"))
            self.frames = [fallMiddle01,fallMiddle02]
            x_position = 135
            self.gravity += 6
            self.animation_speed = 0.15
        elif placement == 6:
            fallRight01 = image_load(playerPlacement(type,"fall_right01"))
            fallRight02 = image_load(playerPlacement(type,"fall_right02"))
            self.frames = [fallRight01,fallRight02]
            x_position = 260
            self.gravity += 6
            self.animation_speed = 0.15
        
        
        self.animation_index = 0 #tells what image in the list will be used based on its index
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(bottomleft=(x_position, 650))

    #method which controls the gravity for the player character    
    def apply_gravity(self):
        self.rect.y += self.gravity
        #gravity increases if player gets under the default y-axis placement of 650
        if self.rect.y > 650:
            self.gravity +=1

    #decides which image of the player will be shown
    def animation_state(self):
        self.animation_index += self.animation_speed #increases the animation_index
        #when length of self.frames is bigger then animation_index, the index will be set back to 0
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    #sprite class has a few methods that can be used outside the class, one of them is update()
    #which is why all the other methods should be executed in the update() mehtod
    def update(self):
        self.animation_state()
        self.apply_gravity()
            
