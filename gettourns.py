import csv
import os, math

players = []
playerArchive = []
WORDS = ["W/O","Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec","&nbsp;","NA","UNP"]
ATP_START = 2000
CHAL_START = 1750
ITF_START = 1000

class Player:
    def __init__(self,id,name,rating):
        self.id = id
        self.name = name
        self.rating = rating
        self.startRat = rating
        self.matches = []
        self.oldMatches = []
        self.totalMatches = 0
        self.live = True

    def getK(self):
        return 800 / (len(self.matches)+5)

    def __str__(self):
        return "%i  %s  %0.2f  %i" % (self.id, self.name, self.rating, len(self.matches))

    def updateRating(self,date):
        total = 0
        i = 0
        while i < len(self.matches):
            match = self.matches[i]
            if abs(date - match[0]) < 10000:
                total += match[1]
                i += 1
            else:
                self.oldMatches.append(self.matches.pop(i))
        self.rating = round(self.startRat + total,2)
        # if len(self.matches) < 20:
        #     self.rating = round(self.rating*(1-.1)**(30-len(self.matches))) 
        if len(self.matches) == 0:
            self.live = False
        else:
            self.live = True

def getData(year):
    tourns = []
    matches = []
    tourn_list_final = []
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    filename = 'atp_matches_' + str(year) + '.csv'
    filename = os.path.join(THIS_FOLDER,'data',filename)
    f = open(filename)
    try:
        csv_f = csv.reader(f)
        next(csv_f)
        for match in csv_f:
            entry = [match[0],match[1],match[2],int(match[3]),match[4],int(match[5]),"ATP"]
            if not entry in tourns:
                tourns.append(entry)
            game = [int(match[5]),int(match[7]),match[10],int(match[15]),match[18],match[23],entry[-1],int(match[6])]
            doing = True
            for word in WORDS:
                if word in game[5]:
                    doing = False
            if doing:
                matches.append(game)
    finally:
        f.close()
    # for event in tourns:
    #     #def __init__(self,id,name,surface,drawSz,level,date,type,base_rating=1500):
    #     newTourn = Tournament(event[0],event[1],event[2],int(event[3]),event[4],int(event[5]),"ATP")
    #     tourn_list_final.append(newTourn)
    if year >= 1978:
        filename = 'atp_matches_qual_chall_' + str(year) + '.csv'
        filename = os.path.join(THIS_FOLDER,'data',filename)
        f = open(filename)
        try:
            csv_f = csv.reader(f)
            next(csv_f)
            for match in csv_f:
                entry = [match[0],match[1],match[2],int(match[3]),match[4],int(match[5]),"Challenger"]
                if not entry in tourns:
                    tourns.append(entry)
                game = [int(match[5]),int(match[7]),match[10],int(match[15]),match[18],match[23],entry[-1],int(match[6])]
                doing = True
                for word in WORDS:
                    if word in game[5]:
                        doing = False
                if doing:
                    matches.append(game)
        finally:
            f.close()
        # for event in tourns:
        #     newTourn = Tournament(event[0],event[1],event[2],int(event[3]),event[4],int(event[5]),"Challenger")
        #     tourn_list_final.append(newTourn)
    if year >= 1991:
        filename = 'atp_matches_futures_' + str(year) + '.csv'
        filename = os.path.join(THIS_FOLDER,'data',filename)
        f = open(filename)
        try:
            csv_f = csv.reader(f)
            next(csv_f)
            for match in csv_f:
                entry = [match[0],match[1],match[2],int(match[3]),match[4],int(match[5]),"Futures"]
                if not entry in tourns:
                    tourns.append(entry)
                game = [int(match[5]),int(match[7]),match[10],int(match[15]),match[18],match[23],entry[-1],int(match[6])]
                doing = True
                for word in WORDS:
                    if word in game[5]:
                        doing = False
                if doing:
                    matches.append(game)
        finally:
            f.close()
        # for event in tourns:
        #     newTourn = Tournament(event[0],event[1],event[2],int(event[3]),event[4],int(event[5]),"Futures")
        #     tourn_list_final.append(newTourn
    tourns.sort(key= lambda x: x[5])
    # for event in tourns:
    #     print(event)
    matches.sort(key= lambda y: y[0])
    return (tourns, matches)



def runSeason(year):
    tourn_list, matches = getData(year)
    dates = []
    # print(tourn_list)
    for tourn in tourn_list:
        if tourn[5] not in dates:
            dates.append(tourn[5])
    for date in dates:
        print(date)
        dateMatches = [x for x in matches if x[0] == date]
        dateMatches.sort(key= lambda x: x[-1])
        for match in dateMatches:
            playMatch(match)
        updatePlayerRatings(date)
        # writeRankings(date)
    displayRankings(10,year)

def displayRankings(n,year=0):
    if year > 0:
        print("----- %s Year-End rankings -----" % str(year))
    players.sort(key=lambda x: -x.rating)
    i,j = (0,0)
    while j < n:
        if players[i].live:
            j += 1
            print(players[i])
        i += 1
    print("\n\n")

def findPlayer(id,name):
    for i in range(len(players)):
        if players[i].id == id or players[i].name == name:
            return i
    return -1

def playMatch(matchData):
    id1 = int(matchData[1])
    name1 = matchData[2]
    id2 = int(matchData[3])
    name2 = matchData[4]
    # if name1 == "Filippo Messori" or name2 == "Filippo Messori":
    #     print("Debug")
    ind = findPlayer(id1,name1)
    if ind >= 0:
        p1 = players.pop(ind)
    elif matchData[-2] == "ATP":
        p1 = Player(matchData[1],matchData[2],ATP_START)
    elif matchData[-2] == "Challenger":
        p1 = Player(matchData[1],matchData[2],CHAL_START)
    else:
        p1 = Player(matchData[1],matchData[2],ITF_START)

    ind = findPlayer(id2,name2)
    if ind >= 0:
        p2 = players.pop(ind)
    elif matchData[-2] == "ATP":
        p2 = Player(matchData[3],matchData[4],ATP_START)
    elif matchData[-2] == "Challenger":
        p2 = Player(matchData[3],matchData[4],CHAL_START)
    else:
        p2 = Player(matchData[3],matchData[4],ITF_START)
    # if p1.name in [x.name for x in players]:
    #     print("STOPPPPP %s" % (p1.name))
    # if p2.name in [x.name for x in players]:
    #     print("STOPPPPP %s " % (p2.name))

    ex1 = 1 / (1 + math.pow(10,(p2.rating-p1.rating)/400))
    ex2 = 1 / (1 + math.pow(10,(p1.rating-p2.rating)/400))
    res1, res2 = parseScore(matchData[5])
    Kfactors = {"ATP":1, "Challenger":0.66, "Futures":0.33}
    K = ((p1.getK() + p2.getK()) / 2) * Kfactors[matchData[-2]]


    # Store date, change factor, weight, own rating, opponent ID, opponent name, opponent rating, score
    p1.matches.append([matchData[0],K*(res1 - ex1),1,p1.rating,matchData[3],matchData[4],p2.rating,matchData[6]])
    p2.matches.append([matchData[0],K*(res2 - ex2),1,p2.rating,matchData[1],matchData[2],p1.rating,matchData[6]])
    # p1.rating = p1.rating + K*(res1 - ex1)
    # p2.rating = p2.rating + K*(res2 - ex2)
    players.append(p1)
    players.append(p2)

def updatePlayerRatings(date):
    i = 0
    while i < len(players):
        players[i].updateRating(date)
        i += 1

def parseScore(score):
    score = score.strip()
    games1 = 0
    games2 = 0
    words = ["RET", "DEF","Default","ABD","Played","and","unfinished","SUS","ABN","In","Progress"]
    if score == "":
        pass
    else:
        sets = score.split(" ")
        for set in sets:
            if set in words:
                break
            if set == "":
                continue
            else:
                games = set.split("-")
                if len(games[0]) > 1:
                    games1 += int(games[0][0])
                else:
                    games1 += int(games[0])
                if len(games) > 1:
                    if len(games[1]) > 1:
                        games2 += int(games[1][0])
                    else:
                        games2 += int(games[1])
    if games1 + games2 > 0:
        res1 = 0.7 * (games1 / (games1 + games2)) + 0.3
        res2 = 0.7 * (games2 / (games2 + games1))
    else:
        res1 = 1
        res2 = 0
    return (res1, res2)

def runYears(start=1968,end=2019):
    year = start
    while year <= end:
        runSeason(year)
        year += 1

def getWriteFile(date):
    if date < 19800000:
        return "atp_rankings_70s.csv"
    elif date < 19900000:
        return "atp_rankings_80s.csv"
    elif date < 20000000:
        return "atp_rankings_90s.csv"
    elif date < 20100000:
        return "atp_rankings_00s.csv"
    else:
        return "atp_rankings_10s.csv"

def writeRankings(date):
    filename = getWriteFile(date)
    players.sort(key= lambda x: -x.rating)
    with open(filename,'a',newline='') as csvfile:
        rankwriter = csv.writer(csvfile)
        i,j = (0,1)
        while i < len(players):
            if players[i].live:
                rankwriter.writerow([date,j,players[i].id,players[i].name,players[i].rating,len(players[i].matches)])
                j += 1
            i += 1

runYears(2004,2019)
