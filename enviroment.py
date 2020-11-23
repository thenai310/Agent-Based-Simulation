from random import randint,choice,sample,choices
from utils import *

dx = [ 0, 0,-1, 1]
dy = [-1, 1, 0, 0]


class Enviroment:

    def __init__(self, n,m,dirt_percent,obst_percent,kids, times):
        self.world = []
        self.amount_kids = kids
        self.kids = []
        self.obs = round(((n*m)*obst_percent)/100)
        self.dirt = round(((n*m)*dirt_percent)/100)
        self.times = times
        self.dimensions = (n,m)

    def __str__(self):
        return (f'{self.amount_kids} kid(s), {self.dirt} dirty box(es)')

    def initialize(self):
        self.create_world()
        self.genBabyCradle()
        self.genObstacles()
        self.genKids()
        self.genDirt()
        self.genRobot()
        
    def create_world(self):
        for i in range(self.dimensions[0]):
            self.world.append([])
            for _ in range(self.dimensions[1]):
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
        self.pos_cradles = []
        index = 0
        init_Pos = choice(emptyBoxes(self.world))
        return genBabyCradle_Rec(init_Pos,init_Pos,self.world,self.amount_kids,self.pos_cradles)

    def genObstacles(self):
        obs = self.obs
        while obs > 0:
            pos = choice(emptyBoxes(self.world))
            self.world[pos[0]][pos[1]].append('|')
            if is_connected(self.world):
                obs -= 1
            else:
                self.world[pos[0]][pos[1]].pop()

    def recreate(self):
        for kid in self.kids:
            if kid.in_cradle:
                kid.in_cradle = False
            if kid.in_robot:
                kid.in_robot = False
        self.variate()

    def variate(self):
        self.world = []
        self.create_world()
        kids_in_cradle, kid_in_robot = 0,0
        for kid in self.kids:
            if kid.in_cradle:
                kids_in_cradle += 1
            if kid.in_robot:
                kid_in_robot += 1
        self.amount_kids = len(self.kids)
        self.kids = []
        self.genBabyCradle()
        for _ in range(kids_in_cradle):
            cradle = self.pos_cradles.pop()
            self.world[cradle[0]][cradle[1]].append('K')
            kid = Kid(cradle,self)
            kid.in_cradle = True
            self.kids.append(kid)
            self.amount_kids-=1
        self.amount_kids -= kid_in_robot
        self.genObstacles()
        self.genKids()
        self.genDirt()
        self.genRobot()
        if kid_in_robot == 1:
            kid = Kid((-1,-1),self)
            kid.in_robot = True
            self.kids.append(kid)
            self.robot.carrying_kid = True
        
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
        if '*' in self.world[self.pos[0]][self.pos[1]]:
            self.world[self.pos[0]][self.pos[1]].remove('*')
            self.env.dirt -= 1
        else:
            path = walkable_path('*',self.pos,self.world)
            self.world[self.pos[0]][self.pos[1]].remove('R')
            self.pos = path.pop(0)
            self.world[self.pos[0]][self.pos[1]].append('R')
    
    def put_kid_to_bed(self):
        if 'C' in self.world[self.pos[0]][self.pos[1]]:
            self.world[self.pos[0]][self.pos[1]].append('K')
            self.carrying_kid = False
            for kid in env.kids:
                if kid.pos == (-1,-1):
                    kid.in_cradle = True
                    kid.in_robot = False
                    kid.pos = self.pos
                    break
        else:
            path = walkable_path('C',self.pos,self.world)
            self.world[self.pos[0]][self.pos[1]].remove('R')
            if randint(0,1) and len(path)>1:
                self.pos = path.pop(1)
            else:
                self.pos = path.pop(0)
            self.world[self.pos[0]][self.pos[1]].append('R')

    def pure_reactive_behavior(self):
        
        if self.carrying_kid:
            if '*' in self.world[self.pos[0]][self.pos[1]]:
                self.world[self.pos[0]][self.pos[1]].remove('*')
                self.env.dirt -= 1
            else:
                self.put_kid_to_bed()
        else:
            if False in [kid.in_cradle for kid in self.env.kids]: 
                self.pick_kids()
            else:
                self.clean_room()    

    def dirt_sensitive_behavior(self,dirt_percent):

        if dirt_percent >= 40:
            self.clean_room()
        else:
            self.internal_state_behavior()

    def internal_state_behavior(self):
        if self.carrying_kid:
            self.put_kid_to_bed()
        else:
            if False in [kid.in_cradle for kid in self.env.kids]: 
                self.pick_kids()
            else:
                self.clean_room() 

if __name__ == "__main__":

    env1 = Enviroment(8,10, 15, 10, 5, 10)
    env2 = Enviroment(8,10, 15, 10, 7, 20)
    env3 = Enviroment(8,10, 40,  0, 7, 20)
    env4 = Enviroment(8,10,  0, 40, 7, 15)
    env5 = Enviroment(8,10, 10, 40, 3, 20)
    env6 = Enviroment(6, 6, 15, 10, 4, 10)
    env7 = Enviroment(6, 6, 15, 10, 5, 15)
    env8 = Enviroment(6, 6, 35, 0,  5, 20)
    env9 = Enviroment(6, 6,  0, 35, 5, 15)
    env10 = Enviroment(6, 6, 25, 25, 2, 20) 

    enviroments = [env1,env2,env3,env4,env5,env6,env7,env8,env9,env10]
    s,f,w = 0,0,0
    for idx , env in enumerate(enviroments):
        print(f'############### Enviroment {idx+1} ################')
        env.initialize()
        stopped, win, fired = 0,0,0
        for _ in range(30):
            e_d = env.dirt
            dirt_percent , rep = 0, 0
            while dirt_percent <= 60 and rep < 100:    

                for _ in range(env.times):

                    # env.robot.internal_state_behavior()
                    env.robot.pure_reactive_behavior()
                    # env.robot.dirt_sensitive_behavior(dirt_percent)
                    
                    for kid in env.kids:
                        if not (kid.in_cradle or kid.in_robot):
                            k_amount,e_boxes = kid.kids_around()
                            kid.move()
                            kid.add_dirt(k_amount,e_boxes)
                
                dirt_percent = round(env.dirt * 100/((len(emptyBoxes(env.world)) + env.dirt)))
                if dirt_percent == 0 and False not in [kid.in_cradle for kid in env.kids]:
                    break

                # print('##################  VARIATION ',rep,' ##################')
                env.variate()
                rep+=1

            if rep >= 100 :
                # print('Simulation stopped')
                stopped +=1
            elif dirt_percent > 60:
                # print('Robot fired')
                fired +=1
            else:
                # print('Simulation succeded')
                win += 1
            env.dirt = e_d
            env.recreate()

        print(f'Forced {stopped} time(s), succeded {win} and got fired {fired} time(s)')
        s += stopped
        w += win
        f += fired
    print('---------------------------------------------------------------')
    print(f'Simulation stopped. Forced stop {s} times, succeded {w} and got fired {f} times in Total')

        # env.world = []
        # env.amount_kids = len(env.kids)