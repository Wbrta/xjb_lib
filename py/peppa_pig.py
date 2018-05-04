import turtle
import math

turtle.speed(0)
turtle.pensize(0.1)
turtle.pencolor("black")

for i in range(-400, 401, 10):
    turtle.penup()
    turtle.goto(-600, i)
    turtle.pendown()
    turtle.goto(600, i)

for i in range(-600, 601, 10):
    turtle.penup()
    turtle.goto(i, 400)
    turtle.pendown()
    turtle.goto(i, -400)

def drawArc(step, angle, stride, pos = None, display = False):
    if pos != None:
        if display == False:
            turtle.penup()
        turtle.goto(pos[0], pos[1])
        if display == False:
            turtle.pendown()
    for _ in range(step):
        turtle.right(angle)
        turtle.forward(stride)

def drawCircle(pensize, pencolor, fillcolor, radius, extent = None, steps = None, pos = None, display = False):
    turtle.pensize(pensize)
    turtle.pencolor(pencolor)
    turtle.fillcolor(fillcolor)
    turtle.begin_fill()
    if pos != None:
        if display == False:
            turtle.penup()
        turtle.goto(pos[0], pos[1])
        if display == False:
            turtle.pendown()
    turtle.circle(radius, extent, steps)
    turtle.end_fill()

turtle.pensize(4)
turtle.pencolor("#E79DC0")
turtle.fillcolor("#F0C5D8")

turtle.begin_fill()
drawArc(300, 0.1, 1, [-200, 200])
drawArc(180, 0.33, 1)
drawArc(600, 0.2, 0.5)
drawArc(200, 0.4, 0.8)
turtle.left(95)
drawArc(100, 0.1, 1.7)
pos = turtle.position()
r = math.sqrt((pos[0] + 200) ** 2 + (pos[1] - 200) ** 2) / 2
turtle.circle(-r, 180)
turtle.end_fill()

turtle.circle(-r, 180)

drawCircle(1, "#F0C5D8", "#C5759A", r / 8, pos = [(pos[0] - 200) / 2 - 15, (pos[1] + 200) / 2 + 15])
drawCircle(1, "#F0C5D8", "#C5759A", -r / 8, pos = [(pos[0] - 200) / 2 + 15, (pos[1] + 200) / 2 - 15])
drawCircle(1, "#F0C5D8", "#E499BA", r / 2, pos = [100 + r / 2, 0])
drawCircle(1, "#F0C5D8", "#E59ABB", r / 4, pos = [-50, 100])
drawCircle(1, "#F0C5D8", "#E59ABB", r / 4, pos = [0, 100])
turtle.done()