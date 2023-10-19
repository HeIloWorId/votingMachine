import random
from blowfish import decrypt
from certificate import checking_certificate
from credentials import generate_credentials
from elgamal import generatePrivateKey
from elgamalUtils import exponentiation_rapide
from pbkdf2 import pbkdf2

class Voter:
    
    def __init__(self, firstName, lastName, email):
        
        self._firstName = firstName
        self._lastName = lastName
        self._email = email

        self._blowfish_key = ""
        self._credential = ""
        
        self._trusteed_certificates = []

    
    
    
    def download_and_check_certificate(self, E_server):
       
        server_cert = E_server.get_certificate()

     

        ca_cert = self._CA_server.get_certificate()

        if (checking_certificate(server_cert, ca_cert)):
          
            self._trusteed_certificates.append(server_cert)
            
            return True

        else:
            return False
    

    def generate_blowfish_key(self):
        salt = "salt"
        password = generate_credentials(22)
        #print(self._firstName + " : "+" je génère une clé symétrique")
        key = pbkdf2(password,salt, 1000, 30)
        key = int.from_bytes(key, 'big')
   
        self._blowfish_key = key


    
    def cipher_and_send_blowfish_key(self, E_server):

        E_server_certificate = self._trusteed_certificates[0]
        
        p = E_server_certificate["request"]["large_prime"]
        g = E_server_certificate["request"]["generator"]
        pub = E_server_certificate["request"]["public_key"]
        key = self._blowfish_key

        print(self._firstName + " sending : " , key)

        y = random.randint(2, p-1)
        c1 = exponentiation_rapide(g, y, p)
        s = exponentiation_rapide(pub, y, p)
        c2 = (key * s) % p

        E_server.add_blowfish_key(c2, c1)

    
    def set_credential(self, ciphered_credential):

        self._credential = decrypt(ciphered_credential, str(self._blowfish_key))
        print(self._credential)


    
    def set_CA_server(self, CA_server):

        self._CA_server = CA_server



    
    def __str__(self):
        return self._firstName + " ; " + self._lastName + " ; " + self._email + " ; " + self._uuid
        
    
    def __repr__(self):
        return self._firstName + " ; " + self._lastName + " ; " + self._email 

    def get_firstName(self):
        return self._firstName

    def get_lastName(self):
        return self._lastName

    def get_email(self):
        return self._email

    def get_credential(self):
        return self._credential
    
    def get_credential(self):
        return self._uuid 
    
    def set_uuid(self, uuid):
        self._uuid = uuid
        

