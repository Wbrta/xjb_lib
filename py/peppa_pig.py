import turtle
import time

turtle.pensize(4)
turtle.pencolor("pink")

turtle.fillcolor("#E699BB")

turtle.begin_fill()

turtle.penup()
turtle.goto(-200, 200)

turtle.pendown()
turtle.speed(0)

turtle.right(20)
for _ in range(60):
    turtle.right(1)
    turtle.forward(0.9)
for _ in range(200):
    turtle.right(0.5)
    turtle.forward(0.9)
for _ in range(80):
    turtle.right(1)
    turtle.forward(0.9)
for _ in range(200):
    turtle.right(0.5)
    turtle.forward(0.9)
for _ in range(20):
    turtle.right(1)
    turtle.forward(0.9)

turtle.left(20)
for _ in range(300):
    turtle.right(0.1)
    turtle.forward(0.75)

for _ in range(180):
    turtle.right(0.33)
    turtle.forward(0.75)

for _ in range(900):
    turtle.right(0.2)
    turtle.forward(0.4)

turtle.left(90)
for _ in range(200):
    turtle.right(0.2)
    turtle.forward(0.6)
turtle.end_fill()

turtle.done()