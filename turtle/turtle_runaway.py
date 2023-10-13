# This example is not working in Spyder directly (F5 or Run)
# Please type '!python turtle_runaway.py' on IPython console in your Spyder.
import turtle, random, time, threading


class RunawayGame:
    def __init__(self, canvas, runner, runner2, chaser, catch_radius=40, init_dist=400):
        self.canvas = canvas
        self.runner = runner
        self.runner2 = runner2
        self.chaser = chaser
        self.catch_radius2 = catch_radius ** 2
        # AI blue
        self.runner.shape('turtle')
        self.runner.color('blue')
        self.runner.penup()
        self.runner.setx(random.randint(-350, 350))
        self.runner.sety(random.randint(-350, 350))
        self.runner.setheading(random.randint(0, 360))
        # AI green
        self.runner2.shape('turtle')
        self.runner2.color('green')
        self.runner2.penup()
        self.runner2.setx(random.randint(-350, 350))
        self.runner2.sety(random.randint(-350, 350))
        self.runner2.setheading(random.randint(0, 360))
        # Player
        self.chaser.shape('turtle')
        self.chaser.color('red')
        self.chaser.penup()
        self.chaser.setx(random.randint(-350, 350))
        self.chaser.sety(random.randint(-350, 350))
        self.chaser.setheading(random.randint(0, 360))

        self.drawer = turtle.RawTurtle(canvas)
        self.drawer.hideturtle()
        self.drawer.penup()

        self.board = turtle.RawTurtle(canvas)
        self.board.hideturtle()
        self.board.penup()

        self.gametime = 60

        # blue 잡음

    def is_catch(self):
        p = self.runner.pos()
        q = self.chaser.pos()
        dx, dy = p[0] - q[0], p[1] - q[1]
        return dx ** 2 + dy ** 2 < self.catch_radius2

    # green 잡음
    def is_catch2(self):
        p = self.runner2.pos()
        q = self.chaser.pos()
        dx, dy = p[0] - q[0], p[1] - q[1]
        return dx ** 2 + dy ** 2 < self.catch_radius2

    def start(self, ai_timer_msec=100, total_score=0, blue_num=0, green_num=0):
        self.ai_timer_msec = ai_timer_msec
        self.total_score = total_score
        self.canvas.ontimer(self.step, self.ai_timer_msec)
        self.start_time = time.time()
        self.blue_num = blue_num
        self.green_num = green_num

    def scorepopup(self, color, score, extra):
        print("hit")
        score_turtle = turtle.RawTurtle(self.canvas)
        score_turtle.hideturtle()
        score_turtle.penup()
        # score_turtle.setpos(self.chaser.pos())
        score_turtle.write(f"Get {color} turtle! [{score}+({extra})]", align="center", font=36)
        time.sleep(2)
        score_turtle.clear()

    def step(self):

        self.runner.run_ai(self.chaser)
        self.runner2.run_ai(self.runner)
        self.chaser.run_ai(self.runner)

        if (abs(self.runner.xcor()) > 400 or abs(self.runner.ycor()) > 400):
            self.runner.setheading(self.runner.heading() + 180)
            self.runner.forward(100)

        if (abs(self.runner2.xcor()) > 400 or abs(self.runner2.ycor()) > 400):
            self.runner2.setheading(self.runner2.heading() + 180)
            self.runner2.forward(150)

        if (abs(self.chaser.xcor()) > 410 or abs(self.chaser.ycor()) > 410):
            self.chaser.setheading(self.chaser.heading() + 180)
            self.chaser.forward(100)

        if (abs(self.runner.heading() - self.chaser.heading()) == 180):
            self.runner.setheading(self.runner.heading() + 90)

        if (abs(self.runner2.heading() - self.chaser.heading()) == 180):
            self.runner2.setheading(self.runner2.heading() + 90)

        is_catched = self.is_catch()
        is_catched2 = self.is_catch2()
        # blue 잡음, 10점 추가
        if (is_catched == True):
            self.blue_num += 1
            self.total_score += 10 + self.blue_num
            self.runner.forward(50)
            self.runner.speed_up()
            # threading.Thread(target=self.scorepopup, args=("blue", 10)).start()
            self.scorepopup("Blue", 10, self.blue_num)
        # green 잡음, 20점 추가
        if (is_catched2 == True):
            self.green_num += 1
            self.total_score += 20 + self.green_num * 2
            self.runner2.forward(100)
            self.runner2.speed_up()
            # threading.Thread(target=self.scorepopup, args=("green", 20)).start()
            self.scorepopup("Green", 20, self.green_num * 2)

        # 점수, 시간, 잡은 거북이 표시
        self.drawer.undo()
        self.drawer.penup()
        score = self.total_score
        blue_num = self.blue_num
        green_num = self.green_num
        elapse = time.time() - self.start_time
        self.drawer.setpos(0, 380)
        self.drawer.write(
            f'Time: {self.gametime - elapse + blue_num + green_num:.0f} / Score: {score:.0f} / catch blue : {blue_num:.0f} / catch green : {green_num:.0f} ',
            align="center")


        if self.gametime - elapse + blue_num + green_num <= 0:
            canvas.clear()
            self.board.undo()
            self.board.write(f"Total Score : {score:.0f}\n Blue : {blue_num}\n Green : {green_num}", align="center", font="40")
            return

        self.canvas.ontimer(self.step, self.ai_timer_msec)




class ManualMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

        canvas.onkeypress(lambda: self.forward(self.step_move), 'Up')
        canvas.onkeypress(lambda: self.backward(self.step_move), 'Down')
        canvas.onkeypress(lambda: self.left(self.step_turn), 'Left')
        canvas.onkeypress(lambda: self.right(self.step_turn), 'Right')
        canvas.listen()

    def run_ai(self, opponent):
        pass


class RandomMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=13, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

    def run_ai(self, oppoenent):
        mode = random.randint(0, 2)
        if mode == 0:
            self.forward(self.step_move)
        elif mode == 1:
            self.left(self.step_turn)
        elif mode == 2:
            self.right(self.step_turn)

    def speed_up(self):
        self.step_turn = self.step_turn + 2
        self.step_move = self.step_move + 5


class LessRandomMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

    def run_ai(self, oppoenent):
        mode = random.randint(0, 3)
        if mode == 0:
            self.forward(self.step_move)
        elif mode == 1:
            self.left(self.step_turn)
        elif mode == 2:
            self.right(self.step_turn)
        elif mode == 3:
            self.forward(self.step_move)

    def speed_up(self):
        self.step_turn = self.step_turn + 2
        self.step_move = self.step_move + 2


if __name__ == '__main__':
    canvas = turtle.Screen()
    runner = RandomMover(canvas)  # 블루
    runner2 = LessRandomMover(canvas)  # 그린
    chaser = ManualMover(canvas)

    game = RunawayGame(canvas, runner, runner2, chaser)
    game.start()
    canvas.mainloop()
