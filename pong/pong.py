import pgzrun
#Vidhaan
WIDTH=400
HEIGHT=400
user=Actor('pad')
opponent=Actor('pad')
restart=Actor('restart_resized')
exit_=Actor('exit_pink')
user.pos=30, HEIGHT//2
opponent.pos=WIDTH-30, HEIGHT//2
ball=Actor('ball_resized')
ball.pos=WIDTH//2, HEIGHT//2
user_score=0
opponent_score=0           
speed_x=3
speed_y=1
opponent_speed=2.25
game_over=False
win=False
def draw():
    global game_over, win
    screen.blit('background', (0, 0))
    user.draw()
    opponent.draw()
    ball.draw()
    if not game_over and not win: 
        screen.draw.text(f'{user_score}   {opponent_score}', centerx=WIDTH//2, top=20, fontsize=80, color='white') 
    elif game_over:
        screen.fill('red')
        place_buttons()
        exit_.draw()
        restart.draw()
        screen.draw.text(f'You Lost :(', color='black', fontsize=50, center=(WIDTH//2, HEIGHT//2-80))
    elif win:
        screen.fill('green')
        place_buttons()
        exit_.draw()
        restart.draw()
        screen.draw.text(f'You Won :)', color='black', fontsize=50, center=(WIDTH//2, HEIGHT//2-80))
def place_buttons():
    restart.x=230
    restart.y=200
    exit_.x=130
    exit_.y=200
def update():
    global speed_x, speed_y, opponent_speed, game_over, win, user_score, opponent_score
    if not game_over and not win:
        if keyboard.up:
            user.y-=3
        elif keyboard.down:
            user.y+=3
        if ball.x>=WIDTH//2+35 and abs(ball.y-opponent.y)>15:
            if ball.y<opponent.y:
                opponent.y-=opponent_speed
            elif ball.y>opponent.y:
                opponent.y+=opponent_speed
        ball.x+=speed_x
        ball.y+=speed_y
        speed_x+=0.01
        speed_y+=0.01
        user.y = max(user.height // 2, min(HEIGHT - user.height // 2, user.y))
        opponent.y = max(opponent.height // 2, min(HEIGHT - opponent.height // 2, opponent.y))
        if ball.colliderect(user):
            speed_x=abs(speed_x)
            ball.left = user.right
        elif ball.colliderect(opponent):
            speed_x=-abs(speed_x)
            ball.right = opponent.left
        speed_y=max(-5, min(speed_y, 5))
        if ball.bottom>=HEIGHT or ball.top<=0:
            speed_y*=-1
        if ball.left<0:
            opponent_score+=1
            ball.pos=WIDTH//2, HEIGHT//2
            speed_x = abs(speed_x)
            speed_y=-speed_y
        elif ball.right>WIDTH:
            user_score+=1
            ball.pos=WIDTH//2, HEIGHT//2
            speed_x = -abs(speed_x)
            speed_y=-speed_y
        if opponent_score==10:
            game_over=True
        elif user_score==10:
            win=True
def on_mouse_down(pos):
    global game_over, win, user_score, opponent_score, speed_x, speed_y
    if game_over or win:
        if exit_.collidepoint(pos):
            exit()
        elif restart.collidepoint(pos):
            ball.pos=WIDTH//2, HEIGHT//2
            speed_x=abs(speed_x)
            speed_y=abs(speed_y)
            user_score=0
            opponent_score=0
            game_over=False
            win=False
pgzrun.go()
