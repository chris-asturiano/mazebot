import heapq
import tkinter as tk

class Node:
    def __init__(self, row, col, type):
        self.row = row
        self.col = col
        self.type = type
        self.cost = None
        self.explored = False
        self.order = None
        self.onFinal = False

    def __lt__(self, obj):
        return self.cost + h(self, goal) < obj.cost + h(obj, goal)
    
    def __eq__(self, obj):
        return self.cost + h(self, goal) == obj.cost + h(obj, goal) 
     
    def __le__(self, obj):
        return self.cost + h(self, goal) <= obj.cost + h(obj, goal) 
    


# Heuristic - Manhattan Distance
def h(node, goal): 
    return abs(node.row - goal.row) + abs(node.col - goal.col)

# Returns a list of all successors of the parameter
def succ(cur):
    succs = []
    if cur.row - 1 >= 0: # move up
        succs.append( maze[cur.row - 1][cur.col] )

    if cur.row + 1 < n: # move down
        succs.append( maze[cur.row + 1][cur.col] )

    if cur.col - 1 >= 0: # move left
        succs.append( maze[cur.row][cur.col - 1] )

    if cur.col + 1 < n: # move right
        succs.append( maze[cur.row][cur.col + 1] )
    
    return [s for s in succs if s.explored == False and s.type != '#']

# To get the neighbors whether theyre explored or not
def succ2(cur):
    succs = []
    if cur.row - 1 >= 0: # move up
        succs.append( maze[cur.row - 1][cur.col] )

    if cur.row + 1 < n: # move down
        succs.append( maze[cur.row + 1][cur.col] )

    if cur.col - 1 >= 0: # move left
        succs.append( maze[cur.row][cur.col - 1] )

    if cur.col + 1 < n: # move right
        succs.append( maze[cur.row][cur.col + 1] )
    
    return [s for s in succs if s.type != '#']


# Read Input
maze = []
start = Node(0, 0, 'a')
goal = Node(0, 0, 'a')

with open('maze.txt') as file:
    if file.readable():
        n = int(file.readline().rstrip(' \n'))

        for i in range(n):
            row = file.readline().rstrip(' \n')
            line = []

            for j in range(n):
                line.append(Node(i, j, row[j]))
                if line[j].type == 'S':
                    start = line[j]
                if line[j].type == 'G':
                    goal = line[j]
                
            maze.append(line)

counter = 1
frontier = []


# A* Search
# Add start to frontier
start.cost = 0
heapq.heappush(frontier, start)

while (frontier != []): 
    current = heapq.heappop(frontier)
    current.explored = True
    current.order = counter
    counter += 1
    
    if current.type == 'G':
        break

    # Add all successors to frontier
    for node1 in succ(current):
        found = False
        for node2 in frontier:
            if node1.row == node2.row and node1.col == node2.col:
                found = True
                
        if found == True:
            node1.cost = min(node1.cost, current.cost + 1)
            continue
        
        node1.cost = current.cost + 1
            
        heapq.heappush(frontier, node1)
        

# Find optimal path, if any path exists
if goal.explored: 
    path = []
    current = goal
    while current.cost != 0: # loops stops when current node is start
        current.onFinal = True
        path.append(current)

        # Find neighbor with smallest optimal cost
        min = 99999
        for node in succ2(current):
            if node.cost == None:
                continue
            
            if node.cost < min:
                min = node.cost
                current = node       

    start.onFinal = True
    path.append(start)



# GUI Window
window = tk.Tk()
window.title('MazeBot (You can click on a tile to print its order count on the terminal)')

# Frame for the labels
frame = tk.Frame(window)

fontsize = 512 // n

def on_label_click(event):
    # labels are clickable
    # prints the order when clicked
    clicked = event.widget
    text = clicked.cget('text')
    if text == 'S':
        text = start.order
    elif text == 'G':
        if goal.order != None:
            text = goal.order
        else:
            text = 'Unexplored'
    if text == '':
        text = 'Unexplored'
    print('Order: ' + str(text))
    
# Labels for each tile
labels = []


# Initialize the labels
for i in range(n):
    row = []
    for j in range(n):
        label = tk.Label(frame, text='', width=2, height=1, relief='solid', bg='white', highlightthickness=1, borderwidth=0.025, font=('Arial', fontsize))
        label.grid(row=i, column=j)
        label.bind('<Button-1>', on_label_click) # clickable
        row.append(label)
    labels.append(row)

for i in range(n):
    row = []
    for j in range(n):
        if maze[i][j].type == 'G': # make the goal red
            labels[i][j]['text'] = 'G' 
            labels[i][j].configure(bg='red') 
        
        if maze[i][j].type == 'S': # make the starting point yellow
            labels[i][j]['text'] = 'S' 
            labels[i][j].configure(bg='yellow')
            
        if  maze[i][j].onFinal == True and maze[i][j].type != 'G' and maze[i][j].type != 'S': # color the optimal path green
            labels[i][j].configure(bg='green')
        
            
        if maze[i][j].type == '#': #make the walls black
            labels[i][j].configure(bg='black')
            
        if maze[i][j].explored == True and maze[i][j].type != 'G' and maze[i][j].type != 'S': # print the order of the explored nodes
            labels[i][j]['text'] = str(maze[i][j].order)
            labels[i][j].config(font=('Arial', fontsize))
  
        if maze[i][j].type == '.' and maze[i][j].onFinal == False and maze[i][j].explored == True: # color the nonfinal explored nodes blue
            labels[i][j].configure(bg='skyblue')
            
    


frame.pack()
# Print the total number of nodes that were visited
print('Number of nodes visited: ' + str(counter - 1))

# Print no solution if theres no path
if goal.onFinal == False:
    print('No solution can be found')
    
window.mainloop()
