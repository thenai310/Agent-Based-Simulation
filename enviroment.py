from random import randint,choice,sample,choices
from utils import *

dx = [ 0, 0,-1, 1]
dy = [-1, 1, 0, 0]


class Enviroment:

    def __init__(self, n,m,dirt_percent,obst_percent,kids):
        self.world = []
        self.amount_kids = kids
        self.kids = []
        self.obs = round(((n*m)*obst_percent)/100)
        self.dirt = round(((n*m)*dirt_percent)/100)
        self.create_world(n,m)

    def initialize(self):
        self.genBabyCradle()
        self.genObstacles()
        self.genKids()
        self.genDirt()
        self.genRobot()
        
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

    def genRobot(self):
        r_pos = choice(emptyBoxes(self.world))
        self.world[r_pos[0]][r_pos[1]].append('R')
        self.robot = Robot(r_pos,self)

    def genKids(self):
        kidsList = sample(emptyBoxes(self.world),self.amount_kids)
        for kid in kidsList:
            new_kid = Kid(kid,self)
            self.kids.append(new_kid)
            self.world[kid[0]][kid[1]].append('K')
       
    def genBabyCradle(self):
        index = 0
        init_Pos = choice(emptyBoxes(self.world))
        return genBabyCradle_Rec(init_Pos,init_Pos,self.world,self.amount_kids)

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

    def __init__(self,pos,env):
        self.pos = pos
        self.world = env.world
        self.env = env
        self.in_cradle = False
        self.in_robot = False

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
                else:
                    break
    
    def kids_around(self):
        k_around = near(self.pos,'K',self.world)
        e_around = near(self.pos,' ',self.world)
        if len(k_around) == 0:
            max_dirt = 1
        elif len(k_around) == 1:
            max_dirt = 3
        elif len(k_around) >= 2:
            max_dirt = 6
        return min(len(e_around),max_dirt),e_around
    
    def add_dirt(self,amount_dirt,e_boxes):
        if self.pos in e_boxes:
            e_boxes.remove(self.pos)
        dirt = randint(0,amount_dirt)
        if len(e_boxes)>= dirt:
            dirtlist = sample(e_boxes,dirt)
            for pos in dirtlist:
                self.world[pos[0]][pos[1]].append('*')
                self.env.dirt += 1
        else:
            pass

class Robot:

    def __init__(self, pos,env):

        self.carrying_kid = False
        self.pos = pos
        self.world = env.world
        self.env = env

    def pick_kids(self):
        path = walkable_path('K',self.pos,self.world)
        self.world[self.pos[0]][self.pos[1]].remove('R')
        self.pos = path.pop(0)
        self.world[self.pos[0]][self.pos[1]].append('R')
        if 'K' in self.world[self.pos[0]][self.pos[1]]:
            self.world[self.pos[0]][self.pos[1]].remove('K')
            self.carrying_kid = True
            for kid in self.env.kids:
                if kid.pos == self.pos:
                    kid.in_robot = True
                    kid.pos = (-1,-1)
                    break

    def clean_room(self):
        path = walkable_path('*',self.pos,self.world)
        self.world[self.pos[0]][self.pos[1]].remove('R')
        self.pos = path.pop(0)
        self.world[self.pos[0]][self.pos[1]].append('R')
        if '*' in self.world[self.pos[0]][self.pos[1]]:
            self.world[self.pos[0]][self.pos[1]].remove('*')
            self.env.dirt -= 1
        if 'C' in self.world[self.pos[0]][self.pos[1]]:
            self.world[self.pos[0]][self.pos[1]].append('K')
            self.carrying_kid = False
            self.env.amount_kids -= 1
            for kid in self.env.kids:
                if kid.pos == (-1,-1):
                    kid.in_cradle = True
                    kid.in_robot = False
                    kid.pos = self.pos
                    break
    
    def put_kid_to_bed(self):
        path = walkable_path('C',self.pos,self.world)
        self.world[self.pos[0]][self.pos[1]].remove('R')
        self.pos = path.pop(0)
        self.world[self.pos[0]][self.pos[1]].append('R')
        if 'C' in self.world[self.pos[0]][self.pos[1]]:
            self.world[self.pos[0]][self.pos[1]].append('K')
            self.carrying_kid = False
            self.env.amount_kids -= 1
            for kid in self.env.kids:
                if kid.pos == (-1,-1):
                    kid.in_cradle = True
                    kid.in_robot = False
                    kid.pos = self.pos
                    break

    

if __name__ == "__main__":
    
    env = Enviroment(6,9,0,5,5)
    env.initialize()
    print_world(env.world)
    rep = 0
    while env.amount_kids > 0 and rep < 1000:
        input()
        if env.robot.carrying_kid and env.dirt > 0:
            env.robot.clean_room()
        elif env.robot.carrying_kid and env.dirt == 0:
            env.robot.put_kid_to_bed()
        else:
            env.robot.pick_kids()
        print_world(env.world)
        for kid in env.kids:
            if not (kid.in_cradle or kid.in_robot):
                k_amount,e_boxes = kid.kids_around()
                kid.move()
                kid.add_dirt(k_amount,e_boxes)
                input()
                print_world(env.world)            
        rep+=1



