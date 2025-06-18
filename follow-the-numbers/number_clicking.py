import pgzrun
from random import randint
WIDTH=400
HEIGHT=400
dots=[]
lines=[]
game_over=False
win=False
next_dot=0
restart=Actor('restart_resized')
exit_=Actor('exit_pink')
for dot in range(0, 10):
    actor=Actor('dot')
    actor.pos=randint(20, WIDTH-20), randint(20, HEIGHT-20)
    dots.append(actor)
def place_buttons():
    restart.x=230
    restart.y=200
    exit_.x=130
    exit_.y=200
def draw():
    global game_over
    global win
    if not win:
        if not game_over:
            screen.clear()
            screen.fill('black')
            number=1
            for dot in dots:
                dot.draw()
                screen.draw.text(str(number), center=(dot.x, dot.y+20))
                number+=1
            for line in lines:
                screen.draw.line(line[0], line[1], (0, 0, 255))
        else:
            screen.fill('red')
            exit_.draw()
            restart.draw()
            screen.draw.text(f'You Lost :(', color='black', fontsize=50, center=(WIDTH//2, HEIGHT//2-80))
    else:
        screen.fill('green')
        exit_.draw()
        restart.draw()
        screen.draw.text(f'You Won :)', color='black', fontsize=50, center=(WIDTH//2, HEIGHT//2-80))  
def on_mouse_down(pos):
    global lines
    global game_over
    global next_dot
    global win
    if not game_over and not win:
        if dots[next_dot].collidepoint(pos):
            if next_dot>0:
                lines.append((dots[next_dot-1].pos, dots[next_dot].pos))
            next_dot+=1
            if next_dot>=len(dots):
                win=True
                place_buttons()
        else:
            place_buttons()
            game_over=True
    else:
        if exit_.collidepoint(pos):
            exit()
        elif restart.collidepoint(pos):
            lines=[]
            next_dot=0
            game_over=False
            win=False
            dots.clear()
            for dot in range(0, 10):
                actor = Actor('dot')
                actor.pos = randint(20, WIDTH - 20), randint(20, HEIGHT - 20)
                dots.append(actor)
pgzrun.go()
