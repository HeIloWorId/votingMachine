class S_server:
    
    def __init__(self, election_public_data):

        self._voting_data =  election_public_data["données_de_vote"] 
        self._election_parameters = election_public_data["paramètres"] 
        self._trustees_public_keys = election_public_data["clés_publiques_utilisateurs_de_confiance"] 
        self._pubs = election_public_data["codes_de_vote"] 
        self._ballots = election_public_data["bulletins_enregistrés"] 
        self._result = election_public_data["resultat"] 
