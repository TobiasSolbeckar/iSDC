p = [0.2, 0.2, 0.2, 0.2, 0.2]
world = ['green', 'red', 'red', 'green', 'green']
measurements = ['red', 'green']
motions = [1,1]
pHit = 0.6
pMiss = 0.2
pExact = 0.8
pOvershoot = 0.1
pUndershoot = 0.1

def sense(p, Z):
    q=[]
    for i in range(len(p)):
        hit = (Z == world[i])
        q.append(p[i] * (hit * pHit + (1-hit) * pMiss))
    s = sum(q)
    for i in range(len(q)):
        q[i] = q[i] / s
    return q

def move(p, U):
    q = []
    for i in range(len(p)):
        s = pExact * p[(i-U) % len(p)]
        s = s + pOvershoot * p[(i-U-1) % len(p)]
        s = s + pUndershoot * p[(i-U+1) % len(p)]
        q.append(s)
    return q

for k in range(len(measurements)):
    p = sense(p, measurements[k])
    p = move(p, motions[k])

print(p)


"""
This is code from the Noteboke
"""
from helpers import normalize, blur

def initialize_beliefs(grid):
    height = len(grid)
    width = len(grid[0])
    area = height * width
    belief_per_cell = 1.0 / area
    beliefs = []
    for i in range(height):
        row = []
        for j in range(width):
            row.append(belief_per_cell)
        beliefs.append(row)
    return beliefs

def sense(color, grid, beliefs, p_hit, p_miss):
    height = len(grid)
    width = len(grid[0]) 
    # make sure to get the right dimensions for new_beliefs.    
    new_beliefs = [[0.0 for i in range(width)] for j in range(height)]
    # perform the measurement update
    for row in range(height):
        for col in range(width):
            if grid[row][col] == color:
                new_beliefs[row][col] = beliefs[row][col] * p_hit
            else:
                new_beliefs[row][col] = beliefs[row][col] * p_miss
    # perform the normailization
    norm_factor = 0
    for i in range(len(new_beliefs)):
        norm_factor += sum(new_beliefs[i])
    for i in range(len(new_beliefs)):
        for j in range(len(new_beliefs[i])):
            new_beliefs[i][j] = new_beliefs[i][j]/norm_factor
    return new_beliefs

def move(dy, dx, beliefs, blurring):
    height = len(beliefs)
    width = len(beliefs[0])
    new_G = [[0.0 for k in range(width)] for l in range(height)]
    for i, row in enumerate(beliefs):
        for j, cell in enumerate(row):
            new_i = (i + dy) % height 
            new_j = (j + dx) % width  
            new_G[int(new_i)][int(new_j)] = cell          
    return blur(new_G, blurring)