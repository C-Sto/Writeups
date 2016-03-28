import socket
import time
import math
import Queue
import threading
import multiprocessing
from operator import itemgetter
HOST = "amazing.2016.volgactf.ru"
PORT = 45678
INVERT_MOVES = {'l':'r','r':'l','u':'d','d':'u'}
def remove_player(string):
    # convert to list
    newlist = list(string)
    #iterate and replace
    for x in range(len(newlist)):
        if newlist[x] == "*":
            newlist[x] = " "
    #return new list
    return ''.join(newlist)
def replace_string_index(string, index, character):
    # convert to list
    newlist = list(string)
    # replace at index
    if len(newlist)<index:
        #exit found
        return string
    newlist[index] = character
    # turn back into string
    newstring = ''.join(newlist)
    # return new string
    return newstring


class Game:
    state = []
    myloc = (1,1)

    def __init__(self, state):
        self.set_state(state)

    def get_state(self):
        return self.state

    def set_state(self, state):
        if type(state) == list:
            self.state = state
        else:
            self.state = state.split('\n')
        self.set_MyLoc()

    def set_MyLoc(self):
        for y in range(len(self.state)):
            for x in range(len(self.state[y])):
                try:
                    v = self.state[y][x]
                except:
                    print "wut"
                    return
                if self.state[y][x] == '*':
                    self.myloc = (x,y)
                    return

    def get_MyLoc(self):
        return self.myloc

    def check_empty(self, spec):
        walls = list("+-|#")
        for w in walls:
            if w == spec:
                return False
        return True

    def check_move(self, direction):
        x,y = self.get_MyLoc()
        # Check l
        if direction == 'l':
            if x-2 > 0 and self.check_empty(self.state[y][x-2]):
                return True
        # Check r
        elif direction == 'r':
            if x+2 < len(self.state[y]) and self.check_empty(self.state[y][x+2]):
                return True
        # check u
        elif direction == 'u':
            if y-1 > 0 and self.check_empty(self.state[y-1][x]):
                return True
        # check d
        elif direction == 'd':
            if y+1 < len(self.state) and self.check_empty(self.state[y+1][x]):
                return True

    def get_available_moves(self):
        MOVES = ['l','r','u','d']
        ret = []
        for m in MOVES:
            if self.check_move(m):
                ret.append(m)
        return ret

    def generate_successor_state(self, move):
        assert self.check_move(move)
        x,y = self.get_MyLoc()
        removed_player = []
        for i in self.get_state():
            removed_player.append(remove_player(i))
        if move == "l":
            removed_player[y] = replace_string_index(removed_player[y],x-4,"*")
        if move == "r":
            removed_player[y] = replace_string_index(removed_player[y],x+4,"*")
        if move == "u":
            removed_player[y-2] = replace_string_index(removed_player[y-2],x,"*")
        if move == "d":
            removed_player[y+2] = replace_string_index(removed_player[y+2],x,"*")
        return Game(removed_player)

    def generate_successors(self,lastMove = ""):
        moves = self.get_available_moves()
        ret = dict()
        for move in moves:
            if lastMove != '' and move == INVERT_MOVES[lastMove]:
                continue
            ret[move] = self.generate_successor_state(move)
        return ret

    def print_state(self):
        print self.state
        print self.get_MyLoc()


class Player:
    game = None
    s = None

    def __init__(self,host, port):
        self.host = host
        self.port = port
        self.connect(host,port)

    def connect(self,HOST,PORT):
        global start_time
        start_time = time.time()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print "Dicks"
        self.s.connect((HOST,PORT))
        print "connected"
        start_time = time.time()
        print self.s.recv(1024)
        self.download_game_state()

    def get_game_state(self):
        return self.game

    def set_exit(self):
        # find game y
        searchme = self.game.get_state()
        for y in range(len(searchme)):
            if len(searchme[y]) > 0 and searchme[y][0] in "+-|#":
                self.game_y = y
        self.game_x = len(self.game.get_state()[0])
        self.exit = self.game_x-3, self.game_y-1
    def download_game_state(self):
        global start_time
        raw = self.s.recv(1024)
        state = raw
        while state.count('\n') < 41:
            if "+" in state:
                state = state[state.index("+"):]
            newraw = self.s.recv(1024)
            state +=newraw
            raw+=newraw
        self.game = Game(state)
        if "Round " in raw or "{" in raw:
            start_time = time.time()
            self.set_exit()
            print raw

    def print_state(self):
        self.game.print_state()

    def send_moves(self,move):
        global start_time
        connected = time.time() - start_time
        if len(move)<1:
            print "No more moves, soz m8"
            self.connect(self.host,self.port)
        print "Total connect time:", connected
        if connected>78:
            print "connection aborted, lets try that again.."
            self.connect(self.host,self.port)
        print "Sending:",move
        self.s.sendall(move+'\n')
        self.download_game_state()

    def find_path(self):
        print "looking for exit at:", self.exit
        print "Player position:", self.game.get_MyLoc()
        print "Thinking.."
        #path = depth_first_search([],"",self.get_game_state(),self.exit)[0]
        path = a_star_search(self.get_game_state(),self.exit)
        return path


def a_star_search(state, exit):
    open_graph = state.generate_successors()
    closed_graph = []
    highScore = -999999999
    highMove = ""
    moveQ = Queue.PriorityQueue()
    for ki in open_graph:
        moveQ.put((-score_function(open_graph[ki].get_MyLoc(),state,exit),ki))
    while len(open_graph.keys()) > 0:
        move = moveQ.get()[1]
        # check for exit
        loc = open_graph[move].get_MyLoc()
        if loc == exit:
            print "Exit found :D"
            return move+'r'
        # check score
        score = score_function(loc,open_graph[move],exit)
        if score>highScore:
            highScore = score
            highMove = move
        # if score high enough, return it
        if score > 900:
            return move
        # move location to closed graph
        closed_graph.append(loc)
        # add successors to open graph if their location isn't in closed
        succ = open_graph[move].generate_successors()
        # no more need for the open graph state, remove it
        del(open_graph[move])
        for m in succ:
            if succ[m].get_MyLoc() not in closed_graph:
                open_graph[move+m] = succ[m]
                moveQ.put((-score_function(succ[m].get_MyLoc(),succ[m],exit),move+m))
        if moveQ.qsize() > 5:
            m = moveQ.get()
            return m[1]
    return highMove

def depth_first_search(visited,path,state,exit):
    visited.append(state.get_MyLoc())
    (x, y) = state.get_MyLoc()
    score = score_function((x,y),state, exit)
    if len(path)==0:
        score = 0
    if (x,y) == exit:
        print "FOUND EXIT"
        print x,y
        print path
        score +=999999999
        path+='r'
        return path, score
    #exit condition of next to hash
    if score>300:
        return path,score
    highscore =-99999999
    bestpath = ""
    results = []
    succ = state.generate_successors(path[len(path)-1] if len(path)>0 else "")
    if succ is None or len(succ) == 0:
        return path,score
    for suc in succ:
        # check if visited
        if succ[suc].get_MyLoc() in visited:
            continue
        # search states
        r = depth_first_search(visited,path+suc,succ[suc],exit)
        if r[1] > 99999:
            return r
        results.append(r)
    for result in results:
        if result[1] > highscore:
            highscore = result[1]
            bestpath = result[0]
    if highscore>score:
        return bestpath, highscore
    return path, score

def score_function((x,y),state, exit):
    if (x,y) == exit:
        return 999999
    score = 0
    #encourage moving to the bottom right
    score += (euclid_dist((exit[0]/3,exit[1]/2))-euclid_dist((exit[0]/3,exit[1]/2), (x/3,y/2)))*8

    #encourage being close to '#'s
    close = closest_hash((x,y),state)
    score -= close*9
    # if we are right next to a hash, that's a bonus
    if close < 4:
        score += 1000
    return score

def closest_hash((x,y),state):
    closest = 99999999
    max_dist = euclid_dist((41/2,170/3))
    for i in range(int(max_dist)):
        if closest<i:
            break
        # search from our point to dist where dist = x+dist, y+dist to x-dist,y-dist
        for hy in range(max(0,y-i),min(y+i,40)):
            for hx in range(max(0,x-i*2),min(x+i*2,150)):
                if hy != y-i and hy !=y+i:
                    if hx > (x-i*2)+3 and hx < (x+i*2)-3:
                        continue
                try:
                    if(state.get_state()[hy][hx]) == "#":
                        distance = i
                        if distance < closest:
                            closest = distance
                except:
                    a = 0#print hy,hx
    return closest

def euclid_dist(otherpoint, me = (0,0)):
    p = me
    q = otherpoint
    return math.sqrt(math.pow(abs(q[0]-p[0]),2)+math.pow((abs(q[1]-p[1])),2))

print "Doing player things"
p = Player(HOST,PORT)
while True:
    p.send_moves(p.find_path())
print "Player things done"


print "Done"
