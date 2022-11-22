import socket
import threading
from time import sleep, time

import player_cls
import intelligence
from gamerules import Game

class ClientThread(threading.Thread):
    def __init__(self, server, conn, adress) -> None:
        """
        Recupération des informations chez le client et inititalisation du Thread
        """
        super().__init__()
        self.server = server
        self.adress = adress
        self.conn = conn
        self.isAI = False
        Server.id_count += 1
        self.send("waiting for pseudo...")
        self.pseudo = self.receive()
        self.id = Server.id_count
        self.player = player_cls.Player.new_player()
        self.send(f"ID:{self.id}")

    def send(self, data):
        """
        Envoie des datas au client
        """
        sleep(0.1) # on s'assure que deux messages ne soient pas envoyés en même temps ce qui pourrait faire planter un socket
        data_encoded = data.encode("utf8")
        self.conn.sendall(data_encoded)
    
    def receive(self, datasize = 1024):
        """
        recoit des données du client
        """
        data_encoded = self.conn.recv(datasize)
        return data_encoded.decode("utf8")

    def ping(self) -> bool:
        """
        ping le client.
        Renvoie True si le client est toujours connecté
        """
        try:
            self.send("ping")
        except:
            print("no ping")
            self.server.remove(self)
            return False
        finally:
            return True
    
    def fromClientToAI(self):
        self = AIThread.fromClientToAI(self, "naive")
        return self

class AIThread(threading.Thread):
    def __init__(self, server, ai):
        """
        Un objet vu par le programme de la même façon qu'un ClientThread mais qui est relié à une IA.
        """
        super().__init__()
        self.server = server
        Server.id_count += 1
        self.id = Server.id_count
        self.ai = intelligence.ai(ai, self.id)
        self.isAI = True
        self.pseudo = self.ai.pseudo
        self.player = player_cls.Player.new_player()
    
    def send(self, data):
        """
        La seule information utile à l'ia est l'état de la partie, représenté par info
        """
        if data.startswith("###"):
            self.ai.get_info(data)
    
    def receive(self, datasize = 1024):
        """
        attente d'un message de l'IA
        """
        return self.ai.decision()
    
    def ping():
        return True # l'IA état liée au serveur elle ne peut pas être déconnectée
    
    @classmethod
    def fromClientToAI(cls, client, ai):
        newAI = AIThread(client.server, ai)
        Server.id_count -= 1
        newAI.id = client.id
        newAI.player = client.player
        return newAI



class Server():
    id_count = 0 # assure l'unicité de toutes les id

    def __init__(self, adresse:tuple, awaited:int, ias:int):
        """
        Initialise le serveur
        adress: couple (host, adresse) utilisé par le bind
        awaited: int correspond au nombre de joueurs attendus
        ias: int correspondant au nombre d'IA à ajouter
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.waiting = False # lorsque plusieurs clients sont connectés au serveur ils peuvent chercher à envoyer plusieurs messages en même temps, waiting perùet de les gérer dans leur ordre d'arrivée.
        self.socket.bind(adresse)
        self.conns = [] # liste des différents clients
        self.awaited = awaited
        self.ias = ias
        print("serveur prêt")
        
    def run(self, blinde, money):    
        """
        Une fois le serveur prêt, il peut être lancé grâce à cette fonction
        """
        self.get_players()
        self.wait_ready = {conn : conn.isAI for conn in self.conns}
        while not all([self.wait_ready[conn] for conn in self.conns]):
            for conn in self.conns:
                if not conn.isAI:
                    if conn.receive() == "ready":
                        self.wait_ready[conn] = True
        self.start_time = time()
        self.game = Game(blinde, money, self.conns, self)
        self.game.play()
        return self.close()
    
    def get_players(self):
        """
        Récupère des joueurs jusqu'à en avoir autant qu'attendu
        """
        while len(self.conns) < self.awaited:
            self.socket.listen() # écoute pour les connections
            conn, addr = self.socket.accept() # le client connecté et son adresse
            self.conns.append(ClientThread(self, conn, addr)) # création du Thread
            print("client connecté !")
            self.conns[-1].start()
            for client in self.conns: client.ping()
        for _ in range(self.ias):
            self.conns.append(AIThread(self, "naive"))
            print("IA connectée !")
            self.conns[-1].start()

    def test(self):
        """
        Cette fonction temporaire permet de tester la communication entre le serveur et les clients.
        """
        # messages tour par tour
        while True:
            for client in self.conns:
                print(client.id, client.pseudo)
                client.send("waiting for message...")
                received = client.receive()
                print(f"{client.pseudo}: {received}")
                if received == "QUIT":
                    return

    def close(self):
        """
        Permet de fermer le serveur
        """
        for client in self.conns:
            if not client.isAI:
                client.send("close")
                client.conn.close()
        print("fin d'exécution")
        if len(self.game.in_game) == 1:
            execution = time() - self.start_time
            print(f"{self.game.in_game[0].pseudo} (id: {self.game.in_game[0].id})  won!")
            print(f"partie jouée en {self.game.nb_coup} coups.")
            print(f"Durée de la partie: {execution}s")
        self.socket.close()
        return (self.game.nb_coup, execution)


if __name__ == "__main__":
    host, port = ('', 5566) # le 5566 a été paramétré par port forward sur ma machine pour être ouvert au réseau extérieur (pour le faire fonctionner chez vous il faut ouvrir le port 5566 sur les paramètres du routeur) 
    BLINDE = 2 # la petite blinde pour la partie
    MONEY = 50 # la monnaie de départ des joueurs
    NB_CLIENTS = 2 # le nombre de clients (joueurs humains)
    NB_IAS = 3 # le nombre d'IA
    server = Server((host, port), NB_CLIENTS, NB_IAS)
    coup, exec = server.run(BLINDE, MONEY)
    
