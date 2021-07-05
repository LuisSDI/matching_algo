from roommate_answers import RoommateIndividual
import string
import random

habitsNumAns = [4, 4, 3, 4, 3, 4, 4, 4, 4, 2,
                4, 2, 3, 5, 4,
                3, 3, 3, 3]

personalityType = [
    'INFP',
    'ENFP',
    'INFJ',
    'ENFJ',
    'INTJ',
    'ENTJ',
    'INTP',
    'ENTP',
    'ISFP',
    'ESFP',
    'ISTP',
    'ESTP',
    'ISFJ',
    'ESFJ',
    'ISTJ',
    'ESTJ', ]

personalityMatch = {
    'INTJ': [
        [],
        [personalityType[12], personalityType[13],
            personalityType[14], personalityType[15]],
        [personalityType[8], personalityType[9],
            personalityType[10], personalityType[11]],
        [personalityType[0], personalityType[2], personalityType[3], personalityType[5],
            personalityType[6], personalityType[4], ],
        [personalityType[1], personalityType[7]]],
    'INTP': [[],
             [personalityType[12], personalityType[13], personalityType[14]],
             [personalityType[8], personalityType[9],
                 personalityType[10], personalityType[11]],
             [personalityType[1], personalityType[2], personalityType[3], personalityType[0],
              personalityType[7], personalityType[4], personalityType[6]],
             [personalityType[15], personalityType[5]]],
    'ENTJ': [[], [],
             [personalityType[8], personalityType[9], personalityType[10], personalityType[11],
              personalityType[12], personalityType[13], personalityType[14], personalityType[15], ],
             [personalityType[1], personalityType[2], personalityType[3], personalityType[5],
              personalityType[7], personalityType[4], ],
             [personalityType[0], personalityType[6]]],
    'ENTP': [[],
             [personalityType[12], personalityType[13],
                 personalityType[14], personalityType[15]],
             [personalityType[8], personalityType[9],
                 personalityType[10], personalityType[11]],
             [personalityType[0], personalityType[1], personalityType[3], personalityType[5],
              personalityType[6], personalityType[7], ],
             [personalityType[2], personalityType[4]]],
    'INFJ': [
        [personalityType[8], personalityType[9], personalityType[10], personalityType[11],
         personalityType[12], personalityType[13], personalityType[14], personalityType[15], ],
        [], [],
        [personalityType[0], personalityType[2], personalityType[3], personalityType[5],
         personalityType[6], personalityType[4], ],
        [personalityType[1], personalityType[7]]],
    'INFP': [
        [personalityType[8], personalityType[9], personalityType[10], personalityType[11],
         personalityType[12], personalityType[13], personalityType[14], personalityType[15], ],
        [], [],
        [personalityType[0], personalityType[1], personalityType[2], personalityType[4],
         personalityType[6], personalityType[7], ],
        [personalityType[3], personalityType[5]]],
    'ENFJ': [
        [personalityType[9], personalityType[10], personalityType[11],
         personalityType[12], personalityType[13], personalityType[14], personalityType[15], ],
        [], [],
        [personalityType[1], personalityType[2], personalityType[3], personalityType[5],
            personalityType[6], personalityType[4], personalityType[7]],
        [personalityType[0], personalityType[8]]],
    'ENFP': [
        [personalityType[8], personalityType[9], personalityType[10], personalityType[11],
         personalityType[12], personalityType[13], personalityType[14], personalityType[15], ],
        [], [],
        [personalityType[0], personalityType[1], personalityType[3], personalityType[5],
         personalityType[6], personalityType[7], ],
        [personalityType[2], personalityType[4]]],
    'ISTJ': [
        [personalityType[0], personalityType[1],
            personalityType[2], personalityType[3]],
        [personalityType[4], personalityType[6], personalityType[7]],
        [personalityType[5], personalityType[9], personalityType[11]],
        [personalityType[12], personalityType[13],
            personalityType[14], personalityType[15]],
        [personalityType[8], personalityType[10]]],
    'ISFJ': [
        [personalityType[0], personalityType[1],
            personalityType[2], personalityType[3]],
        [personalityType[4], personalityType[6], personalityType[7]],
        [personalityType[5], personalityType[9], personalityType[11]],
        [personalityType[12], personalityType[13],
            personalityType[14], personalityType[15]],
        [personalityType[8], personalityType[10]]],
    'ESTJ': [
        [personalityType[0], personalityType[1],
            personalityType[2], personalityType[3]],
        [personalityType[4], personalityType[7]],
        [personalityType[5], personalityType[8], personalityType[10]],
        [personalityType[12], personalityType[13],
            personalityType[14], personalityType[15]],
        [personalityType[6], personalityType[9], personalityType[11]]],
    'ESFJ': [
        [personalityType[0], personalityType[1],
            personalityType[2], personalityType[3]],
        [personalityType[4], personalityType[6], personalityType[7]],
        [personalityType[5], personalityType[8], personalityType[10]],
        [personalityType[12], personalityType[13],
            personalityType[14], personalityType[15]],
        [personalityType[8], personalityType[10]]],
    'ISTP': [
        [personalityType[0], personalityType[1],
            personalityType[2], personalityType[3]],
        [personalityType[8], personalityType[9],
            personalityType[10], personalityType[11]],
        [personalityType[4], personalityType[5], personalityType[6], personalityType[7],
         personalityType[12], personalityType[14]],
        [],
        [personalityType[13], personalityType[15]]],
    'ISFP': [
        [personalityType[0], personalityType[1], personalityType[2], ],
        [personalityType[8], personalityType[9],
            personalityType[10], personalityType[11]],
        [personalityType[4], personalityType[5], personalityType[6], personalityType[7],
         personalityType[12], personalityType[14]],
        [],
        [personalityType[3], personalityType[13], personalityType[15]]],
    'ESTP': [
        [personalityType[0], personalityType[1],
            personalityType[2], personalityType[3]],
        [personalityType[8], personalityType[9],
            personalityType[10], personalityType[11]],
        [personalityType[4], personalityType[5], personalityType[6], personalityType[7],
         personalityType[13], personalityType[15]],
        [],
        [personalityType[12], personalityType[14]]],
    'ESFP': [
        [personalityType[0], personalityType[1],
            personalityType[2], personalityType[3]],
        [personalityType[8], personalityType[9],
            personalityType[10], personalityType[11]],
        [personalityType[4], personalityType[5], personalityType[6], personalityType[7],
         personalityType[13], personalityType[15]],
        [],
        [personalityType[12], personalityType[14]]],
}


def calculatePersonalityMatch(myPerso, roomPerso):
    score = 0
    myMatch = personalityMatch.get(myPerso)
    for list in myMatch:
        exist = list.count(roomPerso)
        if exist > 0:
            break
        else:
            score += 25
    #print(f'{myPerso} vs {roomPerso} = {score}')
    score = score /100
    return score

def generateUid(s):
    ran = ''.join(random.choices(string.ascii_letters + string.digits, k=s))
    #print("The randomly generated string is : " + str(ran))
    return ran


def generatePersonality():
    return personalityType[random.randint(0, 15)]


def generateOthers(n):
    a = []
    for j in range(n):
        a.append(random.randint(0, 4))
    return a


def generateHabits():
    a = []
    for j in range(len(habitsNumAns)):
        a.append(random.randint(0, (habitsNumAns[j] - 1)))
    return a


def generateUser(id, uid):
    roommate = RoommateIndividual(id=id,
                                  uid=uid,
                                  beliefAns=generateOthers(7),
                                  habitsAns=generateHabits(),
                                  interestAns=generateOthers(12),
                                  communAns=generateOthers(9),
                                  socialAns=generateOthers(9),
                                  personality=generatePersonality()
                                  )
    return roommate
