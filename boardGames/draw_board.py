
'''
You can test this py script by
$>python3 draw_board.py
which will execute the commands defined in main
The below codes are significantly modified from https://repl.it/@kiman100/Tic-Tac-Toe-with-turtle
'''
import random
import turtle
import math


class Draw():
    def __init__(self, board_size=400):
        turtle.setup(500,500)
        self.board_size = board_size
        self.board_size /= 2
        self.turtle_obj = turtle.Turtle()
        self.draw_board()

    def draw_board(self):
        self.turtle_obj.speed(0)
        self.turtle_obj.pu()
        self.turtle_obj.goto(-self.board_size/2.5,self.board_size)
        self.turtle_obj.pd()
        self.turtle_obj.goto(-self.board_size/2.5,-self.board_size)
        self.turtle_obj.pu()
        self.turtle_obj.goto(self.board_size/2.5,self.board_size)
        self.turtle_obj.pd()
        self.turtle_obj.goto(self.board_size/2.5,-self.board_size)
        self.turtle_obj.pu()
        self.turtle_obj.goto(self.board_size,-self.board_size/2.5)
        self.turtle_obj.pd()
        self.turtle_obj.goto(-self.board_size,-self.board_size/2.5)
        self.turtle_obj.pu()
        self.turtle_obj.goto(self.board_size,self.board_size/2.5)
        self.turtle_obj.pd()
        self.turtle_obj.goto(-self.board_size,self.board_size/2.5)
        self.board_size *=2
        

    def move_cursor_to_cell(self, r_index, c_index):
        self.turtle_obj.pu()
        if(c_index==0):
            self.turtle_obj.setx(-self.board_size/2.7)
        elif(c_index==1):
            self.turtle_obj.setx(0)
        else:
            self.turtle_obj.setx(self.board_size/2.7)
        if(r_index==0):
            self.turtle_obj.sety(self.board_size/2.7)
        elif(r_index==1):
            self.turtle_obj.sety(0)
        else:
            self.turtle_obj.sety(-self.board_size/2.7)

    def drawX(self):
        self.turtle_obj.speed(2)
        self.turtle_obj.back(self.board_size/7)
        self.turtle_obj.left(90)
        self.turtle_obj.forward(self.board_size/7)
        self.turtle_obj.right(135)
        self.turtle_obj.pd()
        self.turtle_obj.forward(math.sqrt(((self.board_size/3.5)**2)*2))
        self.turtle_obj.pu()
        self.turtle_obj.right(135)
        self.turtle_obj.forward(self.board_size/3.5)
        self.turtle_obj.right(135)
        self.turtle_obj.pd()
        self.turtle_obj.forward(math.sqrt(((self.board_size/3.5)**2)*2))
        self.turtle_obj.pu()
        self.turtle_obj.right(45)

    def drawO(self):
        self.turtle_obj.pu()
        self.turtle_obj.speed(3)
        self.turtle_obj.left(90)
        self.turtle_obj.forward(self.board_size/7)
        self.turtle_obj.right(90)
        self.turtle_obj.pd()
        for x in range(36):
            self.turtle_obj.forward(((math.pi*(self.board_size/3.5))/360)*10)
            self.turtle_obj.right(10)

    def draw_a_shape(self, a_marker):
        if a_marker == "X":
            self.drawX()
        else:
            self.drawO()
    def move_and_draw(self, r_index, c_index, a_marker):
        self.move_cursor_to_cell(r_index, c_index)
        self.draw_a_shape(a_marker)

    def write_text(self, astr):
        turtle.speed(0)
        turtle.pu()
        turtle.sety(210)
        turtle.penup()
        turtle.write(astr, True, align="center", font=("Arial", 20, "normal"))
        turtle.hideturtle()
        #turtle.title(astr)
    def exit_on_click(self):
        turtle.exitonclick()
if __name__=="__main__":

    board_size = 400
    dboard= Draw(board_size)
    dboard.move_cursor_to_cell(2, 2)
    dboard.drawO()
    dboard.move_cursor_to_cell(0, 2)
    dboard.drawX()
    turtle.exitonclick()       # this to exit cleanly
    #turtle.mainloop()
