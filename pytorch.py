import turtle
import random
import time
#init mixer module to playsound
# pygame.mixer.init()




#Apply DeepLearning by Pytorch
import torch
import torch.nn as nn
import torch.optim as optim
import math
import torch.nn.functional as F

from config import AimingNN, BoundaryAvoidanceNN
from config import model, boundary_model,criterion, optimizer, optimizer_boundary

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
            # sound = pygame.mixer.Sound("D:\WORK\Python\Game\spaceshooter\sfx\missle.mp3")
            # sound.play()

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
# turtle.bgpic('D:\WORK\Python\Game\spaceshooter\img\pic.gif')

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
for i in range(5):
    enemies.append(Enemy("circle", "red", -100,0))

allies = [] 
for ally in range(6):
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
# pygame.mixer.Sound("D:\WORK\Python\Game\spaceshooter\sfx\game_music.mp3")


# TargetLock Line Drawer
line_drawer = turtle.Turtle()
line_drawer.color("white")
line_drawer.penup()
line_drawer.hideturtle()
line_drawer.speed(0)


status_writer = turtle.Turtle()
status_writer.hideturtle()
status_writer.penup()
status_writer.goto(0, 310)


#Loop the game 
while True:
    turtle.update()
    time.sleep(0.01)
    player.move()
    missile.move()

    
    if allies:
            for ally in allies:
                angle_to_ally = player.towards(ally)
                friendly_fire_angle = abs((angle_to_ally - player.heading() + 360) % 360)
                if friendly_fire_angle > 180:
                    friendly_fire_angle = 360 - friendly_fire_angle

                if friendly_fire_angle < 2 and missile.status == "firing":
                    missile.status = "ready"  

    if enemies:
        closest_enemy = min(enemies, key=lambda e: player.distance(e))
        dx = closest_enemy.xcor() - player.xcor()
        dy = closest_enemy.ycor() - player.ycor()
        true_angle = player.towards(closest_enemy)

        input_tensor = torch.tensor([[player.xcor(), player.ycor(), closest_enemy.xcor(), closest_enemy.ycor()]], dtype=torch.float32)
        angle_tensor = model(input_tensor)
        predicted_angle = angle_tensor.item()

        target_tensor = torch.tensor([[true_angle]], dtype=torch.float32)
        loss = criterion(angle_tensor, target_tensor)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        player.setheading(predicted_angle)

        for enemy in enemies:
            angle_to_enemy = player.towards(enemy)
            angle_diff = abs((angle_to_enemy - player.heading() + 360) % 360)
            if angle_diff > 180:
                angle_diff = 360 - angle_diff

            if angle_diff < 2 and missile.status == "ready":
                missile.fire()
                break  

            
            
        line_drawer.clear()
        line_drawer.penup()
        line_drawer.goto(player.xcor(), player.ycor())
        line_drawer.pendown()
        line_drawer.goto(closest_enemy.xcor(), closest_enemy.ycor())

            
        mid_x = (player.xcor() + closest_enemy.xcor()) / 2
        mid_y = (player.ycor() + closest_enemy.ycor()) / 2
        distance = player.distance(closest_enemy)

        line_drawer.penup()
        line_drawer.goto(mid_x, mid_y + 10)
        line_drawer.write(f"---{distance:.2f}---", align="center", font=("Arial", 10, "normal"))

        dx = closest_enemy.xcor() - player.xcor()
        dy = closest_enemy.ycor() - player.ycor()
        true_angle = math.degrees(math.atan2(dy, dx))
        player_angle = player.heading()
        angle_diff = (true_angle - player_angle + 360) % 360
        if angle_diff > 180:
            angle_diff = 360 - angle_diff

        line_drawer.goto(mid_x, mid_y - 10)
        line_drawer.write(f"Angle: {angle_diff:.1f}°", align="center", font=("Arial", 10, "normal"))



        #Border Bounce Back
        BOUNDARY_X = 300
        BOUNDARY_Y = 300

        hit_left   = player.xcor() <= -BOUNDARY_X
        hit_right  = player.xcor() >= BOUNDARY_X
        hit_top    = player.ycor() >= BOUNDARY_Y
        hit_bottom = player.ycor() <= -BOUNDARY_Y

        
        player.setx(max(min(player.xcor(), BOUNDARY_X), -BOUNDARY_X))
        player.sety(max(min(player.ycor(), BOUNDARY_Y), -BOUNDARY_Y))

        if (hit_left or hit_right) and (hit_top or hit_bottom):
            player.setheading((player.heading() + 180) % 360)

        elif hit_left or hit_right:
            player.setheading(180 - player.heading())

        elif hit_top or hit_bottom:
            player.setheading(-player.heading())
    
    


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
            # sfx = pygame.mixer.Sound("D:\WORK\Python\Game\spaceshooter\sfx\explosion.mp3")
            # sfx.play()
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




