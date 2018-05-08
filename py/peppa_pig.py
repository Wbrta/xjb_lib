import turtle
import math

turtle.speed(0)
turtle.pensize(1)
turtle.pencolor("black")

turtle.screensize(600, 800)

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
drawArc(30, 1, 6.68, pos = [-146, 208])
drawArc(15, 1, 0.96)
drawArc(53, 1, 3.6)
drawArc(142, 1, 2.017)
drawArc(46, 1, 2.903)
turtle.left(95)
drawArc(56, 1, 1.952)
pos = turtle.position()
drawArc(45, 1, 0.935)
drawArc(62, 1, 1.078)
turtle.goto(-146, 208)
turtle.end_fill()

turtle.right(40)
drawArc(150, 1, 0.85)
turtle.goto(pos[0], pos[1])

turtle.begin_fill()
turtle.penup()
turtle.goto(1, 177)
turtle.pendown()
turtle.right(90)
drawArc(41, 1, 1.617)
drawArc(177, 1, 0.278)
turtle.left(15)
drawArc(15, 1, 3.409)
turtle.end_fill()

turtle.begin_fill()
turtle.penup()
turtle.goto(58, 146)
turtle.pendown()
turtle.right(180)
drawArc(41, 1, 1.617)
drawArc(177, 1, 0.278)
turtle.left(15)
drawArc(15, 1, 3.409)
turtle.end_fill()

turtle.pencolor("#D94583")
turtle.penup()
turtle.goto(1, -4)
turtle.pendown()
turtle.left(90)
drawArc(180, 1, 0.57)

drawCircle(1, "#F0C5D8", "#C5759A", 26, pos = [-30, 153])
drawCircle(1, "#F0C5D8", "#C5759A", 26, pos = [31, 121])
drawCircle(1, "#C5759A", "#FCFCFA", 14, pos = [-40, 153])
drawCircle(1, "#C5759A", "#FCFCFA", 14, pos = [22, 122])
drawCircle(1, "#FCFCFA", "#241615", 7, pos = [-50, 156])
drawCircle(1, "#FCFCFA", "#241615", 7, pos = [10, 125])
drawCircle(1, "#F0C5D8", "#C5759A", 35, pos = [96, 25])
turtle.done()