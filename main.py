from E_server import E_server
from S_server import S_server
from voter import Voter
from trustee import Trustee
import elgamal
import certificate
import sha1
import pickle
import os
import json
from A_server import A_server
from CA import CA
import uuid

LARGE_PRIME_SIZE = 512
# KEY_SIZE =


"""Permet de créer des paramètres el gamal"""


def creatingElgamalParameters(name):

    path = f"elgamal_parameters/{name}.json"

    if not (os.path.isfile(path)):

        large_prime = elgamal.generateP(LARGE_PRIME_SIZE)
        generator = elgamal.generateG(large_prime)
        private_key = elgamal.generatePrivateKey()
        public_key = elgamal.generatePublicKey(
            private_key, generator, large_prime)

        parameters = {"name": name, "large_prime": large_prime,
                      "generator": generator, "private_key": private_key, "public_key": public_key}

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(parameters, f, ensure_ascii=False, indent=4)

    else:

        file = open(path)

        parameters = json.load(file)

        file.close()

    return parameters


"""Permet de créer des paramètres el gamal pour une élection"""


def creatingElgamalParametersForElection():

    path = f"election_parameters.json"

    if not (os.path.isfile(path)):
        id = str(uuid.uuid1())
        large_prime = elgamal.generateP()
        generator = elgamal.generateG(large_prime)

        election_parameters = {
            "id": id, "large_prime": large_prime, "generator": generator}

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(election_parameters, f, ensure_ascii=False, indent=4)

    else:

        file = open(path)

        election_parameters = json.load(file)

        file.close()

    return election_parameters


"""Mise à jour des utilisateurs de confiance"""


def updateTrustees():

    trustees = []

    file = open('trustees.json')

    data = json.load(file)

    for trustee in data['utilisateurs de confiance']:

        firstName = trustee["prenom"]
        lastName = trustee["nom"]
        email = trustee["email"]

        new_trustee = Trustee(firstName, lastName, email)
        trustees.append(new_trustee)

    file.close()

    return trustees


"""Mise à jour des votants"""


def updateVoters():

    voters = []

    file = open('voters.json')

    data = json.load(file)

    for voter in data['votant']:

        firstName = voter["prenom"]
        lastName = voter["nom"]
        email = voter["email"]

        new_voter = Voter(firstName, lastName, email)
        voters.append(new_voter)

    file.close()

    return voters


""" Mise à jour des données de l'élection """


def updateElectionData():

    file = open('election_data.json')

    electionData = json.load(file)

    file.close()

    return electionData


""" Création de l'autorité de certification """

# on lit le fichier CA.json dans le dossier elgamal_parameters, s'il n'existe pas on le crée
elgamal_parameters = creatingElgamalParameters("CA")

# l'autorité de certification récupère les paramètres qu'on a généré et les utilisent pour créer un certificat auto-signé
CA_server = CA(elgamal_parameters)


"""Initialisation de l'élection """
election_parameters = creatingElgamalParametersForElection()
trustees = updateTrustees()  # on lit le fichier trustees.json
voters = updateVoters()  # on lit le fichier voters.json
electionData = updateElectionData()  # on lit le fichier election.json

for voter in voters:  # on donne l'autorité de certification aux votants

    voter.set_CA_server(CA_server)

"""Création du serveur A"""

# on lit le fichier A_server.json dans le dossier elgamal_parameters, s'il n'existe pas on le crée
elgamal_parameters_A = creatingElgamalParameters("A_server")

# le serveur A ajoute les uuid aux votants et demande son certificat au CA_server
A = A_server(trustees, voters, electionData, elgamal_parameters_A, CA_server)

"""Création du serveur E"""
elgamal_parameters_E = creatingElgamalParameters(
    "E_server")  # on lit le fichier E_server.json dans le dossier elgamal_parameters, s'il n'existe pas on le crée
E = E_server(voters, elgamal_parameters_E, CA_server)

# On décide de prendre les paramètres publique de E_server comme paramètres pour toute l'élection

"""Les votants demandent un code secret à E_server"""

"""
le problème qui se pose ici c'est que l'envoi des codes secrets aux votant doit se faire de manière chiffrée.

Pour chaque votant, on doit avoir le processus suivant :

1 / le votant récuprère le certificat de E_server
2/ le votant vérifie que le certificat est bon après avoir récupéré la clé publique de CA_server
3/ le votant génère une clé symétrique Blowfish
4/ le votant utilise la clé publiqe de E_server dans son certificat pour envoyer la clé symétrique à E_server
5/ E_server génère le code secret et le code de vote du votant
6/ E_server chiffre le code secret avec la clé symétrique Blowfish 
7/ E_server envoit le code secret chiffré au votant
8/ le votant déchiffre le code secret et le stock comme un de ses attributs

Cependant, ce qui paraît bizarre c'est que la communication doit être initiée par le votant ... (Peut-être que ce n'est pas un problème après tout...)

"""

# E_server génère les codes secrets et les codes de votes

E.generate_credentials_and_pub()

# E_server envoit son certificat aux votant autorisés (ceux qui lui ont été trasmis par A_server)
# les votants n'accepteront le certificat dans leur magasin que après vérifcation auprès de CA_server
# A noter que dès leur création, les votants doivent connaître CA_server, ie CA_server doit leur être un de leurs atttributs


# les votants récupèrent le certificat de E_server et le vérifie

for voter in voters:

    voter.download_and_check_certificate(E)

# les votants génèrent chacun une clé synmétrique

for voter in voters:

    voter.generate_blowfish_key()

# les votants envoient la clé blowfish chiffrée avec la clé publique de E_server

"""
pour cela le votant doit chosir un nombre aléatoire dans le q de E_server et calculer le secret partagé,
ie, appliquer le nombre aléatoire à pub de E_server
il doit ensuite chiffrer le message avec le secret partagé
il transmet le message chiffré et le secret partagé

"""

for voter in voters:

    # appel la fonction add_blowfish_key de E_server
    voter.cipher_and_send_blowfish_key(E)


# E_server envoit à chaque votant un credential chiffré avec la clé blowfish qui a été echangée puis il supprime les codes secrets et les clés blowfish

E.send_ciphered_credentials()
E.remove_credentials()
E.remove_blowfish_keys()

# E mélange les codes de votes Pub(c) et envoit la liste au serveur A, l'envoi n'a pas besoin d'être sécurisé

E.shuffle_pubs()
E.sending_pubs(A)


# Le serveur A récupère la clé public de chaque trustee

A.ask_trustees_public_key()


# on crée les données de l'élection 

election_public_data = {}

election_public_data["données_de_vote"] = electionData
election_public_data["paramètres"] = election_parameters
election_public_data["clés_publiques_utilisateurs_de_confiance"] = A.get_trustees_public_keys()
election_public_data["codes_de_vote"] = A.get_pubs()
election_public_data["bulletins_enregistrés"] = []
election_public_data["resultat"] = None # je ne sais pas quoi mettre pour le moment

# on crée le serveur de vote S

S = S_server(election_public_data)




