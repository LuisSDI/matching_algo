from six import text_type
from generate_user import generateUid, generateUser
import firebase_admin
import itertools
from firebase_admin import credentials
from firebase_admin import firestore
from roommate_answers import RoommateIndividual, RoommatePreference

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

for x in range(counter,8):
    uid = generateUid(28)
    allRoommates.append(generateUser(x,uid))
    #print(allRoommates[x-1])

roomPref = [[] for i in range(len(allRoommates))]

pairs=list(itertools.combinations(allRoommates, 2))

for o in pairs:
    a = o[0]
    b = o[1]
    print(a.id)
    print(b.id)
    preference1 = RoommatePreference(b.id,b.uid,
    habitsScore= calculateHabits(b.habitsAns,a.habitsAns),
    beliefScore=calculateOther(b.beliefAns,a.beliefAns),
    socialScore=calculateOther(b.socialAns,a.socialAns),
    communScore=calculateOther(b.communAns,a.communAns),
    interestScore=calculateOther(b.interestAns,a.interestAns),
    )
    preference2 = RoommatePreference(a.id,a.uid,
            habitsScore= calculateHabits(b.habitsAns,a.habitsAns),
    beliefScore=calculateOther(b.beliefAns,a.beliefAns),
    socialScore=calculateOther(b.socialAns,a.socialAns),
    communScore=calculateOther(b.communAns,a.communAns),
    interestScore=calculateOther(b.interestAns,a.interestAns))
    preference1.getFinal()
    preference2.getFinal()
    roomPref[b.id-1].append(preference2)
    roomPref[a.id-1].append(preference1)
    #b.add(2)


print('Here 4')
counter2 =1
for room in roomPref:
    room.sort(key=lambda x: x.finalScore, reverse=True)
    print(room)

# for room in allRoommates:
#     print(room)