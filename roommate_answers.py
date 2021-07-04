class RoommateIndividual(object):

    preferenceScore = []

    def __init__(self, id, uid, beliefAns, communAns, habitsAns, interestAns,
                 socialAns,personality):
        self.id = id
        self.uid = uid
        self.beliefAns = beliefAns
        self.communAns = communAns
        self.habitsAns = habitsAns
        self.interestAns = interestAns
        self.socialAns = socialAns
        self.personality = personality

    def add (self, preference):
        self.preferenceScore.append(preference)

    def getPref(self):
        return self.preferenceScore

    def setPref(self,prefL):
        self.preferenceScore = prefL


    def __repr__(self):
        return(f'''RoommateIndividual( id= {self.id}, 
uid= {self.uid}, 
beliefAns = ${self.beliefAns}, 
communAns ={self.communAns}, 
habitsAns ={self.habitsAns}, 
interestAns ={self.interestAns}, 
socialAns ={self.socialAns},)'''
        )

    def __str__(self):
        return(
            f'''RoommateIndividual( id= {self.id}, 
uid= {self.uid}, 
beliefAns = ${self.beliefAns}, 
communAns ={self.communAns}, 
habitsAns ={self.habitsAns}, 
interestAns ={self.interestAns}, 
socialAns ={self.socialAns},
personality = {self.personality})'''
        )
        
class RoommatePreference(object):
    def __init__(self, roomid, roomuid, beliefScore = 0 ,communScore=0, habitsScore=0, interestScore=0,
                 socialScore=0, finalScore=0):
        self.roomid = roomid
        self.roomuid = roomuid
        self.beliefScore = beliefScore 
        self.communScore = communScore
        self.habitsScore = habitsScore
        self.interestScore = interestScore
        self.socialScore = socialScore
        self.finalScore = finalScore


    def getFinal(self):
        self.finalScore = (self.habitsScore*30) + (self.socialScore*10) + (self.beliefScore*5) + (self.communScore*5) + (self.interestScore*20)
        return self.finalScore

    def __repr__(self):
        return str(self)

    def __str__(self):
        return(
            f'''PreferenceScore( roomid = {self.roomid}, roomuid = {self.roomuid} ,finalScore = {self.finalScore})\n'''

#             f'''PreferenceScore(
# roomid = {self.roomid}
# roomuid = {self.roomuid}
# beliefScore = {self.beliefScore*100} 
# communScore = {self.communScore*100}
# habitsScore = {self.habitsScore*100}
# interestScore = {self.interestScore*100}
# socialScore = {self.socialScore*100}
# finalScore = {self.finalScore}'''
        )
        