'''
ahora, yo me imagino tener tres estados x ahora
uno inicial --> buscar un kid, buscar el kid mas cercano
y recogerlo, si se encuentra una basura, limpia, 
hasta poder recoger el kid, entonces ahi pasa a
enviroment sucio --> mandar a limpiar, que seria 
trata de moverte en la direccion de la basura mas cercana
y limpia y asi hasta q el enviroment este limpio
meanwhile, si encuentra un cradle(si en tus adyacentes
hay un cradle), save kid, y pasa al estado inicial 
'''


'''
Robot
'''
def closest(ipos,world,char):
    dx = [-1, 0, 1, 0,-1, 1,-1, 1]
    dy = [ 1,-1,-1, 1, 1, 1, 0, 0]
    visited = []
    visited.append(ipos)
    queue = []
    queue.append(ipos)
    while len(queue) > 0:
        index = 0 
        pos = queue.pop(0)
        while index < 8:
            new_pos = world[pos[0]+dx[index]][pos[1]+dy[index]]
            if in_range(new_pos) and new_pos not in visited:
                if char in world[new_pos[0]][new_pos[1]]:
                    return new_pos
                else:
                    queue.append(new_pos)
                    visted.append(new_pos)
                    index+=1
            else:
                index+=1
    

