from Map import Map_Obj

map_obj = Map_Obj(task=5)

class Node():
    def __init__(self, pos, parent):
        self.pos = pos
        self.cost = 0
        self.heur = 0
        self.total = 0
        self.parent = parent
        self.heuristic(map_obj.get_goal_pos())     
        self.totalCost()

    #Calculates the total cost of the current node pluss the parents cost if the node has a parent
    def totalCost(self):
        if self.parent == []:
            self.cost = map_obj.get_cell_value(self.pos)
        else:
            self.cost = map_obj.get_cell_value(self.pos) + self.parent.cost
        self.total = self.cost + self.heur
        

    def heuristic(self, goal):
        # absolute value of current x minus goal x, plus current y minus goal y
        self.heur = abs(self.pos[0] - goal[0]) + abs(self.pos[1] - goal[1])

class A_star():
    def __init__(self, map_obj):
        self.map_obj = map_obj
        self.activeList = []
        self.current = Node(map_obj.get_start_pos(), [])
        self.activeList.append(self.current)

    #Appends the adjacent nodes (on X and Y axis) to the activeList
    def find_inherit(self):
        x = self.current.pos[0]
        y = self.current.pos[1]
        self.inherit = []
        
        for i in range(4):
            if i == 0:
                if (map_obj.get_cell_value([x+1, y]) > 0):
                   self.inherit.append([x+1,y])
            elif i == 1: 
                if (map_obj.get_cell_value([x, y+1]) > 0):
                    self.inherit.append([x, y+1])
            elif i == 2:
                if (map_obj.get_cell_value([x-1, y]) > 0):
                    self.inherit.append([x-1, y])
            else:
                if (map_obj.get_cell_value([x, y-1]) > 0):
                    self.inherit.append([x, y-1])
            i += 1
            
        self.activeList.remove(self.current)

    #sorts the activeList based on the total value of a node           
    def sort_activeList(self):
        self.activeList.sort(key=lambda val : val.total)

    #Checks if the inheritent node is in activeList, if it is, we check if the total cost of the new instance is less than the one that is already there.
    #If the cost is less, we replace the old instance with the new one because we have found a shorter path to the node.
    def append_to_activeList_and_check_for_duplicates(self, current_node):
        for a in range(len(self.activeList)):
            if current_node.pos == self.activeList[a].pos:
                if current_node.total < self.activeList[a].total: 
                    self.activeList.pop(a)
                    self.activeList.append(current_node)
                return 
            a += 1 
        self.activeList.append(current_node)  
        self.sort_activeList()

    #Loops through all the inherits of the current node and use the function append_to_***
    def next_node(self, parent):
        for i in range(len(self.inherit)):
            curr_check = Node(self.inherit[i], parent)
            self.append_to_activeList_and_check_for_duplicates(curr_check)

    #This function acts like a main funciton. Every function is combined to make the A* algorithm work.
    #It adds color to the map showing the shortest path, and every visited node.
    def move_to_new_node(self):
        steps = 0
        
        while self.current.pos != map_obj.get_goal_pos():
            
            self.find_inherit()
            self.next_node(self.current)
            self.sort_activeList()
            self.current = self.activeList[0]
            map_obj.replace_map_values(self.current.pos, 4, map_obj.get_goal_pos())

            #Moves the goal pos in task 5
            map_obj.tick()

        #Adding a different color to the shortest path
        while self.current.pos != map_obj.get_start_pos():
            map_obj.replace_map_values(self.current.pos, 6, map_obj.get_start_pos())
            self.current = self.current.parent
            steps+=1

        #Adding a third color to the end position so we can clearly see where it is.
        map_obj.replace_map_values(map_obj.get_goal_pos(), 5, map_obj.get_start_pos())
        print(steps, "steps taken")
    
map_obj1 = A_star(map_obj)  
map_obj1.move_to_new_node()
map_obj.get_maps()
map_obj.show_map()


