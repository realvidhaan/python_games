import pgzrun
from random import randint
from pgzero.clock import schedule_unique
WIDTH=800
HEIGHT=600
score=0
apple=Actor("apple")
restart=Actor('restart')
exit_=Actor('exit_pink')
over=False
message=''
def draw():
    global message
    global score
    global over
    if not over:
        screen.clear()
        apple.draw()
        if message:
            screen.draw.text(message, center=(WIDTH//2, HEIGHT//2), fontsize=100, color='white')
        screen.draw.text(f'Score: {score}', topleft=(10, 10), fontsize=50, color='white')
    else:
        screen.clear()
        screen.draw.text('You Lost :(', center=(WIDTH//2, HEIGHT//2+100), fontsize=100, color='white')
        exit_.draw()
        restart.draw()
def clear():
    global message
    message=''
def place_apple():
    apple.x=randint(10, WIDTH-10)
    apple.y=randint(10, HEIGHT-10)
def place_buttons():
    restart.x=340
    restart.y=300
    exit_.x=460
    exit_.y=300
def on_mouse_down(pos):
    global message
    global score
    global over
    if not over:
        if apple.collidepoint(pos):
            message='Good shot!'
            schedule_unique(clear, 0.5)
            score+=1
            place_apple()
        else:
            over=True
            place_buttons()
    else:
        if exit_.collidepoint(pos):
            exit()
        elif restart.collidepoint(pos):
            score=0
            message=''
            place_apple()
            over=False
place_apple()
pgzrun.go()
