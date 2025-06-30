import pgzero
import csv
import time
WIDTH=800
isjump=False
gravity=1.5
velocity=0
HEIGHT=575
TILE_SIZE=48
user=Actor('user_standing', (64, 100))
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
    449: 'wooden_block',
    -1610611806: 'sideways_grassblock',
    -1073740894: 'upsidedown_grassblock',
    1610613666: 'upsidedown_grassblock'
}
map=load_level('level1.csv')
def draw_map(map):
    for x in range(len(map[0])):
        for y in range(len(map)):
            img=blocks.get(map[y][x])
            if img:
                screen.blit(img, (x*TILE_SIZE-camera_x, y*TILE_SIZE-camera_y))
def draw():
    global camera_x, camera_y
    screen.clear()
    screen.blit('background', (0, 0))
    draw_map(map)
    screen.blit(user.image, (user.x - user.width // 2 - camera_x, user.y - user.height // 2 - camera_y))
def collide(x, y):
    try:
        return blocks.get(map[int(y/TILE_SIZE)][int(x/TILE_SIZE)])
    except:
        return None
def update():
    global isjump, velocity, gravity, camera_x, camera_y
    if keyboard.LEFT or keyboard.RIGHT:
        user.image='user_running'
        if keyboard.LEFT and collide(user.x-25, user.y) == None:
            user.x-=5
        elif keyboard.RIGHT and collide(user.x+25, user.y) == None:
            user.x+=5
    else:
        user.image='user_standing'
    if isjump:
        user.image='user_jumping'
    velocity += gravity
    next_y = user.y + velocity
    if collide(user.x, next_y + user.height // 2):
        isjump = False
        velocity = 0
        tile_y = int((next_y+user.height//2 + user.height // 2) // TILE_SIZE)
        user.y = tile_y * TILE_SIZE - user.height // 2
    else:
        user.y = next_y
    if collide(user.x, user.y):
        user.x-=20
    camera_x = max(0, min(int(user.x - WIDTH // 2), len(map[0]) * TILE_SIZE - WIDTH))
    camera_y = max(0, min(int(user.y - HEIGHT // 2), len(map) * TILE_SIZE - HEIGHT))
def on_key_down(key):
    global velocity, isjump, can_jump
    if key==keys.UP and can_jump:
        global isjump
        velocity=-20
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
    print(pos)