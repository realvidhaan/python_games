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
offset= 0
grid=[[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
frame_count = 0
tetrominoes = {
    'purple': [[1, 1, 1, 1]],
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
blocks_on_screen = [{'shape': choice(list(tetrominoes.values())), 'offset': offset, 'start': start}]
curr_block=curr_block = blocks_on_screen[-1]
music.set_volume(0.2)
music.play('background_music')
def draw():
    global score, game_over, blocks_on_screen, curr_block, start, offset, CELL_SIZE, grid
    screen.clear()
    if game_over:
        screen.draw.text("Game Over\nPress ESC", center=(WIDTH//2, HEIGHT//2), fontsize=100, color='red')
    else:
        for block in blocks_on_screen[:]:
            if any((block['offset']+r) in lst for r in range(len(block['shape']))):
                blocks_on_screen.remove(block)
        for block in blocks_on_screen:
            for row in range(len(block['shape'])):
                for i in range(len(block['shape'][row])):
                    if block['shape'][row][i]==1:
                        screen.draw.filled_rect(Rect(block['start']+i*CELL_SIZE, (block['offset']+row)*CELL_SIZE, CELL_SIZE, CELL_SIZE), next(k for k, v in tetrominoes.items() if v == block['shape']))
        for col in range(GRID_WIDTH):
            for row in range(GRID_HEIGHT):
                screen.draw.rect(Rect(col*CELL_SIZE, row*CELL_SIZE, CELL_SIZE, CELL_SIZE), (35, 35, 35))
        screen.draw.text(f"Score: {score}", topleft=(10, 10), fontsize=50, color='white')
def update():
    global game_over, blocks_on_screen, curr_block, start, score, offset, frame_count, CELL_SIZE, grid
    frame_count += 1
    if frame_count%15==0:
        if curr_block['offset'] >= GRID_HEIGHT - len(curr_block['shape']) or check_collision(curr_block, curr_block['offset']+1, curr_block['start']):
            for row in range(len(curr_block['shape'])):
                for col in range(len(curr_block['shape'][row])):
                    if curr_block['shape'][row][col] == 1:
                        grid[curr_block['offset']+row][(curr_block['start']//CELL_SIZE)+col] = 1
            if any(grid[0][col] == 1 for col in range(GRID_WIDTH)):
                game_over = True
                return
            new_shape = choice(list(tetrominoes.values()))
            max_start = GRID_WIDTH - len(new_shape[0])
            start = randint(0, max_start) * CELL_SIZE
            blocks_on_screen.append({'shape': new_shape, 'offset': offset, 'start': start})
            curr_block = blocks_on_screen[-1]
            curr_block['offset'] = offset
            if check_collision(curr_block, curr_block['offset'], curr_block['start']):
                game_over = True
                return
        else:
            curr_block['offset'] += 1
    curr_block['offset'] = min(curr_block['offset'], GRID_HEIGHT - len(curr_block['shape']))
    if game_over:
        music.stop()
        sounds.game_over.set_volume(0.02)
        sounds.game_over.play()
    for block in blocks_on_screen:
        count=0
        for row in lst:
            if row >= block['offset'] and row < block['offset'] + len(block['shape']):
                count+=1
        block['offset']+=count
def on_key_down(key):
    global game_over, blocks_on_screen, curr_block, offset, start, score, CELL_SIZE, grid
    if game_over and key==keys.ESCAPE:
        game_over = False
        score = 0
        offset = 0
        grid=[[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        new_shape = choice(list(tetrominoes.values()))
        max_start = GRID_WIDTH - len(new_shape[0])
        start = randint(0, max_start) * CELL_SIZE
        blocks_on_screen=[{'shape': new_shape, 'offset': offset, 'start': start}]
        curr_block = blocks_on_screen[-1]
        music.play('background_music')
    else:
        if curr_block['offset']< GRID_HEIGHT - len(curr_block['shape']):
            new_start = curr_block['start']
            if key==keys.RIGHT:
                new_start += CELL_SIZE
            elif key==keys.LEFT:
                new_start -= CELL_SIZE
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
                if grid[grid_row][grid_col] == 1:
                    return True
    return False
def reset():
    music.set_volume(0.2)
def clear_full_rows():
    global grid, score, lst
    new_grid = []
    for row in range(GRID_HEIGHT-1, -1, -1):
        if all(grid[row][col] == 1 for col in range(GRID_WIDTH)):
            music.set_volume(0.025)
            clock.schedule_unique(reset, 0.02)
            sounds.lineclear.set_volume(1)
            sounds.lineclear.play()
            lst.append(row)
            score += 1
        else:
            new_grid.insert(0, grid[row])
    while len(new_grid) < GRID_HEIGHT:
        new_grid.insert(0, [0 for _ in range(GRID_WIDTH)])
    grid=new_grid
clock.schedule_interval(clear_full_rows, 0.01)