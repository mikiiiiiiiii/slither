from tkinter import *
import math
import random


#part of the snake
class circle(object):
    def __init__(self,x,y,r,color):
        self.x=x
        self.y=y
        self.color=color
        self.defaultspeed=2
        self.speed=0
        self.angle=0
        self.r=r
    def givespeed(self,speed):
        self.speed=speed
    def follow(self,x,y,speed):
        if (abs(self.x-x)<10 and abs(self.y-y)<10):
            self.speed=0
        else:
            self.speed=self.defaultspeed
            if(x==self.x):
                if(self.y<y):
                    self.angle=math.pi/2
                else:
                    self.angle=math.pi/2*3
            else:
                self.angle=math.atan((y-self.y)/(x-self.x))
                if(x<self.x):
                    self.angle+=math.pi
                self.update(speed)
    def update(self,speed):
        self.x+=speed*math.cos(self.angle)
        self.y+=speed*math.sin(self.angle)
    def draw(self,canvas):
        (x,y,r)=(self.x,self.y,self.r)
        canvas.create_oval(x-r,y-r,x+r,y+r,fill=self.color,outline=self.color)

#whole body of the snake 
class body(object):
    #first position is x
    def __init__(self,x,y,r,color,num):
        self.x=x
        self.y=y
        self.color=color
        self.defaultspeed=2
        self.speed=0
        self.angle=0
        self.r=r
        self.num=num
        self.bodypart=[]
        self.size=0
        self.energy=10
        self.initr=r
        for i in range(num):
            self.bodypart.append(circle(x+i*10,y,r,color))
    def follow(self,x,y):
        self.bodypart[0].follow(x,y,self.speed)
        for i in range(1,self.num):
            self.bodypart[i].follow(self.bodypart[i-1].x-math.cos(self.bodypart[i-1].angle)*self.r/4,self.bodypart[i-1].y-math.sin(self.bodypart[i-1].angle)*self.r/4,self.speed)
            #self.bodypart[i].follow(self.bodypart[i-1].x,self.bodypart[i-1].y)
    def accelerate(self,x,y):
        if(self.energy!=0):
            print("accelerate")
            self.energy-=1
            self.follow(x,y,self.defaultspeed*10)
    def update(self):
        if(self.size==3):
            (x,y)=(self.bodypart[self.num-1].x,self.bodypart[self.num-1].y)
            self.bodypart.append(circle(x,y,self.r,self.color))
            self.num+=1
            self.size=0
        self.r=self.initr+self.energy/2
        for i in range(self.num):
            self.bodypart[i].update(self.defaultspeed)
            self.bodypart[i].r=self.r
    def draw(self,canvas):
        self.update()
        for i in range(self.num):
            self.bodypart[i].draw(canvas)
    def check_collision(self,other):
        if(type(other)==food):
            #print(((self.x-other.x)**2+(self.y-other.y)**2),(self.r+other.r)**2)
            if ((self.bodypart[0].x-other.x)**2+(self.bodypart[0].y-other.y)**2)<(self.r+other.r)**2:
                #print("eat")
                self.size+=1
                self.energy+=1
                self.update()
                return "eat"
        return "no"
            
                
#food            
class food(object):
    def __init__(self,x,y,color):
        self.x=x
        self.y=y
        self.color=color
        self.r=3
    def draw(self,canvas):
        (x,y,r)=(self.x,self.y,self.r)
        canvas.create_oval(x-r,y-r,x+r,y+r,fill=self.color,outline=self.color)

def init(data):
    #initialize all datas
    data["mousePos"]=(data["width"]/2,data["height"]/2)
    #data["snake"]=circle(width/2,height/2,40,"purple")
    data["snake"]=body(data["width"]/2,data["height"]/2,20,"purple",10)
    data["food"]=[]
    data["food_color"]=["yellow","orange","red","green"]
    data["foodnum"]=30
    for i in range(data["foodnum"]):
        randx=random.randint(1,data["width"])
        randy=random.randint(1,data["height"])
        randcolor=random.choice(data["food_color"])
        data["food"].append(food(randx,randy,randcolor))

def mousePressed(event,data):
    #use event.x, event.y
    data["mousePos"]=(event.x,event.y)
    data["snake"].follow(event.x,event.y)

def keyPressed(event,data):
    #use event.char and event.keysym
    print("space")
    if event.keysym=="Space":
        print("space")
        (x,y)=data["mousePos"]
        data["snake"].accelerate(x,y)

def timeFired(data):
    (x,y)=data["mousePos"]
    data["snake"].follow(x,y)
    for foods in data["food"]:
        if(data["snake"].check_collision(foods)=="eat"):
            data["food"].remove(foods)
            data["foodnum"]-=1
    if(data["foodnum"]<15):
        randnum=random.randint(10,20)
        for i in range(randnum):
            randx=random.randint(1,data["width"])
            randy=random.randint(1,data["height"])
            randcolor=random.choice(data["food_color"])
            data["food"].append(food(randx,randy,randcolor))
        data["foodnum"]+=randnum

def redrawAll(canvas,data):
    #draw in canvas
    for food in data["food"]:
        food.draw(canvas)
    data["snake"].draw(canvas)
    

#data is a dictionary

def run(width=300,height=300):
    def redrawAllWrapper(canvas,data):
        canvas.delete(ALL)
        redrawAll(canvas,data)
        canvas.update()

    def mousePressedWrapper(event,canvas,data):
        mousePressed(event,data)
        redrawAllWrapper(canvas,data)

    def keyPressedWrapper(event,canvas,data):
        keyPressed(event,data)
        redrawAllWrapper(canvas,data)

    def timeFiredWrapper(canvas,data):
        timeFired(data)
        redrawAllWrapper(canvas,data)
        canvas.after(data["timeDelay"],timeFiredWrapper,canvas,data)

    #set up data and init
    data=dict()
    data['width']=width
    data['height']=height
    data['timeDelay']=100
    
    init(data)

    root=Tk()
    canvas=Canvas(root,width=data['width'],height=data['height'])
    canvas.pack()

    #set up events
    root.bind("<Motion>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind('<Key>',lambda event: keyPressedWrapper(event,canvas,data))
    timeFiredWrapper(canvas,data)

    #launch the app
    root.mainloop()
    print("bye!")

run(1000,800)
