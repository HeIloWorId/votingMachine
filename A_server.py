from E_server import E_server
from certificate import generate_certificate
from elgamal import generateP, generateG, generatePrivateKey, generatePublicKey
import json
import uuid

class A_server:
    
    def __init__(self, trustees, voters, electionData, elgamal_parameters, ca_server):

        self._name = elgamal_parameters["name"]
        self._large_prime = elgamal_parameters["large_prime"]
        self._generator = elgamal_parameters["generator"]
        self._private_key = elgamal_parameters["private_key"]
        self._public_key = elgamal_parameters["public_key"]
        self._ca_server = ca_server
        self._ca_server_cert = self._ca_server.get_certificate()
        self.set_certificate()

        
        self._electionData = electionData
        self._trustees = trustees
        self._voters = voters
    
        self.set_voters_uuid()

    


    def set_voters_uuid(self):

        for voter in self._voters :
            u_id = uuid.uuid1().int
            voter.set_uuid(u_id)

    
    def set_certificate(self):

        self._certificate = self._ca_server.creating_a_certificate(
            self._name,
            self._large_prime,
            self._generator,
            self._public_key)
        
        cert_path = f"certificates/{self._name}.json"

        with open(cert_path, 'w', encoding='utf-8') as f:
            json.dump(self._certificate, f, ensure_ascii=False, indent=4)

    
    def set_pubs(self, pubs):

        self._pubs = pubs
    
    def ask_trustees_public_key(self):
        self._trustees_public_keys = []
        
        for trustee in self._trustees:
            
            trustee_public_key = trustee.get_public_key()
            self._trustees_public_keys.append(trustee_public_key)
    
    def get_trustees_public_keys(self):

        return self._trustees_public_keys

    def get_pubs(self):

        return self._pubs





    



    

       


