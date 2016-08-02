from tkinter import *
import math

class circle(object):
    def __init__(self,x,y,r,color):
        self.x=x
        self.y=y
        self.color=color
        self.defaultspeed=2
        self.speed=0
        self.angle=0
        self.r=r

    def givespeed(self):
        self.speed=speed

    def follow(self,x,y):
        if ( abs(self.x-x)<1 and abs(self.y-y)<1):
            self.speed=0
        self.speed=self.defaultspeed
        if(x==self.x):
            if(self.y<y):
                self.angle=math.pi/2
            else:
                self.angle=math.pi/2*3
        self.angle=math.atan((y-self.y)/(x-self.x))
        if(x<self.x):
            self.angle+=math.pi
        self.update()
        #print(self.angle/math.pi*180)

    def update(self):
        self.x+=self.speed*math.cos(self.angle)
        self.y+=self.speed*math.sin(self.angle)

    def draw(self,canvas):
        (x,y,r)=(self.x,self.y,self.r)
        canvas.create_oval(x-r,y-r,x+r,y+r,fill=self.color,outline=self.color)

class body(object):
    #first position is x
    def __init__(self,x,y,r,color,num):
        self.x=x
        self.y=y
        self.color=color
        self.defaultspeed=1
        self.speed=0
        self.angle=0
        self.r=r
        self.num=num
        self.bodypart=[]
        for i in range(num):
            self.bodypart.append(circle(x+i*10,y,r,color))

    def follow(self,x,y):
        self.bodypart[0].follow(x,y)
        for i in range(1,self.num):
            self.bodypart[i].follow(self.bodypart[i-1].x-math.cos(self.bodypart[i-1].angle)*10,self.bodypart[i-1].y-math.sin(self.bodypart[i-1].angle)*10)
            #self.bodypart[i].follow(self.bodypart[i-1].x,self.bodypart[i-1].y)

    def update(self):
        for i in range(self.num):
            self.bodypart[i].update() 
    
    def draw(self,canvas):
        self.update()
        for i in range(self.num):
            self.bodypart[i].draw(canvas)

            
def init(data):
    #initialize all datas
    pass

def mousePressed(event,data):
    #use event.x, event.y
    data["mousePos"]=(event.x,event.y)
    print(event.x,event.y)
    data["snake"].follow(event.x,event.y)

def keyPressed(event,data):
    #use event.char and event.keysym
    pass

def timeFired(data):
    print("1")

def redrawAll(canvas,data):
    #draw in canvas
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
    data["snake"]=body(width/2,height/2,20,"purple",10)
    data["mousePos"]=(width/2,height/2)
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
