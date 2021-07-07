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
import pyrebase
from getpass import getpass


firebaseConfig = {
    'apiKey': "AIzaSyAdEg1yANVI8CVuE9Z3HYMiFXHPRBTRIi4",
    'authDomain': "matched--official.firebaseapp.com",
    'projectId': "matched--official",
    'storageBucket': "matched--official.appspot.com",
    'messagingSenderId': "383125817338",
    'databaseURL': "xxxxxx",
    'appId': "1:383125817338:web:8953ee2e21ec01a6cc4643",
    'measurementId': "G-VZHZKBBYCL"
  }

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
    return result


def getPreferences(roommatelist):
    pairs=list(itertools.combinations(roommatelist, 2))
    roompreferences = [[] for i in range(len(roommatelist))]
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
        roompreferences[b.id-1].append(preference2)
        roompreferences[a.id-1].append(preference1)
    
    for room in roompreferences:
        room.sort(key=lambda x: x.finalScore, reverse=True)
    return roompreferences

def generateMatrix(roommates, roompreferences):
    prefMatrix = [[] for i in range(len(roommates))]
    counter = 0
    for room in roompreferences:
        for y in range(len(room)):
            prefMatrix[counter].append(room[y].roomid -1)
        prefMatrix[counter].append(counter)
        counter+=1
    return prefMatrix

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

def getRankings(partnerlist,roomPref):
    for pair in partnerlist:
        counter = 1
        for rank in roomPref[pair[0]-1]:
            if rank.roomid == pair[1]:
                print(f"Roomid: {pair[0]} got his top {counter} , with Score: {rank.finalScore}")
            else:
                counter+=1
        counter = 1
        for rank in roomPref[pair[1]-1]:
            if rank.roomid == pair[0]:
                print(f"Roomid: {pair[1]} got his top {counter} , with Score: {rank.finalScore}")
            else:
                counter+=1 

def combineAns(myList, roomList):
    combineList = []
    for x in range(len(myList)):
        combineList.append((myList[x]+ roomList[x])/2)
    return combineList

def combineRoom(partnerslist,roomates):
    pairRoomates = []
    counter = 1
    for pair in partnerslist:
        print(pair)
        exist = fakeUsers.count(roomates[pair[1]-1].uid)
        if exist > 0:
            print('Fake user in pair')
            pair[1] = pair[0]
        print(pair)
        combineRoommate = RoommateIndividual(id=counter,
                                        uid= f'{roomates[pair[0]-1].uid}_{roomates[pair[1]-1].uid}',
                                        beliefAns= combineAns(roomates[pair[0]-1].beliefAns,roomates[pair[1]-1].beliefAns),
                                        communAns= combineAns(roomates[pair[0]-1].communAns,roomates[pair[1]-1].communAns),
                                        habitsAns= combineAns(roomates[pair[0]-1].habitsAns,roomates[pair[1]-1].habitsAns),
                                        interestAns=combineAns(roomates[pair[0]-1].interestAns,roomates[pair[1]-1].interestAns),
                                        socialAns=combineAns(roomates[pair[0]-1].socialAns,roomates[pair[1]-1].socialAns),
                                        personality= roomates[pair[random.randint(0, 1)]-1].personality
                                        ) 
        print(combineRoommate)
        pairRoomates.append(combineRoommate)
        counter+=1
    return pairRoomates

cred = credentials.Certificate("matched--official-firebase-adminsdk-agzne-ef087005af.json")
default_app= firebase_admin.initialize_app(cred)

firebase = pyrebase.initialize_app(firebaseConfig)
auth =  firebase.auth()

email = input('Please enter the admin email: ')
password = getpass('Please enter the passport: ')

user = auth.sign_in_with_email_and_password(email,password)
print('Success: User Sign In')


print(default_app.name)

db = firestore.client()
users_ref = db.collection(u'roommateTest')
perso_ref = db.collection(u'userInfo')
group_ref = db.collection(u'groups')
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

fakeUsers= []

missing = 4-(counter%4)
if missing != 4:
    for x in range(counter,counter+ missing+ 1):
        uid = generateUid(28)
        fakeUsers.append(uid)
        allRoommates.append(generateUser(x,uid))
    
roomPref = getPreferences(allRoommates)

prefMatrix = generateMatrix(allRoommates,roomPref)

example = np.array(prefMatrix)
partners=Find_all_Irving_partner(example)

partnersList= pairList(partners=partners)

getRankings(partnerlist=partnersList,roomPref=roomPref)        

pairRoomates = combineRoom(partnerslist=partnersList,roomates=allRoommates)

roomPairPref = getPreferences(pairRoomates)

for roomPair in roomPairPref:
    print(roomPair)

prefPairMatrix = generateMatrix(pairRoomates,roomPairPref)

example = np.array(prefPairMatrix)
partners=Find_all_Irving_partner(example)

partnersList= pairList(partners=partners)

getRankings(partnerlist=partnersList,roomPref=roomPairPref) 

fullRoomates = combineRoom(partnerslist=partnersList,roomates=pairRoomates)


#UPDATE FIRESTORE
groupsUid = []
for full in fullRoomates:
        groupsUid.append(full.uid.split('_'))

counter = 1
print(fakeUsers)
for group in groupsUid:
    testgroup = group_ref.document()
    print(group)
    newgroup = []
    for member in group:
        exist = fakeUsers.count(member)
        if exist == 0:
            newgroup.append(member)
    print(newgroup)    
    # if len(newgroup) > 0:
    #     testgroup.set({
    #     'groupName': f'Dorm {counter}',
    #     'groupImage': r'https://firebasestorage.googleapis.com/v0/b/matched--official.appspot.com/o/group_pictures%2Fdorm_pic.jpg?alt=media&token=f6c5a3c8-787e-4b41-a665-0a3bc63ec324',
    #     'members': newgroup,
    #     'groupID': testgroup.id,
    #     })
    #     counter+=1  
    #     for member in newgroup:
    #         memberdoc= perso_ref.document(member)
    #         memberdoc.update({u'groups': firestore.ArrayUnion([testgroup.id])})