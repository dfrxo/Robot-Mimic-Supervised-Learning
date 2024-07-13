from functions import sense
import heapq
from collections import defaultdict

def search_button_increment(ship, robot_position, mouse_positions, ship_probabilities, alpha):
    x, y = robot_position
    def sort_key(item):       # Sort the entire ship probabilities map by PROBABILITY first. Break ties by MANHATTAN DISTANCE. Break ties further by choosing one with the same x or y (direct neighbors) 
        c, v = item
        manhattan_distance = abs(c[0] - x) + abs(c[1] - y)
        tiebreaker = 1
        if x==c[0] or c[1]==y:
             tiebreaker = 0
        return (v, -manhattan_distance, tiebreaker)   ## Sort by value first, then manhattan distance
    
    temp = list(ship_probabilities.items())   # Turn ship probabalities into list: ((x,y), probability)
    temp = sorted(temp, key = sort_key, reverse= True)      # Sort
    coordinates, _ = temp[0]                                # Take the highest probability cell
    path = []
    while not path:                                         # If the path is empty, go there.
          path = robot_shortest_path(ship, robot_position, coordinates)    # Take the shortest path
          temp.pop(0)                                       
          coordinates, _ = temp[0]                          # If the path is empty, try again

    return path 
    

def robot_shortest_path(ship, start, goal):
    ## Find all possible neighbors for a given coordinate
    def get_neighbors(curr_position):
         neighbors = []
         x, y = curr_position
         if x!=0 and (ship[x-1][y] == 'O' or ship[x-1][y] == 'M'):
              neighbors.append((x-1,y))
         if x!=len(ship)-1 and (ship[x+1][y] == 'O' or ship[x+1][y] == 'M'):
              neighbors.append((x+1,y))
         if y!=len(ship)-1 and (ship[x][y+1] == 'O' or ship[x][y+1]== 'M'):
              neighbors.append((x,y+1))
         if y!=0 and (ship[x][y-1] == 'O' or ship[x][y-1] == 'M'):
              neighbors.append((x,y-1))
         return neighbors

    # Shortest path
    fringe = [(0,start)]
    heapq.heapify(fringe)
    parent = {}
    dist = defaultdict(lambda:float('inf'))
    dist[start] = 0 

    while len(fringe)!=0:        
        curr_dist, curr_position = heapq.heappop(fringe)
        if curr_position == goal:
            path = []
            while curr_position in parent:
                   path.append(curr_position)
                   curr_position = parent[curr_position] 
            path.reverse()               
            return path

        neighbors = get_neighbors(curr_position)
        for n in neighbors:
            dist_to_child = dist[curr_position] + 1
            if dist[n] > dist_to_child:
                 dist[n] = dist_to_child 
                 heapq.heappush(fringe, (dist_to_child, n))
                 parent[n] = curr_position
     # If there's no path return false
    return False