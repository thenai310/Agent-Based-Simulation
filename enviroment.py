import random as rd
from utils import *

class Enviroment:

    def __init__(self, n,m,dirt_percent,obst_percent,kids):
        self.world = []
        self.kids = kids
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
        dirtList = rd.sample(emptyBoxes(self.world),self.dirt)
        for elem in dirtList:
            self.world[elem[0]][elem[1]].append('*')

    def genKids(self):
        kidsList = rd.sample(emptyBoxes(self.world),self.kids)
        for elem in kidsList:
            self.world[elem[0]][elem[1]].append('K')
       
    def genBabyCradle(self):
        dx = [-1, 0, 1, 0,-1, 1,-1, 1]
        dy = [ 1,-1,-1, 1, 1, 1, 0, 0]
        index = 0
        # init_Pos = (1,1)
        init_Pos = rd.choice(emptyBoxes(self.world))
        return genBabyCradle_Rec(init_Pos,init_Pos,dx,dy,self.world,self.kids)

    def genObstacles(self):
        obs = self.obs
        while obs > 0:
            pos = rd.choice(emptyBoxes(self.world))
            self.world[pos[0]][pos[1]].append('|')
            if is_connected(self.world):
                obs -= 1
            else:
                self.world[pos[0]][pos[1]].pop()



class Robot:

    def __init__(self, pos):
        
        self.pos = pos

    def pick_kids(self,world):
        kp = closest(self.pos,world,'K')
        world[kp[0]][kp[1]].remove('K')
        while self.pos != kp:
            pos = self.pos
            world[self.pos[0]][self.pos[1]].remove('R')
            if kp[0] > self.pos[0] and '|' not in world[self.pos[0] + 1][self.pos[1]]:
                self.pos = (self.pos[0] + 1,self.pos[1])
            elif kp[0] < self.pos[0] and '|' not in world[self.pos[0] - 1][self.pos[1]]:
                self.pos = (self.pos[0] - 1,self.pos[1])
            else:
                pass
            if kp[1] > self.pos[1] and '|' not in world[self.pos[0]][self.pos[1] + 1]:
                self.pos = (self.pos[0],self.pos[1] + 1)
            elif kp[1] < self.pos[1] and '|' not in world[self.pos[0]][self.pos[1] - 1]:
                self.pos = (self.pos[0],self.pos[1] - 1)
            else:
                pass

            if pos == self.pos:
                if kp[0] > self.pos[0] and '|' not in world[self.pos[0] + 1][self.pos[1] + 1]:
                    self.pos = (self.pos[0] + 1,self.pos[1] + 1)
                elif kp[0] > self.pos[0] and '|' not in world[self.pos[0] + 1][self.pos[1] - 1]:
                    self.pos = (self.pos[0] + 1,self.pos[1] - 1)
                elif kp[0] < self.pos[0] and '|' not in world[self.pos[0] - 1][self.pos[1] + 1]:
                    self.pos = (self.pos[0] - 1,self.pos[1] + 1)
                elif kp[0] < self.pos[0] and '|' not in world[self.pos[0] - 1][self.pos[1] - 1]:
                    self.pos = (self.pos[0] - 1,self.pos[1] - 1)
                
                elif kp[1] > self.pos[1] and '|' not in world[self.pos[0] + 1][self.pos[1] + 1]:
                    self.pos = (self.pos[0] + 1,self.pos[1] + 1)
                elif kp[1] > self.pos[1] and '|' not in world[self.pos[0] - 1][self.pos[1] + 1]:
                    self.pos = (self.pos[0] - 1,self.pos[1] + 1)
                elif kp[1] < self.pos[1] and '|' not in world[self.pos[0] + 1][self.pos[1] - 1]:
                    self.pos = (self.pos[0] + 1,self.pos[1] - 1)
                elif kp[1] < self.pos[1] and '|' not in world[self.pos[0] - 1][self.pos[1] - 1]:
                    self.pos = (self.pos[0] - 1,self.pos[1] - 1)

            world[self.pos[0]][self.pos[1]].append('R')
            print('-----------------------------')
            print_world(world)
            input()


    def clean_dirt(self,world):
        dirt_pos = closest(self.pos,world,'*')
        # side_direction = kid_pos[0]-self.pos[0]
        # vertical_direction = 


if __name__ == "__main__":

    env = Enviroment(6,9,20,20,3)
    env.initialize()
    robot_pos = rd.choice(emptyBoxes(env.world))
    env.world[robot_pos[0]][robot_pos[1]].append('R')
    robot = Robot(robot_pos)
    print_world(env.world)
    input()
    for _ in range(env.kids):
        robot.pick_kids(env.world)
    # mundillo =  [[[],[],['K'],[],[]],[[],[],['|'],[],[]],[[],[],['R'],[],[]]]
    # print_world(mundillo)
    # robot = Robot((2,2)) 
    # robot.pick_kids(mundillo,1)



