import json
import random
import elgamal
import elgamalUtils
import sha1


def generate_request(name, p, g, pub):
    
    request  = {"name" : name, "large_prime" : p, "generator" : g, "public_key"  : pub}

    return request 


def generate_self_signed_signature(request, priv):
        
    p = request["large_prime"]
    g = request["generator"]
    request_string = json.dumps(request)
    request_bytes = bytes(request_string, 'utf8')
    h = sha1.sha1(request_bytes) # request doit être en bytes 
    h = int.from_bytes(h, 'big')
  
    k = random.randint(0, p-1)
    s = 0

   
    while ( s == 0 ):

        while ( elgamalUtils.pgcd(k,p-1) != 1 ):

            k = random.randint(2, p-2)
  
        r = elgamalUtils.exponentiation_rapide(g, k, p)


        inv_k = elgamalUtils.calcul_inverse(k, p-1)

        s = ( (h - priv*r)*inv_k ) % (p-1)

    return {"r" : r, "s" : s}

def generate_signature(request, priv, authority):
        
    p = authority["request"]["large_prime"]
    g = authority["request"]["generator"]
    

    request_string = json.dumps(request)
    request_bytes = bytes(request_string, 'utf8')

    h = sha1.sha1(request_bytes) # request doit être en bytes 

    h = int.from_bytes(h, 'big')
  
    k = random.randint(0, p-1)
    s = 0

   
    while ( s == 0 ):

        while ( elgamalUtils.pgcd(k,p-1) != 1 ):

            k = random.randint(2, p-2)
  
        r = elgamalUtils.exponentiation_rapide(g, k, p)


        inv_k = elgamalUtils.calcul_inverse(k, p-1)

        s = ( (h - priv*r)*inv_k ) % (p-1)

    return {"r" : r, "s" : s}



def generate_certificate(name, p, g, pub, priv, authority):
    
    request = generate_request(name, p, g, pub)

    signature = generate_signature(request, priv, authority)

    certificate = {"request" : request, "signature" : signature}

    return certificate 


def generate_self_signed_certificate(name, p, g, pub, priv):
    
    request = generate_request(name, p, g, pub)


    signature = generate_self_signed_signature(request, priv)

    certificate = {"request" : request, "signature" : signature}

    return certificate 



def checking_certificate(server, authority):

    signature_server = server["signature"]
    request_server = server["request"]
    request_server_string = json.dumps(request_server)
    request_server_bytes = bytes(request_server_string, 'utf8')
    h = sha1.sha1(request_server_bytes)
    h = int.from_bytes(h, 'big')


    # signature issue du certificat du serveur
    r = signature_server["r"]
    s = signature_server["s"]

    # paramètres issues du certificat de l'autorité de certification
    p = authority["request"]["large_prime"]
    g = authority["request"]["generator"]
    pub = authority["request"]["public_key"]    


    if ( ( 0 < r < p) and ( 0 < s < p - 1) ):

             
            premier_terme = elgamalUtils.exponentiation_rapide(g, h, p) 

 
            deuxieme_terme = ( (elgamalUtils.exponentiation_rapide(pub, r, p) * elgamalUtils.exponentiation_rapide(r, s, p)) ) % p 
        

            if ( premier_terme == deuxieme_terme ):
                return True
    
    return False




        


