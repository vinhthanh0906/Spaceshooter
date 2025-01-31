import turtle
import random
import os
from object import Sprite ,Player, Game, Enemy, Missle

#import the turtle module
#Require by MACOS to show the window
turtle.fd(0)

#Set the animation speed to the maximum
turtle.speed(0) # set turtle speed
turtle.bgcolor('black') # initiate a black window

turtle.ht() # this will hide the default turtle cursor
turtle.setundobuffer(1) #limit the memory that turtle use to represent actions
turtle.tracer(1) #Speed up the drawing

#Create objects
player = Player('triangle', 'white', 0,0)
enemy = Enemy('circle','red',-100,0)
missle = Missle('circle','yellow',0,0)


"""Keybinding"""
#Movement
turtle.onkey(player.turn_left, "Left")
turtle.onkey(player.turn_right,"Right")
turtle.onkey(player.foward, "Up")
turtle.onkey(player.backward, "Down")
turtle.onkey(missle.fire,'space')
turtle.listen()

#Shooting
# turtle.onkey(player.shooting(),"Space")
# turtle.listen()



#Create game object(Game window)
game = Game()
game.draw_border()


#Loop the game 
while True: 
    player.move()
    enemy.move() 
    missle.fire()

    
    #Collision
    if player.is_collision(enemy):
        x = random.randint(-250,250)
        y = random.randint(-250,250)
        enemy.goto(x,y)
        
delay = input("Press Enter to finish.>")



