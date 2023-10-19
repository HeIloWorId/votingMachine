from collections import defaultdict
import uuid 
import voter
import E_server

class AdministrationAuthority:
    
    def __init__(self):
        
        self.set_electionName()
        self.set_voterNumber()
        self._voters = dict()
        self.set_qA()
        self._E_server = E_server.E()


    def get_electionName(self):
        return self._electionName

    def get_voterNumber(self):
        return self._voterNumber

    def get_qA(self):
        return self._qA
    
    def get_voters(self):
        return self._voters

    
    def set_electionName(self):
        self._electionName = input ("Entrez le nom de l'élection : \n")

    def set_voterNumber(self):
        self._voterNumber = input ("Entrez le nombre de votant : \n")
        

    def set_qA(self):
        
        questionnaire = dict()

        exit = False

        while exit == False :
        
            if input("(1) ajouter une question\n(2) exit\n\n> ") == "1":
            
                question = input("Entrez votre question :")
                reponses = []
                print("\n Vous devez donner au minimum deux réponses associées à " + question + " : \n")
                exit2 = False
                while exit2 == False :
                
                    if input("(1) ajouter une réponse\n(2) exit\n\n> ") == "1":

                        reponse = input("Entrez une réponse :")
                        reponses.append(reponse)
                    
                    elif (len(reponses) > 1 ):
                        exit2 = True

                questionnaire[question] = reponses
        
        
            else:
                exit=True
        self._qA = questionnaire
    

        
    def add_voter(self):
        id = uuid.uuid1()
        self._voters[str(id)] = voter.Voter()

    def send_voter(self):
        self._E_server.set_voters(self._voters)







    