import random as rd

dx = [ 0, 0,-1, 1]
dy = [-1, 1, 0, 0]

def emptyBoxes(world):
    emptyPos = []
    for row in range(len(world)):
        for box in range(len(world[row])):
            if len(world[row][box]) == 0:
                emptyPos.append((row,box))
    return emptyPos

def in_range(world,pos): 
    if pos[0]<0 or pos[1]<0:
        return False
    elif pos[0]>= len(world) or pos[1]>= len(world[pos[0]]):
        return False
    else:
        return True

def is_connected(world):
    init_Pos = rd.choice(emptyBoxes(world))
    visted = []
    visted.append(init_Pos)
    queue = []
    queue.append(init_Pos)
    while len(queue)>0:
        pos = queue.pop()
        index = 0
        while index<4:
            new_pos = (pos[0]+dx[index],pos[1]+dy[index])
            if in_range(world,new_pos) and new_pos in emptyBoxes(world) and new_pos not in visted:
                visted.append(new_pos)
                queue.append(new_pos)
            index+=1
    if len(visted) == len(emptyBoxes(world)):
        return True
    else:
        return False

def genBabyCradle_Rec(ipos,pos,world,kids):
    if kids == 0: 
        return world 
    else:
        world[pos[0]][pos[1]].append('C')
        pkids = kids - 1
        index = 0
        while index<4:
            new_pos = (pos[0]+dx[index],pos[1]+dy[index])
            if in_range(world,new_pos) and new_pos in emptyBoxes(world):
                return genBabyCradle_Rec(ipos,new_pos,world,pkids)
            else:
                index+=1
        return genBabyCradle_Rec(ipos,ipos,world,kids)

def walkable_path(char,ipos,world):

    path = []
    visited = []
    prev = {}
    prev[ipos] = (-1,-1)
    queue = [ipos]
    while len(queue) > 0:
        index = 0 
        pos = queue.pop(0)
        if char == 'K':
            if char in world[pos[0]][pos[1]] and 'C' not in world[pos[0]][pos[1]]:
                break
        elif char == 'C':
            if char in world[pos[0]][pos[1]] and 'K' not in world[pos[0]][pos[1]]:
                break
        else:
            if char in world[pos[0]][pos[1]]:
                break
        visited.append(pos)
        for index in range(len(dx)):
            new_pos = (pos[0]+dx[index],pos[1]+dy[index])
            if in_range(world,new_pos) and new_pos not in visited \
                and '|' not in world[new_pos[0]][new_pos[1]] and \
                not('K' in world[new_pos[0]][new_pos[1]] and \
                'C' in world[new_pos[0]][new_pos[1]]):
                queue.append(new_pos)
                prev[new_pos] = pos
    path.append(pos)
    while True:
        pos = prev[pos]
        if pos == ipos:
            break
        path.insert(0,pos)        
    return path


def print_world(world):
    for row in world:
        for box in row:
            if len(box) == 0:
                print(' ',end='__')
            else:
                print(box[-1],end= '__')
        print("\n")   

def near(pos,char,world):
    adyacents = []
    ndx = [-1, 0, 1, 0,-1, 1,-1, 1]
    ndy = [ 1,-1,-1, 1, 1, 1, 0, 0]  
    for index in range(8):
        ady = (pos[0]+ndx[index],pos[1]+ndy[index])
        if char == ' ':
            if in_range(world,ady) and len(world[ady[0]][ady[1]]) == 0:
                adyacents.append(ady)
        else:
            if in_range(world,ady) and char in world[ady[0]][ady[1]]:
                adyacents.append(ady)
    return adyacents