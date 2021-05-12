import turtle
import random

KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_PAUSE = "Up", "Down", "Left", "Right", "space"
SIZE = 20
FONT_1 = ("Arial", 12, "normal")
FONT_2 = ("Arial", 14, "normal")
stamp_ids = []
foods_pos = []
snake_body = []
snake_heading = 0
# status
contact_num = 0
play_time = 0
counter = 0

x_border = 250
y_border = 210
snake_move_time = 400
monster_move_time = 0
motion = "Paused"
tmp_motion = ""
state = "run"
is_paused_by_space = False
is_game_over = False
is_death = False
is_clicked = False
g_snake = None
g_monster = None
g_screen = None
g_introduction = None
g_statusbar = None
g_notice = turtle.Turtle()
g_notice.hideturtle()

# food
num_one = None
num_two = None
num_three = None
num_four = None
num_five = None
num_six = None
num_seven = None
num_eight = None
num_nine = None


def configureScreen(w=660, h=740):
    s = turtle.Screen()
    s.setup(w, h)
    s.title("Snake by Pan Tao")
    s.tracer(0)
    return s


def configureBoundary():
    border_tur = turtle.Turtle()
    border_tur.speed(0)
    border_tur.hideturtle()
    border_tur.color("black")
    border_tur.penup()
    border_tur.goto(-250, 300)
    border_tur.pendown()
    border_tur.goto(250, 300)
    border_tur.goto(250, -310)
    border_tur.goto(-250, -310)
    border_tur.goto(-250, 300)
    border_tur.penup()
    border_tur.goto(-250, 230)
    border_tur.pendown()
    border_tur.goto(250, 230)


def configureFood(textnum):
    global foods_pos
    food = turtle.Turtle()
    food.hideturtle()
    food.speed(0)
    food.color("black")
    food.penup()
    x = random.randint(-x_border, x_border)
    y = random.randint(-y_border, y_border)
    food.goto(x, y)
    foods_pos.append((x, y))
    food.write(textnum, font=FONT_1)
    return food


def checkForFoods(foods_pos):
    num = 0
    for i in range(len(foods_pos)):
        if g_snake.distance(foods_pos[i]) < 20:
            num = i+1
            if num == 1:
                num_one.undo()
            elif num == 2:
                num_two.undo()
            elif num == 3:
                num_three.undo()
            elif num == 4:
                num_four.undo()
            elif num == 5:
                num_five.undo()
            elif num == 6:
                num_six.undo()
            elif num == 7:
                num_seven.undo()
            elif num == 8:
                num_eight.undo()
            else:
                num_nine.undo()
    return num


def configureStatusBar():
    status_bar = turtle.Turtle()
    status_bar.speed(0)
    status_bar.hideturtle()
    status_bar.penup()
    status_bar.goto(-220, 245)
    status_bar.write("Contact: {}   Time: {}   Motion: {}".format(
        contact_num, play_time, motion), font=FONT_2)
    return status_bar


def configureIntroduction():
    introduction = turtle.Turtle()
    introduction.speed(0)
    introduction.hideturtle()
    introduction.penup()
    introduction.goto(-220, 100)
    introduction.write("Welcome to Pan Tao's version of Snake Game\n\nYou will use the 4 arrow keys to move the snake around the screen,\n\ntrying to consume all the food items before the monster catches you...\n\nClick anywhere to start the game, have fun!!!", font=FONT_2)
    return introduction


def configureTurtle(shape="square", color="red", x=0, y=0):
    t = turtle.Turtle(shape)
    t.up()
    t.color(color)
    t.goto(x, y)
    return t


def pause():
    global is_paused_by_space
    global motion
    global tmp_motion
    is_paused_by_space = not is_paused_by_space
    if is_paused_by_space == False:
        motion = tmp_motion
    else:
        tmp_motion = motion
        motion = "Paused"
        refresh()


def monsterMoveUp(d=SIZE/2):
    g_monster.setheading(90)
    g_monster.forward(d)
    g_screen.update()


def monsterMoveDown(d=SIZE/2):
    g_monster.setheading(270)
    g_monster.forward(d)
    g_screen.update()


def monsterMoveLeft(d=SIZE/2):
    g_monster.setheading(180)
    g_monster.forward(d)
    g_screen.update()


def monsterMoveRight(d=SIZE/2):
    g_monster.setheading(0)
    g_monster.forward(d)
    g_screen.update()


def moveUp(d=SIZE):
    global snake_heading
    global motion
    if (not is_paused_by_space):
        motion = "Up"
        refresh()
        g_snake.setheading(90)
        snake_heading = 90
        g_screen.update()
    print("Up")


def moveDown(d=SIZE):
    global snake_heading
    global motion
    if (not is_paused_by_space):
        motion = "Down"
        refresh()
        g_snake.setheading(270)
        snake_heading = 270
        g_screen.update()
    print("Down")


def moveLeft(d=SIZE):
    global snake_heading
    global motion
    if (not is_paused_by_space):
        motion = "Left"
        refresh()
        g_snake.setheading(180)
        snake_heading = 180
        g_screen.update()
    print("Left")


def moveRight(d=SIZE):
    global snake_heading
    global motion
    if (not is_paused_by_space):
        motion = "Right"
        refresh()
        g_snake.setheading(0)
        snake_heading = 0
        g_screen.update()
    print("Right")


def refresh():
    g_statusbar.clear()
    g_statusbar.write("Contact: {}   Time: {}   Motion: {}".format(
        contact_num, play_time, motion), font=FONT_2)


def printMessage(str):
    x = g_snake.xcor() - len(str)*3
    y = g_snake.ycor() + 20
    g_finalnotice = turtle.Turtle()
    g_finalnotice.penup()
    g_finalnotice.color("red")
    g_finalnotice.hideturtle()
    g_finalnotice.goto(x, y)
    g_finalnotice.write(str, font=FONT_2)
    return g_finalnotice


def checkForDeath():
    global is_death
    if g_monster.distance(g_snake) < 10:
        is_death = True
        printMessage("Game Over!!!")


def collapse(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    if abs(x1 - x2) <= 10 and abs(y1 - y2) <= 10:
        return True
    return False


def hitBoundary():
    global state, motion
    _x, _y = g_snake.position()
    if not (not ((_x <= -240) and (motion == "Left"))
            and not (
            (_x >= 240) and (motion == "Right"))) \
            or ((_y <= -300) and (motion == "Down"))\
            or ((_y >= 220) and (motion == "Up")):
        state = "hit_boundary"
    else:
        state = "run"


def moveSnake(d=SIZE):
    global is_paused_by_space
    global is_game_over
    global state
    global g_notice
    global snake_move_time
    checkForDeath()
    if is_death == True:
        pass
    hitBoundary()
    if (not is_paused_by_space) and (not is_game_over) and (not is_death) and state == "run":
        g_snake.forward(d)
        index = checkForFoods(foods_pos)
        if index >= 1:
            foods_pos[index-1] = (10000, 10000)
            if foods_pos.count((10000, 10000)) == 9:
                is_game_over = True
                printMessage("You win!!!")
                return
        for _ in range(index):
            extend()
            g_screen.ontimer(g_snake.forward(SIZE), snake_move_time)
        index = 0
        extendSnake(snake_heading)
        g_screen.update()
        snake_move_time += (len(stamp_ids)-6)
        # snake will have a slower and slower move
    elif state == "hit_boundary":
        g_notice = printMessage(
            "Cannot across boundary\nPlease choose another direction!")
        g_screen.ontimer(g_notice.clear(), 1000)
    g_screen.ontimer(moveSnake, snake_move_time)


def extendSnake(direction):
    global snake_body
    g_snake.clearstamp(stamp_ids[0])
    stamp_ids.pop(0)
    snake_body.pop(0)
    color = g_snake.color()
    g_snake.color("blue", "black")
    x, y = g_snake.position()
    snake_body.append((int(x), int(y)))
    stamp_id = g_snake.stamp()
    stamp_ids.append(stamp_id)
    g_snake.setheading(direction)
    g_snake.color(*color)


def moveMonster():
    global counter
    global play_time
    global contact_num
    global monster_move_time
    checkForDeath()
    if is_death == False and is_game_over == False:
        monster_move_time = random.randint(500, 800)
        counter += 1
        if counter % 2 == 0:
            play_time += 1
            refresh()
        angle = g_monster.towards(g_snake)
        if angle >= 45 and angle < 135:
            monsterMoveUp(SIZE)
        elif angle >= 135 and angle < 225:
            monsterMoveLeft(SIZE)
        elif angle >= 225 and angle < 315:
            monsterMoveDown(SIZE)
        else:
            monsterMoveRight(SIZE)
        for i in range(len(snake_body)-1):  # the last pos is the pos of g_snake
            if collapse(g_monster.position(), snake_body[i]):
                contact_num += 1
                refresh()
                break
    g_screen.ontimer(moveMonster, monster_move_time)


def configureKey(s):
    s.onkey(moveUp, KEY_UP)
    s.onkey(moveDown, KEY_DOWN)
    s.onkey(moveLeft, KEY_LEFT)
    s.onkey(moveRight, KEY_RIGHT)
    s.onkey(pause, KEY_PAUSE)
    s.listen()


def onClick(x, y):
    global motion
    global num_one
    global num_two
    global num_three
    global num_four
    global num_five
    global num_six
    global num_seven
    global num_eight
    global num_nine
    global is_clicked  # to ensure onClick function will be called once
    if not is_clicked:
        is_clicked = True
        extend()
        extend()
        extend()
        extend()
        extend()
        extend()
        num_one = configureFood(1)
        num_two = configureFood(2)
        num_three = configureFood(3)
        num_four = configureFood(4)
        num_five = configureFood(5)
        num_six = configureFood(6)
        num_seven = configureFood(7)
        num_eight = configureFood(8)
        num_nine = configureFood(9)
        motion = "Right"
        g_screen.ontimer(moveSnake, 500)
        g_screen.ontimer(moveMonster, 500)
        refresh()
        g_introduction.clear()


def extend(heading=0, dist=SIZE):
    global snake_body
    color = g_snake.color()
    g_snake.color("blue", "black")
    x, y = g_snake.position()
    snake_body.append((int(x), int(y)))
    stamp_id = g_snake.stamp()
    stamp_ids.append(stamp_id)
    g_snake.color(*color)
    g_screen.update()


if __name__ == "__main__":
    g_screen = configureScreen()
    configureBoundary()
    g_statusbar = configureStatusBar()
    g_snake = configureTurtle()
    g_introduction = configureIntroduction()
    g_monster = configureTurtle(color="purple", x=-200, y=-200)
    g_screen.update()
    configureKey(g_screen)
    g_screen.onclick(onClick)
    g_screen.update()
    g_screen.listen()
    g_screen.mainloop()
