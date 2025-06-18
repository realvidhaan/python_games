import pgzrun
from random import randint
WIDTH=400
HEIGHT=400
score=0
game_over=False
fox=Actor('fox')
coin=Actor('coin')
restart=Actor('restart_resized')
exit_=Actor('exit_pink')
fox.pos=100, 100
coin.pos=200, 200
def draw():
    global game_over
    screen.fill('green')
    fox.draw()
    coin.draw()
    if not game_over:
        screen.draw.text(f'Score: {score}', color='black', topleft=(10, 10))
    else:
        screen.fill('red')
        exit_.draw()
        restart.draw()
        screen.draw.text(f'Final Score: {score}', color='black', fontsize=50, center=(HEIGHT//2, WIDTH//2+100))
def place_coin():
    coin.x=randint(10, WIDTH-10)
    coin.y=randint(10, HEIGHT-10)
def place_buttons():
    restart.x=230
    restart.y=200
    exit_.x=130
    exit_.y=200
def time_up():
    global game_over
    game_over=True
    place_buttons()
def update():
    global score
    if keyboard.left:
        fox.x-=2
    elif keyboard.right:
        fox.x+=2
    elif keyboard.up:
        fox.y-=2
    elif keyboard.down:
        fox.y+=2
    fox.x = max(fox.width // 2, min(WIDTH - fox.width // 2, fox.x))
    fox.y = max(fox.height // 2, min(HEIGHT - fox.height // 2, fox.y))
    if fox.collidepoint(coin.pos):
        score+=1
        place_coin()
def on_mouse_down(pos):
    global game_over
    global score
    if game_over:
        if exit_.collidepoint(pos):
            exit()
        elif restart.collidepoint(pos):
            score=0
            place_coin()
            game_over=False
            clock.schedule(time_up, 10)
place_coin()
clock.schedule(time_up, 10)
pgzrun.go()
