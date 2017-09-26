#Jairo Reyes AI project 5/13/2016

from tkinter import *

import operator
import random
import math


fLen = 1000 # (Field Length)
fWid =.64*fLen # (Field Width)
bRad = .010*fLen #ball icon radius
pRad = .014*fLen #player icon radius

ballRate = 1.5*bRad
chaseRate = .1*pRad
dribbleRate = .1*pRad
shootRate = 1.5*pRad
homeRate = .075*pRad
passRate = 1.5*bRad
dmin = pRad

bOwnership = (0,0) #(team, player) if team: 0 then A TEAM if team: 1 then B

WAIT = 0
HOME = 1
DRIBBLE = 2
PASS = 3
SHOOT = 4
CHASE = 5
#break cycles list, 0 component is count, 1 component is ownership (Count,(Team,Player#)
bc = [(0,(0,0)), (0,(0,0)), (0,(0,0)), (0,(0,0)), (0,(0,0)), (0,(0,0)), (0,(0,0)), (0,(0,0)), (0,(0,0)), (0,(0,0))] #used in breaking cycling


speedA = [1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0] #relative speeds of A team players
speedB = [1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0] #relative speeds of B team players

class score: 

    def __init__(self,r,b):
            self.red = r #red score
            self.blue = b #blue score
            self.ctr = 0 #total count

class ball:

    def __init__(self, x, y, ox, oy):
        self.curPos_x = x
        self.curPos_y = y
        self.startPos_x = ox
        self.startPos_y = oy

class player:

    def __init__(self, num, equipo, role, start_x, start_y, home_x, home_y):
        self.player_num = num
        self.team = equipo
        self.role = role
        self.home_x = home_x
        self.home_y = home_y
        self.start_x = start_x
        self.start_y = start_y
        self.curPos_x = start_x
        self.curPos_y = start_y
        self.speed = 1.0
        self.state = WAIT

    def inArea(self, b, l, m, r): #determines if a player is in a certain area of the field
        if self.team == "a":
            if self.role == "D" and 0 <= self.curPos_x <= l and 0 <= b.curPos_x <= l:
                return True
            elif self.role == "M" and l <= self.curPos_x <= m and l <= b.curPos_x <= m:
                return True
            elif self.role == "F" and m <= self.curPos_x <= r and m <= b.curPos_x <= r:
                return True
            elif self.role == "G" and 0 <= self.curPos_x <= l and 0 <= b.curPos_x <= l:
                return True
            else:
                return False
        elif self.team == "b":
            if self.role == "D" and m <= self.curPos_x <= r and m <= b.curPos_x <= r:
                return True
            elif self.role == "M" and l <= self.curPos_x <= m and l <= b.curPos_x <= m:
                return True
            elif self.role == "F" and 0 <= self.curPos_x <= l and 0 <= b.curPos_x <= l:
                return True
            elif self.role == "G" and m <= self.curPos_x <= r and m <= b.curPos_x <= r:
                return True
            else:
                return False

    def moveA(self, b, pe): #moves the A-team players according to their states
        bx = b.curPos_x
        by = b.curPos_y
        if (0 <= b.curPos_x <= 20 and .2834*fLen <= b.curPos_y <= .3566*fLen):#goal case if red scores
            s.red = s.red + 1 #add score to reds
            for i in range (1,12):
                A[i].reset(b)
                B[i].reset(b)
        if ((fLen-20) <= b.curPos_x <= fLen and .2834*fLen <= b.curPos_y <= .3566*fLen): #goal case if blue scores
            s.blue = s.blue + 1
            for i in range (1,12):
                A[i].reset(b)
                B[i].reset(b)
        if self.state == HOME:
            if self.player_num == 1 and self.team == "a": #Ateam goalie
                a = random.randrange(0,3)
                self.home_x = pRad
                self.home_y = (.2468*a/2.0+.3932*(1-a/2.0))*fLen  #goalie area randomized
                d = (self.curPos_x-self.home_x)**2 #distance formula d = sqrt((x1-x2)^2+....)))
                d = d+(self.curPos_y-self.home_y)**2
                d=d**0.5
            else:
                d = (self.curPos_x-self.home_x)**2.0
                d = d+(self.curPos_y-self.home_y)**2.0
                d=d**0.5
            if d > dmin:
                cos = float(self.home_x-self.curPos_x)/d
                sin = float(self.home_y-self.curPos_y)/d
                self.curPos_x = self.curPos_x + homeRate*self.speed * cos
                self.curPos_y = self.curPos_y + homeRate*self.speed * sin
        elif self.state == CHASE:
            d = (b.curPos_x - self.curPos_x)**2.0
            d = d + (b.curPos_y - self.curPos_y)**2.0
            d = d**0.5
            if d > dmin:
                cos = float(b.curPos_x - self.curPos_x)/d
                sin = float(b.curPos_y - self.curPos_y)/d
                self.curPos_x = self.curPos_x + cos*chaseRate*self.speed
                self.curPos_y = self.curPos_y + sin*chaseRate*self.speed
        elif self.state == PASS:
            d = (b.curPos_x-A[pe[0][2]].curPos_x)**2.0
            d = d+(b.curPos_y-A[pe[0][2]].curPos_y)**2.0
            d=d**0.5
            if d > dmin:
                cos = float(A[pe[0][2]].curPos_x-b.curPos_x)/d
                sin = float(A[pe[0][2]].curPos_y-b.curPos_y)/d
                b.curPos_x = b.curPos_x + ballRate* cos
                b.curPos_y = b.curPos_y + ballRate* sin
        elif self.state == DRIBBLE:
            lst = list()
            ls = find_closest_playerB(self.curPos_x, self.curPos_y)
            for j in range (0,11):
                if B[ls[j][1]].curPos_x > self.curPos_x:
                    lst.append((ls[j][0], ls[j][1]))
            lst = sorted(lst)
            if len(lst) == 0:
                px = fLen
                py = .32*fLen
            elif len(lst) == 1:
                if B[lst[0][1]].curPos_y >= .5*fWid:
                    px = B[lst[0][1]].curPos_x #dirbble same x coord as b player
                    py = .5*(B[lst[0][1]].curPos_y + 0) #ycoord is 
                else:
                    px = B[lst[0][1]].curPos_x
                    py = .5*(B[lst[0][1]].curPos_y + fWid)
            else:
                px = .5*(B[lst[0][1]].curPos_x + B[lst[1][1]].curPos_x)#go between the 2 B players
                py = .5*(B[lst[0][1]].curPos_y + B[lst[1][1]].curPos_y)#go between the 2 B players
            d = (self.curPos_x-px)**2.0
            d = d+(self.curPos_y-py)**2.0
            d=d**0.5
            if d > 0:
                cos = float(px-self.curPos_x)/d
                sin = float(py-self.curPos_y)/d
                self.curPos_x = self.curPos_x + (dribbleRate*self.speed)*cos #dribble player
                self.curPos_y = self.curPos_y + (dribbleRate*self.speed)*sin
                b.curPos_x = self.curPos_x + (dribbleRate*self.speed+pRad+bRad) * cos #dribble ball, ball must stay in front of player
                b.curPos_y = self.curPos_y + (dribbleRate*self.speed+pRad+bRad) * sin
        elif self.state == SHOOT:
            rd = random.uniform(.2834,.3566) #choose random place to shoot
            d = (b.curPos_x-fLen)**2.0
            d = d+(b.curPos_y-rd*fLen)**2.0
            d=d**0.5
            if d > dmin:
                cos = float(fLen-b.curPos_x)/d
                sin = float(rd*fLen-b.curPos_y)/d
                b.curPos_x = b.curPos_x + shootRate * cos
                b.curPos_y = b.curPos_y + shootRate * sin

    def moveB(self, b, pe): #moves the B-team players according to their states
        bx = b.curPos_x
        by = b.curPos_y
        if (0 <= b.curPos_x <= 20 and .2834*fLen <= b.curPos_y <= .3566*fLen):
            s.red = s.red + 1
            for i in range (1,12):
                A[i].reset(b)
                B[i].reset(b)
        if ((fLen-20) <= b.curPos_x <= fLen and .2834*fLen <= b.curPos_y <= .3566*fLen):
            s.blue = s.blue + 1
            for i in range (1,12):
                A[i].reset(b)
                B[i].reset(b)
        if self.state == HOME:
            if self.player_num == 1 and self.team == "b":
                a = random.randrange(0,3)
                self.home_x = fLen-pRad
                self.home_y = (.2468*a/2.0+.3932*(1-a/2.0))*fLen
                d = (self.curPos_x-self.home_x)**2
                d = d+(self.curPos_y-self.home_y)**2
                d=d**0.5
            else:
                d = (self.curPos_x-self.home_x)**2.0
                d = d+(self.curPos_y-self.home_y)**2.0
                d=d**0.5
            if d > dmin:
                cos = float(self.home_x-self.curPos_x)/d
                sin = float(self.home_y-self.curPos_y)/d
                self.curPos_x = self.curPos_x + homeRate*self.speed * cos
                self.curPos_y = self.curPos_y + homeRate*self.speed * sin
        elif self.state == CHASE:
            d = (b.curPos_x - self.curPos_x)**2.0
            d = d + (b.curPos_y - self.curPos_y)**2.0
            d = d**0.5
            if d > dmin:
                cos = float(b.curPos_x - self.curPos_x)/d
                sin = float(b.curPos_y - self.curPos_y)/d
                self.curPos_x = self.curPos_x + chaseRate*self.speed*cos
                self.curPos_y = self.curPos_y + chaseRate*self.speed*sin
        elif self.state == PASS:
            d = (b.curPos_x-B[pe[0][2]].curPos_x)**2.0
            d = d+(b.curPos_y-B[pe[0][2]].curPos_y)**2.0
            d=d**0.5
            if d > dmin:
                cos = float(B[pe[0][2]].curPos_x-b.curPos_x)/d
                sin = float(B[pe[0][2]].curPos_y-b.curPos_y)/d
                b.curPos_x = b.curPos_x + passRate*self.speed * cos
                b.curPos_y = b.curPos_y + passRate*self.speed * sin
        elif self.state == DRIBBLE:
            lst = list()
            ls = find_closest_playerA(self.curPos_x, self.curPos_y)
            for j in range (0,11):
                if A[ls[j][1]].curPos_x < self.curPos_x:
                    lst.append((ls[j][0], ls[j][1]))
            lst = sorted(lst)
            if len(lst) == 0:
                px = 0
                py = .32*fLen
            elif len(lst) == 1:
                if A[lst[0][1]].curPos_y >= .5*fWid:
                    px = A[lst[0][1]].curPos_x
                    py = .5*(A[lst[0][1]].curPos_y + 0)
                else:
                    px = A[lst[0][1]].curPos_x
                    py = .5*(A[lst[0][1]].curPos_y + fWid)
            else:
                px = .5*(A[lst[0][1]].curPos_x + A[lst[1][1]].curPos_x)
                py = .5*(A[lst[0][1]].curPos_y + A[lst[1][1]].curPos_y)
            d = (self.curPos_x-px)**2.0
            d = d+(self.curPos_y-py)**2.0
            d=d**0.5
            if d > .01:
                cos = float(px-self.curPos_x)/d
                sin = float(py-self.curPos_y)/d
                self.curPos_x = self.curPos_x + (dribbleRate*self.speed)*cos
                self.curPos_y = self.curPos_y + (dribbleRate*self.speed)*sin
                b.curPos_x = self.curPos_x + (dribbleRate*self.speed+pRad+bRad)*cos 
                b.curPos_y = self.curPos_y + (dribbleRate*self.speed+pRad+bRad)*sin
        elif self.state == SHOOT:
            rd = random.uniform(.2834,.3566)
            d = (b.curPos_x-0)**2.0
            d = d+(b.curPos_y-rd*fLen)**2.0
            d=d**0.5
            if d > dmin:
                cos = float(0-b.curPos_x)/d
                sin = float(rd*fLen-b.curPos_y)/d
                b.curPos_x = b.curPos_x + shootRate*self.speed * cos
                b.curPos_y = b.curPos_y + shootRate*self.speed * sin
                
    def reset(self,b): #resets the field after a goal; some randomness for defenders
        b.curPos_x = .5*fLen
        b.curPos_y = .5*fWid
        for i in range (1,12):
            self.state = WAIT
            if self.role == "D": #add some randomization to defenders
                self.curPos_y = self.start_y + random.uniform(-2*pRad,2*pRad)
                if self.team == "a":
                    self.curPos_x = self.start_x + random.uniform(0,2*pRad)
                else:
                    self.curPos_x = self.start_x + random.uniform(-2*pRad,0)
            else:
                self.curPos_x = self.start_x
                self.curPos_y = self.start_y
                
            
        

fillColor = '#040'
outlineColor = 'white'

A = [] #team A
A.append("")
jugador = player(1,"a","G", pRad, .32*fLen, pRad, .32*fLen) #Goalie
A.append(jugador)
jugador = player(2,"a","D", .165*fLen + pRad, .1216*fLen - pRad, .175*fLen + pRad, .1216*fLen - pRad) #Defender
A.append(jugador)
jugador = player(3,"a","D", .165*fLen + pRad, .32*fLen, .175*fLen + pRad, .32*fLen) 
A.append(jugador)
jugador = player(4,"a","D", .165*fLen + pRad, .5216*fLen+12, .175*fLen + pRad, .5216*fLen+12) 
A.append(jugador)
jugador = player(5,"a","M", .5*fLen - pRad - 5, .1216*fLen - pRad, .5*fLen - pRad - 5, .1216*fLen - pRad) #Mid-fielder
A.append(jugador)
jugador = player(6,"a","M", .5*fLen - .75*pRad, .32*fLen, .5*fLen - pRad - 5, .32*fLen) #Mid-fielder
A.append(jugador)    
jugador = player(7,"a","M", .40*fLen - 3*pRad - 10, .32*fLen, .4185*fLen - 3*pRad - 10, .32*fLen) #Mid-fielder
A.append(jugador)
jugador = player(8,"a","M", .5*fLen - pRad - 5, .5216*fLen + pRad,.5*fLen - pRad - 5, .5216*fLen + pRad) #Mid-fielder
A.append(jugador)    
jugador = player(9,"a","F", .5*fLen - pRad - 5, .1755*fLen - pRad, .725*fLen+pRad, .17*fLen) #Forward
A.append(jugador)
jugador = player(10,"a","F", .5*fLen - pRad - 5, .2285*fLen - pRad, .725*fLen+pRad, .32*fLen) #Forward
A.append(jugador)
jugador = player(11,"a","F", .5*fLen - pRad - 5, .4677*fLen + pRad, .725*fLen+pRad, .47*fLen) #Forward
A.append(jugador)

B = [] #team B
B.append("")
jugador = player(1,"b","G", fLen-pRad, .32*fLen, fLen-pRad, .32*fLen) #Goalie
B.append(jugador)
jugador = player(2,"b","D", .835*fLen - pRad, .1216*fLen - pRad, .825*fLen - pRad, .1216*fLen - pRad) #Defender
B.append(jugador)
jugador = player(3,"b","D", .835*fLen - pRad, .32*fLen, .825*fLen - pRad, .32*fLen) #Defender
B.append(jugador)
jugador = player(4,"b","D", .835*fLen - pRad, .5216*fLen+12, .825*fLen - pRad, .5216*fLen+12) 
B.append(jugador)
jugador = player(5,"b","M", .5*fLen + pRad + 5, .1216*fLen - pRad, .5*fLen + pRad + 5, .1216*fLen - pRad) 
B.append(jugador)
jugador = player(6,"b","M", .5*fLen + pRad + 5, .415*fLen + pRad, .5*fLen + pRad + 5,.32*fLen) #Mid-fielder
B.append(jugador)    
jugador = player(7,"b","M", .60*fLen + 3*pRad + 10, .32*fLen, .5815*fLen + 3*pRad + 10, .32*fLen) #Mid-fielder
B.append(jugador)
jugador = player(8,"b","M", .5*fLen + pRad + 5, .5216*fLen + pRad, .5*fLen + pRad + 5, .5216*fLen + pRad) #Mid-fielder
B.append(jugador)
jugador = player(9,"b","F", .5*fLen + pRad + 5, .1755*fLen - pRad, .275*fLen+pRad, .17*fLen) #Forward
B.append(jugador)   
jugador = player(10,"b","F", .5*fLen + pRad + 5, .2285*fLen - pRad,.275*fLen+pRad, .32*fLen) #Forward
B.append(jugador)
jugador = player(11,"b","F", .5*fLen + pRad + 5, .4677*fLen + pRad, .275*fLen+pRad, .47*fLen) #Forward
B.append(jugador)

for i in range (0,11): #set speeds of players
    A[i+1].speed = speedA[i]
    B[i+1].speed = speedB[i]

b = ball(.5*fLen, .5*fWid, .5*fLen, .5*fWid)#starting position of the ball

s = score(0,0) #making an instance of the score class

penaltyBoxA = (0,.1216*fLen, .165*fLen, .5216*fLen)
goalAreaA = (0, .2284*fLen, .055*fLen, .4116*fLen)
goalNetA = (5, .2834*fLen, 5, .3566*fLen)
penaltyBoxB = (fLen, .1216*fLen, .835*fLen, .5216*fLen)
goalAreaB = (fLen, .2284*fLen, .945*fLen, .4116*fLen)
penaltyArcA = (.0185*fLen, .2285*fLen, .2015*fLen, .4115*fLen)
goalNetB = (fLen - 5, .2834*fLen, fLen - 5, .3566*fLen)
penaltyArcB = (.9815*fLen, .2285*fLen, .7985*fLen, .4115*fLen)
cornerA1 = (.01*fLen + 3, .01*fLen + 3, -.01*fLen - 3, -.01*fLen - 3)
cornerA2 = (.01*fLen + 3, .65*fLen + 3, -.01*fLen - 3, .63*fLen - 3)
cornerB1 = (1.01*fLen + 3, .01*fLen + 3, .99*fLen - 3, -.01*fLen - 3)
cornerB2 = (1.01*fLen + 3, .65*fLen + 3, .99*fLen - 3, .63*fLen - 3)

def distance(px,py,qx,qy):
    d = (px-qx)**2 + (py-qy)**2
    d = d**0.5
    return d
    
    #The following function returns a list of the A-team players along with their distance
    #from the point (px,py) The list is sorted from smallest to largest distance.
def find_closest_playerA(px,py): 
    ls = list()
    for i in range (1,12):
        d = (A[i].curPos_x - px)**2 + (A[i].curPos_y - py)**2
        d = d**0.5
        ls.append((d,i))
    ls = sorted(ls)
    return ls
    
    #The following function returns a list of the B-team players along with their distance
    #from the point (px,py) The list is sorted from smallest to largest distance.
def find_closest_playerB(px,py):
    ls = list()
    for i in range (1,12):
        d = (B[i].curPos_x - px)**2 + (B[i].curPos_y - py)**2
        d = d**0.5
        ls.append((d,i))
    ls = sorted(ls)
    return ls
    
    #The following function determines if there are any players in the A-team that A[n]
    #can pass to so that the ball will reach that player before any B-team member can
    #reach that player. A list is returned ordered by players being closest to the goal.
def passingEvaluationA(n):
    ls = list()
    for i in range (1,12):
        if i != n:
            d0 = (A[i].curPos_x - A[n].curPos_x)**2
            d0 = d0 + (A[i].curPos_y - A[n].curPos_y)**2
            d0 = d0**0.5
            if d0 < .75*fWid:
                p = find_closest_playerB(A[i].curPos_x, A[i].curPos_y)
                d1 = (A[n].curPos_x - A[i].curPos_x)**2
                d1 = d1 + (A[n].curPos_y - A[i].curPos_y)**2
                d1 = d1**0.5
                t1 = float(d1/ballRate)
                d2 = (A[i].curPos_x - B[p[0][1]].curPos_x)**2
                d2 = d2 + (A[i].curPos_y - B[p[0][1]].curPos_y)**2
                d2 = d2**0.5
                t2 = float(d2/chaseRate)
                if t1-t2 < 0:
                    ls.append((t1-t2, 1000-A[i].curPos_x, i, p[0][1]))
    ls = sorted(ls, key=operator.itemgetter(1))
    return ls

    #The following function determines if there are any players in the B-team that B[n]
    #can pass to so that the ball will reach that player before any A-team member can
    #reach that player. A list is returned ordered by players being closest to the goal.
    
def passingEvaluationB(n):
    ls = list()
    for i in range (1,12):
        if i != n:
            d0 = (B[i].curPos_x - B[n].curPos_x)**2
            d0 = d0 + (B[i].curPos_y - B[n].curPos_y)**2
            d0 = d0**0.5
            if d0 < .75*fWid:
                p = find_closest_playerA(B[i].curPos_x, B[i].curPos_y)
                d1 = (B[n].curPos_x - B[i].curPos_x)**2
                d1 = d1 + (B[n].curPos_y - B[i].curPos_y)**2
                d1 = d1**0.5
                t1 = float(d1/ballRate)
                d2 = (B[i].curPos_x - A[p[0][1]].curPos_x)**2
                d2 = d2 + (B[i].curPos_y - A[p[0][1]].curPos_y)**2
                d2 = d2**0.5
                t2 = float(d2/chaseRate)
                if t1-t2 < 0:
                    ls.append((t1-t2, B[i].curPos_x, i, p[0][1]))
    ls = sorted(ls, key=operator.itemgetter(1))
    return ls
    
    #The following function returns an ordered pair (team, player number) of the
    #player that currently owns the ball. Once a player owns the ball, the 
    #ownership can only change if another player takes possession of the ball.
def ballOwnership(): 
        bx = b.curPos_x
        by = b.curPos_y
        cA = find_closest_playerA(bx,by)
        cB = find_closest_playerB(bx,by)
        if cA[0][0] < cB[0][0] and cA[0][0] < dmin:
            teamOwnership = 0 #team A is owner
            return ((0,cA[0][1])) #(Owning Team, player#)
        elif cB[0][0] < cA[0][0] and cB[0][0] < dmin:
            teamOwnership = 1
            return ((1, cB[0][1]))
        elif cA[0][0] == cB[0][0] and cA[0][0] < dmin:
            if randrange(0,2) == 0:
                teamOwnership = 0
                B[cB[0][1]].curPos_x = B[cB[0][1]].curPos_x + 2*pRad
                B[cB[0][1]].curPos_y = B[cB[0][1]].curPos_y + 2*pRad
                return ((0,cA[0][1]))
            else:
                teamOwnership = 1
                A[cA[0][1]].curPos_x = A[cA[0][1]].curPos_x + 2*pRad
                A[cA[0][1]].curPos_y = A[cA[0][1]].curPos_y + 2*pRad
                return ((1,cB[0][1]))
        else:
            return bOwnership
            
peA = list()
peB = list()

master = Tk()
canvas = Canvas(master,width=fLen, height=fWid + 50, background='black')
canvas.pack()

while 1:
    
    field = canvas.create_rectangle(0, 0, fLen, fWid, fill=fillColor, 
        outline=outlineColor, width=3)
    center = canvas.create_oval(.4085*fLen, .4115*fLen, 
        .5915*fLen, .2285*fLen, fill = fillColor, outline = outlineColor, width=3)
    center = canvas.create_oval(penaltyArcA, fill=fillColor, outline=outlineColor, width=3)
    center = canvas.create_oval(penaltyArcB, fill=fillColor, outline=outlineColor, width=3)
    line = canvas.create_line(fLen/2, 0, fLen/2, fWid, fill=outlineColor, width=3)
    rectangle = canvas.create_rectangle(penaltyBoxA, fill = fillColor, outline=outlineColor, width=3)
    rectangle = canvas.create_rectangle(goalAreaA, fill = fillColor, outline=outlineColor, width=3)
    line = canvas.create_line(goalNetA, fill='blue', width=6)
    rectangle = canvas.create_rectangle(penaltyBoxB, fill = fillColor, outline=outlineColor, width=3)
    rectangle = canvas.create_rectangle(goalAreaB, fill = fillColor, outline=outlineColor, width=3)
    corner = canvas.create_oval(cornerA1, fill=fillColor, outline=outlineColor, width=3)
    corner = canvas.create_oval(cornerA2, fill=fillColor, outline=outlineColor, width=3)
    corner = canvas.create_oval(cornerB1, fill=fillColor, outline=outlineColor, width=3)
    corner = canvas.create_oval(cornerB2, fill=fillColor, outline=outlineColor, width=3)
    line = canvas.create_line(goalNetB, fill='red', width=6)
    
    ball = canvas.create_oval(b.curPos_x - bRad, b.curPos_y + bRad,  
        b.curPos_x + bRad, b.curPos_y - bRad, fill='white',outline='black', width=2)
        
    for i in range(1, 12):
        canvas.create_oval(A[i].curPos_x-pRad, A[i].curPos_y+pRad,A[i].curPos_x+pRad, A[i].curPos_y-pRad,fill='blue',outline='black',width=2)
        canvas.create_text(A[i].curPos_x,A[i].curPos_y, text=str(A[i].role + str(A[i].player_num)),fill='white')
        canvas.create_oval(B[i].curPos_x-pRad, B[i].curPos_y+pRad,B[i].curPos_x+pRad, B[i].curPos_y-pRad,fill='red',outline='black',width=2)
        canvas.create_text(B[i].curPos_x,B[i].curPos_y, text=str(B[i].role + str(B[i].player_num)),fill='white')
        
    name_red = canvas.create_text(.75*fLen,660,fill="white", anchor = NW)
    name_blue = canvas.create_text(.25*fLen,660,fill="white", anchor = NW)
    red_name = canvas.itemconfig(name_red, text = "RED: ")
    blue_name = canvas.itemconfig(name_blue, text = "BLUE: ")
    score_red = canvas.create_text(.75*fLen + 50, 660, fill="white", anchor = NW)
    red_score = canvas.itemconfig(score_red, text = s.red)
    score_blue = canvas.create_text(.25*fLen + 50, 660, fill="white", anchor = NW)
    blue_score = canvas.itemconfig(score_blue, text = s.blue)
           
    if bOwnership != ballOwnership():
        chng = True #ball did change ownership
        bOwnership = ballOwnership() #update ownership
        if bc[0][1] != bOwnership and bc[1][1] != bOwnership and \
            bc[2][1] != bOwnership and bc[3][1] != bOwnership and \
            bc[4][1] != bOwnership and bc[5][1] != bOwnership and \
            bc[6][1] != bOwnership and bc[7][1] != bOwnership and \
            bc[8][1] != bOwnership and bc[9][1] != bOwnership: 
            bc[9] = (0,bc[8][1])
            bc[8] = (0,bc[7][1])
            bc[7] = (0,bc[6][1])
            bc[6] = (0,bc[5][1])
            bc[5] = (0,bc[4][1])
            bc[4] = (0,bc[3][1])
            bc[3] = (0,bc[2][1])
            bc[2] = (0,bc[1][1])
            bc[1] = (0,bc[0][1])
            bc[0] = (0,bOwnership)
            ct = 0
        else: #add to count to the one already in list (cycle)
            for i in range (0,10):
                if bc[i][1] == bOwnership:
                    bc[i] = (bc[i][0] + 1, bc[i][1])
                    ct = ct + 1
        rand = random.randrange(1,6)
        if ct > 10 + rand:
            bc = sorted(bc)
            mv = bc[9][1]
            if mv[0] == 0:
                A[mv[1]].curPos_x = A[mv[1]].curPos_x + pRad
                A[mv[1]].curPos_y = A[mv[1]].curPos_y + pRad
            else:
                B[mv[1]].curPos_x = B[mv[1]].curPos_x + pRad
                B[mv[1]].curPos_y = B[mv[1]].curPos_y + pRad
            ct = 0
            for i in range (0,10):
                bc[i] = (0,bc[i][1])
    else:
        chng = False
    if bOwnership[0] == 0:
        if chng == True:
            peA = passingEvaluationA(bOwnership[1])
        for i in range (1,12):
            if i != bOwnership[1]:
                A[i].state = HOME
            else:
                if len(peA) > 0 and distance(A[i].curPos_x, A[i].curPos_y, fLen, 0.5*fWid) > 350:
                    A[i].state = PASS
                elif len(peA) >= 0 and distance(A[i].curPos_x, A[i].curPos_y, fLen, 0.5*fWid) > 280:
                    A[i].state = DRIBBLE
                else:
                    A[i].state = SHOOT
        for i in range (1,12):
            if B[i].inArea(b, .34*fLen, .67*fLen, fLen):
                B[i].state = CHASE
            else:
                B[i].state = HOME
    elif bOwnership[0] == 1:
        if chng == True:
            peB = passingEvaluationB(bOwnership[1])
        for i in range (1,12):
            if i != bOwnership[1]:
                B[i].state = HOME
            else:
                if len(peB) > 0  and distance(B[i].curPos_x, B[i].curPos_y, 0, 0.5*fWid) > 350:
                    B[i].state = PASS
                elif len(peB) >= 0 and distance(B[i].curPos_x, B[i].curPos_y, 0, 0.5*fWid) > 280:
                    B[i].state = DRIBBLE
                else:
                    B[i].state = SHOOT
        for i in range (1,12):
            if A[i].inArea(b, .34*fLen, .67*fLen, fLen):
                A[i].state = CHASE
            else:
                A[i].state = HOME
                
    for i in range (1,12):
        if bOwnership[0] == 0:
            A[i].moveA(b,peA)
            B[i].moveA(b,peA)
    for i in range (1,12):
        if bOwnership[0] == 1:
            A[i].moveB(b,peB)
            B[i].moveB(b,peB)
    
    for i in range (1,12):
        if A[i].curPos_x > fLen:
            A[i].curPos_x = fLen
        if B[i].curPos_x > fLen:
            B[i].curPos_x = fLen
        if A[i].curPos_x < 0:
            A[i].curPos_x = 0
        if B[i].curPos_x < 0:
            B[i].curPos_x = 0
        if A[i].curPos_y > fWid:
            A[i].curPos_y = fWid
        if B[i].curPos_y > fWid:
            B[i].curPos_y = fWid
        if A[i].curPos_y < 0:
            A[i].curPos_y = 0
        if B[i].curPos_y < 0:
            B[i].curPos_y = 0
            
    if s.red + s.blue == 10000:        
        print ("Red = ", s.red, "Blue = ", s.blue, "Total = ", s.red+s.blue)
         
    canvas.update()
    canvas.after(50)
    canvas.delete(ALL)
    
master.mainloop()
    