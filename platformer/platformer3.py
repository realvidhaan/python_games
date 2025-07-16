import pgzero
import csv
import pyganim
import pygame
import os
import sys
WIDTH=800
l=False
spring=Actor('spring', (1377, 335))
spike_monster=Actor('spike_monster', (1075, 299))
draw_wing=True
flying_monster=Actor('flying_monster', (722, 430))
wing=Actor('wing', (1520, 163))
sped=2
wingy=False
isjump=False
play_bob=False
draw_blob_2=True
spi=2
frames=[('resized_tile00{}.png'.format(i), 50) for i in range(0, 7)]
bob=pyganim.PygAnimation(frames, loop=False)
coin_x=0
draw_spring=True
coin_y=0
was_on_ladder=False
draw_spike_monster=True
counter=0
spe=3.5
gliding=False
show_umbrella=True
draw_blob=True
umbrella=Actor('umbrella', (1315, 97))
opaqueness=0
resetting=False
fading=False
trophy=Actor('trophy', (2180, 104))
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
blob=Actor('blob', (356, 436))
coins=[('frame_{:02d}_delay-0.08s.gif'.format(i), 50) for i in range(0, 10)]
coins_anim=pyganim.PygAnimation(coins, loop=True)
show_text=False
HEIGHT=575
TILE_SIZE=48
health=100 
user=Actor('user_flying', (64, 111))
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
    1610613666: 'sideways_grassblock_1',
    -1073741824: 'upsidedown_spike',
    0: 'upsidedown_spike',
    1: 'ladder',
    -536870912: 'sideways_spike',
    450: 'wooden_block',
    536871842: 'sideways_grassblock_1',
    -2147482718: 'grass_block',
    -536869982: 'sideways_grassblock',
    1073742754: 'upsidedown_grassblock',

}
map=load_level('level3.csv')
def draw_map(map):
    for x in range(len(map[0])):
        for y in range(len(map)):
            img=blocks.get(map[y][x])
            if img:
                screen.blit(img, (x*TILE_SIZE-camera_x, y*TILE_SIZE-camera_y))
def draw():
    global camera_x, camera_y, health, x, y, draw_blob, draw_coin, exploding, exploding_pos, score
    screen.clear()
    screen.blit('background', (0, 0))
    draw_map(map)
    if exploding:
        anim.blit(screen.surface, (exploding_pos[0] - camera_x, exploding_pos[1] - camera_y))
    if draw_coin:
        coins_anim.blit(screen.surface, (coin_x - camera_x, coin_y - camera_y))
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
        screen.blit(trophy.image, (trophy.x-camera_x, trophy.y-camera_y))
    if fading:
        fade_surface = pygame.Surface((WIDTH, HEIGHT))
        fade_surface.fill((0, 0, 0))
        fade_surface.set_alpha(opaqueness)  
        screen.surface.blit(fade_surface, (0, 0))
    screen.blit(flying_monster.image, (flying_monster.x-camera_x, flying_monster.y-camera_y))
    screen.blit(spike_monster.image, (spike_monster.x-camera_x, spike_monster.y-camera_y))
    if draw_spring:
        screen.blit(spring.image, (spring.x-camera_x, spring.y-camera_y))
    if play_bob:
        bob.blit(screen.surface, (spring.x-camera_x, spring.y-camera_y))
    if draw_wing:
        screen.blit(wing.image, (wing.x-camera_x, wing.y-camera_y))
def collide(x, y):
    try:
        return blocks.get(map[int(y/TILE_SIZE)][int(x/TILE_SIZE)])
    except:
        return None
def update():
    global isjump, velocity, gravity, l, draw_wing, wingy, draw_spring, play_bob, draw_spike_monster, spi, counter, sped, was_on_ladder,camera_x, camera_y, spe, can_jump, can_bounce, health, exploding, resetting, exploding_pos, speed, draw_blob, draw_coin, score, can_bounce, show_text, draw_trophy, fading, opaqueness, fading, health, draw_blob, draw_coin, draw_trophy, sign, coins_anim, blob, anim, text_anim, trophy, draw_blob, draw_coin, draw_trophy, sign, coins_anim, blob, anim, text_anim, trophy, platform, gliding, show_umbrella, coin_x, coin_y, user,  umbrella, draw_spike_monster, spike_monster, draw_blob_2, blob_2
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
    if velocity < 0:
        if collide(user.x, next_y - user.height // 2) in ['spike', 'upsidedown_spike', 'sideways_spike']:
            sounds.damage.play(maxtime=1000)
            user.y = next_y
            health -= 5
        if collide(user.x, user.y + user.height // 2) == 'ladder' and keyboard.UP:
            user.y = next_y
        elif collide(user.x, next_y - user.height // 2) not in [None, 'spike', 'upsidedown_spike', 'sideways_spike', 'ladder']:
            velocity = 0
            tile_y = int((next_y - user.height // 2) // TILE_SIZE)
            user.y = (tile_y + 1) * TILE_SIZE + user.height // 2
        else:
            user.y = next_y
    elif velocity>=0:
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
    if blob.x<=251 or blob.x>=430:
        speed*=-1
    if user.y - velocity + user.height // 2 <= blob.top and user.y + user.height // 2 >= blob.top and user.right > blob.left and user.left < blob.right and velocity > 0:                                      
        sounds.explosion.play()
        velocity=-10
        draw_blob=False
        exploding_pos=blob.pos
        exploding=True
        anim.play()
        coin_x=blob.x
        coin_y=blob.y
        clock.schedule(show_coin, 0.5)
        blob.pos=(-1000, -1000)
    elif user.collidepoint(blob.pos):
        sounds.damage.play(maxtime=1000)
        health-=1
    flying_monster.y-=sped
    if flying_monster.y<=235 or flying_monster.y>=431:
        sped*=-1
    if user.colliderect(flying_monster):
        sounds.damage.play()
        health-=15
    if draw_coin and abs(user.x-coin_x)<10:
        sounds.coin.play()
        draw_coin=False
        score+=1
    if user.x + user.width // 2 >= (len(map[0]) * TILE_SIZE)-18:
        user.x = (len(map[0]) * TILE_SIZE - user.width // 2)-18
    if score==2:
        draw_trophy=True
    if user.top>HEIGHT or health<=0 and not fading and not resetting:
       fading=True
       resetting=True
       clock.schedule(reset, 1)
    if fading:
        if opaqueness<255:
            opaqueness+=5
        else:
            fading=False
            opaqueness=0
    if collide(user.x - user.width // 2, user.y) in ['spike', 'sideways_spike']:
        sounds.damage.play(maxtime=1000)
        health -= 5
    if collide(user.x + user.width // 2, user.y) in ['spike', 'sideways_spike']:
        sounds.damage.play(maxtime=1000)
        health -= 5
    spike_monster.x+=spi
    if spike_monster.x<=981 or spike_monster.x>=1200:
        spi*=-1
    if user.colliderect(spike_monster):
        sounds.damage.play()
        health-=15
    if user.y - velocity + user.height // 2 <= spring.top and user.y + user.height // 2 >= spring.top and user.right > spring.left and user.left < spring.right and velocity > 0:                                      
        sounds.boing.play()
        velocity=-25
        isjump=True
        can_jump=False
        clock.schedule(stop_can_jump, 0.5)
        play_bob=True
        bob.play()
    if bob._state==pyganim.PLAYING:
        draw_spring=False
    else:
        draw_spring=True
    if user.colliderect(wing):
        draw_wing=False
        wing.pos=(-1000, -1000)
        sounds.power_up.play()
        wingy=True
    if wingy and velocity!=0:
        user.image='user_flying'
    if user.x>=1773 and not l:
        coin_x=2304
        coin_y=340
        draw_coin=True
        l=True
def top_touches_bottom(actor_top, actor_bottom):
    vertical_touch = abs(actor_top.top - actor_bottom.bottom) < 5  
    horizontal_overlap = (
        actor_top.right > actor_bottom.left and
        actor_top.left < actor_bottom.right
    )
    return vertical_touch and horizontal_overlap

def show_coin():
    global draw_coin
    draw_coin=True
def can_bounce_true():
    global can_bounce
    can_bounce=True
def on_key_down(key):
    global velocity, isjump, can_jump, gliding, gravity
    if key==keys.UP and can_jump and not wingy:
        sounds.jump.play()
        velocity=-22
        isjump=True
        can_jump=False
        clock.schedule(stop_can_jump, 0.5)
    if wingy and key==keys.UP:
        sounds.flap.play()
        velocity=-20
        isjump=True
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
    global camera_x, camera_y, health, counter, draw_blob, draw_coin, exploding, exploding_pos
    global score, draw_trophy, fading, opaqueness, isjump, can_jump, was_on_ladder
    global text_anim, anim, gravity, can_bounce, speed, coins_anim, show_text
    global user, velocity, resetting, gliding, show_umbrella, blob, coins
    global spike_monster, draw_spike_monster, platform, spe, umbrella
    global blob_2, draw_blob_2, spi, coin_x, coin_y
    global flying_monster, sped
    global l, wingy, draw_wing
    l = False
    wingy = False
    wing.pos = (1520, 163)  # or wherever the original position was
    draw_wing = True
    # Reset visual/game state
    opaqueness = 0
    fading = False
    draw_blob = True
    draw_blob_2 = True
    draw_coin = False
    draw_trophy = False
    exploding = False
    exploding_pos = (0, 0)
    score = 0
    health = 100
    velocity = 0
    gravity = 1.5
    can_jump = True
    isjump = False
    can_bounce = True
    gliding = False
    resetting = False
    show_umbrella = True
    show_text = False
    counter = 0
    was_on_ladder = False

    # Reset user
    user.pos = (64, 111)
    camera_x = user.x - WIDTH // 2
    camera_y = user.y - HEIGHT // 2

    # Reset blob to its initial position
    blob.pos = (356, 436)
    speed = 1

    # Reset blob_2
    blob_2.pos = (2081, 100)
    spi = 3.5

    # ✅ Correct spike monster position
    spike_monster.pos = (1075, 299)
    draw_spike_monster = True

    # Reset flying monster
    flying_monster.pos = (722, 430)
    sped = 2

    # Reset umbrella and platform
    umbrella.pos = (1315, 97)
    platform.pos = (490, 480)
    spe = 3.5

    # Reset coin position
    coin_x = 0
    coin_y = 0

    # Reset animations
    text = [('black_text.png', 300), ('blue_text.png', 300)]
    text_anim = pyganim.PygAnimation(text)
    text_anim.play()

    frames = [('sprite ({})-modified.png'.format(i), 50) for i in range(1, 12)]
    anim = pyganim.PygAnimation(frames, loop=False)

    coins = [('frame_{:02d}_delay-0.08s.gif'.format(i), 50) for i in range(0, 10)]
    coins_anim = pyganim.PygAnimation(coins, loop=True)
    coins_anim.play()
music.play('m')