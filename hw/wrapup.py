from tkinter import *
import math
import random
import wave
import simpleaudio as sa

defaultspeed=5
acceleratespeed=10
defaultsnakelength=15
maxwidth=5000
maxheight=4000

##quote from##
##http://simpleaudio.readthedocs.io/en/latest/simpleaudio.html#examples##
bgmpath="bgm.wav"
eatpath="eat.wav"
wave_read=wave.open(bgmpath,'rb')
audio_data = wave_read.readframes(wave_read.getnframes())
num_channels = wave_read.getnchannels()
bytes_per_sample = wave_read.getsampwidth()
sample_rate = wave_read.getframerate()
wave_obj = sa.WaveObject.from_wave_file(eatpath)
global play_obj
play_obj = sa.play_buffer(audio_data, num_channels, bytes_per_sample, sample_rate)
##end quote##

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
    def __init__(self,x,y,r,color,name):
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
        self.name=name
        for i in range(self.num):
            self.bodypart.append(circle(x+5*i,y,r,color))
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
            self.bodypart[i].follow(self.bodypart[i-1].x-math.cos(self.bodypart[i-1].angle)*5,self.bodypart[i-1].y-math.sin(self.bodypart[i-1].angle)*5,accelerate)
        return "go"
    def check_collision(self,other):
        if(type(other)==food):
            if ((self.bodypart[0].x-other.x)**2+(self.bodypart[0].y-other.y)**2)<(self.r+other.r)**2:
                self.size+=other.r/3
                self.energy+=other.r/3
                self.update()
                eat_play_obj = wave_obj.play()
                return "eat"
        if(type(other)==lua or type(other)==body):
            (x0,y0,r0)=(self.bodypart[0].x,self.bodypart[0].y,self.bodypart[0].r)
            for ani in other.bodypart:
                (x,y,r)=(ani.x,ani.y,ani.r)
                if((x-x0)**2+(y-y0)**2<=(r+r0)**2):
                    return "die"                
        return "no"

class food(object):
    def __init__(self,x,y,r,color):
        self.x=x
        self.y=y
        self.color=color
        self.r=r

class lua(body):
    def __init__(self,x,y,r,color,name):
        super().__init__(x,y,r,color,name)
    def update(self):
        super().update()
    def follow(self,x,y,accelerate):
        super().follow(x,y,accelerate)
    def check_collision(self,other):
        if(type(other)==food):
            if ((self.bodypart[0].x-other.x)**2+(self.bodypart[0].y-other.y)**2)<(self.r+other.r)**2:
                #print("eat")
                self.size+=1
                self.energy+=1
                self.update()
                return "eat"
        if(type(other)==lua or type(other)==body):
            (x0,y0,r0)=(self.bodypart[0].x,self.bodypart[0].y,self.bodypart[0].r)
            for ani in other.bodypart:
                (x,y,r)=(ani.x,ani.y,ani.r)
                if((x-x0)**2+(y-y0)**2<=(r+r0)**2):
                    return "die"                
        return "no"
    def automove(self,food):
        mindis=6000
        (x0,y0)=(self.bodypart[0].x,self.bodypart[0].y)
        minx=0
        miny=0
        for point in food:
            (x,y)=(point.x,point.y)
            if(((x-x0)**2+(y-y0)**2)**0.5<mindis):
                minx=x
                miny=y
                mindis=((x-x0)**2+(y-y0)**2)**0.5
        r=random.randint(0,1000)
        if(r>995):
            ran=True
        else:
            ran=False
        return self.follow(minx,miny,ran)

def init(data):
    #initialize all datas
    data["mousePos"]=(data["width"]/2-5,data["height"]/2)
    data["name"]="user"
    data["snake"]=body(data["totalWidth"]/2,data["totalHeight"]/2,20,"orange red",data["name"])
    data["food"]=[]
    data["aisnake"]=[]
    data["food_color"]=["yellow","orange","azure","green","cyan","pink","lemon chiffon"]
    data["foodnum"]=500
    data["accelerate"]=False
    data["mousemoved"]=False
    data["mouseClickedTimer"]=0
    data["leaderboard"]=dict()
    #init food
    for i in range(data["foodnum"]):
        randx=random.randint(1,data["totalWidth"])
        randy=random.randint(1,data["totalHeight"])
        randcolor=random.choice(data["food_color"])
        randr=random.randint(3,6)
        data["food"].append(food(randx,randy,randr,randcolor))
    #init AI snakes
    data["ainum"]=10
    for i in range(data["ainum"]):
        randx=random.randint(0,5000)
        randy=random.randint(0,4000)
#        randx=2800
#        randy=2000
        randcolor=random.choice(data["food_color"])
        data["aisnake"].append(lua(randx,randy,20,randcolor,"bot"+str(i)))

def mousePressed(event,data):
    #use event.x, event.y
    data["mousePos"]=(event.x,event.y)
    data["accelerate"]=False

def mouseClicked(event,data):
    if(data["stage"]=="game"):
        data["mousePos"]=(event.x,event.y)
        data["accelerate"]=True
        data["mouseClickedTimer"]=0
    if(data["stage"]=="menu" or data["stage"]=="gameover"):
        if (400<=event.x<=600 and 400<=event.y<=480):
            init(data)
            data["stage"]="game"

def keyPressed(event,data):
    pass
    
def timeFired(data):
    global play_obj
    if(not play_obj.is_playing()):
        play_obj = sa.play_buffer(audio_data, num_channels, bytes_per_sample, sample_rate)
    if(data["stage"]=="game"):
        (x,y)=data["mousePos"]
        (x,y)=(x+data["snake"].bodypart[0].x-data["width"]/2,y+data["snake"].bodypart[0].y-data["height"]/2)
        if(data["snake"].follow(x,y,data["accelerate"])=="die"):
            data["stage"]="gameover"
            for i in range(data["snake"].num):
                (xi,yi)=(data["snake"].bodypart[i].x,data["snake"].bodypart[i].y)
                randx=random.randint(-10,10)
                randy=random.randint(-10,10)
                data["food"].append(food(xi+randx,yi+randy,10,data["snake"].bodypart[i].color))
        data["mouseClickedTimer"]+=1
        if(data["mouseClickedTimer"]==10):
            data["accelerate"]=False
            data["mouseClickedTimer"]=0
    if(data["stage"]!="menu"):
        #AI snakes find path
        for l in data["aisnake"]:
            dis=random.randint(0,10)
            if(dis>5):
                l.follow(data["snake"].bodypart[0].x,data["snake"].bodypart[0].y,False)
            else:
                if(l.automove(data["food"])=="die"):
                    data["aisnake"].remove(l)
        #if collide with AI snakes
        for l in data["aisnake"]:
            if(data["stage"]=="game"):
                if(data["snake"].check_collision(l)=="die"):
                    for i in range(data["snake"].num):
                        (xi,yi)=(data["snake"].bodypart[i].x,data["snake"].bodypart[i].y)
                        randx=random.randint(-10,10)
                        randy=random.randint(-10,10)
                        data["food"].append(food(xi+randx,yi+randy,10,data["snake"].bodypart[i].color))
                    data["stage"]="gameover"
        #if ate something
        for foods in data["food"]:
            if(data["snake"].check_collision(foods)=="eat"):
                data["food"].remove(foods)
                data["foodnum"]-=1
        #if ai collide and die
        for l in data["aisnake"]:
            if(data["stage"]=="game"):
                if(l.check_collision(data["snake"])=="die"):
                    for i in range(l.num):
                        (xi,yi)=(l.bodypart[i].x,l.bodypart[i].y)
                        randx=random.randint(-10,10)
                        randy=random.randint(-10,10)
                        data["food"].append(food(xi+randx,yi+randy,3,l.bodypart[i].color))            
                    data["aisnake"].remove(l)
                    #print("remove",l)
        for l in data["aisnake"]:
            for m in data["aisnake"]:
                if(l==m):
                    continue
                elif(l.check_collision(m)=="die"):
                    for i in range(l.num):
                        (xi,yi)=(l.bodypart[i].x,l.bodypart[i].y)
                        randx=random.randint(-10,10)
                        randy=random.randint(-10,10)
                        data["food"].append(food(xi+randx,yi+randy,10,l.bodypart[i].color))            
                    data["aisnake"].remove(l)
                    #print("remove",l)
                    break
        #if ai ate something:
        for l in data["aisnake"]:
            for foods in data["food"]:
                if(l.check_collision(foods)=="eat"):
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
        #calculate leader board
        d=dict()
        d[data["snake"].name]=int(data["snake"].energy)
        for i in data["aisnake"]:
            d[i.name]=i.energy
        d=sorted(d.items(),key=lambda d:d[1],reverse=True)
        data["leaderboard"]=d


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
    if(data["stage"]!="menu"):
        #draw border            
        canvas.create_rectangle(0-x0,0-y0,data["totalWidth"]-x0,data["totalHeight"]-y0,outline="white",width=10)
        #draw food
        for foods in data["food"]:
            (x,y,r)=(foods.x,foods.y,foods.r)
            canvas.create_oval(x-x0-r,y-y0-r,x-x0+r,y-y0+r,fill=foods.color,outline=foods.color)
        if(data["stage"]=="game"):
        #draw snake
            for i in range(data["snake"].num-1,-1,-1):
                (x,y,r)=(data["snake"].bodypart[i].x,data["snake"].bodypart[i].y,data["snake"].bodypart[i].r)
                canvas.create_oval(x-x0-r,y-y0-r,x-x0+r,y-y0+r,fill=data["snake"].color,outline=data["snake"].color)
                if(i==0):
                    r=r-5
                    canvas.create_oval(x-x0-r,y-y0-r,x-x0+r,y-y0+r,fill="white",outline=data["snake"].color)
                    r=r-6
                    canvas.create_oval(x-x0-r,y-y0-r,x-x0+r,y-y0+r,fill="black",outline=data["snake"].color)

        #draw ai snakes
        for l in data["aisnake"]:
            for i in range(l.num-1,-1,-1):
                (x,y,r)=(l.bodypart[i].x,l.bodypart[i].y,l.bodypart[i].r)
                canvas.create_oval(x-x0-r,y-y0-r,x-x0+r,y-y0+r,fill=l.color,outline=l.color)
                if(i==0):
                    r=r-6
                    canvas.create_oval(x-x0-r,y-y0-r,x-x0+r,y-y0+r,fill="white",outline=l.color)
                    r=r-8
                    canvas.create_oval(x-x0-r,y-y0-r,x-x0+r,y-y0+r,fill="black",outline=l.color)
        #draw mini map
        (x0,y0)=(800,580)
        canvas.create_rectangle(x0,y0,x0+150,y0+120,fill="black",outline="white")
        (x1,y1,r1)=(data["snake"].bodypart[0].x/40,data["snake"].bodypart[0].y/40,data["snake"].r/5)
        canvas.create_oval(x0+x1-r1,y0+y1-r1,x0+x1+r1,y0+y1+r1,fill=data["snake"].color)
        for l in data["aisnake"]:
            (x1,y1,r1)=(l.bodypart[0].x/40,l.bodypart[0].y/40,l.r/5)
            canvas.create_oval(x0+x1-r1,y0+y1-r1,x0+x1+r1,y0+y1+r1,fill=l.color)
        #draw leaderboard
        (x0,y0)=(900,100)
        con=0
        for i in data["leaderboard"]:
            (n,e)=i
            t=n+"   "+str(e)
            canvas.create_text(x0,y0+20*con,text=t,font=("Time New Roman",20),fill="white")
            con+=1
        if(data["stage"]=="gameover"):
            t="Your Final Score is "+ str(int(data["snake"].energy))
            canvas.create_text(500,300,text=t,fill="white",font=("Lithos Pro Regular",60))
            canvas.create_rectangle(400,400,600,480,fill="white",outline="brown",width=5)
            canvas.create_text(500,440,text="RESTART",font=("Times New Roman",20))
    if(data["stage"]=="menu"):
        canvas.create_text(500,200,text="SLITHER",font=("Lithos Pro Regular",100),fill="white")
        canvas.create_rectangle(400,400,600,480,fill="white",outline="brown",width=5)
        canvas.create_text(500,440,text="START",font=("Times New Roman",20))

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
    data["totalWidth"]=5000
    data["totalHeight"]=4000
    data["name"]="user"
    data["stage"]="menu"
    data["snake"]=body(data["totalWidth"]/2,data["totalHeight"]/2,20,"orange red",data["name"])
    paly_obj = sa.play_buffer(audio_data, num_channels, bytes_per_sample, sample_rate)

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

run(1000,700)
