from tkinter import *

def init(data):
    #initialize all datas
    pass

def mousePressed(event,data):
    #use event.x, event.y
    pass

def keyPressed(event,data):
    #use event.char and event.keysym
    pass

def timeFired(data):
    pass

def redrawAll(canvas,data):
    #draw in canvas
    pass

#data is a dictionary

def run(width=300,height=300):
    def redrawAllWrapper(canvas,data):
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
    root.bind('<Key>',lambda event: keyPressedWrapper(event,canvas,data))
    timeFiredWrapper(canvas,data)

    #launch the app
    root.mainloop()
    print("bye!")

run(400,200)

#xxtu?
