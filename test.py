 
def move(self,ambiente):
        #Mover Random & falta actualizar cuando me como una basuara la cantidad de basura
        # canMove = False

        # for k in range(len(moves_x)):
        #     newx = self.pos_x + moves_x[k]
        #     newy = self.pos_y + moves_y[k]
        #     if in_range(newx,newy,ambiente.r,ambiente.c) and  "O" not in ambiente.world[newx][newy]:
        #         canMove = True
        #         break
        # if "S" in ambiente.world[self.pos_x][self.pos_y]:
        #     ambiente.world[self.pos_x][self.pos_y].remove("S")
        #     ambiente.amount_dirty -= 1
        # elif canMove :
                   
        #     while True:
        #         x =randint(0,3)
        #         newx = self.pos_x + moves_x[x]
        #         newy = self.pos_y + moves_y[x]
        #         if in_range(newx,newy,ambiente.r,ambiente.c) and  "O" not in ambiente.world[newx][newy]:
        #             ambiente.world[self.pos_x][self.pos_y].remove("R")
        #             ambiente.world[newx][newy].append("R")
        #             self.pos_x = newx
        #             self.pos_y = newy
        #             break

        #Recoger Todos los ninos
        #for i in range(ambiente.amount_childs):
        
        if ambiente.amount_childs == 0 and not self.with_child:
            print("no hay ninos por recoger")

        elif "S" in ambiente.world[self.pos_x][self.pos_y]:
            ambiente.world[self.pos_x][self.pos_y].remove("S")
            ambiente.amount_dirty -= 1
        else:
            if self.with_child:
                if self.target == None :     
                    road = []
                    queue = [(self.pos_x,self.pos_y)]
                    visited = []
                    ant_dic = {}
                    ant_dic[(self.pos_x,self.pos_y)] = (-1,-1)
                    x = 0
                    y = 0
                    while len(queue) > 0:
                        x , y= queue.pop(0)
                        if "C" in ambiente.world[x][y]:
                            break 
                        visited.append((x,y))
                        
                        for i in range(0,len(moves_x)):
                            new_x = x + moves_x[i]
                            new_y = y + moves_y[i]
                            
                            if in_range(new_x,new_y,ambiente.r,ambiente.c) and "O" not in ambiente.world[new_x][new_y] and (new_x,new_y) not in visited and not ("N" in ambiente.world[new_x][new_y] and "C" in ambiente.world[new_x][new_y]):
                                queue.append((new_x,new_y))
                                ant_dic[(new_x,new_y)] = (x,y)


                    road.append((x,y))
                    while True:
                        x,y = ant_dic[(x,y)]
                        if x == -1:
                            break
                        road.append((x,y))

                    road.reverse()
                    print(road)
                    road = road[1:]
                    self.target = road
                try:
                    new_x ,new_y = self.target.pop(0)
                    ambiente.world[self.pos_x][self.pos_y].remove("R")
                    self.pos_x = new_x
                    self.pos_y = new_y
                    ambiente.world[new_x][new_y].append("R")
                    if "C" in ambiente.world[new_x][new_y]:
                        self.with_child = False
                        self.target = None
                        ambiente.world[new_x][new_y].append("N")
                        for ch in ambiente.childs:
                            if ch.pos_x == -1 and ch.pos_y == -1:
                                ch.in_robot = False
                                ch.in_robot = True
                                ch.pos_x = new_x
                                ch.pos_y = new_y
                                break
                except:
                    print("No veo mi objetivo")
                    #actualizar child.robot = False
                    #actualizar child.yard = True

            else:    
                #if self.target == None :     
                road = []
                queue = [(self.pos_x,self.pos_y)]
                visited = []
                ant_dic = {}
                ant_dic[(self.pos_x,self.pos_y)] = (-1,-1)
                x = 0
                y = 0
                while len(queue) > 0:
                    x , y= queue.pop(0)
                    if "N" in ambiente.world[x][y] and "C" not in ambiente.world[x][y]:
                        break 
                    visited.append((x,y))
                    
                    for i in range(0,len(moves_x)):
                        new_x = x + moves_x[i]
                        new_y = y + moves_y[i]
                        
                        if in_range(new_x,new_y,ambiente.r,ambiente.c) and "O" not in ambiente.world[new_x][new_y] and (new_x,new_y) not in visited and not ("N" in ambiente.world[new_x][new_y] and "C" in ambiente.world[new_x][new_y]):
                            queue.append((new_x,new_y))
                            ant_dic[(new_x,new_y)] = (x,y)


                road.append((x,y))
                while True:
                    x,y = ant_dic[(x,y)]
                    if x == -1:
                        break
                    road.append((x,y))

                road.reverse()
                print(road)
                road = road[1:]
                self.target = road

                new_x ,new_y = self.target.pop(0)
                ambiente.world[self.pos_x][self.pos_y].remove("R")
                self.pos_x = new_x
                self.pos_y = new_y
                ambiente.world[new_x][new_y].append("R")
                if "N" in ambiente.world[new_x][new_y]:
                    self.with_child = True
                    ambiente.world[new_x][new_y].remove("N")
                    self.target = None
                    ambiente.amount_childs -= 1
                    for ch in ambiente.childs:
                        if ch.pos_x == new_x and ch.pos_y == new_y:
                            ch.in_robot = True
                            ch.pos_x = -1
                            ch.pos_y = -1
                            break
                    #actualizar child.robot = True
            
            
            #print(road)
            #input()

