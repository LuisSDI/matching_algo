from six import text_type
from generate_user import calculatePersonalityMatch, generateUid, generateUser
import firebase_admin
import itertools
from firebase_admin import credentials
from firebase_admin import firestore
from roommate_answers import RoommateIndividual, RoommatePreference
import numpy as np
from irving_algorithm import Find_all_Irving_partner
import random

habitsNumAns = [4,4,3,4,3
,4,4,4,4,2,
4,2,3,5,4,
3,3,3,3]

def getPoints(ans1, ans2, numAns):
    result = 1 - abs((ans1 - ans2)/(numAns-1))
    return result

def calculateHabits(myHabits , roomHabits):
    
    habitsScore = 0

    for x in range(len(myHabits)):
        habitsScore+=getPoints(myHabits[x],roomHabits[x], habitsNumAns[x])
    habitsScore = habitsScore / len(myHabits)
    #print(habitsScore)
    return habitsScore

def calculateOther(myScore, roomScore):
    myScore = [x+1 for x in myScore]
    roomScore = [x+1 for x in roomScore]
    result = 0
    for x in range(len(myScore)):
        result +=getPoints(myScore[x],roomScore[x], 5)
    result = result / len(myScore)
    #print(result)
    return result

cred = credentials.Certificate("matched--official-firebase-adminsdk-agzne-ef087005af.json")
default_app= firebase_admin.initialize_app(cred)

print(default_app.name)

db = firestore.client()
users_ref = db.collection(u'roommateTest')
perso_ref = db.collection(u'userInfo')
docs = users_ref.stream()

counter = 1

allRoommates = []

roomPref = []

for doc in docs:
    uid = doc.to_dict().get('uid')
    personalityDoc = perso_ref.document(uid).get()
    personality = personalityDoc.to_dict().get('personality')
    allRoommates.append(RoommateIndividual(counter, doc.to_dict().get('uid'), beliefAns=doc.to_dict().get('beliefAns'),
   communAns= doc.to_dict().get('communAns'),
   habitsAns= doc.to_dict().get('habitsAns'), interestAns= doc.to_dict().get('interestAns'), 
    socialAns= doc.to_dict().get('socialAns'),
    personality = personality))
    counter+=1

for x in range(counter,9):
    uid = generateUid(28)
    allRoommates.append(generateUser(x,uid))
    #print(allRoommates[x-1])

# allRoommates[2].socialAns = allRoommates[0].socialAns
# allRoommates[2].personality = allRoommates[0].personality
# allRoommates[2].beliefAns = allRoommates[0].beliefAns
# allRoommates[2].communAns = allRoommates[0].communAns
# allRoommates[2].habitsAns = allRoommates[0].habitsAns
# allRoommates[2].interestAns = allRoommates[0].interestAns

# allRoommates[3].socialAns = allRoommates[0].socialAns
# allRoommates[3].personality = allRoommates[0].personality
# allRoommates[3].beliefAns = allRoommates[0].beliefAns
# allRoommates[3].communAns = allRoommates[0].communAns
# allRoommates[3].habitsAns = allRoommates[0].habitsAns
# allRoommates[3].interestAns = allRoommates[0].interestAns
roomPref = [[] for i in range(len(allRoommates))]

pairs=list(itertools.combinations(allRoommates, 2))

for o in pairs:
    a = o[0]
    b = o[1]
    #print(a.id)
    #print(b.id)
    preference1 = RoommatePreference(b.id,b.uid,
    habitsScore= calculateHabits(b.habitsAns,a.habitsAns),
    beliefScore=calculateOther(b.beliefAns,a.beliefAns),
    socialScore=calculateOther(b.socialAns,a.socialAns),
    communScore=calculateOther(b.communAns,a.communAns),
    interestScore=calculateOther(b.interestAns,a.interestAns),
    personalityScore= calculatePersonalityMatch(b.personality,a.personality)
    )
    preference2 = RoommatePreference(a.id,a.uid,
            habitsScore= calculateHabits(b.habitsAns,a.habitsAns),
    beliefScore=calculateOther(b.beliefAns,a.beliefAns),
    socialScore=calculateOther(b.socialAns,a.socialAns),
    communScore=calculateOther(b.communAns,a.communAns),
    interestScore=calculateOther(b.interestAns,a.interestAns),
    personalityScore= calculatePersonalityMatch(b.personality,a.personality))
    preference1.getFinal()
    preference2.getFinal()
    roomPref[b.id-1].append(preference2)
    roomPref[a.id-1].append(preference1)
    #b.add(2)


#print('Here 4')
counter2 =1
for room in roomPref:
    room.sort(key=lambda x: x.finalScore, reverse=True)
prefMatrix = [[] for i in range(len(allRoommates))]

counter3 = 0
for room in roomPref:
    for y in range(len(room)):
        prefMatrix[counter3].append(room[y].roomid -1)
    prefMatrix[counter3].append(counter3)
    counter3+=1

example = np.array(prefMatrix)
partners=Find_all_Irving_partner(example)

def pairList(partners):
    seen = []
    pairs=[]
    to_print = []
    pairlist = []
    for sol in partners:
        for people in range(0, len(sol)):
            if people not in seen:
                seen.append(people)
                pairs.append((people+1,sol[people]+1))
                pairlist.append([people+1,sol[people]+1])
                seen.append(sol[people])
        to_print.append(list(pairs))
        pairs = []
        seen=[] 
    return pairlist

partnersList= pairList(partners=partners)


for pair in partnersList:
    counter4 = 1
    for rank in roomPref[pair[0]-1]:
        if rank.roomid == pair[1]:
            print(f"Roomid: {pair[0]} got his top {counter4} , with Score: {rank.finalScore}")
        else:
            counter4+=1
    counter4 = 1
    for rank in roomPref[pair[1]-1]:
        if rank.roomid == pair[0]:
            print(f"Roomid: {pair[1]} got his top {counter4} , with Score: {rank.finalScore}")
        else:
            counter4+=1        

def combineRoom(myList, roomList):
    combineList = []
    for x in range(len(myList)):
        combineList.append((myList[x]+ roomList[x])/2)
    return combineList

pairRoomates = []

counter6 = 1
for pair in partnersList:
    print(pair)
    combineRoommate = RoommateIndividual(id=counter6,
                                        uid= f'{allRoommates[pair[0]-1].uid}_{allRoommates[pair[1]-1].uid}',
                                        beliefAns= combineRoom(allRoommates[pair[0]-1].beliefAns,allRoommates[pair[1]-1].beliefAns),
                                        communAns= combineRoom(allRoommates[pair[0]-1].communAns,allRoommates[pair[1]-1].communAns),
                                        habitsAns= combineRoom(allRoommates[pair[0]-1].habitsAns,allRoommates[pair[1]-1].habitsAns),
                                        interestAns=combineRoom(allRoommates[pair[0]-1].interestAns,allRoommates[pair[1]-1].interestAns),
                                        socialAns=combineRoom(allRoommates[pair[0]-1].socialAns,allRoommates[pair[1]-1].socialAns),
                                        personality= allRoommates[pair[random.randint(0, 1)]-1].personality
                                        ) 
    pairRoomates.append(combineRoommate)
    counter6+=1
    
roomPairPref = [[] for i in range(len(pairRoomates))]

pairs=list(itertools.combinations(pairRoomates, 2))

for o in pairs:
    a = o[0]
    b = o[1]
    #print(a.id)
    #print(b.id)
    preference1 = RoommatePreference(b.id,b.uid,
    habitsScore= calculateHabits(b.habitsAns,a.habitsAns),
    beliefScore=calculateOther(b.beliefAns,a.beliefAns),
    socialScore=calculateOther(b.socialAns,a.socialAns),
    communScore=calculateOther(b.communAns,a.communAns),
    interestScore=calculateOther(b.interestAns,a.interestAns),
    personalityScore= calculatePersonalityMatch(b.personality,a.personality)
    )
    preference2 = RoommatePreference(a.id,a.uid,
            habitsScore= calculateHabits(b.habitsAns,a.habitsAns),
    beliefScore=calculateOther(b.beliefAns,a.beliefAns),
    socialScore=calculateOther(b.socialAns,a.socialAns),
    communScore=calculateOther(b.communAns,a.communAns),
    interestScore=calculateOther(b.interestAns,a.interestAns),
    personalityScore= calculatePersonalityMatch(b.personality,a.personality))
    preference1.getFinal()
    preference2.getFinal()
    roomPairPref[b.id-1].append(preference2)
    roomPairPref[a.id-1].append(preference1)
    #b.add(2)


#print('Here 4')
counter2 =1
for room in roomPairPref:
    room.sort(key=lambda x: x.finalScore, reverse=True)
    print(room)
    
prefPairMatrix = [[] for i in range(len(pairRoomates))]

counter3 = 0
for room in roomPairPref:
    for y in range(len(room)):
        prefPairMatrix[counter3].append(room[y].roomid -1)
    prefPairMatrix[counter3].append(counter3)
    counter3+=1

example = np.array(prefPairMatrix)
partners=Find_all_Irving_partner(example)

partnersList= pairList(partners=partners)


for pair in partnersList:
    counter4 = 1
    for rank in roomPairPref[pair[0]-1]:
        if rank.roomid == pair[1]:
            print(f"Roomid: {pair[0]} got his top {counter4} , with Score: {rank.finalScore}")
        else:
            counter4+=1
    counter4 = 1
    for rank in roomPairPref[pair[1]-1]:
        if rank.roomid == pair[0]:
            print(f"Roomid: {pair[1]} got his top {counter4} , with Score: {rank.finalScore}")
        else:
            counter4+=1        
fullRoomates = []

counter6 = 1
for pair in partnersList:
    print(pair)
    combineRoommate = RoommateIndividual(id=counter6,
                                        uid= f'{pairRoomates[pair[0]-1].uid}_{pairRoomates[pair[1]-1].uid}',
                                        beliefAns= combineRoom(pairRoomates[pair[0]-1].beliefAns,pairRoomates[pair[1]-1].beliefAns),
                                        communAns= combineRoom(pairRoomates[pair[0]-1].communAns,pairRoomates[pair[1]-1].communAns),
                                        habitsAns= combineRoom(pairRoomates[pair[0]-1].habitsAns,pairRoomates[pair[1]-1].habitsAns),
                                        interestAns=combineRoom(pairRoomates[pair[0]-1].interestAns,pairRoomates[pair[1]-1].interestAns),
                                        socialAns=combineRoom(pairRoomates[pair[0]-1].socialAns,pairRoomates[pair[1]-1].socialAns),
                                        personality= pairRoomates[pair[random.randint(0, 1)]-1].personality
                                        ) 
    fullRoomates.append(combineRoommate)
    counter6+=1
    
    for full in fullRoomates:
        print(full)
    