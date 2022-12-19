import hashlib
import time
from bottle import get, run
import requests
import json

class block:
    def __init__(self, id, n, trans, prev, dif, nonce, time) -> None:
        self.id = id            #id del bloque (profundidad del bloque)
        self.n = n              #número de transacciones en este bloque
        self.trans = trans      #lista de transacciones
        self.prev = prev        #hash del bloque anterior
        self.dif = dif          #dificultad para el nonce del siguiente bloque
        self.nonce = nonce      #nonce del bloque
        self.time = time        #fecha y hora en la que se creó el bloque
    
    def __str__(self) -> str:
        return 'id = {}, n = {}, trans = {}, prev = {}, dif = {}, nonce = {}, tiempo = {}'.format(self.id, self.n, self.trans, self.prev, self.dif, self.nonce, self.time)

@get('/getNonce/<diff>')
def searchNonce(diff):   #Esto recibe el hash del bloque y buscará el nonce
    datajson = requests.get(url='http://localhost:8081/getTrans').text  #pool es la lista en formato Json

    datajson = json.loads(datajson)
    nextid = datajson['nextid']
    lasthash = datajson["lasthash"]
    pool = datajson["transactions"]
    
    encontrado = False
    nonce = 0
    while not encontrado:
        tempBlock = block(nextid, len(pool), pool, lasthash, int(diff), nonce, time.time())  #El bloque que estamos intentando generar

        if int(hashlib.sha256(str(tempBlock).encode('utf-8')).hexdigest(), 16) % pow(10, 12) < int(diff):
            encontrado = True
            print(nonce)
            return str(nonce) 
        nonce = nonce + 1

run(host='localhost', port=8000)