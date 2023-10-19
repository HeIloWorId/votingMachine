from voter import Voter
from elgamal import generatePrivateKey, generatePublicKey
import paths
import json


class Trustee(Voter):

    def __init__(self, firstName, lastName, email):
        
        file = open(paths.ELECTION_PARAMETERS)

        election_parameters = json.load(file)

        file.close()

        election_large_prime = election_parameters["large_prime"]
        election_generator = election_parameters["generator"]
        self.set_large_prime(election_large_prime)
        self.set_generator(election_generator)
        self.generate_keys()
        super().__init__(firstName, lastName, email)
    

    def set_large_prime(self, large_prime):

       self._large_prime = large_prime
    
    def set_generator(self, generator):

       self._generator = generator
    
    
    def generate_keys(self):

        self._private_key = generatePrivateKey()
        
        self._public_key = generatePublicKey(
            self._private_key,
            self._generator,
            self._large_prime)

    def get_public_key(self):

        return self._public_key



    
  
        

