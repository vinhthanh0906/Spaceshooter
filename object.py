import turtle
import random
from main import player

#Define object in the game
class Sprite(turtle.Turtle): # inheritent all attribute from Turtle class
    def __init__(self, sprite_shape, color, startx, starty):
        #Initiate a class from Turtle class
        turtle.Turtle.__init__(self,shape = sprite_shape) 
        self.speed(0) #Speed of animation, not movement
        self.penup()
        self.color(color)
        self.fd(0) #Make turtle stand by
        self.goto(startx,starty)
        self.speed = 1 #Set movement speed
        self.bullets = [] # Set a shooting function for it 
        
    def move(self):
        self.fd(self.speed)
        #Boucing movement
        #xcor() and ycor() are function, try not to compare instance method a
        if self.xcor() > 290:
            self.setx(290) # this will reset the position to make the game smoother
            self.rt(60)
        if self.xcor() < -290:
            self.setx(-290)
            self.rt(60)
        if self.ycor() > 290:
            self.sety(290)
            self.rt(60)
        if self.ycor() < -290:
            self.sety(-290)
            self.rt(60)
    
    """Constructing
    #Make your        
    # def shooting(self):
    #     bullet = turtle.Turtle()
    #     bullet.shape('circle')
    #     bullet.shapesize(2)
    #     bullet.penup()
    #     bullet.speed(0)
    #     bullet.goto(self.xcor(), self.ycor())
    #     bullet.setheading(self.heading())        
    #     self.bullets.append(bullet)

    # def move_bullets(self):
    #     Move all bullets forward and remove them when they go off-screen.
    #     for bullet in self.bullets:
    #         bullet.forward(15)
    #         if bullet.xcor() > 300 or bullet.xcor() < -300 or bullet.ycor() > 300 or bullet.ycor() < -300:
    #             bullet.hideturtle()
    #             self.bullets.remove(bullet)
    """          
                
class Player(Sprite):   
    def __init__(self, sprite_shape, color, startx, starty):
        Sprite.__init__(self, sprite_shape, color, startx, starty) # inheritate from Sprite class
        self.speed = 4
        self.lives = 3
    #Movement
    def foward(self):
        self.speed += 1

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
    def __init__(self, sprite_shape, color, startx, starty):
        Sprite.__init__(self, sprite_shape, color, startx, starty)
        self.speed = 6
        self.setheading(random.randint(0,360))
    

#Shooting Mechanic
class Missle(Sprite):
    def __init__(self, sprite_shape, color, startx, starty):
        Sprite.__init__(self,sprite_shape, color, startx, starty)    
        self.speed = 20
        self.shape = 'circle'
        self.shapesize(stretch_len=0.4, stretch_wid=0.3, outline=None)
        self.status = 'ready'
        # self.goto(-1000,1000)
    
    def fire(self):
        if self.status == 'ready': # You can only shoot when missle ready 
            self.goto(player.xcor,player.ycor())
            self.status = 'shoot'
    
    def move(self):
        if self.status == 'shoot':
            self.fd(self.speed)
        
    
    
    
    
    
    
    
    
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