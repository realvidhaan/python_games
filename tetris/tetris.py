import pgzero
from random import choice, randint
from pgzero import music
CELL_SIZE = 40
GRID_WIDTH = 10
GRID_HEIGHT = 15
WIDTH=400
lst=[]
HEIGHT=600
score=0
game_over = False
colors = {
    'violet': (238, 130, 238),
    'blue': (0, 0, 255),
    'green': (0, 255, 0),
    'red': (255, 0, 0),
    'yellow': (255, 255, 0),
    'cyan': (0, 255, 255),
    'orange': (255, 165, 0),
}
color = {
    ((1, 1, 1, 1),): (238, 130, 238),  
    ((0, 1, 0),
     (1, 1, 1)): (0, 0, 255),         
    ((1, 1),
     (1, 0),
     (1, 0)): (0, 255, 0),            
    ((1, 1),
     (1, 1)): (255, 0, 0),            
    ((0, 1, 1),
     (1, 1, 0)): (255, 255, 0),       
    ((1, 0, 0),
     (1, 1, 1)): (0, 255, 255),       
    ((0, 0, 1),
     (1, 1, 1)): (255, 165, 0)        
}
offset= 0
grid=[[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
frame_count = 0
tetrominoes = {
    'violet': [[1, 1, 1, 1]],
    'blue': [[0, 1, 0],
             [1, 1, 1]],
    'green': [[1, 1],
              [1, 0],
              [1, 0]],
    'red': [[1, 1],
            [1, 1]],
    'yellow': [[0, 1, 1],
               [1, 1, 0]],
    'cyan': [[1, 0, 0],
             [1, 1, 1]],
    'orange': [[0, 0, 1],
               [1, 1, 1]],
}
start=randint(0, GRID_WIDTH-10) * CELL_SIZE
s=choice(list(tetrominoes.keys()))
blocks_on_screen = [{'shape': s, 'offset': offset, 'start': start, 'color': color[tuple(tuple(row) for row in tetrominoes[s])]}]
curr_block=curr_block = blocks_on_screen[-1]
curr_block['offset']+=1
music.set_volume(0.2)
music.play('background_music')
def draw():
    global score, game_over, blocks_on_screen, curr_block, start, offset, CELL_SIZE, grid
    screen.clear()
    if game_over:
        screen.draw.text("Game Over\nPress ESC", center=(WIDTH//2, HEIGHT//2), fontsize=100, color='red')
    else:
        for row in range(GRID_HEIGHT):
            for col in range(GRID_WIDTH):
                if grid[row][col] is not None:
                    screen.draw.filled_rect(Rect(col*CELL_SIZE, row*CELL_SIZE, CELL_SIZE, CELL_SIZE), grid[row][col])
        for row in range(len(curr_block['shape'])):
            for i in range(len(curr_block['shape'][row])):
                if curr_block['shape'][row][i]==1:
                    screen.draw.filled_rect(Rect(curr_block['start']+i*CELL_SIZE, (curr_block['offset']+row)*CELL_SIZE, CELL_SIZE, CELL_SIZE), curr_block['color'])
        for col in range(GRID_WIDTH):
            for row in range(GRID_HEIGHT):
                screen.draw.rect(Rect(col*CELL_SIZE, row*CELL_SIZE, CELL_SIZE, CELL_SIZE), (35, 35, 35))
        screen.draw.text(f"Score: {score}", topleft=(10, 10), fontsize=50, color='white')
def update():
    global game_over, blocks_on_screen, curr_block, start, score, offset, frame_count, CELL_SIZE, grid
    if frame_count==0:
        curr_block['offset']+=10
    frame_count += 1
    if frame_count%25==0:
        if curr_block['offset'] >= GRID_HEIGHT - len(curr_block['shape']) or check_collision(curr_block, curr_block['offset']+1, curr_block['start']):
            for row in range(len(curr_block['shape'])):
                for col in range(len(curr_block['shape'][row])):
                    if curr_block['shape'][row][col] ==1:
                        try:
                            grid[curr_block['offset']+row][(curr_block['start']//CELL_SIZE)+col] = curr_block['color']
                        except:
                            pass
            if any(grid[0][col] is not None for col in range(GRID_WIDTH)):
                game_over = True
                return
            new_shape = choice(list(tetrominoes.values()))
            shape_key = tuple(tuple(row) for row in new_shape)
            max_start = GRID_WIDTH - len(new_shape[0])
            start = randint(0, max_start) * CELL_SIZE
            new_block = {'shape': new_shape, 'offset': 0, 'start': start, 'color': color[shape_key]}
            if check_collision(new_block, new_block['offset'], new_block['start']):
                game_over = True
                return
            blocks_on_screen.append(new_block)
            curr_block = new_block
        else:
            curr_block['offset'] += 1
    curr_block['offset'] = min(curr_block['offset'], GRID_HEIGHT - len(curr_block['shape']))
    if game_over:
        music.stop()
        sounds.game_over.set_volume(0.02)
        sounds.game_over.play()
def on_key_down(key):
    global game_over, blocks_on_screen, curr_block, offset, start, score, CELL_SIZE, grid
    if game_over and key==keys.ESCAPE:
        game_over = False
        score = 0
        offset = 0
        grid=[[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        new_shape = choice(list(tetrominoes.values()))
        shape_key = tuple(tuple(row) for row in new_shape)
        blocks_on_screen.append({'shape': new_shape, 'offset': offset, 'start': start, 'color': color[shape_key]})
        max_start = GRID_WIDTH - len(new_shape[0])
        start = randint(0, max_start) * CELL_SIZE
        curr_block = blocks_on_screen[-1]
        music.play('background_music')
    else:
        if curr_block['offset']< GRID_HEIGHT - len(curr_block['shape']):
            new_start = curr_block['start']
            if key==keys.RIGHT:
                new_start += CELL_SIZE
            elif key==keys.LEFT:
                new_start -= CELL_SIZE
            elif key==keys.UP:
                shape = [list(row)[::-1] for row in zip(*curr_block['shape'])]
                if not check_collision({'shape': shape}, curr_block['offset'], curr_block['start']):
                    curr_block['shape'] = shape
            elif key==keys.DOWN:
                if not check_collision(curr_block, curr_block['offset'] + 2, curr_block['start']):
                    curr_block['offset'] += 2
            new_start = max(0, min(new_start, (GRID_WIDTH - len(curr_block['shape'][0])) * CELL_SIZE))
            if not check_collision(curr_block, curr_block['offset'], new_start):
                curr_block['start'] = new_start
def check_collision(block, offset, start):
    global grid, CELL_SIZE
    for row in range(len(block['shape'])):
        for col in range(len(block['shape'][row])):
            if block['shape'][row][col] == 1:   
                grid_row = offset + row
                grid_col = (start // CELL_SIZE) + col
                if grid_row<0 or grid_row>=GRID_HEIGHT or grid_col<0 or grid_col>=GRID_WIDTH:
                    return True
                if grid[grid_row][grid_col] is not None:
                    return True
    return False
def reset():
    music.set_volume(0.2)
def clear_full_rows():
    global grid, score, lst
    new_grid = []
    for row in range(GRID_HEIGHT-1, -1, -1):
        if all(grid[row][col] is not None for col in range(GRID_WIDTH)):
            sounds.lineclear.set_volume(1)
            sounds.lineclear.play()
            lst.append(row)
            score += 1
        else:
            new_grid.insert(0, grid[row])
    while len(new_grid) < GRID_HEIGHT:
        new_grid.insert(0, [None for _ in range(GRID_WIDTH)])
    grid=new_grid
clock.schedule_interval(clear_full_rows, 0.2)
update()