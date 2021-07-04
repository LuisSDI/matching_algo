from roommate_answers import RoommateIndividual
import string    
import random

habitsNumAns = [4,4,3,4,3
,4,4,4,4,2,
4,2,3,5,4,
3,3,3,3]

personalityMatch = {
    'INTJ': 'Analysts',
    'INTP': 'Analysts',
    'ENTJ': 'Analysts',
    'ENTP': 'Analysts',
    'INFJ': 'Diplomats',
    'INFP': 'Diplomats',
    'ENFJ': 'Diplomats',
    'ENFP': 'Diplomats',
    'ISTJ': 'Sentinels',
    'ISFJ': 'Sentinels',
    'ESTJ': 'Sentinels',
    'ESFJ': 'Sentinels',
    'ISTP': 'Explorers',
    'ISFP': 'Explorers',
    'ESTP': 'Explorers',
    'ESFP': 'Explorers',
  }

personalityType = [
    'INTJ',
    'INTP',
    'ENTJ',
    'ENTP',
    'INFJ',
    'INFP',
    'ENFJ',
    'ENFP',
    'ISTJ',
    'ISFJ',
    'ESTJ',
    'ESFJ',
    'ISTP',
    'ISFP',
    'ESTP',
    'ESFP',
  ]  


def generateUid(s):
    ran = ''.join(random.choices(string.ascii_letters + string.digits, k = s))    
    print("The randomly generated string is : " + str(ran)) 
    return personalityType[random.randint(0,15)]

def generatePersonality():
    return

def generateOthers(n):
    a=[]
    for j in range(n):
        a.append(random.randint(0,4))
    return a

def generateHabits():
    a=[]
    for j in range(len(habitsNumAns)):
        a.append(random.randint(0,(habitsNumAns[j] - 1)))
    return a

def generateUser(id,uid):
    roommate = RoommateIndividual(id= id, 
     uid= uid,
     beliefAns= generateOthers(7),
     habitsAns= generateHabits(),
     interestAns= generateOthers(12),
     communAns=generateOthers(9),
     socialAns=generateOthers(9),
     personality=generatePersonality()
     )
    return roommate