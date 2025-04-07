import turtle
import random
import os
import pygame
import time
#init mixer module to playsound
pygame.mixer.init()


#GAME DEV
class Sprite(turtle.Turtle):
	def __init__(self, spriteshape, color, startx, starty):
		turtle.Turtle.__init__(self, shape = spriteshape)
		self.speed(0)
		self.penup()
		self.color(color)
		self.fd(0)
		self.goto(startx, starty)
		self.speed = 0
		
	def is_collision(self, other):
		if (self.xcor() >= (other.xcor() - 20)) and \
			(self.xcor() <= (other.xcor() + 20)) and \
			(self.ycor() >= (other.ycor() - 20)) and \
			(self.ycor() <= (other.ycor() + 20)):
			return True
		else:
			return False
			
	def move(self):
		self.fd(self.speed)
		
		if self.xcor() < -290:
			self.rt(60)
			self.setx(-290)
		
		elif self.xcor() > 290:
			self.rt(60)
			self.setx(290)
			
		if self.ycor() < -290:
			self.rt(60)
			self.sety(-290)		
		
		elif self.ycor() > 290:
			self.rt(60)
			self.sety(290)

    
                
class Player(Sprite):   
    def __init__(self, sprite_shape, color, startx, starty):
        Sprite.__init__(self, sprite_shape, color, startx, starty) # inheritate from Sprite class
        self.speed = 0
        self.lives = 3
        self.shapesize(stretch_wid=0.6, stretch_len=1.1, outline=None)
    #Movement
    def forward(self):
        self.speed += 2

    def turn_left(self):
        self.lt(45)
    
    def turn_right(self):
        self.rt(45)
        
    def backward(self):
        self.speed -= 1
    
    #Contact with object, adjust collision
    def is_collision(self,other):
        if (self.xcor() >= (other.xcor() - 20)) and (self.xcor() <= (other.xcor() + 20 )) and \
        (self.ycor() <= (other.ycor() + 20)) and \
        (self.ycor() >= (other.ycor() - 20)):
            return True
        else:
            return False # if collide with enemy, break the game loop
    
            
class Enemy(Sprite):
	def __init__(self, spriteshape, color, startx, starty):
		Sprite.__init__(self, spriteshape, color, startx, starty)
		self.speed = 2
		self.setheading(random.randint(0,360))
		

class Ally(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self,spriteshape, color, startx, starty)
        self.speed = 3
        self.setheading(random.randint(0,360))



#Shooting Mechanic
class Missile(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.2, stretch_len=0.4, outline=None)
        self.status = "ready"
        self.speed = 50

    def fire(self):
        if self.status == "ready":
            self.status = "shoot"
            sound = pygame.mixer.Sound("D:/WORK/Python/Game/spaceshooter/sound/Sound Effect - Laser.mp3")
            sound.play()

    def move(self):
        if self.status == "ready":
            self.hideturtle()
            self.goto(-1000, 1000)  # Send the missile off the screen

        elif self.status == "shoot":
            self.goto(player.xcor(), player.ycor())  # Reset missile to player position
            self.setheading(player.heading())  # Set heading direction
            self.showturtle()  # Show the missile
            self.status = "firing"

        elif self.status == "firing":
            self.fd(self.speed)

        # Border Check - Reset missile when it goes out of bounds
        if self.xcor() < -290 or self.xcor() > 290 or self.ycor() < -290 or self.ycor() > 290:
            self.status = "ready"
    
    
    
    
#Drawing map
class Game(turtle.Turtle):
    def __init__(self):
        self.level = 1
        self.score = 0
        self.state = "playing"
        self.pen = turtle.Turtle()
        self.lives = 3
    
    #Draw game border 
    def draw_border(self):
        self.pen.speed(0)
        self.pen.color('white')
        self.pen.pensize(3)
        self.pen.penup()
        self.pen.goto(-300,300)
        self.pen.pendown()
        for side in range(4):
            self.pen.fd(600)
            self.pen.rt(90)
        self.pen.penup
        self.pen.ht() 
        self.pen.pendown()
    
    

    #Game status
    def show_status(self):
        self.pen.undo()
        msg = "Score: %s" %(self.score)
        self.pen.penup()
        self.pen.goto(-300,310)
        self.pen.write(msg, font=("Arial",16,"normal"))

    



#TESTING
#import the turtle module
#Require by MACOS to show the window
turtle.fd(0)

#FPS adjust(Coming soon)



#Set the animation speed to the maximum
turtle.speed(0) # set turtle speed
turtle.bgcolor('black') # initiate a black window
# turtle.bgpic('D:\WORK\Python\Game\spaceshooter\pic\desktop-wallpaper-pure-black-solid-black.jpg')

#window title
turtle.title("Spacewar")



turtle.ht() # this will hide the default turtle cursor
turtle.setundobuffer(1) #limit the memory that turtle use to represent actions
turtle.tracer(0) #Speed up the drawing

#Create objects
player = Player("triangle","white", 0, 0 )
missile = Missile("triangle","yellow",0 ,0)

#Multiple enemies and allies
enemies = []
for i in range(6):
    enemies.append(Enemy("circle", "red", -100,0))

allies = [] 
for i in range(7):
    allies.append(Ally("square", "cyan",0,0 ))
    


"""Keybinding"""
#Movement
turtle.onkey(player.turn_left, "Left")
turtle.onkey(player.turn_right, "Right")
turtle.onkey(player.forward, "Up")
turtle.onkey(player.backward, "Down")
turtle.onkey(missile.fire, "space")
turtle.listen()


#Create game object(Game window)
game = Game()
game.draw_border()

#Show status
game.show_status()
pygame.mixer.Sound("D:/WORK/Python/Game/spaceshooter/sound/Travis Scott - HIGHEST IN THE ROOM (Audio).mp3")


#Loop the game 

while True:
    turtle.update()
    time.sleep(0.01)
    player.move()
    missile.move()
    
    #Multiple object movement
    for enemy in enemies:
        enemy.move()
        
        if player.is_collision(enemy):
            x = random.randint(-250,250)
            y = random.randint(-250,250)
            enemy.goto(x,y)
            game.score -= 5
            game.show_status()
            
            
        if missile.is_collision(enemy):
            game.score += 10
            sfx = pygame.mixer.Sound("D:/WORK/Python/Game/spaceshooter/sound/Big Explosion Sound Effect.mp3")
            sfx.play()
            x = random.randint(-250,250)
            y = random.randint(-250,250)
            enemy.goto(x,y)
            missile.status = 'ready'
            game.show_status()
            
    
    for ally in allies:
        ally.move()
        if missile.is_collision(ally):
            x = random.randint(-250,250)
            y = random.randint(-250,250)
            ally.goto(x,y)
            game.score -= 10
            game.show_status()
        
        

    
        
delay = input("Press Enter to finish.>")





