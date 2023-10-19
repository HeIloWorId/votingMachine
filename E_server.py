from credentials import generate_credentials
from certificate import generate_certificate
from elgamal import generateP, generateG, generatePrivateKey, generatePublicKey
from blowfish import encrypt
from elgamalUtils import calcul_inverse, exponentiation_rapide
import random
from pbkdf2 import pbkdf2
import json


class E_server:

    def __init__(self, voters, elgamal_parameters, ca_server):

        self._name = elgamal_parameters["name"]
        self._large_prime = elgamal_parameters["large_prime"]
        self._generator = elgamal_parameters["generator"]
        self._private_key = elgamal_parameters["private_key"]
        self._public_key = elgamal_parameters["public_key"]
        self._ca_server = ca_server
        self._ca_server_cert = self._ca_server.get_certificate()
        self.set_certificate()

        self._voters = voters

        file = open("election_parameters.json")

        self._election_parameters = json.load(file)

        file.close()

        self._credentials = []
        self._pubs = []
        self._blowfish_keys = []

    def set_certificate(self):

        self._certificate = self._ca_server.creating_a_certificate(
            self._name,
            self._large_prime,
            self._generator,
            self._public_key)

        cert_path = f"certificates/{self._name}.json"

        with open(cert_path, 'w', encoding='utf-8') as f:
            json.dump(self._certificate, f, ensure_ascii=False, indent=4)

    def generate_credentials_and_pub(self):

        for voter in self._voters:

            credential = generate_credentials(14)
            secret = self.generate_secret(credential)
            pub = self.generate_pub(secret)

            self._credentials.append(credential)
            self._pubs.append(pub)

    def generate_secret(self, credential):
        salt = self._election_parameters["id"]
        s_bytes = pbkdf2(credential, salt, 1000, 30)
        s = int.from_bytes(s_bytes, 'big')
        return s

    def generate_pub(self, secret):

        p = self._election_parameters["large_prime"]
        g = self._election_parameters["generator"]
        pub = exponentiation_rapide(g, secret, p)
        return pub

    def add_blowfish_key(self, ciphered, shared_secret):
        s = exponentiation_rapide(shared_secret, self._private_key, self._large_prime)
        plain_key  = ( ciphered * calcul_inverse(s, self._large_prime) ) % self._large_prime
        print(self._name + " received : " , plain_key)
        self._blowfish_keys.append(plain_key)
    
    def send_ciphered_credentials(self):

        for i in range (len(self._voters)):
        
            ciphered_credential = encrypt(str(self._credentials[i]), str(self._blowfish_keys[i]))
            self._voters[i].set_credential(ciphered_credential)
    
    def remove_credentials(self):
        self._credentials.clear()
    
    def remove_blowfish_keys(self):
        self._credentials.clear()

    
    def shuffle_pubs(self):

        self._pubs = random.shuffle(self._pubs)


    def sending_pubs(self, A):

            A.set_pubs(self._pubs)        


    def get_certificate(self):

        return self._certificate
