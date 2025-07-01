import pgzero
import csv
import pyganim
WIDTH=800
isjump=False
draw_blob=True
exploding=False
frames = [('sprite ({}).png'.format(i), 50) for i in range(1, 12)]
anim=pyganim.PygAnimation(frames, loop=False)
exploding=False
exploding_pos=(0, 0)
gravity=1.5
can_bounce=True
speed=1
velocity=0
blob=Actor('blob', (783, 290))
HEIGHT=575
TILE_SIZE=48
health=100 
user=Actor('user_standing', (64, 111))
can_jump=True
camera_x = user.x - WIDTH // 2
camera_y = user.y - HEIGHT // 2
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
    0: 'spike'
}
map=load_level('level1.csv')
def draw_map(map):
    for x in range(len(map[0])):
        for y in range(len(map)):
            img=blocks.get(map[y][x])
            if img:
                screen.blit(img, (x*TILE_SIZE-camera_x, y*TILE_SIZE-camera_y))
def draw():
    global camera_x, camera_y, health, draw_blob
    screen.clear()
    screen.blit('background', (0, 0))
    draw_map(map)
    if exploding:
        blob.pos=(0, 0)
        anim.blit(screen.surface, (exploding_pos[0] - camera_x, exploding_pos[1] - camera_y))
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
def collide(x, y):
    try:
        return blocks.get(map[int(y/TILE_SIZE)][int(x/TILE_SIZE)])
    except:
        return None
def update():
    global isjump, velocity, gravity, camera_x, camera_y, can_jump, can_bounce, health, exploding, exploding_pos, speed, draw_blob
    if keyboard.LEFT or keyboard.RIGHT:
        if keyboard.LEFT and collide(user.x-25, user.y) in [None, 'spike', 'upsidedown_spike']:
            user.image='user_running_left'
            user.x-=5
        elif keyboard.RIGHT and collide(user.x+25, user.y) in [None, 'spike', 'upsidedown_spike']:
            user.image='user_running'
            user.x+=5
    else:
        user.image='user_standing'
    if isjump:
        user.image='user_jumping'
    velocity += gravity
    next_y = user.y + velocity
    if velocity < 0 and collide(user.x, next_y - user.height // 2) not in [None, 'spike', 'upsidedown_spike']:
        velocity = 0
        tile_y = int((next_y - user.height // 2) // TILE_SIZE)
        user.y = (tile_y + 1) * TILE_SIZE + user.height // 2
    else:
        user.y = next_y
    if collide(user.x, next_y + user.height // 2) not in [None, 'spike', 'upsidedown_spike']:
        isjump = False
        velocity = 0
        tile_y = int((next_y+user.height//2 + user.height // 2) // TILE_SIZE)
        user.y = tile_y * TILE_SIZE - user.height // 2
    elif collide(user.x, next_y+user.height//2) in ['spike', 'upsidedown_spike']:
        user.y=next_y
        health-=5
    else:
        user.y = next_y
    camera_x = max(0, min(int(user.x - WIDTH // 2), len(map[0]) * TILE_SIZE - WIDTH))
    camera_y = max(0, min(int(user.y - HEIGHT // 2), len(map) * TILE_SIZE - HEIGHT))
    blob.x+=speed
    if blob.x<=760 or blob.x>=920:
        speed*=-1
    if user.y - velocity + user.height // 2 <= blob.top and user.y + user.height // 2 >= blob.top and user.right > blob.left and user.left < blob.right and velocity > 0:                                      
        velocity=-10
        draw_blob=False
        exploding_pos=blob.pos
        exploding=True
        anim.play()
    elif user.right > blob.left and user.left < blob.right and abs(user.centery - blob.centery) < (user.height // 2):
        health-=1
def can_bounce_true():
    global can_bounce
    can_bounce=True
def on_key_down(key):
    global velocity, isjump, can_jump
    if key==keys.UP and can_jump:
        global isjump
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