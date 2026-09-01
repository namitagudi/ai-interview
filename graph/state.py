from typing import List

class InterviewState:
    def __init__(self):
        self.sessionid = ""
        self.candidatename = ""
        self.askedquestions = []      
        self.currentquestion = ""
        self.currenttranscript = ""    
        self.techscore = 0.0
        self.commscore = 0.0
        self.wpm = 0
        self.verifierscore = 0.0
        self.perfectedphrase = ""
        self.quizpassed = False
