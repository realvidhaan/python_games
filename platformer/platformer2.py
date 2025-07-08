import pgzero
import csv
import pyganim
import pygame
import os
import sys
WIDTH=800
isjump=False
spe=3.5
gliding=False
show_umbrella=True
draw_blob=True
umbrella=Actor('umbrella', (1315, 97))
opaqueness=0
resetting=False
fading=False
trophy=Actor('trophy', (2340, 296))
platform=Actor('platform', (490, 480))
draw_trophy=False
exploding=False
draw_coin=False
text = [('black_text.png', 300), ('blue_text.png', 300)]
text_anim = pyganim.PygAnimation(text)
text_anim.play()
frames = [('sprite ({})-modified.png'.format(i), 50) for i in range(1, 12)]
anim=pyganim.PygAnimation(frames, loop=False)
exploding=False
exploding_pos=(0, 0)
gravity=1.5
can_bounce=True
speed=1
score=0
velocity=0
blob=Actor('blob', (920, 243))
coins=[('frame_{:02d}_delay-0.08s.gif'.format(i), 50) for i in range(0, 10)]
coins_anim=pyganim.PygAnimation(coins, loop=True)
show_text=False
HEIGHT=575
TILE_SIZE=48
health=100 
user=Actor('user_standing', (64, 111))
can_jump=True
camera_x = user.x - WIDTH // 2
camera_y = user.y - HEIGHT // 2
coins_anim.play()
def load_level(file):
    with open(file) as f:
        reader = csv.reader(f)
        return [list(map(int, row)) for row in reader]
blocks={
    -1: None,
    930: 'grass_block',
    962: 'dirt_block',
    448: 'wooden_block',
    -1610611806: 'sideways_grassblock',
    -1073740894: 'upsidedown_grassblock',
    1610613666: 'upsidedown_grassblock',
    -1073741824: 'upsidedown_spike',
    0: 'spike',
    1: 'ladder',
    -536870912: 'sideways_spike',

}
map=load_level('level2.csv')
def draw_map(map):
    for x in range(len(map[0])):
        for y in range(len(map)):
            img=blocks.get(map[y][x])
            if img:
                screen.blit(img, (x*TILE_SIZE-camera_x, y*TILE_SIZE-camera_y))
def draw():
    global camera_x, camera_y, health, draw_blob, draw_coin, exploding, exploding_pos, score
    screen.clear()
    screen.blit('background', (0, 0))
    draw_map(map)
    if exploding:
        blob.pos=(-1000, -1000)
        anim.blit(screen.surface, (exploding_pos[0] - camera_x, exploding_pos[1] - camera_y))
    if draw_coin:
        coins_anim.blit(screen.surface, (1011 - camera_x, 229 - camera_y))
    if draw_blob:
        screen.blit(blob.image, (blob.x - camera_x, blob.y - camera_y))
    screen.draw.rect(Rect((10, 10), (150, 20)), 'grey')
    screen.blit(user.image, (user.x - user.width // 2 - camera_x, user.y - user.height // 2 - camera_y))
    if health>50:
        screen.draw.filled_rect(Rect((10, 10, int(150*health/100), 20)), 'green')
    elif 20<health<=50:
        screen.draw.filled_rect(Rect((10, 10, int(150*health/100), 20)), 'yellow')
    else:
        screen.draw.filled_rect(Rect((10, 10, int(150*health/100), 20)), 'red')
    y = 5
    start_x = 180
    spacing = 40
    count = 10
    for i in range(score):
        x = start_x + i * spacing
        screen.blit('coin', (x, y))
    if show_text:
        text_anim.blit(screen.surface, (380-camera_x, 250-camera_y))
    if draw_trophy:
        screen.blit(trophy.image, (2340-camera_x, 296-camera_y))
    if fading:
        fade_surface = pygame.Surface((WIDTH, HEIGHT))
        fade_surface.fill((0, 0, 0))
        fade_surface.set_alpha(opaqueness)  
        screen.surface.blit(fade_surface, (0, 0))
    screen.blit(platform.image, (platform.x-camera_x, platform.y-camera_y))
    if show_umbrella:
        screen.blit(umbrella.image, (umbrella.x-camera_x, umbrella.y-camera_y))
def collide(x, y):
    try:
        return blocks.get(map[int(y/TILE_SIZE)][int(x/TILE_SIZE)])
    except:
        return None
def update():
    global isjump, velocity, gravity, camera_x, camera_y, spe, can_jump, can_bounce, health, exploding, resetting, exploding_pos, speed, draw_blob, draw_coin, score, can_bounce, show_text, draw_trophy, fading, opaqueness, fading, health, draw_blob, draw_coin, draw_trophy, sign, coins_anim, blob, anim, text_anim, trophy, draw_blob, draw_coin, draw_trophy, sign, coins_anim, blob, anim, text_anim, trophy, platform, gliding, show_umbrella
    if keyboard.LEFT or keyboard.RIGHT:
        if keyboard.LEFT and collide(user.x-25, user.y) in [None, 'spike', 'upsidedown_spike', 'sideways_spike', 'ladder']:
            user.image='user_running_left'
            user.x-=5
        elif keyboard.RIGHT and collide(user.x+25, user.y) in [None, 'spike', 'upsidedown_spike', 'sideways_spike', 'ladder']:
            user.image='user_running' 
            user.x+=5
    else:
        user.image='user_standing'
    if isjump:
        user.image='user_jumping'
    velocity += gravity
    next_y = user.y + velocity
    if velocity < 0 and collide(user.x, next_y - user.height // 2) not in [None, 'spike', 'upsidedown_spike', 'sideways_spike', 'ladder']:
        velocity = 0
        tile_y = int((next_y - user.height // 2) // TILE_SIZE)
        user.y = (tile_y + 1) * TILE_SIZE + user.height // 2
    else:
        user.y = next_y
    foot_left  = collide(user.x - user.width // 4, next_y + user.height // 2)
    foot_right = collide(user.x + user.width // 4, next_y + user.height // 2)
    if foot_left not in [None, 'spike', 'upsidedown_spike', 'sideways_spike', 'ladder'] or foot_right not in [None, 'spike', 'upsidedown_spike', 'sideways_spike', 'ladder']:
        isjump = False
        velocity = 0
        tile_y = int((next_y + user.height // 2) // TILE_SIZE)
        user.y = tile_y * TILE_SIZE - user.height // 2  
    if collide(user.x, next_y + user.height // 2) not in [None, 'spike', 'upsidedown_spike', 'sideways_spike', 'ladder']:
        isjump = False
        velocity = 0
        tile_y = int((next_y+user.height//2 + user.height // 2) // TILE_SIZE)
        user.y = tile_y * TILE_SIZE - user.height // 2
    elif collide(user.x, next_y+user.height//2) in ['spike', 'upsidedown_spike', 'sideways_spike']:
        sounds.damage.play(maxtime=1000)
        user.y=next_y
        health-=5
    else:
        user.y = next_y
    camera_x = max(0, min(int(user.x - WIDTH // 2), len(map[0]) * TILE_SIZE - WIDTH))
    camera_y = max(0, min(int(user.y - HEIGHT // 2), len(map) * TILE_SIZE - HEIGHT))
    blob.x+=speed
    if blob.x<=920 or blob.x>=1060:
        speed*=-1
    if user.y - velocity + user.height // 2 <= blob.top and user.y + user.height // 2 >= blob.top and user.right > blob.left and user.left < blob.right and velocity > 0:                                      
        sounds.explosion.play()
        velocity=-10
        draw_blob=False
        exploding_pos=blob.pos
        exploding=True
        anim.play()
        clock.schedule(show_coin, 0.5)
    elif user.collidepoint(blob.pos):
        sounds.damage.play(maxtime=1000)
        health-=1
    if draw_coin and abs(user.x-1011)<10:
        sounds.coin.play()
        draw_coin=False
        score+=1
    if user.x + user.width // 2 >= (len(map[0]) * TILE_SIZE)-18:
        user.x = (len(map[0]) * TILE_SIZE - user.width // 2)-18
    if score==1:
        draw_trophy=True
    if (user.top>HEIGHT or health==0) and not fading and not resetting:
       fading=True
       resetting=True
       clock.schedule(reset, 1)
    if fading:
        if opaqueness<255:
            opaqueness+=5
        else:
            fading=False
            opaqueness=0
    platform.y += spe 
    if platform.y >= 490 or platform.y <= 100:
        spe *= -1
    if user.bottom + velocity >= platform.top and user.top < platform.top and user.right > platform.left+70 and user.left < platform.right+30 and velocity > 0:
        user.bottom = platform.top+20
        velocity = 0
        isjump = False
        can_jump = True
    if user.colliderect(umbrella):
        sounds.power_up.play()
        show_umbrella=False
        umbrella.pos=(-1000, -1000)
        gliding=True
    if gliding and keyboard.SPACE and velocity>0:
        user.image='user_gliding'
        gravity=0.1
    else:
        gravity=1.5
    if collide(user.x, user.y+user.height//2)=='ladder' and keyboard.UP:
        user.y-=50
        gravity=0
def show_coin():
    global draw_coin
    draw_coin=True
def can_bounce_true():
    global can_bounce
    can_bounce=True
def on_key_down(key):
    global velocity, isjump, can_jump, gliding, gravity
    if key==keys.UP and can_jump:
        sounds.jump.play()
        velocity=-22
        isjump=True
        can_jump=False
        clock.schedule(stop_can_jump, 0.5)
def stop_can_jump():
    global can_jump
    can_jump=True
def stop_jump():
    global isjump
    isjump=False
def on_mouse_down(pos):
    global camera_x, camera_y
    world_x = pos[0] + camera_x
    world_y = pos[1] + camera_y
    print("World coordinates:", world_x, world_y)
def reset():
    global camera_x, camera_y, health, draw_blob, draw_coin, exploding, exploding_pos, score, draw_trophy, fading, opaqueness, isjump, can_jump, text, text_anim, anim, sign, gravity, can_bounce, speed, blob, coins, coins_anim, show_text, user, velocity, resetting, gliding, show_umbrella
    opaqueness=0
    show_umbrella=True
    isjump=False
    draw_blob=True
    trophy.pos=(2340, 296)
    draw_trophy=False
    resetting=True
    umbrella.pos=(1315, 97)
    gliding=False
    exploding=False
    draw_coin=False
    text = [('black_text.png', 300), ('blue_text.png', 300)]
    text_anim = pyganim.PygAnimation(text)
    text_anim.play()
    frames = [('sprite ({})-modified.png'.format(i), 50) for i in range(1, 12)]
    anim=pyganim.PygAnimation(frames, loop=False)
    exploding=False
    exploding_pos=(0, 0)
    gravity=1.5
    can_bounce=True
    speed=1
    score=0
    velocity=0
    coins=[('frame_{:02d}_delay-0.08s.gif'.format(i), 50) for i in range(0, 10)]
    coins_anim=pyganim.PygAnimation(coins, loop=True)
    show_text=False
    health=100 
    user.pos=(64, 111)
    can_jump=True
    camera_x = user.x - WIDTH // 2
    camera_y = user.y - HEIGHT // 2
    coins_anim.play()
    resetting=False
    blob.pos=(920, 243)
music.set_volume(1)
music.play('m')