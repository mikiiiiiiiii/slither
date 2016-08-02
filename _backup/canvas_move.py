from tkinter import *
import math
import random

defaultspeed=5
acceleratespeed=10
defaultsnakelength=15
maxwidth=5000
maxheight=4000

class circle(object):
    def __init__(self,x,y,r,color):
        self.x=x
        self.y=y
        self.r=r
        self.color=color
        self.speed=defaultspeed
        self.acceleratespeed=acceleratespeed
        self.angle=0 
    def follow(self,x,y,accelerate):#accelerate is a bool flag
        prevangle=self.angle
        if(x==self.x and y == self.y):
            self.angle=prevangle
        elif(x==self.x and y!=self.y):
            if(self.y<y):
                self.angle=math.pi/2
            else:
                self.angle=math.pi/2*3
        else:
            self.angle=math.atan((y-self.y)/(x-self.x))
            if(x<self.x):
                self.angle+=math.pi
        #deal with angel:
        if(math.pi/16<self.angle-prevangle<=math.pi):
            self.angle=prevangle+math.pi/16
        if(math.pi<self.angle-prevangle<math.pi/16*31):
            self.angle=prevangle-math.pi/16
        if(-math.pi<=self.angle-prevangle<-math.pi/16):
            self.angle=prevangle-math.pi/16
        if(-math.pi/16*31<self.angle-prevangle<-math.pi):
            self.angle=prevangle+math.pi/16

        if accelerate:
            #   print("accelerate")
            self.x+=self.acceleratespeed*math.cos(self.angle)
            if self.x<0 or self.x>maxwidth:
                return "die"
            self.y+=self.acceleratespeed*math.sin(self.angle)
            if self.y<0 or self.y>maxheight:
                return "die"
        else:
            self.x+=self.speed*math.cos(self.angle)
            if self.x<0 or self.x>maxwidth:
                return "die"
            self.y+=self.speed*math.sin(self.angle)
            if self.y<0 or self.y>maxheight:
                return "die"
        return "go"

class body(object):
    def __init__(self,x,y,r,color):
        self.x=x
        self.y=y
        self.r=r
        self.color=color
        self.speed=defaultspeed
        self.angle=0
        self.num=defaultsnakelength
        self.bodypart=[]
        self.size=0
        self.energy=0
        self.initr=r
        for i in range(self.num):
            self.bodypart.append(circle(x+10*i,y,r,color))
    def update(self):
        self.r=self.initr+self.energy/6
        for i in range(self.num):
            self.bodypart[i].r=self.r
        if(self.size>1):
            (x,y)=(self.bodypart[self.num-1].x-math.cos(self.bodypart[self.num-1].angle)*self.r/4,self.bodypart[self.num-1].y-math.sin(self.bodypart[self.num-1].angle)*self.r/4)
            self.bodypart.append(circle(x,y,self.r,self.color))
            self.bodypart[self.num].angle=self.bodypart[self.num-1].angle
            self.num+=1
            self.size-=1
    def follow(self,x,y,accelerate):#accelerate is a bool flag
        if accelerate and self.energy<=0:
            accelerate=False
        elif accelerate:
            self.energy-=1
            self.update()
        if(self.bodypart[0].follow(x,y,accelerate)=="die"):
            return "die"
        for i in range(1,self.num):            
            self.bodypart[i].follow(self.bodypart[i-1].x-math.cos(self.bodypart[i-1].angle)*self.r/4,self.bodypart[i-1].y-math.sin(self.bodypart[i-1].angle)*self.r/4,accelerate)
        return "go"
    def check_collision(self,other):
        if(type(other)==food):
            if ((self.bodypart[0].x-other.x)**2+(self.bodypart[0].y-other.y)**2)<(self.r+other.r)**2:
                #print("eat")
                self.size+=other.r/3
                self.energy+=other.r/3
                self.update()
                return "eat"
        return "no"

class food(object):
    def __init__(self,x,y,r,color):
        self.x=x
        self.y=y
        self.color=color
        self.r=r

def init(data):
    #initialize all datas
    data["totalWidth"]=5000
    data["totalHeight"]=4000
    data["mousePos"]=(data["width"]/2-100,data["height"]/2)
    data["snake"]=body(data["totalWidth"]/2,data["totalHeight"]/2,20,"orange red")
    data["food"]=[]
    data["food_color"]=["yellow","orange","azure","green","cyan","pink","lemon chiffon"]
    data["foodnum"]=500
    data["accelerate"]=False
    data["mousemoved"]=False
    data["mouseClickedTimer"]=0
    for i in range(data["foodnum"]):
        randx=random.randint(1,data["totalWidth"])
        randy=random.randint(1,data["totalHeight"])
        randcolor=random.choice(data["food_color"])
        randr=random.randint(3,6)
        data["food"].append(food(randx,randy,randr,randcolor))

def mousePressed(event,data):
    #use event.x, event.y
    data["mousePos"]=(event.x,event.y)
    data["accelerate"]=False

def mouseClicked(event,data):
    data["mousePos"]=(event.x,event.y)
    data["accelerate"]=True
    data["mouseClickedTimer"]=0

def keyPressed(event,data):
    pass
    
def timeFired(data):
    (x,y)=data["mousePos"]
    (x,y)=(x+data["snake"].bodypart[0].x-data["width"]/2,y+data["snake"].bodypart[0].y-data["height"]/2)
    if(not data["mousemoved"]):
        data["snake"].follow(x,y,data["accelerate"])
    data["mousemoved"]=False
    data["mouseClickedTimer"]+=1
    if(data["mouseClickedTimer"]==10):
        data["accelerate"]=False
        data["mouseClickedTimer"]=0
    for foods in data["food"]:
        if(data["snake"].check_collision(foods)=="eat"):
            data["food"].remove(foods)
            data["foodnum"]-=1
    
    if(data["foodnum"]<480):
        randnum=random.randint(10,30)
        for i in range(randnum):
            randx=random.randint(1,data["width"])
            randy=random.randint(1,data["height"])
            randcolor=random.choice(data["food_color"])
            randr=random.randint(3,6)
            data["food"].append(food(randx,randy,randr,randcolor))
        data["foodnum"]+=randnum        

def redrawAll(canvas,data):
    (x0,y0)=(data["snake"].bodypart[0].x-data["width"]/2,data["snake"].bodypart[0].y-data["height"]/2)
   #draw background
    (x1,y1)=(x0+data["width"],y0+data["height"])
    (j0,i0)=((y0//300)*300,(x0//int(2*(3**0.5)*50))*int(2*(3**0.5)*50))
    (j1,i1)=((y1//300+2)*300,(x1//int(2*(3**0.5)*50)+2)*int(2*(3**0.5)*50))
    for i in range(int(i0),int(i1),int(2*(3**0.5)*50)+1):
        for j in range(int(j0),int(j1),300):
            canvas.create_polygon(i-x0-(3**0.5)*50,j-y0-1*50,i-x0,j-y0-2*50,i-x0+(3**0.5)*50,j-y0-1*50,i-x0+(3**0.5)*50,j-y0+1*50,i-x0,j-y0+2*50,i-x0-(3**0.5)*50,j-y0+1*50,fill="dark slate blue",outline="MistyRose4",width=15)
        for j in range(int(j0+150),int(j1+150),300):
            canvas.create_polygon(i-x0-2*(3**0.5)*50,j-y0-1*50,i-x0-(3**0.5)*50,j-y0-2*50,i-x0,j-y0-1*50,i-x0,j-y0+1*50,i-x0-(3**0.5)*50,j-y0+2*50,i-x0-2*(3**0.5)*50,j-y0+1*50,fill="dark slate blue",outline="MistyRose4",width=15)
            
    
    #draw food
    for foods in data["food"]:
        (x,y,r)=(foods.x,foods.y,foods.r)
        canvas.create_oval(x-x0-r,y-y0-r,x-x0+r,y-y0+r,fill=foods.color,outline=foods.color)
    #draw snake
    for i in range(data["snake"].num-1,-1,-1):
        (x,y,r)=(data["snake"].bodypart[i].x,data["snake"].bodypart[i].y,data["snake"].bodypart[i].r)
        canvas.create_oval(x-x0-r,y-y0-r,x-x0+r,y-y0+r,fill=data["snake"].color,outline=data["snake"].color)

#data is a dictionary

def run(width=300,height=300):
    def redrawAllWrapper(canvas,data):
        canvas.delete(ALL)
        redrawAll(canvas,data)
        canvas.update()

    def mousePressedWrapper(event,canvas,data):
        mousePressed(event,data)
        
    def mouseClickedWrapper(event,canvas,data):
        mouseClicked(event,data)

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
    data['timeDelay']=30
    
    init(data)

    root=Tk()
    canvas=Canvas(root,width=data['width'],height=data['height'])
    canvas.pack()

    #set up events
    root.bind("<Motion>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Button-1>", lambda event: mouseClickedWrapper(event,canvas,data))
    root.bind('<Key>',lambda event: keyPressedWrapper(event,canvas,data))
    timeFiredWrapper(canvas,data)

    #launch the app
    root.mainloop()
    print("bye!")

run(1000,800)
