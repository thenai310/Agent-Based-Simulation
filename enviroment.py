from random import randint,choice,sample,choices
from utils import *

dx = [ 0, 0,-1, 1]
dy = [-1, 1, 0, 0]


class Enviroment:

    def __init__(self, n,m,dirt_percent,obst_percent,kids):
        self.world = []
        self.kids = kids
        self.kidList = []
        self.obs = round(((n*m)*obst_percent)/100)
        self.dirt = round(((n*m)*dirt_percent)/100)
        self.create_world(n,m)

    def initialize(self):
        self.genBabyCradle()
        self.genObstacles()
        self.genKids()
        self.genDirt()
        
    def create_world(self,n,m):
        for i in range(n):
            self.world.append([])
            for _ in range(m):
                self.world[i].append([])
        return self.world

    def genDirt(self):
        dirtList = sample(emptyBoxes(self.world),self.dirt)
        for elem in dirtList:
            self.world[elem[0]][elem[1]].append('*')

    def genKids(self):
        kidsPosList = sample(emptyBoxes(self.world),self.kids)
        for kid in kidsPosList:
            new_kid = Kid(kid,self.world)
            self.kidList.append(new_kid)
            self.world[kid[0]][kid[1]].append('K')
       
    def genBabyCradle(self):
        index = 0
        init_Pos = choice(emptyBoxes(self.world))
        return genBabyCradle_Rec(init_Pos,init_Pos,self.world,self.kids)

    def genObstacles(self):
        obs = self.obs
        while obs > 0:
            pos = choice(emptyBoxes(self.world))
            self.world[pos[0]][pos[1]].append('|')
            if is_connected(self.world):
                obs -= 1
            else:
                self.world[pos[0]][pos[1]].pop()

class Kid:
    def __init__(self,pos,world):
        self.pos = pos
        self.world = world

    def move(self):
        while True:
            index = randint(0,len(dx) - 1)
            new_pos = (self.pos[0] + dx[index],self.pos[1] + dy[index])
            if in_range(self.world,new_pos):
                if new_pos in emptyBoxes(self.world):
                    self.world[self.pos[0]][self.pos[1]].remove('K')
                    self.pos = new_pos
                    self.world[self.pos[0]][self.pos[1]].append('K')
                    break
                elif '|' in self.world[new_pos[0]][new_pos[1]]:
                    temp = new_pos
                    self.world[new_pos[0]][new_pos[1]].remove('|')
                    while True:
                        new_pos2 = (new_pos[0] + dx[index],new_pos[1] + dy[index])
                        if in_range(self.world,new_pos2):
                            if new_pos2 in emptyBoxes(self.world):
                                self.world[self.pos[0]][self.pos[1]].remove('K')
                                self.pos = temp
                                self.world[self.pos[0]][self.pos[1]].append('K')
                                self.world[new_pos2[0]][new_pos2[1]].append('|')
                                break
                            elif '|' in self.world[new_pos2[0]][new_pos2[1]]:
                                new_pos = new_pos2
                            else:
                                self.world[temp[0]][temp[1]].append('|')
                                break
                        else:
                            self.world[temp[0]][temp[1]].append('|')
                            break
                    break






class Robot:

    def __init__(self, pos):
        
        self.pos = pos

    def pick_kids(self,world):
        visited = []
        visited.append(self.pos)
        prev = {}
        queue = []
        queue.append(self.pos)
        while len(queue) > 0:
            index = 0 
            pos = queue.pop(0)
            while index < 8:
                new_pos = (pos[0]+dx[index],pos[1]+dy[index])
                if in_range(world,new_pos) and new_pos not in visited:
                    if char in world[new_pos[0]][new_pos[1]]:
                        return new_pos
                    else:
                        queue.append(new_pos)
                        visited.append(new_pos)
                        index+=1
                else:
                    index+=1
        return None



if __name__ == "__main__":

    # env = Enviroment(6,9,20,20,3)
    # env.initialize()
    # robot_pos = choice(emptyBoxes(env.world))
    # env.world[robot_pos[0]][robot_pos[1]].append('R')
    # robot = Robot(robot_pos)
    # print_world(env.world)
    mundillo =  [[['K'],[],['|'],[],[]],[[],[],[],[],[]],[[],[],[],[],[]]]
    print_world(mundillo)
    kid = Kid((0,0),mundillo)
    # robot = Robot((2,2)) 
    # robot.pick_kids(mundillo,1)



